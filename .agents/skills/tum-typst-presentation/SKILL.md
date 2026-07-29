---
name: tum-typst-presentation
description: >
  Creates, edits, and converts presentations built on the TUM (Technical University of
  Munich) Polylux/Typst template in this repository - theme.typ, title-slide,
  title-content-slide, title-image-slide, empty-slide. Use this skill whenever the user
  wants to write a new TUM presentation, add or edit slides, restructure a talk, fix a
  slide that renders wrong, or convert an existing PowerPoint (PPTX) deck into Typst.
  Trigger even for casual requests like "make slides about X", "add a slide on Y",
  "turn this pptx into typst", "why is my slide duplicated", or "how do I animate this".
---

# TUM Typst Presentation Skill

This repo is a Polylux template producing TUM-branded 16:9 slides. `theme.typ` defines the
slide functions, `colors.typ` the corporate palette, `resources/` the logos and photos.

The single most useful thing you can do here is **compile and look at the result**. Typst
silently reflows overfull slides onto a second page, so a deck can compile cleanly and
still be wrong. See [Verifying your work](#verifying-your-work) - do it before you report
back.

## Setting up a presentation

```typ
#import "theme.typ": *

#show: tum-theme.with(
  authors: ("Your Name",),
  title: "Presentation Title",
  footer-infos: ("Optional extra footer text",),
  school: "TUM School of ...",                     // optional
  chair: "Lehrstuhl für ...",                      // optional
  lang: "en",                                      // or "de"
  date: datetime(year: 2025, month: 6, day: 10),   // optional, defaults to today
)
```

**About the import path.** `theme.typ` loads its logos with root-absolute paths
(`/resources/TUM-logo.svg`), and Typst resolves those against the *project root*, which
defaults to the directory of the file you compile. So the import path and the compile
command have to agree:

| Layout | Import | Compile from |
|---|---|---|
| Deck next to `theme.typ` (this repo) | `#import "theme.typ": *` | that directory |
| Theme copied into `theme/`, `resources/` at top level | `#import "/theme/theme.typ": *` | project root |
| Deck in a subfolder, theme above it | `#import "/theme.typ": *` | `typst compile --root . slides/deck.typ` |

A bare `../theme.typ` fails with *"would escape the project root"* - Typst will not read
outside the root. Pass `--root` rather than rewriting the theme's paths.

## Slide types

### `#title-slide()`
Opening slide: title, authors, university, school, chair, location, date. Default has the
TUM tower watermark; `#title-slide(flags: true)` uses the full-bleed TUM flags photo with
white text. Use the flags variant once, for impact - the default reads as more formal.

### `#title-content-slide(title: "...")[body]`
The workhorse. Takes any content in the body: text, lists, tables, code, images, grids.

`title:` accepts content, not just a string, so you can style it. **Titles render black by
default** - if the user wants TUM blue, do it explicitly:

```typ
#title-content-slide(title: text(TUM_primary_blue)[Key Findings])[
  - Result one
  - Result two
]
```

### `#title-image-slide(title: "...", image_path: "/resources/foo.jpg")`
Convenience wrapper for a single centered image. Two sharp edges worth knowing:

- It takes **no body** and gives you **no control over image size**. The image renders at
  its natural size (pixels ÷ DPI), shrunk to the body width but never to the body height,
  so a tall or low-DPI image overflows onto a second page. When in doubt use a content
  slide with an explicit `height:` (see [Layout recipes](#layout-recipes)).
- `image_path` has no default that works - omitting it fails with *"expected path, string,
  or bytes, found none"*. Only emit this slide once the file actually exists.

### `#empty-slide[body]`
Footer and page number, no title. For full-bleed layouts, section statements, or anything
you want to arrange yourself.

## Layout recipes

The slide body is about **31.9 cm wide and 10.5 cm tall**. Percentage heights do not help
here - the body block has automatic height, so `height: 70%` resolves against nothing
useful. Size images in absolute units and stay under the budget.

**Image with a caption or a line of text** - cap at `9cm` to leave room for the text:

```typ
#title-content-slide(title: "Throughput")[
  #align(center, image("/resources/chart.png", height: 9cm))
  Measured on 4x A100, batch size 32.
]
```

**Image beside text** - the fixed box means it never overflows in either direction,
whatever shape the image is:

```typ
#title-content-slide(title: "Architecture")[
  #grid(columns: (1fr, 1fr), gutter: 1cm, align: horizon,
    [
      - Ingest layer batches requests
      - Scheduler assigns GPUs
    ],
    image("/resources/arch.png", width: 100%, height: 10cm, fit: "contain"),
  )
]
```

**Image alone on a content slide** - `height: 10cm` is the practical ceiling.

**A statement slide** for a section break or closing line:

```typ
#empty-slide[
  #align(center + horizon, text(size: 40pt, TUM_primary_blue)[40% faster, same accuracy])
]
```

## Step-by-step reveals

`#show: later` reveals everything after it on the next click. Each `later` adds one PDF
page, so a slide with two `later`s becomes three pages - expected, not a bug.

```typ
#title-content-slide(title: "Three Steps")[
  *Step 1:* Set up the environment.

  #show: later
  *Step 2:* Run the experiment.

  #show: later
  *Step 3:* Analyze the results.
]
```

For `uncover`, `only`, and other Polylux primitives see the
[Polylux book](https://polylux.dev/book/polylux.html).

## Writing good slides

Give each slide one idea. If a slide needs more than ~6 bullets, split it. Make titles
carry the message - "Results show 40% speedup" beats "Results", because the audience reads
the title first and often only the title.

Keep bodies to phrases rather than sentences; the slides support the talk, they are not a
transcript. And vary the rhythm - several text slides in a row lose the room, so break
them up with an image slide, a reveal, or a statement slide.

## Verifying your work

```sh
typst compile deck.typ                 # produces deck.pdf
typst watch deck.typ                   # live reload while iterating
```

Compiling is necessary but not sufficient - an overfull slide produces a *silently
duplicated* page rather than an error. Render the pages and actually look at them:

```sh
typst compile deck.typ page-{n}.png --format png --ppi 60
```

Then read the PNGs. You are checking for: a page whose content area is empty or whose
title is missing (that is the overflow half of the previous slide), images running past
the footer, and text that has wrapped badly. Count the pages too - they should equal the
number of slides plus one extra per `#show: later`.

Fix overflow by lowering the image `height:`, trimming body text, or splitting the slide.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `file not found (searched at .../theme.typ)` | Compiling from the wrong directory. Compile where `theme.typ` lives, or use a root-absolute import plus `--root`. |
| `path "../theme.typ" would escape the project root` | Typst will not read above the root. Add `--root <project-dir>`. |
| `expected path, string, or bytes, found none` | `#title-image-slide` called without `image_path`. |
| A slide appears twice, second copy blank or headerless | Content overflow, not a duplicate. Reduce image height or split the slide. |
| Text renders in a serif fallback; `typst fonts` lacks Arial | The theme sets `font: "Arial"`. On Linux install `ttf-mscorefonts-installer` (this is what `.github/workflows/` does) or change the font in `theme.typ`. |
| Image missing though the file exists | Image paths are root-absolute (`/resources/...`), not relative to the `.typ` file. |

## Converting a PPTX deck

`scripts/pptx_to_typst.py` extracts titles, nested bullets, tables, speaker notes **and the
embedded images**, then emits a draft that compiles as-is. It needs `python-pptx`
(`pip install python-pptx`).

Run it from the Typst project root so the extracted images land where the deck expects
them:

```bash
python3 .agents/skills/tum-typst-presentation/scripts/pptx_to_typst.py deck.pptx -o draft.typ
```

Images go to `resources/<deck-name>/` and are referenced as `/resources/<deck-name>/...`;
override with `--assets-dir`. Use `--theme-import "/theme/theme.typ"` if your theme is not
next to the deck, and `--no-notes` to drop speaker notes. A slide-by-slide summary of what
was detected goes to stderr.

The script picks the slide type from the content it finds - cover, section divider, image,
image-beside-text, or plain content - and sizes images so nothing overflows. What it
cannot do is judge meaning, so the draft is a starting point. Work through it and:

- Check the `// REVIEW:` comments; each marks something the script could not place, such
  as a second image on a slide.
- Confirm the author, title, school, and chair in the `tum-theme` block.
- Condense the bodies. PowerPoint bullets are usually full sentences and read as walls of
  text at 14pt; the `// note:` comments carry the speaker notes, which often say what the
  slide was actually for.
- Merge or drop slides that only existed to work around PowerPoint's layout.
- Add `#show: later` where a build would help the narration.

Then compile and inspect the pages as described above before handing it back.

## Reference

`references/theme-api.md` - full `tum-theme` parameter list, the color palette from
`colors.typ`, and the measured page geometry.
