# Maintaining The Sovereign Codex

## Design and files

The cover is an illuminated manuscript jacket. The seal combines a surveyor's compass, a book and an iron hood. The emerald cloak and stone archive carry the medieval setting. The title, author and contrasting gold details were typeset over an original AI-generated pixel-art scene. The narrow cover moves the name and title below the illustration. All visible artwork ships with the repository.

| File | Purpose |
|---|---|
| `README.md` | Profile copy, citations, responsive cover and a generated activity summary between two HTML comments |
| `art/citadel.png`, `art/cover.svg` | Source illustration and editable cover typography, frame and layouts |
| `assets/codex/cover.png`, `assets/codex/cover-small.png` | Desktop and phone cover exports |
| `assets/codex/seal.svg`, `folio.svg`, `coffer.svg`, `compass.svg`, `anvil.svg`, `chalice.svg`, `standard.svg`, `lectern.svg`, `gate.svg` | Original seal, inventory objects, advancement emblems and closing portal, all in the same directory |
| `art/atlas.svg`, `data/contributions.csv`, `scripts/atlas.py`, `assets/codex/kingdom.svg` | Terrain artwork, dated input, generator and rendered map |
| `scripts/export_cover.py` | Optional cover export with Pillow, Playwright and Chromium. The profile and atlas have no package-install step. |
| `.github/workflows/atlas.yml` | Read-only reproducibility check and weekly review artifact |
| `docs/verification.md` | Sources for the public profile and outstanding claims |

The historical evidence graphic in `assets/proof.svg` remains linked from the expandable measurement record.

## Preview

Open the repository folder and use **Markdown: Open Preview to the Side** on `README.md` in VS Code. Narrow the preview to phone width. Follow the four section links, expand the additional projects, and inspect the atlas beside its CSV on GitHub or in a spreadsheet viewer.

The local QA preview used cmark-gfm, Chromium and GitHub's public stylesheets. GitHub applies additional sanitization and image handling on its servers. After pushing an approved review branch, use the branch README preview for a final hosted check.

## Rebuild the map

Check the tracked snapshot from the repository root with Python 3.10 or newer.

```sh
python scripts/atlas.py --check
```

Use `python scripts/atlas.py` to rebuild the SVG and its README summary offline. These commands fetch and verify a fresh public snapshot.

```sh
python scripts/atlas.py --refresh
python scripts/atlas.py --check
```

The fetch reads GitHub's signed-out calendar and pairs each dated cell with its accessible count. It takes the 13 complete Sunday–Saturday weeks preceding the current UTC week. Missing days or unrecognized counts stop the refresh. A value of zero represents a day GitHub explicitly labels as having no contributions. The CSV records GitHub's reported contributions, which can include several kinds of activity.

The workflow runs an offline comparison on relevant pushes and pull requests. On Sundays at 06:37 UTC, or on manual dispatch, it also fetches the calendar and produces a downloadable `contribution-atlas` artifact. To adopt an artifact, copy its CSV to `data/contributions.csv`, then rebuild and review locally. The published profile keeps the approved, dated snapshot until its replacement is merged.

## Rebuild the covers

The checked-in PNGs are ready to display. Edit `art/cover.svg` to change the lettering or frame. It references the seal and source illustration. These export commands use a Python environment with Pillow and Playwright installed.

```sh
python -m playwright install chromium
python scripts/export_cover.py
```

The exports are 1200 × 400 and 600 × 298. The design uses Georgia with serif fallbacks. A different installed font can change the lettering slightly.

<details>
<summary>Original prompt for the built-in image generator</summary>

> Create an ORIGINAL ultra-wide cinematic pixel-art illuminated manuscript illustration, 3:1 landscape composition for the header of a professional engineer's portfolio called The Sovereign Codex. Full bleed artwork, NO lettering, no typography or emblems from any franchise. Museum-quality late medieval engraving drawn as deliberately hand-clustered pixel art, restrained square pixel stair-steps and palette dithering, like a beautifully art-directed vintage strategy game's title plate. Deep obsidian near-black #101510, shadowy forest and malachite #174B32, illuminated emerald #50C878, weathered vellum gold #B9A16B, iron #BFC5C3. A gothic stone archive citadel rises at far right on a high terraced cliff, arch bridge, distant ridges, a quiet moon. In foreground towards middle-right, an original armored scholar seen from behind in a handsome long dark green hooded mantle, holding an open golden-page codex at a stone parapet, no visible face, no skull/mask, absolutely no resemblance to a comic character. A few pinpoint gilt motes lift from the book. Stone diamond-inlay and tracery, woodcut hatching, trees and meticulously placed warm lamps, layered depth. Leave the LEFT 48% dark with broad deep green contemplative sky, subdued ridges and very faint masonry receding into near-black, used later as a text-safe area. Keep hero subject cluster in right 50%. Bold silhouette, mature art direction, flattened limited palette, not an airbrushed fantasy painting. No modern technology, no sci-fi, no neon, no logos, no fake writing, no colored frame, no UI. Frame for a wide horizontal crop.

</details>

## Publish after approval

1. Review the README and the source checklist. Run the offline atlas check, `git status --short --branch` and `git diff --check`.
2. Stage the reviewed README, art, assets, data, scripts, workflow and documentation. Inspect the staged diff and commit on the review branch.
3. Push that branch to `CodesbyRohit/CodesbyRohit` and open a pull request into `main`. Check the rendered branch README, the CI result and the phone cover before merging.
4. Once the approved change reaches the default branch, check the public profile at [github.com/CodesbyRohit](https://github.com/CodesbyRohit).
