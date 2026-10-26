from PIL import Image
from pathlib import Path

img_offset = {0: (0, 0), 1: (342, 0), 2: (686, 0), 3: (1030, 0), 4: (0, 339), 5: (342, 339), 6: (686, 339), 7: (1030, 339)}

image_depth = Image.new("RGB", (1356, 676), "#FFFFFF")

files = [
    Path('condensed_images_wide', '100bb_10bb_condensed_ev.png'),
    Path('condensed_images_wide', '100bb_10bb_condensed_frequency.png'),
    None, #Path('condensed_images_wide', '9bb_2bb_condensed_ev.png'),
    None, #Path('condensed_images_wide', '9bb_2bb_condensed_frequency.png'),
    Path('condensed_images_wide', '100bb_10bb_extended_ev.png'),
    Path('condensed_images_wide', '100bb_10bb_extended_frequency.png'),
    None, #Path('condensed_images_wide', '9bb_2bb_extended_ev.png'),
    None, #Path('condensed_images_wide', '9bb_2bb_extended_frequency.png')
]

for i, path in enumerate(files):
    if not path:

        continue

    x, y = img_offset[i]

    img = Image.open(path).convert("RGB")
    image_depth.paste(img, (x, y))

image_depth.show()
