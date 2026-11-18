# dayeon603-pixel.github.io

Personal research portfolio for Dayeon Kang. Live at <https://dayeon603-pixel.github.io>

`index.html` is generated. Edit `src/` and run `python3 src/build.py`.

- `src/app_shell.html`: layout, design tokens and the small scroll script
- `src/cv.py`: about, papers, leadership, honours
- `src/meta.py`: per-project metadata, stats and figures
- `src/panels.html`: project write-ups, one `<dt>/<dd>` pair per row
- `IMAGE_SOURCES.md`: where each image came from

## Design

The page follows the 2026 인재상 presentation deck: warm paper ground (`--wash`),
lavender accents, a ghost watermark behind each heading, numbered white rows and a
check strip of verified numbers under every project. Type is IBM Plex Sans with
IBM Plex Sans KR for Korean. All colour decisions live in `:root` in `app_shell.html`.

Old notebook-era links (`#p/metamirage`, `#s/research`) redirect to the new anchors.
