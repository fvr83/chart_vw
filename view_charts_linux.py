import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk



def show_group(group_index):
    global current_group
    current_depth = depth_var.get()
    current_group = group_index
    nearest_depth = min(groups[current_group], key=lambda d: abs(int(d) - int(current_depth)))
    depth_var.set(nearest_depth)
    for widget in depth_frame.winfo_children():
        widget.destroy()
    x = 0
    for i, group in enumerate(groups):
        if i == current_group:
            for depth in group:
                tk.Radiobutton(depth_frame, command=update_image, text=depth, variable=depth_var, value=depth, indicatoron=False, selectcolor="#77dd77", background="#d0f0c0" ).place(x=x, y=0, width=btn_width, height=btn_height)
                x += btn_width + gap
        else:
            local_width = 40
            tk.Button(depth_frame, text=f"{group[0]}-{group[-1]}", command=lambda i=i: show_group(i), background="#448b44").place(x=x, y=0, width=local_width, height=btn_height)
            x += local_width + gap
    update_image()


def change_position(step):
    index = positions.index(position_var.get())
    index = (index + step) % len(positions)   # continuous
    position_var.set(positions[index])
    update_image()


def change_depth(step):
    index = depths.index(depth_var.get())
    index = (index + step) % len(depths)      # continuous
    depth = depths[index]
    depth_var.set(depth)
    group = index // 13
    if group != current_group:
        show_group(group)
    else:
        update_image()


def change_depth_from_jump(depth):
    index = depths.index(depth)
    depth = depths[index]
    depth_var.set(depth)
    group = index // 13
    if group != current_group:
        show_group(group)
    else:
        update_image()


def action_keys(event):
    if event.keysym == "r":
        spot_action_var.set("raise-raise-low")
    elif event.keysym == "a":
        spot_action_var.set("call-raise-low")
    elif event.keysym == "s":
        spot_action_var.set("call-raise-low_med")
    elif event.keysym == "t":
        spot_action_var.set("raise-shove")
    elif event.keysym == "x":
        spot_action_var.set("call-shove")
    update_image()


def depth_jump(event):
    index = jump_keys.index(event.char)
    depth = jumps_vars[index].get()
    change_depth_from_jump(depth)


# def mouse_zoom(event):
#     global zoom_index

#     # determina o quadrante do mouse
#     half_width = root.winfo_width() / 2
#     half_height = root.winfo_height() / 2

#     if event.x < half_width and event.y < half_height:
#         quadrant = 1
#     elif event.x >= half_width and event.y < half_height:
#         quadrant = 2
#     elif event.x < half_width and event.y >= half_height:
#         quadrant = 3
#     else:
#         quadrant = 4

#     # muda o zoom
#     if event.delta > 0:
#         zoom_index = min(zoom_index + 1, len(zoom_modes) - 1)
#     else:
#         zoom_index = max(zoom_index - 1, 0)
#     if info_image:
#         update_info_image(info_image, quadrant)
#     else:
#         update_image(quadrant)
def mouse_zoom(event):
    global zoom_index

    # determina o quadrante do mouse
    half_width = root.winfo_width() / 2
    half_height = root.winfo_height() / 2

    if event.x < half_width and event.y < half_height:
        quadrant = 1

    elif event.x >= half_width and event.y < half_height:
        quadrant = 2

    elif event.x < half_width and event.y >= half_height:
        quadrant = 3

    else:
        quadrant = 4

    # determina a direção do scroll
    if hasattr(event, "delta") and event.delta:
        # Windows
        direction = 1 if event.delta > 0 else -1

    elif event.num == 4:
        # Linux: scroll para cima
        direction = 1

    elif event.num == 5:
        # Linux: scroll para baixo
        direction = -1

    else:
        return

    # muda o zoom
    zoom_index = max(
        0,
        min(zoom_index + direction, len(zoom_modes) - 1)
    )

    # atualiza a imagem mantendo o quadrante
    if info_image:
        update_info_image(info_image, quadrant)
    else:
        update_image(quadrant)


def start_drag(event):
    global drag_start_x, drag_start_y
    global image_start_x, image_start_y

    # Só permite arrastar com zoom > 1
    if zoom_modes[zoom_index] <= 1:
        return

    drag_start_x = event.x_root
    drag_start_y = event.y_root

    image_start_x = image_label.winfo_x()
    image_start_y = image_label.winfo_y()


def drag_image(event):
    global image_start_x, image_start_y

    if zoom_modes[zoom_index] <= 1:
        return

    dx = event.x_root - drag_start_x
    dy = event.y_root - drag_start_y

    new_x = image_start_x + dx
    new_y = image_start_y + dy

    # tamanho atual da imagem
    width = image_label.winfo_width()
    height = image_label.winfo_height()

    # área disponível (sem o menu inferior)
    screen_width = root.winfo_width()
    screen_height = root.winfo_height() - 27

    # Limites horizontais
    min_x = screen_width - width + 1
    max_x = -1

    # Limites verticais
    min_y = screen_height - height + 3
    max_y = -1

    new_x = max(min_x, min(new_x, max_x))
    new_y = max(min_y, min(new_y, max_y))

    image_label.place(x=new_x, y=new_y)


def update_image(quadrant = 1):
    global info_image
    info_image = None
    image_depth = Image.new("RGB", (1356, 676), "#FFFFFF")

    default_folder = Path(
        f"img_results/MTT/ChipEV/G0_T0/ranking/raise-raise-low/{depth_var.get()}/{position_var.get()}"
    )

    target_folder = Path(
        f"img_results/MTT/ChipEV/G0_T0/ranking/{spot_action_var.get()}/{depth_var.get()}/{position_var.get()}"
    )

    # usa target se existir, senão usa default
    folder = target_folder if target_folder.exists() else default_folder

    if not folder.exists():
        print("Pasta não existe:", folder)
        return

    for path in folder.glob("*.png"):

        name = path.stem

        # Descobre a posição da imagem
        if " oR" in name:
            # Exemplo: EP oR.png
            pos = position_var.get()

        elif "vs_" in name:

            after_vs = name.split("vs_")[1]

            # Formato:
            # HJ vs_MP R2.png
            # EP vs_EP R2.1_BB R12.6.png

            if "_" in after_vs:

                # procura a última posição depois do _
                pos = None

                for p in reversed(positions):
                    if f"_{p}" in name:
                        pos = p
                        break

                if pos is None:
                    continue

            else:
                # formato HJ vs_MP R2.png
                pos = after_vs.split()[0]

        else:
            continue


        if pos not in positions_offset:
            continue


        x, y = positions_offset[pos]

        try:
            img = Image.open(path).convert("RGB")
            image_depth.paste(img, (x, y))

        except Exception as e:
            print("Erro carregando:", path)
            print(e)

    zoom = zoom_modes[zoom_index]

    width = int(image_depth.width * zoom)
    height = int(image_depth.height * zoom)

    zoomed_image = image_depth.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    tk_img = ImageTk.PhotoImage(zoomed_image)

    image_label.configure(image=tk_img)
    image_label.image = tk_img

    if zoom == 1:
        x = -1
        y = -1

    elif quadrant == 1:
        x = -1
        y = -1

    elif quadrant == 2:
        x = root.winfo_width() - width - 1
        y = -1

    elif quadrant == 3:
        x = -1
        y = root.winfo_height() - height - 26

    elif quadrant == 4:
        x = root.winfo_width() - width - 1
        y = root.winfo_height() - height - 26

    image_label.place(x=x, y=y)


def update_info_image(info_path, quadrant=1):
    try:
        image_depth = Image.open(info_path).convert("RGB")

    except Exception as e:
        print("Erro carregando:", info_path)
        print(e)
        return

    zoom = zoom_modes[zoom_index]

    width = int(image_depth.width * zoom)
    height = int(image_depth.height * zoom)

    zoomed_image = image_depth.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    tk_img = ImageTk.PhotoImage(zoomed_image)

    image_label.configure(image=tk_img)
    image_label.image = tk_img

    # Mesmo posicionamento da update_image()
    if zoom == 1:
        x = -1
        y = -1

    elif quadrant == 1:
        x = -1
        y = -1

    elif quadrant == 2:
        x = root.winfo_width() - width - 1
        y = -1

    elif quadrant == 3:
        x = -1
        y = root.winfo_height() - height - 26

    elif quadrant == 4:
        x = root.winfo_width() - width - 1
        y = root.winfo_height() - height - 26

    image_label.place(x=x, y=y)


def toggle_info_image(image_path, event=None):
    global info_image

    if info_image == image_path:
        info_image = None
        update_image()

    else:
        info_image = image_path
        update_info_image(image_path)



color_data = { # call color 20% S in HSV BB+BU+CO R -10% V in HSV
    "EP": ['#FFFFFF', '#ffcccc', '#ff0000', '#bf0000', '#800000', '#400000', '#ffff00'],
    "MP": ['#FFFFFF', '#ffe7cc', '#ff8000', '#bf6000', '#804000', '#402000', '#ffff00'],
    "LJ": ['#FFFFFF', '#e7ccff', '#8000ff', '#6000bf', '#400080', '#200040', '#ffff00'],
    "HJ": ['#FFFFFF', '#ffccff', '#ff00ff', '#bf00bf', '#800080', '#400040', '#ffff00'],
    "CO": ['#FFFFFF', '#ccffe7', '#00e673', '#00a653', '#006633', '#002613', '#ffff00'],
    "BU": ['#FFFFFF', '#edffcc', '#99e600', '#6fa600', '#446600', '#1a2600', '#ffff00'],
    "SB": ['#FFFFFF', '#cce7ff', '#0080ff', '#0060bf', '#004080', '#002040', '#ffff00'],
    "BB": ['#FFFFFF', '#ccffff', '#00e6e6', '#00a6a6', '#006666', '#002626', '#ffff00'],
}

# positions_offset = {'EP': (0, 0), 'MP': (344, 0), 'LJ': (688, 0), 'HJ': (1032, 0), 'CO': (0, 339), 'BU': (344, 339), 'SB': (688, 339), 'BB': (1032, 339)}

positions_offset = {'EP': (0, 0), 'MP': (342, 0), 'LJ': (686, 0), 'HJ': (1030, 0), 'CO': (0, 339), 'BU': (342, 339), 'SB': (686, 339), 'BB': (1030, 339)}

positions = ['EP', 'MP', 'LJ', 'HJ', 'CO', 'BU', 'SB', 'BB']
depths = ["200", "160", "130", "100", "80", "70", "60", "55", "50", "45", "40", "38", "35", "32", "30", "28", "26", "25", "22", "20", "19", "17", "16", "15", "14", "13", "12", 
          "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
groups = [depths[i:i+13] for i in range(0, len(depths), 13)]
action_btn_dict = {"RR": "raise-raise-low", "RS": "raise-shove", "CR1": "call-raise-low", "CR2": "call-raise-low_med", "CS": "call-shove"}
raise_sizes = ["low", "low_med"]

zoom_modes = [1, 1.33, 2]
zoom_index = 0
drag_start_x = 0
drag_start_y = 0
image_start_x = 0
image_start_y = 0
info_image = None

jump_keys = ["Y", "U", "I", "O", "P"]#, "H", "J", "K", "L"]
jump_keys = [i.lower() for i in jump_keys]

root = tk.Tk()
root.title("XXXXXXXXX")
root.geometry("1356x701+0+0")
root.resizable(False, False)

position_var = tk.StringVar(value="EP")
depth_var = tk.StringVar(value="50")
spot_action_var = tk.StringVar(value="raise-raise-low")
jump_1_var = tk.StringVar(value="100")
jump_2_var = tk.StringVar(value="50")
jump_3_var = tk.StringVar(value="25")
jump_4_var = tk.StringVar(value="15")
jump_5_var = tk.StringVar(value="10")
# jump_6_var = tk.StringVar(value="15")
# jump_7_var = tk.StringVar(value="10")
# jump_8_var = tk.StringVar(value="5")
# jump_9_var = tk.StringVar(value="1")
jumps_vars = [jump_1_var, jump_2_var, jump_3_var, jump_4_var, jump_5_var]#, jump_6_var, jump_7_var, jump_8_var, jump_9_var]

image_label = tk.Label(root)
image_label.place(x=-2, y=-2)

top_tab = 1
left_tab = 5
btn_width = 25
btn_height = 25
spacing = 6
gap = 2
bottom_menu_background = "#AAAAA7"

bottom_menu = tk.Frame(root, width=1366, height=27, bg=bottom_menu_background)
bottom_menu.place(x=0, y=676)

for p, pos in enumerate(positions):
    color_selected = color_data[pos][2]
    color_unselected = color_data[pos][1]
    tk.Radiobutton(bottom_menu, command=update_image, text=pos, variable=position_var, value=pos, indicatoron=False, selectcolor=color_selected, background= color_unselected).place(x= left_tab + (p * (btn_width + gap)), y=top_tab, width=btn_width, height=btn_height)

prev = (spacing + left_tab) + len(positions) * (btn_width + gap)
depth_frame = tk.Frame(bottom_menu, background=bottom_menu_background)
depth_frame.place(x=prev, y=top_tab, width=433, height=btn_height)
current_group = 0
show_group(0)

prev = prev + spacing + gap + 433
for a, (k, v) in enumerate(action_btn_dict.items()):
    tk.Radiobutton(bottom_menu, command=update_image, text=k, variable=spot_action_var, value=v, indicatoron=False, selectcolor="#7b5eb1", background="#c3b4dd").place(x= prev + (a * (btn_width + gap)), y=top_tab, width=btn_width, height=btn_height)

prev = prev + spacing + gap + 140
for i in range(len(jump_keys)):
    # jump_entry_label = tk.Label(bottom_menu, bg=bottom_menu_background, justify="right", width=2, text=f"{jump_keys[i]}:").place(x=prev - 15 + (i * (gap + 42)), y=top_tab + 1)
    if jump_keys[i].lower() in ['y', 'p', 'j']:
        jump_entry_label = tk.Label(bottom_menu, bd=0, relief="flat", bg=bottom_menu_background, justify="right", text=f"{jump_keys[i]}:").place(x=prev - 14 + (i * (gap + 30)), y=top_tab + 2)
    else:
        jump_entry_label = tk.Label(bottom_menu, bd=0, relief="flat", bg=bottom_menu_background, justify="right", text=f"{jump_keys[i]}:").place(x=prev - 14 + (i * (gap + 30)), y=top_tab + 3)

    jump_entry = tk.Entry(bottom_menu, width=3, font=("Arial", 8), textvariable=jumps_vars[i], justify="right")
    jump_entry.place(x=prev - 4 + (i * (gap + 30)), y=top_tab + 3)



root.bind("<Left>", lambda e: change_position(-1))
root.bind("<Right>", lambda e: change_position(1))
root.bind("<Up>", lambda e: change_depth(-1))
root.bind("<Down>", lambda e: change_depth(1))
root.bind("r", action_keys)
root.bind("a", action_keys)
root.bind("s", action_keys)
root.bind("t", action_keys)
root.bind("x", action_keys)
root.bind("1", lambda *vars: (position_var.set("EP"), update_image()))
root.bind("2", lambda *vars: (position_var.set("MP"), update_image()))
root.bind("3", lambda *vars: (position_var.set("LJ"), update_image()))
root.bind("4", lambda *vars: (position_var.set("HJ"), update_image()))
root.bind("5", lambda *vars: (position_var.set("CO"), update_image()))
root.bind("6", lambda *vars: (position_var.set("BU"), update_image()))
root.bind("7", lambda *vars: (position_var.set("SB"), update_image()))
root.bind("8", lambda *vars: (position_var.set("BB"), update_image()))
for key in jump_keys:
    root.bind(key, depth_jump)
# for key in jump_keys:
#     root.bind(f"<Shift-{key}>", depth_jump)
root.bind("<Tab>", lambda e: (root.focus(), "break")[1])

# root.bind("<MouseWheel>", mouse_zoom)
root.bind("<MouseWheel>", mouse_zoom)
root.bind("<Button-4>", mouse_zoom)
root.bind("<Button-5>", mouse_zoom)
root.bind("<ButtonPress-1>", start_drag)
root.bind("<B1-Motion>", drag_image)
root.bind("<m>", lambda event: toggle_info_image("adds/min.png", event))

root.mainloop()
