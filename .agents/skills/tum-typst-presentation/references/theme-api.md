# TUM Theme API Reference

## `tum-theme` parameters

| Parameter      | Type              | Default                        | Description |
|----------------|-------------------|--------------------------------|-------------|
| `aspect-ratio` | string            | `"16-9"`                       | Slide ratio; becomes Typst's `presentation-<ratio>` paper. |
| `lang`         | string            | `"en"`                         | `"en"` or `"de"`. Selects the university name and the default location (Munich/München). |
| `title`        | string            | `"Title of the TUM presentation"` | Shown on title slides and set as PDF document title. |
| `location`     | string or none    | `none` → Munich/München        | Event location, shown on the title slide. |
| `date`         | datetime          | `datetime.today()`             | Rendered as `[day]. [month repr:long] [year]`. |
| `authors`      | array of strings  | `()`                           | Joined with `, ` on the title slide, and prepended to the footer. |
| `school`       | string            | `"TUM School of Musterverfahren"` | Title slide only. |
| `chair`        | string            | `"Lehrstuhl für Mustertechnik"` | Title slide only. |
| `footer-infos` | array of strings  | `()`                           | Appended after `authors`; the whole list is joined with ` \| `. |

Note `authors` must be a Typst array - a single author needs the trailing comma:
`authors: ("Max Mustermann",)`.

## Slide functions

| Function | Body? | Notes |
|---|---|---|
| `title-slide(flags: false)` | no | `flags: true` swaps the tower watermark for the full-bleed flags photo and white text. |
| `title-content-slide(title: "Title", body)` | yes | `title` accepts content, so `text(TUM_primary_blue)[...]` works. Renders black by default. |
| `title-image-slide(title: "Title", image_path: none)` | no | Centers `image(image_path)` with no size control. Omitting `image_path` gives a title-only slide. A path to a missing file is a hard error. |
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

Re-exported by `theme.typ`, so `#import "theme.typ": *` is enough.

| Variable                  | Hex value  | Usage |
|---------------------------|------------|-------|
| `TUM_primary_blue`        | `#0065BD`  | Primary brand color - headings, accents |
| `TUM_primary_white`       | `#ffffff`  | Backgrounds |
| `TUM_primary_black`       | `#000000`  | Body text |
| `TUM_secondary_blue`      | `#005293`  | Darker blue for contrast |
| `TUM_secondary_blue_dark` | `#003359`  | Darkest blue |
| `TUM_secondary_grey_dark` | `#333333`  | Dark grey text |
| `TUM_secondary_grey_mid`  | `#808080`  | Mid grey |
| `TUM_secondary_grey_light`| `#CCCCCC`  | Light grey borders/dividers |
| `TUM_accent_white`        | `#DAD7CB`  | Warm off-white |
| `TUM_accent_orange`       | `#E37222`  | Orange accent (accents only, never backgrounds) |
| `TUM_accent_green`        | `#A2AD00`  | Green accent (accents only) |
| `TUM_accent_blue_light`   | `#98C6EA`  | Light blue accent |
| `TUM_accent_blue_mid`     | `#64A0C8`  | Mid blue accent |

## Bundled resources

`/resources/TUM-logo.svg`, `/resources/TUM-logo-white.svg`, `/resources/TUM-turm.jpg`,
`/resources/TUM-flags.jpg`. Referenced with root-absolute paths by the theme, so they must
sit at the Typst project root regardless of where the theme itself lives.

## Polylux

Template pins `@preview/polylux:0.4.0`.

- `#show: later` - everything after this point appears on the next step; one extra PDF
  page per `later`.
- `toolbox.slide-number` - used by the theme's footer.

Further primitives (`uncover`, `only`, `pause`) in the
[Polylux book](https://polylux.dev/book/polylux.html).
