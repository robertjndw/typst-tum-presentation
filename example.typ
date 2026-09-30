#import "theme.typ": later, title-content-slide, title-image-slide, title-slide, tum-theme

#show: tum-theme.with(
  authors: ("Max Mustermann",),
  title: "My awesome topic I want to put into a presentation",
  school: "TUM School of Musterverfahren",
  chair: "Lehrstuhl für Mustertechnik",
  footer-infos: ("Excellence",),
)

#title-slide()

#title-slide(flags: true)

#title-content-slide(title: "Section 1")[
  This is the first section of the presentation.

  #show: later
  It is a very important section.

  #show: later
  It is the best section.
]

#title-image-slide(
  title: "Section 2",
  image-path: "/resources/TUM-turm.jpg",
  alt: "The TUM tower",
)

#title-content-slide(title: "Section 3")[
  #lorem(100)
]
