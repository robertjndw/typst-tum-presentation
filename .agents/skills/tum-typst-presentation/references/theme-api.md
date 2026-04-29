# TUM Theme API Reference

## `tum-theme` parameters

| Parameter      | Type              | Default                        | Description |
|----------------|-------------------|--------------------------------|-------------|
| `aspect-ratio` | string            | `"16-9"`                       | Slide ratio. See Typst `paper` values. |
| `lang`         | string            | `"en"`                         | `"en"` or `"de"`. Affects university name and default location. |
| `title`        | string            | `"Title of the TUM presentation"` | Presentation title shown on title slides. |
| `location`     | string or none    | `none` (defaults to Munich/München) | Event location for footer. |
| `date`         | datetime          | `datetime.today()`             | Presentation date. |
| `authors`      | array of strings  | `()`                           | Author names. |
| `school`       | string            | `"TUM School of Musterverfahren"` | School name shown on title slide. |
| `chair`        | string            | `"Lehrstuhl für Mustertechnik"` | Chair name shown on title slide. |
| `footer-infos` | array of strings  | `()`                           | Extra items in the footer (joined with authors by ` \| `). |

## Colors (`colors.typ`)

Import with `#import "colors.typ": *` (already included via `theme.typ`).

| Variable                  | Hex value  | Usage |
|---------------------------|------------|-------|
| `TUM_primary_blue`        | `#0065BD`  | Primary brand color — headings, accents |
| `TUM_primary_white`       | `#ffffff`  | Backgrounds |
| `TUM_primary_black`       | `#000000`  | Body text |
| `TUM_secondary_blue`      | `#005293`  | Darker blue for contrast |
| `TUM_secondary_blue_dark` | `#003359`  | Darkest blue |
| `TUM_secondary_grey_dark` | `#333333`  | Dark grey text |
| `TUM_secondary_grey_mid`  | `#808080`  | Mid grey |
| `TUM_secondary_grey_light`| `#CCCCCC`  | Light grey borders/dividers |
| `TUM_accent_white`        | `#DAD7CB`  | Warm off-white |
| `TUM_accent_orange`       | `#E37222`  | Orange accent (use sparingly) |
| `TUM_accent_green`        | `#A2AD00`  | Green accent (use sparingly) |
| `TUM_accent_blue_light`   | `#98C6EA`  | Light blue accent |
| `TUM_accent_blue_mid`     | `#64A0C8`  | Mid blue accent |

## Polylux animations

The template uses `@preview/polylux:0.4.0`. Key function:

- `#show: later` — reveal subsequent content on the next click/page

Each `later` produces an additional PDF page. The polylux viewer in PDF readers
shows these as presentation steps.

For more advanced animations (uncover, only, pause), see the
[Polylux book](https://polylux.dev/book/polylux.html).
