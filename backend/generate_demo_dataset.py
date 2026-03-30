"""
Generate demo saree-like images for testing.
Creates ~30 images with varying colors, patterns, and textures.
"""

import os
import random
import math
from PIL import Image, ImageDraw, ImageFilter

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
NUM_IMAGES = 30

# Saree-inspired color palettes
PALETTES = [
    # Reds & Golds
    [(180, 30, 30), (220, 50, 20), (200, 160, 50), (255, 200, 80)],
    # Royal Blue
    [(20, 40, 140), (30, 60, 180), (80, 120, 220), (200, 180, 100)],
    # Green & Gold
    [(20, 100, 40), (40, 140, 60), (180, 160, 50), (220, 200, 80)],
    # Purple & Magenta
    [(100, 20, 120), (150, 40, 160), (200, 60, 180), (220, 180, 100)],
    # Orange & Maroon
    [(180, 60, 20), (220, 100, 30), (140, 20, 30), (240, 180, 60)],
    # Pink & Rose
    [(220, 80, 120), (240, 120, 150), (200, 50, 90), (255, 200, 180)],
    # Teal & Turquoise
    [(20, 140, 140), (40, 180, 170), (60, 200, 190), (200, 220, 100)],
    # Maroon & Cream
    [(120, 20, 40), (160, 40, 50), (240, 220, 180), (200, 180, 140)],
    # Yellow & Orange
    [(240, 200, 40), (240, 180, 20), (220, 120, 30), (180, 80, 20)],
    # Navy & Silver
    [(20, 20, 80), (40, 40, 120), (180, 180, 200), (220, 220, 230)],
]

PATTERN_TYPES = ["stripes", "zigzag", "dots", "paisley", "checks", "waves", "border", "diagonal", "floral_dots", "mesh"]


def draw_stripes(draw, w, h, colors):
    stripe_w = random.randint(8, 30)
    for x in range(0, w, stripe_w):
        c = random.choice(colors)
        draw.rectangle([x, 0, x + stripe_w - 2, h], fill=c)


def draw_zigzag(draw, w, h, colors):
    amp = random.randint(10, 30)
    freq = random.randint(3, 8)
    for y in range(0, h, random.randint(15, 30)):
        points = []
        for x in range(0, w, 5):
            offset = amp * math.sin(x * freq * math.pi / w)
            points.append((x, y + offset))
        if len(points) > 1:
            draw.line(points, fill=random.choice(colors), width=random.randint(2, 5))


def draw_dots(draw, w, h, colors):
    spacing = random.randint(15, 35)
    r = random.randint(3, 8)
    for x in range(spacing, w, spacing):
        for y in range(spacing, h, spacing):
            ox = random.randint(-3, 3)
            oy = random.randint(-3, 3)
            draw.ellipse([x - r + ox, y - r + oy, x + r + ox, y + r + oy], fill=random.choice(colors))


def draw_checks(draw, w, h, colors):
    size = random.randint(15, 40)
    for x in range(0, w, size):
        for y in range(0, h, size):
            if (x // size + y // size) % 2 == 0:
                draw.rectangle([x, y, x + size, y + size], fill=random.choice(colors[:2]))


def draw_waves(draw, w, h, colors):
    for y_base in range(0, h, random.randint(20, 40)):
        points = []
        amp = random.randint(5, 20)
        for x in range(0, w, 3):
            y = y_base + amp * math.sin(x * 4 * math.pi / w)
            points.append((x, y))
        if len(points) > 1:
            draw.line(points, fill=random.choice(colors), width=random.randint(2, 4))


def draw_border(draw, w, h, colors):
    border = random.randint(20, 50)
    draw.rectangle([0, 0, w, border], fill=colors[0])
    draw.rectangle([0, h - border, w, h], fill=colors[0])
    draw.rectangle([0, 0, border, h], fill=colors[1])
    draw.rectangle([w - border, 0, w, h], fill=colors[1])
    # Inner decorations
    for x in range(border + 10, w - border, 20):
        draw.ellipse([x - 3, border - 10, x + 3, border - 4], fill=colors[2])
        draw.ellipse([x - 3, h - border + 4, x + 3, h - border + 10], fill=colors[2])


def draw_diagonal(draw, w, h, colors):
    spacing = random.randint(15, 35)
    for offset in range(-h, w + h, spacing):
        draw.line([(offset, 0), (offset + h, h)], fill=random.choice(colors), width=random.randint(2, 5))


def draw_floral_dots(draw, w, h, colors):
    spacing = random.randint(30, 60)
    for cx in range(spacing, w, spacing):
        for cy in range(spacing, h, spacing):
            r = random.randint(6, 12)
            petals = random.randint(4, 6)
            for i in range(petals):
                angle = 2 * math.pi * i / petals
                px = cx + int(r * math.cos(angle))
                py = cy + int(r * math.sin(angle))
                pr = random.randint(3, 5)
                draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=random.choice(colors))
            draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=colors[0])


def draw_mesh(draw, w, h, colors):
    spacing = random.randint(15, 30)
    lw = random.randint(1, 3)
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=random.choice(colors), width=lw)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=random.choice(colors), width=lw)


PATTERN_FUNCS = {
    "stripes": draw_stripes,
    "zigzag": draw_zigzag,
    "dots": draw_dots,
    "checks": draw_checks,
    "waves": draw_waves,
    "border": draw_border,
    "diagonal": draw_diagonal,
    "floral_dots": draw_floral_dots,
    "mesh": draw_mesh,
    "paisley": draw_dots,  # fallback
}


def generate_saree_image(idx):
    w, h = 400, 600
    palette = random.choice(PALETTES)
    bg = palette[0]
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # Fill background with gradient
    for y in range(h):
        ratio = y / h
        r = int(bg[0] * (1 - ratio * 0.3))
        g = int(bg[1] * (1 - ratio * 0.3))
        b = int(bg[2] * (1 - ratio * 0.3))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Draw 1-2 patterns
    n_patterns = random.randint(1, 2)
    chosen = random.sample(PATTERN_TYPES, n_patterns)
    for pat in chosen:
        fn = PATTERN_FUNCS.get(pat, draw_dots)
        fn(draw, w, h, palette[1:])

    # Add slight blur for textile feel
    img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.2)))

    return img


def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    print(f"Generating {NUM_IMAGES} demo saree images in {DATASET_DIR}...")

    saree_names = [
        "banarasi", "kanjeevaram", "chanderi", "patola", "bandhani",
        "tussar", "chiffon", "georgette", "organza", "cotton",
        "silk", "mysore", "paithani", "sambalpuri", "pochampally",
        "ikat", "kalamkari", "tant", "muga", "gadwal",
        "nauvari", "bomkai", "baluchari", "jamdani", "uppada",
        "maheshwari", "kota", "bhagalpuri", "murshidabad", "venkatagiri",
    ]

    for i in range(NUM_IMAGES):
        img = generate_saree_image(i)
        name = saree_names[i % len(saree_names)]
        filename = f"saree_{name}_{i + 1:03d}.jpg"
        filepath = os.path.join(DATASET_DIR, filename)
        img.save(filepath, "JPEG", quality=90)
        print(f"  Created: {filename}")

    print(f"\nDone! {NUM_IMAGES} images saved to {DATASET_DIR}")


if __name__ == "__main__":
    main()
