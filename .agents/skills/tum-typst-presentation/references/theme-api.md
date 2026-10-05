# TUM Theme API Reference

## `tum-theme` parameters

| Parameter      | Type                 | Default                            | Description |
|----------------|----------------------|------------------------------------|-------------|
| `aspect-ratio` | string               | `"16-9"`                           | `"16-9"` or `"4-3"`. |
| `lang`         | string               | `"en"`                             | `"en"` or `"de"`. Localizes the university name, the default location, the date and the outline title. |
| `font`         | string or array      | `"Arial"`                          | Font family for all text, also used in article mode. |
| `title`        | content              | `[Title of the TUM presentation]`  | Shown on the title slide and set as PDF document title. |
| `subtitle`     | content or none      | `none`                             | Shown below the title on the title slide. |
| `authors`      | string or array      | `()`                               | Joined with `, ` on the title slide, prepended to the footer, and set as PDF author. |
| `date`         | datetime, content or auto | `auto` (today)                | Rendered as `05. October 2026` / `05. Oktober 2026` and set as PDF document date. |
| `school`       | content or none      | `none`                             | Title slide only; the line is omitted if unset. |
| `chair`        | content or none      | `none`                             | Title slide only; the line is omitted if unset. |
| `location`     | content or auto      | `auto` → Munich/München            | Shown on the title slide before the date. |
| `footer-infos` | array                | `()`                               | Appended after `authors`; the whole list is joined with ` \| `. |
| positional     | `config-*` dicts     |                                    | Passed through to Touying, e.g. `config-common(handout: true)`. |

A single author still works as a plain string, but `footer-infos` must be an array: one
entry needs the trailing comma, `("Excellence",)`.

Useful pass-through configs:

- `config-common(show-notes-on-second-screen: right)` - speaker-note panel beside every slide.
- `config-common(handout: true)` - same as `--input export-mode=handout`.
- `config-methods(cover: utils.alpha-changing-cover)` - show not-yet-revealed content greyed out instead of hidden.

## Slide functions

| Function | Notes |
|---|---|
| `== Title` | A content slide. The usual way to make one. |
| `= Section` | A section divider slide, plus outline and bookmark entry. |
| `title-slide(flags: false, ..fields)` | `flags: true` swaps the tower watermark for the full-bleed flags photo and white text. Named arguments override metadata fields for this slide. Not numbered. |
| `outline-slide(title: ..)` | Lists the `=` sections. Title localized ("Outline"/"Inhalte") unless given. |
| `focus-slide[body]` | TUM blue background, 32pt white text. Not numbered. |
| `image-slide(body)` | Scales `body` to fill the space below the title. Place after a `==` heading. |
| `slide(composer: ..)[..][..]` | The underlying content slide. Use after a `==` heading for multi-column layouts: `composer: (1fr, 2fr)` or `composer: 2`. |
| `new-section-slide` | What `=` calls. Rarely called directly. |

Everything from Touying is re-exported: `pause`, `meanwhile`, `uncover`, `only`,
`alternatives`, `item-by-item`, `speaker-note`, `article-text`, `article-only`, `utils`,
`components`, `config-*`.

## Page geometry

Measured on the default `16-9` page (29.7 × 16.7 cm), margins top 4.4 cm, bottom 1.5 cm,
x 1 cm:

| Quantity | Value |
|---|---|
| Body width | ~27.7 cm |
| Body height below the title | ~10.8 cm |
| Safe image height, image alone | `10cm` (or use `image-slide`) |
| Safe image height with a caption below | `9cm` |
| Title size | 25 pt |
| Section title size | 32 pt |
| Base text size | 14 pt, font Arial |

Percentage heights (`height: 70%`) do not constrain anything useful - the body block has
automatic height. Use absolute units. Content exceeding the body height continues on an
extra page with the same title and no warning, unless `config-common(breakable: false)` is
set, which keeps it on one page and warns instead.

## Colors (`colors.typ`)

All colors are in the `tum-colors` dictionary (defined in `colors.typ`, exported by
`theme.typ`), e.g. `tum-colors.primary-blue`. The theme also maps them to Touying's color
slots: `primary` is TUM blue, `secondary` the secondary blue, `tertiary` the dark blue.

| Variable                  | Hex value  | Usage |
|---------------------------|------------|-------|
| `tum-colors.primary-blue`         | `#0065BD`  | Primary brand color - headings, accents, strong text, focus slides |
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

## Touying

The theme pins `@preview/touying:0.8.0`, which needs Typst 0.15+. Full documentation at
[touying-typ.github.io](https://touying-typ.github.io/).
