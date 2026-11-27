"""Refresh from the signed-out GitHub calendar, or rebuild offline from its CSV."""

import argparse
import csv
import io
import re
import sys
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from string import Template
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://github.com/users/CodesbyRohit/contributions"
CSV = ROOT / "data" / "contributions.csv"
MAP = ROOT / "assets" / "codex" / "kingdom.svg"
README = ROOT / "README.md"
START = "<!-- atlas:begin -->"
END = "<!-- atlas:end -->"
WEEKS = 13
DAYS = WEEKS * 7
TERRAIN = (
    (0, "moor", "0"), (1, "grove", "1–3"), (4, "village", "4–9"),
    (10, "tower", "10–19"), (20, "keep", "20+"),
)


class Calendar(HTMLParser):
    """GitHub relates each dated cell to its accessible count by element ID."""

    def __init__(self):
        super().__init__()
        self.dates = {}
        self.labels = {}
        self.tooltip = None

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if tag == "td" and "data-date" in fields:
            key = fields["id"]
            if key in self.dates:
                raise ValueError(f"Duplicate calendar cell {key}")
            self.dates[key] = date.fromisoformat(fields["data-date"])
        if tag == "tool-tip" and "for" in fields:
            self.tooltip = fields["for"]
            if self.tooltip in self.labels:
                raise ValueError(f"Duplicate calendar label {self.tooltip}")
            self.labels[self.tooltip] = ""

    def handle_data(self, data):
        if self.tooltip is not None:
            self.labels[self.tooltip] += data

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.tooltip = None

    def completed_weeks(self, today):
        # Even on a Saturday, exclude the week containing the capture day.
        last_saturday = today - timedelta(days=(today.weekday() + 1) % 7 + 1)
        first = last_saturday - timedelta(days=DAYS - 1)
        rows = []
        for key, day in self.dates.items():
            if first <= day <= last_saturday:
                label = self.labels.get(key, "").strip()
                match = re.fullmatch(r"(No|[0-9]+(?:,[0-9]{3})*) contributions? on .+\.", label)
                if not match:
                    raise ValueError(f"Missing or unknown count on {day}: {label!r}")
                amount = match[1]
                rows.append((day, 0 if amount == "No" else int(amount.replace(",", ""))))
        return validate(sorted(rows))


def validate(rows):
    if len(rows) != DAYS or rows[0][0].weekday() != 6:
        raise ValueError(f"Expected {WEEKS} complete Sunday–Saturday weeks")
    for offset, (day, count) in enumerate(rows):
        if day != rows[0][0] + timedelta(days=offset) or count < 0:
            raise ValueError(f"Invalid, missing or duplicate date/count near {day}")
    return rows


def download():
    req = Request(SOURCE, headers={"User-Agent": "Sovereign-Codex-atlas", "Accept-Language": "en"})
    with urlopen(req, timeout=25) as response:
        parser = Calendar()
        parser.feed(response.read().decode("utf-8"))
        parser.close()
    return parser.completed_weeks(datetime.now(timezone.utc).date())


def read_snapshot():
    with CSV.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ["date", "contributions"]:
            raise ValueError("Unexpected CSV header")
        return validate([(date.fromisoformat(r["date"]), int(r["contributions"])) for r in reader])


def render(rows):
    tiles = []
    for i, (day, count) in enumerate(rows):
        week, weekday = divmod(i, 7)
        kind = next(name for low, name, _ in reversed(TERRAIN) if count >= low)
        x, y = 293 + 34 * (week - weekday), 104 + 14 * (week + weekday)
        tile = (f'<g transform="translate({x} {y})"><title>{day} · {count}</title>'
                f'<use href="#{kind}"/></g>')
        tiles.append((week + weekday, week, tile))
    legend = []
    for i, (_, name, band) in enumerate(TERRAIN):
        y = 175 + 47 * i
        legend.append(f'<use href="#{name}" transform="translate(803 {y}) scale(.55)"/>'
                      f'<text x="833" y="{y-3}" fill="#e6dab9" font-size="17">{name.title()}</text>'
                      f'<text x="834" y="{y+14}" font-size="13">{band}</text>')
    first, last = rows[0][0], rows[-1][0]
    period = f"{first:%d %b %Y} – {last:%d %b %Y}"
    total = sum(n for _, n in rows)
    active = sum(n > 0 for _, n in rows)
    template = Template((ROOT / "art" / "atlas.svg").read_text(encoding="utf-8"))
    image = template.substitute(period=period, total=total, active=active,
                                terrain="\n  ".join(t for _, _, t in sorted(tiles)),
                                legend="\n    ".join(legend))
    summary = f"**{period}** · {total} contributions across {active} active days."
    return image, summary


def replace_text(path, content):
    # Close before replacing on Windows. A failed write leaves the old file intact.
    temporary = NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                  dir=path.parent, delete=False)
    staging = Path(temporary.name)
    try:
        with temporary:
            temporary.write(content)
        staging.replace(path)
    finally:
        staging.unlink(missing_ok=True)


def main():
    args = argparse.ArgumentParser(description=__doc__)
    mode = args.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true", help="fetch the last 13 completed public weeks")
    mode.add_argument("--check", action="store_true", help="check tracked output offline without writing")
    options = args.parse_args()
    rows = download() if options.refresh else read_snapshot()
    svg, summary = render(rows)
    readme = README.read_text(encoding="utf-8")
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) > readme.index(END):
        raise ValueError("README needs exactly one ordered atlas marker pair")
    before, block = readme.split(START)
    _, after = block.split(END)
    outputs = {MAP: svg, README: f"{before}{START}\n{summary}\n{END}{after}"}
    if options.refresh:
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(("date", "contributions"))
        writer.writerows(rows)
        # Install the source first. An interrupted refresh can be rebuilt offline.
        outputs = {CSV: buffer.getvalue(), **outputs}
    for path, content in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8") == content:
            continue
        if options.check:
            raise ValueError(f"{path.name} differs from the snapshot. Run python scripts/atlas.py")
        replace_text(path, content)
    print(f"Atlas matches {len(rows)} days from {rows[0][0]} through {rows[-1][0]}.")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, OSError) as error:
        sys.exit(f"Atlas error: {error}")
