ranks = 'AKQJT98765432'

combos_matrix = [[f"{r_1}{r_2}" if i == j else f"{r_1}{r_2}s" if i < j else f"{r_2}{r_1}o" for j, r_2 in enumerate(ranks)] for i, r_1 in enumerate(ranks)]

for i in combos_matrix:
    print(i)

combos_list = [f"{r_1}{r_2}" if i == j else f"{r_1}{r_2}s" if i < j else f"{r_2}{r_1}o" for i, r_1 in enumerate(ranks) for j, r_2 in enumerate(ranks)]

print(combos_list)