# TUM Theme API Reference

## `tum-theme` parameters

| Parameter      | Type              | Default                        | Description |
|----------------|-------------------|--------------------------------|-------------|
| `aspect-ratio` | string            | `"16-9"`                       | Slide ratio; becomes Typst's `presentation-<ratio>` paper. |
| `lang`         | string            | `"en"`                         | `"en"` or `"de"`. Selects the university name and the default location (Munich/München). |
| `font`         | string or array   | `"Arial"`                     | Font family for all text. |
| `title`        | string            | `"Title of the TUM presentation"` | Shown on title slides and set as PDF document title. |
| `location`     | string or none    | `none` → Munich/München        | Event location, shown on the title slide. |
| `date`         | datetime or auto  | `auto` (today)                 | Rendered as `[day]. [month repr:long] [year]` and set as PDF document date. |
| `authors`      | array of strings  | `()`                           | Joined with `, ` on the title slide, and prepended to the footer. |
| `school`       | string or none    | `none`                         | Title slide only; the line is omitted if unset. |
| `chair`        | string or none    | `none`                         | Title slide only; the line is omitted if unset. |
| `footer-infos` | array of strings  | `()`                           | Appended after `authors`; the whole list is joined with ` \| `. |

Note `authors` must be a Typst array - a single author needs the trailing comma:
`authors: ("Max Mustermann",)`.

## Slide functions

| Function | Body? | Notes |
|---|---|---|
| `title-slide(flags: false)` | no | `flags: true` swaps the tower watermark for the full-bleed flags photo and white text. |
| `title-content-slide(title: "Title", body)` | yes | `title` accepts content, so `text(tum-colors.primary-blue)[...]` works. Renders black by default. The title is a level 1 heading. |
| `title-image-slide(title: "Title", image-path: none, alt: none)` | no | Centers `image(image-path, alt: alt)` with no size control. `image-path` must be root-absolute. Omitting it gives a title-only slide. A path to a missing file is a hard error. `alt` describes the image in accessible PDFs. |
| `empty-slide(body)` | yes | Footer and slide number only. The other two build on this. |

## Page geometry

Measured on the default `16-9` paper (33.87 × 19.05 cm) with the theme's margins
(top 3 cm, bottom 1 cm, x 1 cm):

| Quantity | Value |
|---|---|
| Body width | ~31.9 cm |
| Body height below the title | ~10.5 cm |
| Safe image height, image alone | `10cm` |
| Safe image height with a caption below | `9cm` |
| Title size | 25 pt (both title slide and content slides) |
| Base text size | 14 pt, font Arial |

Percentage heights (`height: 70%`) do not constrain anything useful - the body block has
automatic height. Use absolute units. Content exceeding the body height reflows onto a
second page with no warning.

## Colors (`colors.typ`)

All colors are in the `tum-colors` dictionary (defined in `colors.typ`, exported by `theme.typ`), e.g. `tum-colors.primary-blue`.

| Variable                  | Hex value  | Usage |
|---------------------------|------------|-------|
| `tum-colors.primary-blue`         | `#0065BD`  | Primary brand color - headings, accents |
| `tum-colors.primary-white`        | `#ffffff`  | Backgrounds |
| `tum-colors.primary-black`        | `#000000`  | Body text |
| `tum-colors.secondary-blue`       | `#005293`  | Darker blue for contrast |
| `tum-colors.secondary-blue-dark`  | `#003359`  | Darkest blue |
| `tum-colors.secondary-grey-dark`  | `#333333`  | Dark grey text |
| `tum-colors.secondary-grey-mid`   | `#808080`  | Mid grey |
| `tum-colors.secondary-grey-light` | `#CCCCCC`  | Light grey borders/dividers |
| `tum-colors.accent-white`         | `#DAD7CB`  | Warm off-white |
| `tum-colors.accent-orange`        | `#E37222`  | Orange accent (accents only, never backgrounds) |
| `tum-colors.accent-green`         | `#A2AD00`  | Green accent (accents only) |
| `tum-colors.accent-blue-light`    | `#98C6EA`  | Light blue accent |
| `tum-colors.accent-blue-mid`      | `#64A0C8`  | Mid blue accent |

## Bundled resources

`resources/TUM-logo.svg`, `resources/TUM-logo-white.svg`, `resources/TUM-turm.jpg`,
`resources/TUM-flags.jpg`. The theme references them relative to `theme.typ`, so keep the
`resources/` folder next to it.

## Polylux

Template pins `@preview/polylux:0.4.0`.

- `#show: later` - everything after this point appears on the next step; one extra PDF
  page per `later`.
- `toolbox.slide-number` - used by the theme's footer.

`theme.typ` re-exports `later`.

Further primitives (`uncover`, `only`, `pause`) in the
[Polylux book](https://polylux.dev/book/polylux.html).
