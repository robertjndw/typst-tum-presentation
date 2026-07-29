#!/usr/bin/env python3
"""Convert a PPTX deck into a TUM Typst presentation draft.

    python3 pptx_to_typst.py deck.pptx -o draft.typ

Extracts titles, bullet text (with nesting), tables, speaker notes and the
embedded images, then emits Typst using the slide functions from theme.typ.
Images are written into an assets directory and referenced with root-absolute
paths (/resources/...), which is what theme.typ's own image references use.

The output is a *draft*: it is meant to compile as-is so you can iterate on it,
not to be the finished deck. Read the "REVIEW" comments it leaves behind.
"""

import argparse
import re
import sys
from pathlib import Path

# Typst markup characters that would otherwise be interpreted as syntax.
# `[` and `]` matter because body text is emitted inside a `[...]` content block.
_MARKUP_SPECIALS = "\\#$*_`<>@~[]"

# Geometry of a 16:9 slide body, measured against theme.typ's page margins
# (top 3cm / bottom 1cm / x 1cm on a 33.87 x 19.05cm page) minus the title block.
# An image taller than this silently spills onto a second page, which reads as a
# duplicated slide in the PDF, so we size images against it instead of guessing.
BODY_WIDTH_CM = 31.87
BODY_HEIGHT_CM = 10.5
SAFE_IMAGE_HEIGHT = "10cm"  # fits on its own
SAFE_CAPTION_HEIGHT = "9cm"  # leaves room for a line or two of text below


def _require_pptx():
    try:
        from pptx import Presentation
    except ImportError:
        sys.exit(
            "python-pptx is required.\n"
            "  pip install python-pptx    (or: python3 -m pip install --user python-pptx)"
        )
    return Presentation


def typst_string(text):
    """Escape text for use inside a Typst "..." string literal."""
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return " ".join(text.split())


def typst_markup(text):
    """Escape text for use inside a Typst content block."""
    out = []
    for ch in text:
        if ch in _MARKUP_SPECIALS:
            out.append("\\")
        out.append(ch)
    return "".join(out)


def _shape_text(shape):
    """Paragraphs of a shape as (indent_level, text), blank lines dropped."""
    if not shape.has_text_frame:
        return []
    paragraphs = []
    for para in shape.text_frame.paragraphs:
        text = "".join(run.text for run in para.runs).strip()
        # PowerPoint renders bullet glyphs from the list style, but some decks
        # type them literally. Strip them so we don't end up with "- • item".
        text = re.sub(r"^[•●▪–—\-\*]\s+", "", text)
        if text:
            paragraphs.append((max(0, para.level or 0), text))
    return paragraphs


def _walk(shapes):
    """Yield every shape, descending into groups."""
    for shape in shapes:
        if shape.shape_type == 6:  # GROUP
            yield from _walk(shape.shapes)
        else:
            yield shape


def _is_title(shape):
    if not shape.is_placeholder:
        return False
    try:
        fmt = shape.placeholder_format
    except (ValueError, AttributeError):
        return False
    # 13 = PP_PLACEHOLDER.TITLE, 0 = CENTER_TITLE; idx 0 is the title slot.
    return fmt.type in (13, 0) or fmt.idx == 0


def _area(shape):
    try:
        return int(shape.width) * int(shape.height)
    except (TypeError, ValueError):
        return 0


def split_title_and_body(slide):
    """Return (title, body_paragraphs). A shape used as the title is never reused."""
    text_shapes = [s for s in _walk(slide.shapes) if s.has_text_frame and _shape_text(s)]

    title_shape = next((s for s in text_shapes if _is_title(s)), None)
    if title_shape is None and len(text_shapes) == 1:
        # No title placeholder and only one text box: if it reads like a heading,
        # promote it rather than emitting a titleless slide with orphan text.
        paras = _shape_text(text_shapes[0])
        if len(paras) == 1 and len(paras[0][1]) <= 80:
            title_shape = text_shapes[0]

    title = _shape_text(title_shape)[0][1] if title_shape else ""
    body = []
    for shape in text_shapes:
        if shape is title_shape:
            continue
        body.extend(_shape_text(shape))
    return title, body


def _fits_unsized(image):
    """Would `image(path)` with no width/height stay inside one slide body?

    Typst lays an image out at its natural size (pixels / DPI), shrinking it to
    the body width if it is wider. Height is never constrained, so a tall or
    low-DPI image overflows. `title-image-slide` gives no way to size the image,
    so we predict the result here and fall back to a sized content slide.
    """
    try:
        px_w, px_h = image.size
        dpi_x = image.dpi[0] or 72
    except (AttributeError, TypeError, IndexError, ValueError):
        return False  # unknown: assume the worst and size it explicitly
    if not px_w or not px_h:
        return False
    natural_w = px_w / dpi_x * 2.54
    rendered_w = min(natural_w, BODY_WIDTH_CM)
    return rendered_w * (px_h / px_w) <= BODY_HEIGHT_CM


def extract_images(slide, index, assets_dir, typst_prefix):
    """Save the slide's pictures; return [(typst_path, fits_unsized)] largest first."""
    pictures = [s for s in _walk(slide.shapes) if s.shape_type == 13]  # PICTURE
    pictures.sort(key=_area, reverse=True)

    saved = []
    for n, shape in enumerate(pictures, start=1):
        try:
            picture = shape.image
            blob, ext = picture.blob, picture.ext
        except (AttributeError, ValueError):
            continue  # linked-but-not-embedded picture, nothing to save
        assets_dir.mkdir(parents=True, exist_ok=True)
        name = f"slide{index:02d}-img{n}.{ext}"
        (assets_dir / name).write_bytes(blob)
        saved.append((f"{typst_prefix}/{name}", _fits_unsized(picture)))
    return saved


def extract_tables(slide):
    """Return each table as a list of rows of cell strings."""
    tables = []
    for shape in _walk(slide.shapes):
        if not getattr(shape, "has_table", False):
            continue
        tables.append(
            [[cell.text.strip() for cell in row.cells] for row in shape.table.rows]
        )
    return tables


def render_body(paragraphs, indent="  "):
    """Body paragraphs to a Typst bullet list, preserving nesting."""
    return [f"{indent}{'  ' * level}- {typst_markup(text)}" for level, text in paragraphs]


def render_table(rows):
    if not rows:
        return []
    columns = max(len(r) for r in rows)
    lines = ["  #table(", f"    columns: {columns},"]
    for row in rows:
        padded = row + [""] * (columns - len(row))
        cells = ", ".join(f"[{typst_markup(c)}]" for c in padded)
        lines.append(f"    {cells},")
    lines.append("  )")
    return lines


def classify(index, body, images, tables):
    """Pick the TUM slide function that fits this slide's content."""
    if index == 1:
        return "cover"
    if not body and not images and not tables:
        return "divider"
    if images and not tables:
        if not body:
            return "image"
        if len(body) <= 2:
            # A caption, not real content: keep the image full width and fold
            # the caption into the body of a content slide instead.
            return "image-caption"
        return "image-text"
    return "content"


def convert(pptx_path, assets_dir, typst_prefix, theme_import, include_notes):
    Presentation = _require_pptx()
    prs = Presentation(str(pptx_path))
    slides = list(prs.slides)

    props = prs.core_properties
    cover_title, cover_body = split_title_and_body(slides[0]) if slides else ("", [])
    title = props.title or cover_title or "Presentation Title"
    author = props.author or (cover_body[0][1] if cover_body else "Author")

    out = [
        f'#import "{theme_import}": *',
        "",
        "#show: tum-theme.with(",
        f'  authors: ("{typst_string(author)}",),',
        f'  title: "{typst_string(title)}",',
        "  footer-infos: (),",
        '  // school: "TUM School of ...",',
        '  // chair: "Lehrstuhl für ...",',
        ")",
        "",
        "#title-slide()",
        "",
    ]
    if cover_body:
        out.insert(
            len(out) - 2,
            "// REVIEW: cover slide text from the PPTX, check authors/title above:\n"
            + "\n".join(f"//   {t}" for _, t in cover_body),
        )

    summary = []
    for index, slide in enumerate(slides, start=1):
        slide_title, body = split_title_and_body(slide)
        images = extract_images(slide, index, assets_dir, typst_prefix)
        tables = extract_tables(slide)
        kind = classify(index, body, images, tables)
        summary.append((index, kind, slide_title, len(body), len(images), len(tables)))

        if kind == "cover":
            continue

        heading = f'title: "{typst_string(slide_title)}"' if slide_title else 'title: ""'

        if kind == "divider":
            out += [f"// Slide {index} - section divider", f"#title-content-slide({heading})[]", ""]
            continue

        path, fits = images[0] if images else (None, False)
        extras = [f"  // REVIEW: unplaced image {p}" for p, _ in images[1:]]

        if kind == "image" and fits:
            out += [f"// Slide {index}", f'#title-image-slide({heading}, image_path: "{path}")']
            out += [line.lstrip() for line in extras] + [""]
            continue

        out.append(f"// Slide {index}")
        out.append(f"#title-content-slide({heading})[")

        if kind == "image":
            # Too tall for title-image-slide, which cannot size its image.
            out.append(f'  #align(center, image("{path}", height: {SAFE_IMAGE_HEIGHT}))')
            out += extras
        elif kind == "image-caption":
            out.append(f'  #align(center, image("{path}", height: {SAFE_CAPTION_HEIGHT}))')
            out += render_body(body) + extras
        elif kind == "image-text":
            out.append("  #grid(columns: (1fr, 1fr), gutter: 1cm, align: horizon,")
            out.append("    [")
            out += render_body(body, indent="      ")
            out.append("    ],")
            out.append(f'    image("{path}", width: 100%, height: {SAFE_IMAGE_HEIGHT}, fit: "contain"),')
            out.append("  )")
            out += extras
        else:
            out += render_body(body)
            for rows in tables:
                out += render_table(rows)
            out += [f"  // REVIEW: unplaced image {p}" for p, _ in images]

        out.append("]")

        if include_notes and slide.has_notes_slide:
            note = slide.notes_slide.notes_text_frame.text.strip()
            if note:
                out += [f"// note: {line}" for line in note.splitlines() if line.strip()]
        out.append("")

    return "\n".join(out), summary


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="write draft here (default: stdout)")
    parser.add_argument(
        "--assets-dir",
        default=None,
        help="where to save extracted images, relative to the Typst project root "
        "(default: resources/<deck-name>)",
    )
    parser.add_argument("--theme-import", default="theme.typ", help='import path (default: "theme.typ")')
    parser.add_argument("--no-notes", action="store_true", help="drop speaker notes")
    args = parser.parse_args()

    if not args.pptx.exists():
        sys.exit(f"File not found: {args.pptx}")

    stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", args.pptx.stem).strip("-").lower() or "deck"
    rel_assets = Path(args.assets_dir) if args.assets_dir else Path("resources") / stem
    typst_prefix = "/" + rel_assets.as_posix().lstrip("/")

    draft, summary = convert(
        args.pptx, rel_assets, typst_prefix, args.theme_import, not args.no_notes
    )

    print(f"Converted {args.pptx.name}: {len(summary)} slides", file=sys.stderr)
    for index, kind, title, n_body, n_img, n_tbl in summary:
        extra = f"{n_body} lines, {n_img} img, {n_tbl} tbl"
        print(f"  {index:>3}  {kind:<14} {title[:44]:<44} ({extra})", file=sys.stderr)
    print(f"Images written to {rel_assets}/ (referenced as {typst_prefix}/...)", file=sys.stderr)

    if args.output:
        args.output.write_text(draft, encoding="utf-8")
        print(f"Draft written to {args.output}", file=sys.stderr)
    else:
        print(draft)


if __name__ == "__main__":
    main()
