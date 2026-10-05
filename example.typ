#import "theme.typ": *

#show: tum-theme.with(
  title: [My awesome topic I want to put into a presentation],
  subtitle: [A short tour of the theme],
  authors: ("Max Mustermann",),
  school: [TUM School of Musterverfahren],
  chair: [Lehrstuhl für Mustertechnik],
  footer-infos: ("Excellence",),
)

#title-slide()

#title-slide(flags: true)

#outline-slide()

= Basics

== Writing slides

Every `==` heading starts a new slide, every `=` heading a section.

- No slide functions needed
- Sections show up in the outline and PDF bookmarks
- *Strong text* is highlighted in TUM blue

#speaker-note[
  Only visible with
  `config-common(show-notes-on-second-screen: right)`.
]

== Step-by-step reveals

This is shown first.

#pause
It is a very important section.

#pause
It is the best section.

#meanwhile
#text(fill: tum-colors.secondary-grey-mid)[`#meanwhile` shows this on every step.]

== Fine-grained animations

#uncover("2-")[`#uncover` keeps the space reserved.]

#only("3")[`#only` takes no space until it appears.]

#alternatives[First alternative][Second alternative][Third alternative]

= Layouts

== Two columns

#slide(composer: (1fr, 1fr))[
  - Left column
  - Lists, tables, code
][
  #lorem(30)
]

== The TUM tower

#image-slide(image("/resources/TUM-turm.jpg", alt: "The TUM tower"))

#focus-slide[
  Focus slides are for a single statement.
]

== Long text

#lorem(100)
