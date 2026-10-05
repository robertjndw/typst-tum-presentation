# TUM Typst Presentation Template

This is a Typst template for presentations at the Technical University of Munich (TUM). It is based on the [TUM Corporate Design](https://www.it.tum.de/en/it/faq/media-production-design/corporate-design/where-can-i-find-templates-for-the-tum-corporate-design/).

It is built on [Touying](https://touying-typ.github.io/), which handles animations, speaker notes, handouts and article export. Anything not covered here is in the [Touying documentation](https://touying-typ.github.io/docs/intro).

![Slides from the example presentation](https://raw.githubusercontent.com/robertjndw/typst-tum-presentation/main/.github/images/preview.png)

An example presentation is included in the [`example.typ`](./example.typ) file. The latest compiled version of the example presentation can be found in the release section of GitHub.

Feel free to use this template for your presentations at TUM. If you have any questions or suggestions, open an issue or pull request. Contributions are welcome!

## Installation
For detailed installation instructions, please refer to the [official installation guide](https://github.com/typst/typst). Here, we provide basic steps for installing Typst's CLI:

- You can get sources and pre-built binaries from the [releases page](https://github.com/typst/typst/releases).
- Use package managers like `brew` or `pacman` to install Typst. Be aware that the versions in the package managers might lag behind the latest release.
- If you have a [Rust](https://rustup.rs/) toolchain installed, you can also install the latest development version.

Nix and Docker users, please refer to the official installation guide for detailed instructions.


## Usage
To use this template for your presentation, you download this repository and copy the files into your presentation directory (except the `example.typ` file). Recommended is to create a dedicated directory named `theme` for copying the files. Keep the `resources` folder next to `theme.typ`.

Needs Typst 0.15+ and the Arial font (or pass `font:` to `tum-theme`).

#### 1. Importing the Template
Import the theme. It re-exports all of Touying, so this one import is all you need:
```typ
#import "/theme/theme.typ": *
```

Alternatively, you can use the GitHub template feature to create a new repository with this template. In this case, you can directly start creating your presentation in the `example.typ` file (rename it to `presentation.typ`).

#### 2. Setting Metadata
Configure the theme with the metadata of your presentation:
```typ
#show: tum-theme.with(
  lang: "en", // or "de"
  title: [My awesome topic I want to put into a presentation],
  authors: ("Max Mustermann",),
  school: [TUM School of Musterverfahren],
  chair: [Lehrstuhl für Mustertechnik],
  footer-infos: ("Excellence",),
)
```
`subtitle`, `date` and `location` are optional too. Any Touying `config-*` dictionary can be passed alongside, e.g. `config-common(handout: true)`.

#### 3. Creating Slides
Slides are written as a document: every `==` heading starts a slide and every `=` heading a section with its own divider slide.
```typ
#title-slide()           // or #title-slide(flags: true)
#outline-slide()

= Introduction

== Motivation
This is the first slide of the presentation.
```

The theme also provides:

| Function | Purpose |
|---|---|
| `#title-slide(flags: false)` | Opening slide. `flags: true` uses the TUM flags photo. |
| `#outline-slide()` | Table of contents built from the `=` sections. |
| `#focus-slide[...]` | Full-bleed TUM blue slide for a key statement. |
| `#image-slide(image(...))` | Scales an image to fill the space below the title. |
| `#slide(composer: (1fr, 1fr))[...][...]` | Multi-column layout, placed after a `==` heading. |

#### 4. Adding Dynamics
Reveal content step by step with `#pause`, or use `#uncover`, `#only` and `#alternatives` for finer control:
```typ
This is shown first.
#pause
This is hidden first.
```
See the [Touying animation docs](https://touying-typ.github.io/docs/tutorials/dynamic/simple) for more.

#### 5. Speaker Notes
Add `#speaker-note[...]` to a slide. To show the notes next to the slides, for example in [pdfpc](https://pdfpc.github.io/) or on a second screen, pass `config-common(show-notes-on-second-screen: right)` to `tum-theme`.

#### 6. Compiling the Presentation
Once you have created your presentation, you can compile it by running the following standard Typst command in the terminal:
```sh
# Creates `presentation.pdf` in working directory.
typst compile presentation.typ
```

You can also watch source files and automatically recompile on changes. This is faster than compiling from scratch each time because Typst has incremental compilation.
```sh
# Watches source files and recompiles on changes.
typst watch presentation.typ
```

The same source can also produce a handout (one page per slide, animations collapsed) or a continuous A4 document:
```sh
typst compile presentation.typ handout.pdf --input export-mode=handout
typst compile presentation.typ article.pdf --input export-mode=article
```

---
## Further Resources

- [Typst Documentation](https://typst.app/docs/)
- [Touying Documentation](https://touying-typ.github.io/)
- [Typst Guide for LaTeX Users](https://typst.app/docs/guides/guide-for-latex-users/)
- [Tinymist VS Code Extension](https://marketplace.visualstudio.com/items?itemName=myriad-dreamin.tinymist)