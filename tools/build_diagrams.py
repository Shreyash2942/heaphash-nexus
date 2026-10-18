"""Rebuild editable SVG and print-resolution PNG project diagrams."""

from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "diagrams"
NAVY = "#142D4E"
INK = "#18324F"
BLUE = "#E7F0FC"
TEAL = "#DEF4EE"
GOLD = "#FFF0CB"


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


class Diagram:
    def __init__(self, title, subtitle, height=1480):
        self.height = height
        self.image = Image.new("RGB", (1920, height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="{height}" viewBox="0 0 1920 {height}">', '<rect width="100%" height="100%" fill="white"/>']
        self.rect((0, 0, 1920, 125), NAVY, NAVY)
        self.text(65, 38, title, 49, "white", True, anchor="left")
        self.text(65, 154, subtitle, 30, INK, anchor="left")

    def rect(self, bounds, fill, outline=INK):
        self.draw.rounded_rectangle(bounds, radius=18, fill=fill, outline=outline, width=3)
        x1, y1, x2, y2 = bounds
        self.svg.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="18" fill="{fill}" stroke="{outline}" stroke-width="3"/>')

    def text(self, x, y, text, size=34, color=INK, bold=False, anchor="center"):
        chosen = font(size, bold)
        text_anchor = "la" if anchor == "left" else "ma"
        self.draw.text((x, y), text, font=chosen, fill=color, anchor=text_anchor)
        align = "start" if anchor == "left" else "middle"
        self.svg.append(f'<text x="{x}" y="{y+size*0.9}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{align}" fill="{color}">{escape(text)}</text>')

    def box(self, x, y, width, height, lines, fill=BLUE):
        self.rect((x, y, x+width, y+height), fill)
        top = y + (height - len(lines)*46) / 2
        for index, line in enumerate(lines):
            self.text(x+width/2, top+index*46, line, 35, bold=index == 0)

    def arrow(self, points):
        self.draw.line(points, fill=INK, width=5, joint="curve")
        encoded = " ".join(f"{x},{y}" for x, y in points)
        self.svg.append(f'<polyline points="{encoded}" fill="none" stroke="{INK}" stroke-width="5"/>')
        x, y = points[-1]
        px, py = points[-2]
        if y > py:
            head = [(x, y), (x-12, y-20), (x+12, y-20)]
        elif y < py:
            head = [(x, y), (x-12, y+20), (x+12, y+20)]
        elif x > px:
            head = [(x, y), (x-20, y-12), (x-20, y+12)]
        else:
            head = [(x, y), (x+20, y-12), (x+20, y+12)]
        self.draw.polygon(head, fill=INK)
        self.svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in head)}" fill="{INK}"/>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        self.image.save(OUT / f"{name}.png", dpi=(300, 300))
        (OUT / f"{name}.svg").write_text("\n".join(self.svg + ["</svg>"]), encoding="utf-8")
        print(f"Wrote {name}.png and {name}.svg")


def main():
    architecture = Diagram("Project architecture", "Runtime layers and workflows; each structure owns its own containers.")
    architecture.box(710, 220, 500, 105, ["main.py"], TEAL)
    architecture.box(510, 405, 900, 150, ["CLI navigation and presentation", "menu.py / input_handler.py / submenu modules"], TEAL)
    architecture.box(510, 635, 900, 150, ["Application state", "original records + independent table and queue"], BLUE)
    architecture.box(60, 905, 540, 215, ["Dataset package", "generation / CSV loading", "field and ID validation"], BLUE)
    architecture.box(690, 905, 540, 215, ["Data structures", "HashTable + list chains", "PriorityQueue + max-heap"], TEAL)
    architecture.box(1320, 905, 540, 215, ["Performance package", "HashTable + manual scan", "verified timing + reports"], GOLD)
    architecture.arrow([(960, 325), (960, 405)])
    architecture.arrow([(960, 555), (960, 635)])
    for target in (330, 960, 1590):
        architecture.arrow([(960, 785), (960, 835), (target, 835), (target, 905)])
    architecture.box(60, 1220, 1800, 145, ["Shared foundations", "settings.py: paths/constants     |     DataItem: immutable student record"], GOLD)
    architecture.text(960, 1410, "Unit and integration tests verify modules, workflows, and state independence.", 31)
    architecture.save("project_architecture")

    flow = Diagram("Data flow", "Source records remain unchanged during interactive edits, benchmarks, and demonstrations.")
    flow.box(660, 215, 600, 115, ["data/students.csv (150 records)"], GOLD)
    flow.box(610, 405, 700, 145, ["CSV loader + validator", "typed DataItem records / unique IDs"], BLUE)
    flow.box(610, 625, 700, 125, ["Original loaded-record snapshot"], BLUE)
    flow.arrow([(960, 330), (960, 405)])
    flow.arrow([(960, 550), (960, 625)])
    for target in (330, 960, 1590):
        flow.arrow([(960, 750), (960, 800), (target, 800), (target, 875)])
    flow.box(60, 875, 540, 205, ["Editable HashTable", "insert / search / delete", "separate bucket chains"], TEAL)
    flow.box(690, 875, 540, 205, ["Verified benchmark", "fresh table + linear search", "same records and targets"], GOLD)
    flow.box(1320, 875, 540, 205, ["Editable PriorityQueue", "insert / search / delete", "peek / extract / validate"], TEAL)
    flow.box(60, 1170, 540, 145, ["CLI results and inspection", "records / buckets / statistics"], BLUE)
    flow.box(690, 1170, 540, 145, ["Saved performance report", "results/performance_results.txt"], GOLD)
    flow.box(1320, 1170, 540, 145, ["CLI results and inspection", "records / heap array / root"], BLUE)
    for target in (330, 960, 1590):
        flow.arrow([(target, 1080), (target, 1170)])
    flow.text(960, 1370, "Reset re-reads the CSV, validates it, then replaces both interactive containers.", 31)
    flow.text(960, 1420, "The complete demonstration uses separate containers and preserves interactive edits.", 31)
    flow.save("data_flow")


if __name__ == "__main__":
    main()
