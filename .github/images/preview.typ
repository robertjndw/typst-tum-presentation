// Builds the README preview from the compiled example:
//   typst compile example.typ example.pdf
//   typst compile --root . .github/images/preview.typ .github/images/preview.png --ppi 144
#let pages = (1, 2, 3, 5, 13, 15)

#set page(width: auto, height: auto, margin: 12pt, fill: rgb("#e6e6e6"))
#grid(
  columns: 3,
  gutter: 12pt,
  ..pages.map(n => box(
    // The slides have no page fill of their own.
    fill: white,
    stroke: 0.5pt + rgb("#cccccc"),
    image("/example.pdf", page: n, width: 9cm),
  )),
)
