from PIL import Image
from pathlib import Path

img_offset = {0: (0, 0), 1: (342, 0), 2: (686, 0), 3: (1030, 0), 4: (0, 339), 5: (342, 339), 6: (686, 339), 7: (1030, 339)}

image_depth = Image.new("RGB", (1356, 676), "#FFFFFF")

destination_folder = Path('condensed_images_wide_mounted')

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

string_set = set()

for i, path in enumerate(files):
    if not path:

        continue

    depth_string = "_".join(path.name.split("_")[:2])
    string_set.add(depth_string)
    
    x, y = img_offset[i]

    img = Image.open(path).convert("RGB")
    image_depth.paste(img, (x, y))

file_name = '_'.join(sorted(string_set)) + '.png'

destination_folder.mkdir(parents=True, exist_ok=True)
final_path = Path(destination_folder, file_name)

image_depth.show()
image_depth.save(final_path)
