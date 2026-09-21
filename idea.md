origin_folder = Path('G0_T0_text_results')
desination_folder = create if not exists

for path in Path(origin_folder).iterdir():
    if not path.is_file(): continue
    gap, tier, depth_str, game_mode_str, chip_mode_str = file_stem.split('_')
    content = path.read_text(encoding='utf-8')
    blocks = content.split('**************************************************')

gap = 0
gaps = [0]

tier = 0
tiers = [0]

game_modes = ['MTT']
chip_modes = ['ChipEV']

<get_data(block)> get_data(arg) already exists
mode_depth = (game_mode: str, chip_mode: str, depth: int)

positions_actions = ((position: str, fic_stack: float, chosen_action: str, (*avaliable_actions: str)), ...)

pot_odds_and_stacks = ({'initial_pot': float(), 'current_pot': float(), 'pot_odds': float()}, {position: current_stack, ...})

actions_frequencies = ((action: str, frequency: float, combos_played: float, rgb: str), ...)

combos_dict = {'combo': (ev_max, combo_acions_dict) | 'combo': 0, ...}

prefolded_combos: list[str]
</get_data(block)>

combo_acions_dict = {'action_n': [freq_n, ev_n], ...}

COMBO STATS

max_ev_actions: list[str]
positive_ev_actions: list[str]

has_raise_freq: bool
has_raise_ev: bool
raises_only: bool
has_multi_raises: bool
raise_actions_sorted_by_frequency: list[str]
raise_actions_sorted_by_ev: list[str]
raise_actions_sorted_by_size: list[str]

has_shove_freq: bool
has_shove_ev: bool
shoves_only: bool

has_call_freq: bool
has_call_ev: bool
calls_only: bool

has_fold_freq: bool
folds_only: bool

A ideia é ler várias profundidades de uma mesma situação e encontrar a média entre as ações de combo_acions_dict = {'action_n': [freq_n, ev_n], ...} e retorar um results_dict = {'combo': condensed_combo_acions_dict}