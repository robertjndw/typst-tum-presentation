#import "@preview/polylux:0.4.0": later, slide, toolbox
#import "colors.typ": tum-colors

// Set by tum-theme, read back by the slide functions.
#let tum-meta = state("tum-meta", (:))

#let tum-theme(
  aspect-ratio: "16-9",
  lang: "en",
  font: "Arial",
  title: "Title of the TUM presentation",
  location: none,
  date: auto,
  authors: (),
  school: none,
  chair: none,
  footer-infos: (),
  body,
) = {
  assert(type(authors) == array, message: "authors must be an array, e.g. (\"Max Mustermann\",)")
  assert(type(footer-infos) == array, message: "footer-infos must be an array")

  let university-name = (en: "Technical University Munich", de: "Technische Universität München")
  let default-location = (en: "Munich", de: "München")
  let date = if date == auto { datetime.today() } else { date }

  set document(title: title, author: authors, date: date)
  set page(
    paper: "presentation-" + aspect-ratio,
    margin: 0em,
    background: place(
      top + right,
      pad(1cm, image("resources/TUM-logo.svg", height: 1cm, alt: "TUM logo")),
    ),
  )

  set text(lang: lang, font: font, size: 14pt)
  set block(spacing: 1em)

  // Titles are real headings so the PDF gets bookmarks. Polylux already
  // un-outlines the copies on `later` subslides.
  show heading.where(level: 1): set text(size: 25pt, weight: "regular")
  show heading.where(level: 1): set block(above: 0pt, below: 0.8cm)

  tum-meta.update((
    title: title,
    university: university-name.at(lang),
    location: if location == none { default-location.at(lang) } else { location },
    date: date.display("[day]. [month repr:long] [year]"),
    authors: authors.join(", "),
    school: school,
    chair: chair,
    footer: (authors + footer-infos).join(" | "),
  ))

  body
}

#let title-slide(flags: false) = {
  slide({
    // Decorative, so no alt text.
    if flags {
      pdf.artifact(place(center, image("resources/TUM-flags.jpg", width: 100%, height: 100%)))
      pdf.artifact(place(
        top + right,
        pad(1cm, image("resources/TUM-logo-white.svg", height: 1cm)),
      ))
    } else {
      pdf.artifact(place(
        right + bottom,
        pad(1cm, image("resources/TUM-turm.jpg", height: 12cm)),
      ))
    }
    set text(fill: white) if flags

    context {
      let meta = tum-meta.get()
      // Skip unset school/chair instead of leaving a gap.
      let lines = (
        meta.authors,
        meta.university,
        meta.school,
        meta.chair,
        [#meta.location, #meta.date],
      ).filter(line => line not in (none, ""))

      pad(x: 2cm, y: 3cm, {
        heading(level: 1, meta.title)
        stack(dir: ttb, spacing: 0.5cm, ..lines)
      })
    }
  })
}

#let empty-slide(body) = {
  let footer = context {
    set align(left + bottom)
    set text(size: 11pt)
    pad(bottom: 0.4cm, {
      tum-meta.get().footer
      h(1fr)
      toolbox.slide-number
    })
  }

  set page(
    margin: (top: 3cm, bottom: 1cm, x: 1cm),
    footer: footer,
  )

  slide(body)
}

#let title-content-slide(title: "Title", body) = {
  empty-slide({
    heading(level: 1, title)
    body
  })
}

// image-path is resolved relative to this file, so use a root-absolute path
// like "/resources/photo.jpg".
#let title-image-slide(title: "Title", image-path: none, alt: none) = {
  title-content-slide(title: title, {
    if image-path != none {
      align(center, image(image-path, alt: alt))
    }
  })
}
