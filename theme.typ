#import "@preview/polylux:0.4.0": *
#import "colors.typ": *

// State definitions
#let title-state = state("title-state", none)
#let date-state = state("date-state", none)
#let location-state = state("location-state", none)
#let author-state = state("author-state", none)

#let university-state = state("university-state", none)
#let school-state = state("school-state", none)
#let chair-state = state("chair-state", none)

#let footer-state = state("footer-state", none)

// Dictionary for translations
#let university-name = (en: "Technical University Munich", de: "Technische Universität München")
#let default-location = (en: "Munich", de: "München")

#let tum-theme(
  aspect-ratio: "16-9",
  lang: "en", 
  title: "Title of the TUM presentation",
  location: none,
  date: datetime.today(),
  authors: (),
  school: "TUM School of Musterverfahren",
  chair: "Lehrstuhl für Mustertechnik",
  footer-infos: (),
  body
) = {
  set document(
    title: title,
    author: authors,
    date: datetime.today()
  )
  set page(
    paper: "presentation-" + aspect-ratio,
    margin: 0em,
    header: none,
    footer: none,
    background: place(top + right,
        pad(1cm, image("/resources/TUM-logo.svg", height: 1cm))
      )
  )

  set text(lang: lang, font: "Arial", size: 14pt)
  set block(spacing: 1em )

  university-state.update(university-name.at(lang))
  if location == none {
    location-state.update(default-location.at(lang))
  } else {
    location-state.update(location)
  }
  title-state.update(title)
  date-state.update(date.display("[day]. [month repr:long] [year]"))
  author-state.update(authors.join(", "))
  school-state.update(school)
  chair-state.update(chair)

  let complete_footer = authors + footer-infos
  footer-state.update(complete_footer.join(" | "))

  body
}

#let title-slide(flags: false) = {
  slide({
    if flags {
      // TUM Background
      place(center, 
        pad(image("/resources/TUM-flags.jpg", width: 100%, height: 100%))
      )
      place(top + right,
        pad(1cm, image("/resources/TUM-logo-white.svg", height: 1cm))
      )
    } else {
      // TUM Watermark
      place(right + bottom, 
        pad(1cm, image("/resources/TUM-turm.jpg", height: 12cm))
      )
    }
    set text(white) if flags
    // Presentation information
    context pad(
      x: 2cm,
      y: 3cm,
      {
        text(title-state.get(), size: 25pt)
        v(1cm)
        stack(
          dir: ttb,
          spacing: 0.5cm,
          author-state.get(),
          university-state.get(),
          school-state.get(),
          chair-state.get(),
          [#location-state.get(), #date-state.get()],
        )
      }
    )
  })
}

#let empty-slide(body) = {
  // Footer styling
  let footer = {
    set align(left + bottom)
    set text(size: 11pt)
    context pad(
      bottom: 0.4cm,
      {
        footer-state.get()
        h(1fr)
        toolbox.slide-number
      }
    )
  }
  // Page setup
  set page(
    margin: ( top: 3cm, bottom: 1cm, x: 1cm ),
    footer: footer,
  )

  slide({
    body
  })
}

#let title-content-slide(title: "Title", body) = {
  // Reuse empty-slide with predefined layout
  empty-slide({
    text(title, size: 25pt)
    v(0.8cm)
    body
  })
}

#let title-image-slide(title: "Title", image_path: none) = {
  // Reuse empty-slide with predefined layout
  title-content-slide(title: title, {
      if image != none {
        align(center, image(image_path))
      }
    }
  )
}