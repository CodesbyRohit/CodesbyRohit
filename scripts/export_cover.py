"""Export the editable jacket at the two sizes used by GitHub's picture element."""

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "art"
ASSETS = ROOT / "assets" / "codex"


def export():
    source = (ART / "cover.svg").read_text(encoding="utf-8")
    for reference, kind in (("citadel.png", "png"), ("../assets/codex/seal.svg", "svg+xml")):
        encoded = base64.b64encode((ART / reference).read_bytes()).decode("ascii")
        source = source.replace(f'href="{reference}"', f'href="data:image/{kind};base64,{encoded}"')

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for name, width, height in (("cover", 1200, 400), ("cover-small", 600, 298)):
            page = browser.new_page(viewport={"width": width, "height": height})
            page.set_content("<style>html,body{margin:0;width:100%;height:100%}svg{display:block}</style>" + source)
            page.evaluate("document.fonts.ready")
            raster = Image.open(BytesIO(page.screenshot())).convert("RGB")
            output = ASSETS / f"{name}.png"
            raster.quantize(colors=128).save(output, optimize=True)
            print(f"{output.name} — {width} x {height}, {output.stat().st_size:,} bytes")
            page.close()
        browser.close()


if __name__ == "__main__":
    export()
