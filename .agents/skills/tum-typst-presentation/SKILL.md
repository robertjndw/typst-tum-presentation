---
name: tum-typst-presentation
description: >
  Creates, edits, and converts presentations using the TUM (Technical University of Munich)
  Typst template in this repository. Use this skill whenever the user wants to write a new
  TUM presentation, add or edit slides, structure content for a talk, or convert an existing
  PowerPoint (PPTX) file into Typst format. Trigger even for casual requests like "make slides
  about X", "add a slide on Y", "convert my PPTX to Typst", or "how do I animate this".
---

# TUM Typst Presentation Skill

This skill helps you work with the TUM Polylux Typst template in this repo. The template
produces TUM-branded 16:9 presentations with the official TUM blue (`#0065BD`) color scheme.

## Template setup

Every presentation file must start with this **exact import** — do not use relative path
traversal (e.g. `../../theme.typ`). The file must be compiled from the repo root where
`theme.typ` lives, and the import must be:

```typ
#import "theme.typ": *

#show: tum-theme.with(
  authors: ("Your Name",),
  title: "Presentation Title",
  footer-infos: ("Optional extra footer text",),
  school: "TUM School of ...",        // optional
  chair: "Lehrstuhl für ...",         // optional
  lang: "en",                          // or "de"
  date: datetime(year: 2025, month: 6, day: 10),  // optional, defaults to today
)
```

If the template is in a subdirectory (e.g., `theme/`), adjust the import path:
`#import "theme/theme.typ": *`

---

## Slide types

### `#title-slide()`
The opening slide. Shows the title, authors, university, school, chair, location, and date.

- Default: TUM tower watermark on the right
- With flags: `#title-slide(flags: true)` — full TUM flags photo background with white text

Use the flags variant for high-impact openers; the default for more formal contexts.

### `#title-content-slide(title: "...")[body]`
The standard workhorse slide. Title in TUM blue at the top, freeform body content below.

```typ
#title-content-slide(title: "Key Findings")[
  - Result one: explanation
  - Result two: explanation

  #show: later
  - Result three (revealed on click)
]
```

Use for: text, bullet lists, code blocks, tables, diagrams, most content.

### `#title-image-slide(title: "...", image_path: "path/to/image.jpg")`
Full-width image centered below the title. Use this whenever a slide's main content is
visual — architecture diagrams, screenshots, charts, photos, or any placeholder that will
eventually become an image. **Do not** put an image or chart inside a `#title-content-slide`
body; use this slide type instead.

When the real image doesn't exist yet, use a placeholder path and leave a comment:
```typ
// TODO: replace with actual chart path
#title-image-slide(title: "Experimental Results", image_path: "/resources/results-chart.png")
```

If the image truly doesn't exist and you want a compiled placeholder, use `#title-content-slide`
with a visually distinct `#rect` — but switch it to `#title-image-slide` the moment a real file
is available.

### `#empty-slide[body]`
Bare slide with footer but no title. Useful for full-bleed layouts or custom arrangements.

---

## Animations (step-by-step reveals)

Use `#show: later` inside a slide body to reveal content progressively. Each `later` creates
a new "click" in the PDF. The content before is shown first; after each click more appears.

```typ
#title-content-slide(title: "Three Steps")[
  *Step 1:* Set up the environment.

  #show: later
  *Step 2:* Run the experiment.

  #show: later
  *Step 3:* Analyze the results.
]
```

Polylux generates one PDF page per reveal step — this is normal. Compile with `typst compile`
and view in a PDF viewer that supports presentation mode.

---

## Content guidance

**Structure your slides around one idea each.** If a slide needs more than ~6 bullet points,
split it. The title should tell the audience what to take away — "Results show 40% speedup"
is better than "Results".

**Mix slide types.** Don't use only title-content slides. After several text slides, break
the rhythm with a title-image slide or an animated reveal. Use the flags title slide only
once (at the start or a major section break).

**Keep body text concise.** Slides support the talk; they're not a transcript. Aim for
phrases, not full sentences.

---

## Compiling

```sh
typst compile presentation.typ          # produces presentation.pdf
typst watch presentation.typ            # live-recompile on save
```

For the example file in this repo: `typst compile example.typ`

---

## Converting PPTX to Typst

When the user provides a `.pptx` file, use the conversion script to extract content and
map it to Typst slide types.

### Step 1 — Extract PPTX content

```bash
python3 .agents/skills/tum-typst-presentation/scripts/pptx_to_typst.py input.pptx
```

This prints a Typst file draft to stdout and a slide summary to stderr. Redirect:

```bash
python3 .agents/skills/tum-typst-presentation/scripts/pptx_to_typst.py input.pptx > draft.typ
```

### Step 2 — Review and refine the draft

The script makes reasonable guesses about slide types, but you should:

- Check that the title slide metadata (author, date) is correct
- Review every `title-content-slide` body — PPTX body text is often verbose and should
  be condensed for Typst
- If a slide's content is mainly one image, switch it to `title-image-slide`
- Add `#show: later` to any slides that benefit from step-by-step reveals
- Remove or merge slides that don't translate meaningfully to the TUM layout

### Step 3 — Compile and check

```sh
typst compile draft.typ
```

Fix any compilation errors (usually missing image paths or unsupported characters) before
delivering the result to the user.

### Slide type mapping heuristic

| PPTX slide                                 | Typst slide type          |
|--------------------------------------------|---------------------------|
| First/cover slide                          | `#title-slide()`          |
| Slide with only a title + large image      | `#title-image-slide`      |
| Section divider (title only, no body)      | `#title-slide()` or `#title-content-slide` with empty body |
| Standard title + bullets/text              | `#title-content-slide`    |
| Complex custom layout                      | `#empty-slide` + manual layout |

---

## Reference

See `references/theme-api.md` for the full `tum-theme` parameter list and all available
colors from `colors.typ`.
