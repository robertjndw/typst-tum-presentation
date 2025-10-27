#import "theme.typ": *

#show: tum-theme.with(
  authors: ("Max Mustermann",), 
  title: "My awesome topic I want to put into a presentation",
  footer-infos: ("Excellence",)
)

#title-slide()

#title-slide(flags: true)

#title-content-slide(title: "Section 1", [ 
  #text("This is the first section of the presentation.")

  #show: later
  #text("It is a very important section.")

  #show: later
  #text("It is the best section.")
])

#title-image-slide(title: "Section 2", image_path: "/resources/TUM-turm.jpg")

#title-content-slide(title: "Section 3", lorem(100))