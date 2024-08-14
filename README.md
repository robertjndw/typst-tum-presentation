# TUM Typst Presentation Template

This is a Typst polylux template for presentations at the Technical University of Munich (TUM). It is based on the [TUM Corporate Design](https://www.it.tum.de/en/it/faq/media-production-design/corporate-design/where-can-i-find-templates-for-the-tum-corporate-design/).

It utilizes the [Polylux package](https://github.com/andreasKroepelin/polylux) for Typst. For optimal results, it is recommended to take a look into the [Polylux book](https://polylux.dev/book/polylux.html)

An example presentation is included in the [`example.typ`](./example.typ) file. The latest compiled version of the example presentation can be found in the release section of GitHub.

Feel free to use this template for your presentations at TUM. If you have any questions or suggestions, open an issue or pull request. Contributions are welcome!

## Installation
For detailed installation instructions, please refer to the [official installation guide](https://github.com/typst/typst). Here, we provide basic steps for installing Typst's CLI:

- You can get sources and pre-built binaries from the [releases page](https://github.com/typst/typst/releases).
- Use package managers like `brew` or `pacman` to install Typst. Be aware that the versions in the package managers might lag behind the latest release.
- If you have a [Rust](https://rustup.rs/) toolchain installed, you can also install the latest development version.

Nix and Docker users, please refer to the official installation guide for detailed instructions.


## Usage
To use this template for your presentation, you download this repository and copy the files into your presentation directory (except the `example.typ` file). Recommended is to create a dedicated directory named `theme` for copying the files. 

#### 1. Importing the Template
You can start creating your presentation by creating a new `.typ` file (e.g. `presentation.typ`) and import the template with the following line:
```
#import "/theme/theme.typ": *
```

Alternatively, you can use the GitHub template feature to create a new repository with this template. In this case, you can directly start creating your presentation in the `example.typ` file (rename it to `presentation.typ`).

#### 2. Setting Metadata
Configure the theme with the metadata of your presentation. This can be done by setting the following variables:
```
#show: tum-theme.with(
  authors: ("Max Mustermann",), 
  title: "My awesome topic i want to put into a presentation",
  footer-infos: ("Excellence",),
  school: "TUM School of Musterverfahren",
  chair: "Lehrstuhl für Mustertechnik",
)
```

#### 3. Creating Slides
Once the metadata is set, you can start creating your slides. The template provides a variety of slide types, which can be used by calling the respective function. For example, to create a title slide, you can use the following code:
```
#title-slide()
```
For a standard title-content slide you can use:
```
#title-content-slide(title: "Section 1", [ #text("This is the first section of the presentation.")] )
```

#### 4. Adding Dynamic
You can step-by-step reveal content on slides by using the `#pause` function. For example, to reveal a list of items one by one, you can use the following code:
```
#text("This is shown first.")
#pause
#text("This is hidden first.")
```

#### 5. Compiling the Presentation
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

---
## Further Resources

- [Typst Documentation](https://typst.app/docs/)
- [Typst Polylux Book](https://polylux.dev/book/polylux.html)
- [Typst Guide for LaTeX Users](https://typst.app/docs/guides/guide-for-latex-users/)
- [Typst VS Code Extension (inofficial)](https://marketplace.visualstudio.com/items?itemName=nvarner.typst-lsp)