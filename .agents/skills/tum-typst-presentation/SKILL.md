---
name: tum-typst-presentation
description: >
  Creates, edits, and converts presentations built on the TUM (Technical University of
  Munich) Touying/Typst template in this repository - theme.typ, tum-theme, title-slide,
  outline-slide, focus-slide, image-slide, heading-based slides. Use this skill whenever
  the user wants to write a new TUM presentation, add or edit slides, restructure a talk,
  fix a slide that renders wrong, add speaker notes or animations, export a handout, or
  convert an existing PowerPoint (PPTX) deck into Typst. Trigger even for casual requests
  like "make slides about X", "add a slide on Y", "turn this pptx into typst", "why is my
  slide duplicated", or "how do I animate this".
---

# TUM Typst Presentation Skill

This repo is a [Touying](https://touying-typ.github.io/) theme producing TUM-branded
16:9 slides. `theme.typ` defines the theme and slide functions and re-exports all of
Touying, `colors.typ` the corporate palette, `resources/` the logos and photos.

The single most useful thing you can do here is **compile and look at the result**. Typst
silently reflows overfull slides onto a second page, so a deck can compile cleanly and
still be wrong. See [Verifying your work](#verifying-your-work) - do it before you report
back.

## Setting up a presentation

```typ
#import "theme.typ": *

#show: tum-theme.with(
  title: [Presentation Title],
  authors: ("Your Name",),
  subtitle: [Optional subtitle],                   // optional
  school: [TUM School of ...],                     // optional, line omitted if unset
  chair: [Lehrstuhl für ...],                      // optional
  footer-infos: ("Optional extra footer text",),
  lang: "en",                                      // or "de"
  date: datetime(year: 2025, month: 6, day: 10),   // optional, defaults to today
)
```

Any Touying `config-*` dictionary can be passed as an extra positional argument, e.g.
`config-common(show-notes-on-second-screen: right)`.

**About the import path.** `theme.typ` loads its own logos relative to itself, so keep
`resources/` next to it. Image paths you pass to `image()` are root-absolute, and Typst
resolves those against the *project root*, which defaults to the directory of the file you
compile. So the import path and the compile command have to agree:

| Layout | Import | Compile from |
|---|---|---|
| Deck next to `theme.typ` (this repo) | `#import "theme.typ": *` | that directory |
| Theme copied into `theme/` (with its `resources/`) | `#import "/theme/theme.typ": *` | project root |
| Deck in a subfolder, theme above it | `#import "/theme.typ": *` | `typst compile --root . slides/deck.typ` |

A bare `../theme.typ` fails with *"would escape the project root"* - Typst will not read
outside the root. Pass `--root` rather than rewriting paths.

## Writing slides

Slides are written as a document. **Every `==` heading starts a new slide** and every `=`
heading starts a section, which automatically gets a section divider slide and an entry in
the outline and PDF bookmarks.

```typ
#title-slide()
#outline-slide()

= Introduction

== Key findings
- Result one
- Result two
```

Content placed directly after a `=` heading, or in a `#slide[...]` with no `==` heading
before it in that section, becomes a slide without a title. `---` on its own line starts a
new slide that keeps the current title.

### `#title-slide()`
Opening slide built from the `tum-theme` metadata: title, subtitle, authors, university,
school, chair, location, date. Default has the TUM tower watermark;
`#title-slide(flags: true)` uses the full-bleed TUM flags photo with white text. Use the
flags variant once, for impact - the default reads as more formal. Fields can be overridden
per call, e.g. `#title-slide(subtitle: [Final talk])`.

### `#outline-slide()`
Table of contents from the `=` sections. The title is localized ("Outline"/"Inhalte");
pass `title: [Agenda]` to change it.

### `#focus-slide[...]`
Full-bleed TUM blue slide with large white text, for a key statement, a closing line or
"Questions?". Does not count towards the slide number.

### `#image-slide(image(...))`
Scales its content to fill the space below the title, so it never overflows whatever the
image's size. Put it after a `==` heading:

```typ
== Architecture
#image-slide(image("/resources/arch.png", alt: "System architecture"))
```

A path to a missing file is a hard error (*"file not found"*), so only write the path once
the file is actually there.

### `#slide(composer: ...)[...][...]`
Multi-column layout. Put it right after the `==` heading whose title it should carry:

```typ
== Comparison
#slide(composer: (1fr, 1fr))[
  - Left column
][
  #image("/resources/chart.png", width: 100%)
]
```

### Strong text and alerts
`*strong*` text renders in TUM blue (Touying's alert). Use `tum-colors.<name>` from
`colors.typ` for any other color, e.g. `#text(fill: tum-colors.accent-orange)[...]`.

## Layout recipes

The body of a content slide below the title is about **27.7 cm wide and 10.8 cm tall**.
Percentage heights do not help here, because the body block has automatic height, so
`height: 70%` resolves against nothing useful. Size images in absolute units and stay
under the budget, or use `image-slide` to let the theme scale them.

**Image with a caption or a line of text** - cap at `9cm` to leave room for the text:

```typ
== Throughput
#align(center, image("/resources/chart.png", height: 9cm))
Measured on 4x A100, batch size 32.
```

**Image beside text** - the fixed box means it never overflows in either direction:

```typ
== Architecture
#slide(composer: (1fr, 1fr))[
  - Ingest layer batches requests
  - Scheduler assigns GPUs
][
  #image("/resources/arch.png", width: 100%, height: 10cm, fit: "contain")
]
```

**Image alone** - prefer `image-slide`; with an explicit size, `height: 10cm` is the
practical ceiling.

## Animations

`#pause` reveals everything after it on the next step. `#meanwhile` resets to the first
step, so content after it shows from the start. Each step adds one PDF page, so a slide
with two `#pause`s becomes three pages - expected, not a bug.

```typ
== Three steps
*Step 1:* Set up the environment.
#pause
*Step 2:* Run the experiment.
#pause
*Step 3:* Analyze the results.
```

For finer control:

- `#uncover("2-")[...]` - visible from step 2 on, space reserved before that.
- `#only("3")[...]` - present only on step 3, no space reserved otherwise.
- `#alternatives[A][B][C]` - swaps content in place, one per step.
- `#item-by-item[- a\n- b\n- c]` - reveals list items one at a time.

See the [Touying animation docs](https://touying-typ.github.io/docs/tutorials/dynamic/simple)
for callback-style animations, math and CeTZ/Fletcher animations.

## Speaker notes

Put `#speaker-note[...]` on the slide it belongs to. Notes are invisible by default. To
present with notes, pass `config-common(show-notes-on-second-screen: right)` to
`tum-theme`. Every page then gets the notes panel on its right half, which pdfpc and
most dual-screen PDF viewers can split off.

## Output modes

The same source compiles to three outputs, picked on the command line:

```sh
typst compile deck.typ                                       # slides with animations
typst compile deck.typ handout.pdf --input export-mode=handout   # last step of each slide only
typst compile deck.typ article.pdf --input export-mode=article   # continuous A4 document
```

Article mode drops the title and outline slides (it prints its own title block) and
collapses animations to their final state. Use `#article-text[...]` on a slide to give the
article a prose paragraph instead of the slide's bullets, and `#article-only[...]` for
content that only appears in the article.

## Writing good slides

Give each slide one idea. If a slide needs more than ~6 bullets, split it. Make titles
carry the message - "Results show 40% speedup" beats "Results", because the audience reads
the title first and often only the title.

Keep bodies to phrases rather than sentences; the slides support the talk, they are not a
transcript. Move the full sentences into `#speaker-note`. And vary the rhythm - several
text slides in a row lose the room, so break them up with an image slide, a reveal, or a
focus slide.

## Verifying your work

```sh
typst compile deck.typ                 # produces deck.pdf
typst watch deck.typ                   # live reload while iterating
```

Compiling is necessary but not sufficient - an overfull slide silently continues on an
extra page with the same title rather than raising an error. To catch that, compile once
with overflow detection, which keeps every slide on one page and warns about the ones that
do not fit:

```typ
#show: tum-theme.with(..., config-common(breakable: false))
```

The warning reads `[touying] detecting slide content overflow at page N` (Typst reports it
as an "unknown font family" warning, which is how Touying emits it). Remove the option
again once the deck is clean. Then render the pages and actually look at them:

```sh
typst compile deck.typ page-{0p}.png --format png --ppi 60
```

Then read the PNGs. You are checking for: two consecutive pages with the same title but
different content and slide numbers (that is overflow, not an animation step), images
running past the footer, and text that has wrapped badly. Count the pages too - they should equal the number of slides (including one
divider per `=` section) plus one extra per animation step.

Fix overflow by lowering the image `height:`, switching to `image-slide`, trimming body
text, or splitting the slide.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `file not found (searched at .../theme.typ)` | Compiling from the wrong directory. Compile where `theme.typ` lives, or use a root-absolute import plus `--root`. |
| `path "../theme.typ" would escape the project root` | Typst will not read above the root. Add `--root <project-dir>`. |
| A slide appears twice with the same title, the second copy holding the rest of the content | Content overflow. Reduce image height, use `image-slide`, trim text, or split the slide. |
| A slide has no title | Its content follows a `=` section heading with no `==` heading in between. Add one. |
| Text renders in a serif fallback; `typst fonts` lacks Arial | The theme defaults to `font: "Arial"`. On Linux install `ttf-mscorefonts-installer` (this is what `.github/workflows/` does) or pass `font:` to `tum-theme`. |
| Image missing though the file exists | Image paths are root-absolute (`/resources/...`), not relative to the `.typ` file. |
| `#show: later` is unknown | Old Polylux syntax. Use `#pause`. |
| `title-content-slide` is unknown | Old Polylux syntax. Use an `== Title` heading. |

## Converting a PPTX deck

`scripts/pptx_to_typst.py` extracts titles, nested bullets, tables, speaker notes **and the
embedded images**, then emits a heading-based draft that compiles as-is. It needs
`python-pptx` (`pip install python-pptx`).

Run it from the Typst project root so the extracted images land where the deck expects
them:

```bash
python3 .agents/skills/tum-typst-presentation/scripts/pptx_to_typst.py deck.pptx -o draft.typ
```

Images go to `resources/<deck-name>/` and are referenced as `/resources/<deck-name>/...`;
override with `--assets-dir`. Use `--theme-import "/theme/theme.typ"` if your theme is not
next to the deck, and `--no-notes` to drop speaker notes. A slide-by-slide summary of what
was detected goes to stderr.

The script picks the layout from the content it finds - cover, section (`=`), image
(`image-slide`), image-beside-text (two-column `slide`), or plain content - and sizes
images so nothing overflows. Speaker notes become `#speaker-note[...]`. What it cannot do
is judge meaning, so the draft is a starting point. Work through it and:

- Check the `// REVIEW:` comments; each marks something the script could not place, such
  as a second image on a slide or a slide without a title.
- Confirm the authors, title, school, and chair in the `tum-theme` block.
- Add `alt:` descriptions to images if the PDF should be accessible.
- Condense the bodies. PowerPoint bullets are usually full sentences and read as walls of
  text at 14pt; the speaker notes often say what the slide was actually for.
- Merge or drop slides that only existed to work around PowerPoint's layout.
- Add `#pause` where a build would help the narration, and an `#outline-slide()` if the
  deck has sections.

Then compile and inspect the pages as described above before handing it back.

## Reference

`references/theme-api.md` - full `tum-theme` parameter list, slide functions, the color
palette from `colors.typ`, and the measured page geometry.
