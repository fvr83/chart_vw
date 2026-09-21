from pathlib import Path
import ast
from PIL import Image, ImageDraw, ImageFont
import subprocess
import os



# ==================================================
# ------- VARIABLES -------
# ==================================================
ranks = 'AKQJT98765432'

combos_set = {f'{r_1}{r_2}' if r_1 == r_2 else f'{r_1}{r_2}s' if ranks.index(r_1) < ranks.index(r_2) else f'{r_2}{r_1}o' for r_1 in ranks for r_2 in ranks}
combos_matrix = [[f"{r1}{r2}" if r1 == r2 else (f"{r1}{r2}s" if i < j else f"{r2}{r1}o")for j, r2 in enumerate(ranks)]for i, r1 in enumerate(ranks)]

name_replace_dict = {'UTG': 'EP', 'UTG1': 'MP', 'LJ': 'LJ', 'HJ': 'HJ', 'CO': 'CO', 'BTN': 'BU', 'SB': 'SB'}
positions = list(name_replace_dict.keys())
colors_dict = {'UTG': '#ff0000', 'UTG1': '#ff8000', 'LJ': '#8000ff', 'HJ': '#ff00ff', 'CO': '#00CC66', 'BTN': '#99e600', 'SB': '#0080ff'}

matrix_font = ImageFont.truetype('ROBOTOCONDENSED-BLACK.ttf', 14)
title_font = ImageFont.truetype('ROBOTOCONDENSED-SEMIBOLD.ttf', 11)
legend_font = ImageFont.truetype('ROBOTOCONDENSED-SEMIBOLD.ttf', 11)

cell_size = 25
matrix_size = 13
title_box_height = 11
image_width = cell_size * matrix_size + 1
image_height = cell_size * matrix_size + title_box_height + 1



# ==================================================
# ------- FUNCTIONS -------
# ==================================================
def get_data(block: str):
    data = {}
    for line in block.splitlines():
        if ' = ' not in line:

            continue
        var_name, value = line.split(' = ', 1)
        data[var_name] = ast.literal_eval(value)
    mode_depth = data.get('mode_depth')
    positions_actions = data.get('positions_actions')
    pot_odds_and_stacks = data.get('pot_odds_and_stacks')
    actions_frequencies = data.get('actions_frequencies')
    combos_dict = data.get('combos_dict')
    prefolded_combos = data.get('prefolded_combos')

    return mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict, prefolded_combos


def get_text_boundaries(text: str, font: tuple) -> tuple[int]:
    text_len = len(text)
    img_size = text_len * 11
    img = Image.new("RGB", (img_size, int(img_size / 3)), "#ffffff")
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    return width, height


def draw_image(dictionary, title_string):
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((1, -1), title_string, fill='black', font=title_font)
    ts_width, ts_height = get_text_boundaries(title_string, title_font)
    sq_size = title_box_height - 5
    print(f'{sq_size = }')
    text_spacing = 10
    text_width = get_text_boundaries('UTG', legend_font)[0]
    for i, (p, c) in enumerate(colors_dict.items()):
        if len(title_string) > 27:
            r_x_0 = ts_width + 2 + (i * (sq_size + 16)) 
            gap = 1
        else:
            r_x_0 = ts_width + text_spacing + (i * (sq_size + text_width))
            gap = 2
        r_y_0 = 2
        r_x_1 = r_x_0 + sq_size
        r_y_1 = r_y_0 + sq_size
        t_x_0 = r_x_1 
        t_y_0 = r_y_0
        idx_width, _ = get_text_boundaries(name_replace_dict[p], legend_font)
        draw.rectangle([r_x_0, r_y_0, r_x_1, r_y_1], fill=c, outline='black')
        draw.text((t_x_0 + gap, t_y_0 - 3), name_replace_dict[p], fill='black', font=legend_font)
    draw.rectangle([0, 0, image_width - 1, title_box_height], fill=None, outline='#000000')

    for row in range(matrix_size):
        for col in range(matrix_size):
            x0 = col * cell_size
            y0 = row * cell_size + title_box_height
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            combo = combos_matrix[row][col]
            def get_color():
                for k, v in dictionary.items():
                    if combo in v:
                        bck_color = colors_dict[k]
                        return bck_color
            bck_color = get_color()
            combo_width, combo_height = get_text_boundaries(combo, matrix_font)
            text_x = x0 + (cell_size - combo_width) // 2
            text_y = y0 + (cell_size - combo_height) // 2
            draw.rectangle([x0, y0, x1, y1], fill=bck_color, outline='#000000')
            draw.text((text_x + 1, text_y - 2), combo, fill='black', font=matrix_font)

    return image



# ==================================================
# ------- MAIN LOOP -------
# ==================================================
origin_folder = Path('G0_T0_text_results')
destination_folder = Path('img_results_test')

depths = [
    '200bb', '160bb', '130bb', '100bb', '80bb', '70bb', '60bb', '55bb', '50bb', '45bb', '40bb', '38bb', '35bb', '32bb', '30bb', '28bb', '26bb', '25bb', '22bb', '20bb', '19bb', '17bb', '16bb', 
    '15bb', '14bb', '13bb', '12bb', '11bb', '10bb', '9bb', '8bb', '7bb', '6bb', '5bb', '4bb', '3bb', '2bb', '1bb'
]

chosen_depths = [
    '200bb', '160bb', '130bb', '100bb', '80bb', '70bb', '60bb', '55bb', '50bb', '45bb', '40bb', '38bb', '35bb', '32bb', '30bb', '28bb', '26bb', '25bb', '22bb', '20bb', '19bb', '17bb', '16bb', 
    '15bb', '14bb', '13bb', '12bb', '11bb', '10bb', '9bb', '8bb', '7bb', '6bb', '5bb', '4bb', '3bb', '2bb'
]

agg_condensed_ev = {}
agg_condensed_freq = {}

agg_any_ev = {}
agg_any_freq = {}

depth_ev = {}
depth_freq = {}

for path_idx, path in enumerate(Path(origin_folder).iterdir()):
    if not path.is_file():
        continue

    file_stem = path.stem
    gap, tier, depth_str, game_mode_str, chip_mode_str = file_stem.split('_')

    if depth_str not in chosen_depths:
        continue

    content = path.read_text(encoding='utf-8')
    blocks = content.split('**************************************************')

    depth_ev.setdefault(depth_str, {})
    depth_freq.setdefault(depth_str, {})

    for block_idx, block in enumerate(blocks):
        if not block.strip():
            continue

        mode_depth, positions_actions, pot_odds_and_stacks, actions_frequencies, combos_dict, prefolded_combos = get_data(block)

        spot_sequency = {}

        for idx, positon_action_tuple in enumerate(positions_actions):
            position, immediate_stack, chosen_action, avaliable_actions = positon_action_tuple

            if chosen_action not in ["N/A", "Fold"]:
                spot_sequency[idx + 1] = {position: chosen_action}

        if len(spot_sequency) != 1:
            continue

        hero_position = next(
            position
            for sequence in spot_sequency.values()
            for position, action in sequence.items()
            if action == 'spot'
        )

        depth_ev[depth_str].setdefault(hero_position, set())
        depth_freq[depth_str].setdefault(hero_position, set())

        for combo, data in combos_dict.items():
            if not data:
                continue

            actions_dict = data[1]

            has_agg_ev = any(
                v[1] > 0
                for k, v in actions_dict.items()
                if k.startswith('R') or k.startswith('A')
            )

            has_agg_freq = any(
                v[0] > 0
                for k, v in actions_dict.items()
                if k.startswith('R') or k.startswith('A')
            )

            if has_agg_ev:
                depth_ev[depth_str][hero_position].add(combo)

            if has_agg_freq:
                depth_freq[depth_str][hero_position].add(combo)

for depth_str in chosen_depths:

    for hero_position in depth_ev.get(depth_str, {}):

        ev_set = depth_ev[depth_str][hero_position]
        freq_set = depth_freq[depth_str][hero_position]

        agg_any_ev.setdefault(hero_position, set())
        agg_any_freq.setdefault(hero_position, set())

        agg_any_ev[hero_position] |= ev_set
        agg_any_freq[hero_position] |= freq_set

        if hero_position not in agg_condensed_ev:
            agg_condensed_ev[hero_position] = ev_set.copy()
            agg_condensed_freq[hero_position] = freq_set.copy()
        else:
            agg_condensed_ev[hero_position] &= ev_set
            agg_condensed_freq[hero_position] &= freq_set
            
# print(f'{agg_condensed_ev = }')
# print(f'{agg_any_ev = }')
# print(f'{agg_condensed_freq = }')
# print(f'{agg_any_freq = }')

for dictionary, title_string in [
    (agg_condensed_ev, 'ALL DEPTHS CONDENSED EV'),
    (agg_any_ev, 'ALL DEPTHS EXTENDED EV'),
    (agg_condensed_freq, 'ALL DEPTHS CONDENSED FREQUENCY'),
    (agg_any_freq, 'ALL DEPTHS EXTENDED FREQUENCY'),
]:
    chart = draw_image(dictionary, title_string)
    chart.show()
