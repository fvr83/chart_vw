# pyinstaller --noconsole --onefile --icon=icon.ico --add-data="icon.ico;." --hidden-import=os --hidden-import=sys --hidden-import=PIL.Image --hidden-import=PIL.ImageTk --hidden-import=tkinter --hidden-import=tkinter.ttk --add-data "C:\local_DEV\Python\Poker\VIEWER MOUNT _ PORT_LOCAL\res_res;res_res" main.py

import tkinter as tk
from tkinter import ttk
import sys
import os
from PIL import Image, ImageTk

def on_closing():
    confirm = tk.Toplevel(root)
    confirm.title("Confirm Exit")
    confirm.geometry("300x100")
    confirm.resizable(False, False)

    # pega tamanho da tela
    screen_width = confirm.winfo_screenwidth()
    screen_height = confirm.winfo_screenheight()

    # centraliza no monitor
    confirm_x = (screen_width // 2) - (300 // 2)
    confirm_y = (screen_height // 2) - (100 // 2)
    confirm.geometry(f"300x100+{confirm_x}+{confirm_y}")

    confirm.grab_set()  
    label = tk.Label(confirm, text="Are you sure you want to quit?")
    label.pack(pady=10)

    def yes():
        root.destroy()

    def no():
        confirm.destroy()

    b1 = tk.Button(confirm, text="Yes", width=10, command=yes)
    b1.pack(side="left", padx=20, pady=10)
    b2 = tk.Button(confirm, text="No", width=10, command=no)
    b2.pack(side="right", padx=20, pady=10)

def show_instructions():
    def update_language(event):
        selected_language = language_var.get()
        if selected_language == "English":
            instructions_text = r"""
========================================
        CONTROLS & SHORTCUTS GUIDE  
========================================

📌 **NAVIGATION CONTROLS**  
- **Zoom:**  
  - Scroll mouse up/down → Zoom in/out  
  - Press **'Z'** → 2x Zoom  
  - Press **'\'** → Reset zoom  

- **Move the image:**  
  - Click and drag  

- **Switch between positions and stack depths:**  
  - **Arrows ←/→** → Change position  
  - **Arrows ↑/↓** → Change stack depth  

----------------------------------------

🎮 **GAME MODES**  
- **Raise:**  
  - **'R'** → Low 3-bet (RR1)  
  - **'E'** → High 3-bet (RR5)  
  - **'T'** → All-in (R/S)  

- **Call:**  
  - **'C'** → Call / Low Raise (CR1)  
  - **'A' to 'F'** → Call / Raise (Sizes 1-4: Low → High)  
  - **'X'** → Call / All-in  

- **Limp:**  
  - **'K'** → Toggle 'with limp' and 'without limp'  
  - **'L'** → Select 'with limp' options  
  - **'J'** → Select 'without limp' options  

----------------------------------------

📍 **POSITION SELECTION**  
(Press the corresponding number)  
- **'3'** → EP  
- **'4'** → MP  
- **'5'** → LJ  
- **'6'** → HJ  
- **'7'** → CO  
- **'8'** → BU  
- **'9'** → SB  
- **'0'** → BB  

----------------------------------------

📏 **STACK DEPTH SELECTION**  
(Press the corresponding key)  
- **'Y'** → 100bb  
- **'U'** → 40bb  
- **'I'** → 20bb  
- **'O'** → 10bb  
- **'P'** → 6bb  

----------------------------------------

⚙️ **OTHER CONTROLS**  

**Click the buttons** → Toggle positions, stack depths, and modes  

** q, -, ', 1, 2, =, [, ] > → Toggle statistics page  

----------------------------------------

🎯 **POINTS (EV Indicators)**  

Blue Bands: Large = 8 points, Small = 4 points

- < / > → Shows the combos ranked by the EV of the actions in the 
    spot, and additionally by equity.   

- < ; > → Shows the EV of the most aggressive action at the top 
    and the most passive one at the bottom. Show indicative 
    EV stripes (see below)

- < . > → Show the highest EV and the action with the highest EV.   

- < , > → Group of **99% to 68%** of the total EV  
  - No points → Outside the group of hands that sum up to 99% of EV  
  - 32 points → Within the group of hands that sum up to 68% of EV  

- **'M'** → Group of **67% to 36%** of the total EV  
  - No points → Outside the group of hands that sum up to 67% of EV  
  - 32 points → Within the group of hands that sum up to 36% of EV  

- **'N'** → Group of **35% to 4%** of the total EV  
  - No points → Outside the group of hands that sum up to 35% of EV  
  - 32 points → Within the group of hands that sum up to 4% of EV  

- **'B'** → percent of the maximum EV of the best combo  
  - 16 points → Represent between **0.25% and 10%** of the max EV  
  
  **EV+ Indicative Stripes:**  
  - **Green** → Call  
  - **Red** → Raise  
  - **Black & White** → All-in  

========================================
"""
        elif selected_language == "Português":
            instructions_text = r"""
========================================
        GUIA DE CONTROLES E ATALHOS  
========================================

📌 **CONTROLES DE NAVEGAÇÃO**  
- **Zoom:**  
  - Roda de rolagem do mouse para cima/baixo → Aproximar/Afastar  
  - Pressione **'Z'** → Zoom 2x  
  - Pressione **'\'** → Redefinir zoom  

- **Mover a imagem:**  
  - Clique e arraste  

- **Alternar entre posições e profundidades:**  
  - **Setas ←/→** → Mudar posição  
  - **Setas ↑/↓** → Mudar profundidade de stack  

----------------------------------------

🎮 **MODOS DE JOGO**  
- **Raise:**  
  - **'R'** → 3-bet baixo (RR1)  
  - **'E'** → 3-bet alto (RR5)  
  - **'T'** → All-in (R/S)  

- **Call:**  
  - **'C'** → Call / Raise baixo (CR1)  
  - **'A' a 'F'** → Call / Raise (Tamanhos 1-4: Baixo → Alto)  
  - **'X'** → Call / All-in  

- **Limp:**  
  - **'K'** → Alterna 'com limp' e 'sem limp'  
  - **'L'** → Seleciona opções 'com limp'  
  - **'J'** → Seleciona opções 'sem limp'  

----------------------------------------

📍 **SELEÇÃO DE POSIÇÕES**  
(Pressione o número correspondente)  
- **'3'** → EP  
- **'4'** → MP  
- **'5'** → LJ  
- **'6'** → HJ  
- **'7'** → CO  
- **'8'** → BU  
- **'9'** → SB  
- **'0'** → BB  

----------------------------------------

📏 **SELEÇÃO DE PROFUNDIDADE DE STACK**  
(Pressione a tecla correspondente)  
- **'Y'** → 100bb  
- **'U'** → 40bb  
- **'I'** → 20bb  
- **'O'** → 10bb  
- **'P'** → 6bb  

----------------------------------------

⚙️ **OUTROS CONTROLES**  

- **Clique nos botões** → Alterna posições, profundidades e modos  

** q, -, ', 1, 2, =, [, ] > → Alterna página de estatísticas

----------------------------------------

🎯 **PONTOS (Indicadores de EV)**  

Faixas Azuis: Grande = 8 pontos, Pequena = 4 pontos

- < / > → Mostra os combos rankeados pelo EV das ações do 
    spot e suplementarmente pela equidade

- < ; > → Mostra o EV da ação mais agressiva no topo 
    e da mais passiva na parte inferior. Mostra faixas 
    indicativas de EV (ver abaixo)  

- < . > → Mostra o maior EV e a ação de maior EV.

- **','** → Grupo de **99% a 68%** do EV total  
  - Nenhum ponto → Fora do grupo das mãos que somam 99% do EV  
  - 32 pontos → Dentro do grupo das mãos que somam 68% do EV  

- **'M'** → Grupo de **67% a 36%** do EV total  
  - Nenhum ponto → Fora do grupo das mãos que somam 67% do EV  
  - 32 pontos → Dentro do grupo das mãos que somam 36% do EV  

- **'N'** → Grupo de **35% a 4%** do EV total  
  - Nenhum ponto → Fora do grupo das mãos que somam 35% do EV  
  - 32 pontos → Dentro do grupo das mãos que somam 4% do EV  

- **'B'** → Percentual do EV máximo do melhor combo  
  - 16 pontos → Representam entre **0.25% e 10%** do EV máximo  

  **Faixas indicativas de EV+:**  
  - **Verde** → Call  
  - **Vermelho** → Raise  
  - **Preto e Branco** → All-in  

========================================
"""  
        text.configure(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(tk.END, instructions_text)
        text.configure(state=tk.DISABLED)
    instructions_window = tk.Toplevel(root)
    instructions_window.title("Instructions")
    instructions_window.geometry("500x707+0+0") 
    language_var = tk.StringVar(value="English")
    language_dropdown = ttk.Combobox(
        instructions_window, textvariable=language_var, state="readonly", 
        values=["English", "Português"]
    )
    language_dropdown.bind("<<ComboboxSelected>>", update_language)
    language_dropdown.pack(pady=0)
    text = tk.Text(instructions_window, wrap=tk.WORD, font=("Arial", 12))
    text.insert(tk.END, "")  
    text.pack(fill=tk.BOTH, expand=True, padx=5, pady=0)
    update_language(None)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

def get_dir():
    if not size_var.get():
        return resource_path(os.path.join('res_res', view_var.get(), 'preflop', f'{mode_var.get()}, {limp_var.get()}', f'{depth_var.get()}bb', position_var.get()))
    else:
        return resource_path(os.path.join('res_res', view_var.get(), 'preflop', f'{mode_var.get()}, {limp_var.get()}, {size_var.get()}', f'{depth_var.get()}bb', position_var.get()))

def get_file_path(target_dir, pattern):
  if os.path.exists(target_dir):
    file_name = next(f for f in os.listdir(target_dir) if pattern in f)
    return os.path.join(target_dir, file_name)
  return None

def put_imgage(file_path, offset, image_depth):
  with Image.open(file_path) as img:
    image_depth.paste(img, offset)
    
def update_mode_size(key):
    mode_var.set(mode_size[key][0])
    size = mode_size[key][1]
    size_var.set("" if size is None else size)

def on_mouse_wheel(event):
    mouse_x, mouse_y = event.x, event.y
    image_label_width = image_label.winfo_width()
    image_label_height = image_label.winfo_height()
    zoom_values = [1, 1.344, 2.0]
    current_zoom_value = float(current_zoom.get())
    if event.delta > 0:  #
        new_zoom_index = min(zoom_values.index(current_zoom_value) + 1, len(zoom_values) - 1)
    else:  
        new_zoom_index = max(zoom_values.index(current_zoom_value) - 1, 0)
    current_zoom.set(zoom_values[new_zoom_index])
    if new_zoom_index == 0:
        image_label.place(x=0, y=0)
    elif new_zoom_index == 1:
        a = 0 if mouse_x <= image_label_width // 2 else -463 # -523
        b = 0 if mouse_y <= image_label_height // 2 else -232 # -260
        image_label.place(x=a, y=b)
    elif new_zoom_index == 2:
        c = 0 if mouse_x <= image_label_width // 2 else -1362
        f = 0 if mouse_y <= image_label_height // 2 else -677
        image_label.place(x=c, y=f)
    update_image()  

def on_click(event):
    global start_x, start_y  
    start_x = event.x_root
    start_y = event.y_root

def on_drag(event):
    zoom = float(current_zoom.get())
    if zoom == 1:
        image_label.place(x=3 , y=0)
    else:
        global start_x, start_y
        delta_x = event.x_root - start_x
        delta_y = event.y_root - start_y
        start_x = event.x_root
        start_y = event.y_root
        current_x = image_label.winfo_x()
        current_y = image_label.winfo_y() 
        image_width = image_label.current_width
        image_height = image_label.current_height
        root_width = root.winfo_width()
        root_height = root.winfo_height()
        if zoom == 1.344:
            container_width = max(root_width, image_width * zoom * 0.7486) #0.724
            container_height = max(root_height, image_height * zoom * 0.805) # 0.779
        else:
            container_width = max(root_width, image_width * zoom * 0.508)
            container_height = max(root_height, image_height * zoom * 0.525)
        min_x = root_width - container_width + 31 if zoom == 2 else root_width - container_width + 7 if zoom == 1.344 else root_width - container_width + 21
        max_x = 0
        min_y = root_height - container_height + 43 if zoom == 1.344 else root_height - container_height + 36
        max_y = 0
        new_x = max(min_x, min(current_x + delta_x, max_x))
        new_y = max(min_y, min(current_y + delta_y, max_y))
        image_label.place(x=new_x, y=new_y)

def update_image(*kwargs):
    image_depth = Image.new("RGB", (1358, 676), "#FFFFFF")
    if min_var.get() in ['min', 'percent', 'eq1', 'eq2', 'eq3', 'eq1-7', 'eq2-7', 'eq3-7']:
        # Determina o nome do arquivo baseado no valor de min_var
        if min_var.get() == 'min':
            filename = 'min.png'
        elif min_var.get() == 'percent':
            filename = 'percent.png'
        elif min_var.get() == 'eq1':
            filename = 'eq1.png'
        elif min_var.get() == 'eq2':
            filename = 'eq2.png'
        elif min_var.get() == 'eq3':
            filename = 'eq3.png'
        elif min_var.get() == 'eq1-7':
            filename = 'eq1-7.png'
        elif min_var.get() == 'eq2-7':
            filename = 'eq2-7.png'
        elif min_var.get() == 'eq3-7':
            filename = 'eq3-7.png'
            
        base_dir = resource_path(f'res_res\\results\\preflop\\adds\\{filename}')
        if os.path.exists(base_dir):
            try:
                image_depth = Image.open(base_dir)
                zoom_value = float(current_zoom.get())
                new_width = int(image_depth.width * zoom_value)
                new_height = int(image_depth.height * zoom_value)
                resized_image = image_depth.resize((new_width, new_height), resample=Image.LANCZOS)
                photo_image = ImageTk.PhotoImage(resized_image)
                image_label.config(image=photo_image)
                image_label.image = photo_image
                image_label.current_width = new_width
                image_label.current_height = new_height
                if current_zoom.get() == '1':
                    image_label.place(x=0, y=0)
            except Exception as e:
                print(f"Error loading image '{base_dir}': {e}")
        else:
            print(f"Image '{base_dir}' not found.")
    else:
        for pos, offset in positions_offset.items():
            base_dir = get_dir()
            search_pattern = 'oR' if pos == position_var.get() else pos  
            file_path = None
            if os.path.exists(base_dir):  
                try:
                    file_name = next(f for f in os.listdir(base_dir) if search_pattern in f)
                    file_path = os.path.join(base_dir, file_name)
                except StopIteration:
                    pass 
            if not file_path and mode_var.get() == 'call-shove':
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\call-shove, True\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir):  
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass
            if not file_path and mode_var.get().endswith('shove'):
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-shove, {limp_var.get()}\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir):  
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass
            if not file_path and mode_var.get().endswith('shove'):
                alt_dir = resource_path(f'res_res\\results\\preflop\\raise-shove, True\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir):  
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass
            if not file_path and mode_var.get().startswith('call-raise'):
                size_list = ['low', 'low-med', 'med', 'med-high', 'high']
                current_size = size_var.get()  
                size_index = size_list.index(current_size)
                for i in range(size_index - 1, -1, -1):
                    prev_size = size_list[i]
                    alt_dir = resource_path(
                        f'res_res\\{view_var.get()}\\preflop\\call-raise, True, {prev_size}\\{depth_var.get()}bb\\{position_var.get()}'
                    )
                    if os.path.exists(alt_dir):
                        try:
                            file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                            file_path = os.path.join(alt_dir, file_name)
                            break 
                        except StopIteration:
                            continue  
            if not file_path and mode_var.get().startswith('call'):
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-raise, True, low\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir):  
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path:
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-raise, {limp_var.get()}, {size_var.get()}\\{depth_var.get()}bb\\{position_var.get()}') if not mode_var.get().startswith('call') else resource_path(f'{view_var.get()}\\preflop\\raise-raise, True, {size_var.get()}\\{depth_var.get()}bb\\{position_var.get()}') 
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path and mode_var.get() == 'call-shove':
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-raise, True, low\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path:
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-raise, {limp_var.get()}, low\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path:
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-raise, True, low\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path:
                alt_dir = resource_path(f'res_res\\results\\preflop\\raise-raise, True, low\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path:
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-shove, {limp_var.get()}\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path:
                alt_dir = resource_path(f'res_res\\{view_var.get()}\\preflop\\raise-shove, True\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        pass  
            if not file_path:
                alt_dir = resource_path(f'res_res\\results\\preflop\\raise-shove, True\\{depth_var.get()}bb\\{position_var.get()}')
                if os.path.exists(alt_dir): 
                    try:
                        file_name = next(f for f in os.listdir(alt_dir) if search_pattern in f)
                        file_path = os.path.join(alt_dir, file_name)
                    except StopIteration:
                        continue  
                else:
                    continue  
            try:
                with Image.open(file_path) as img:
                    image_depth.paste(img, offset)
            except Exception as e:
                continue
    zoom_value = float(current_zoom.get())
    new_width = int(image_depth.width * zoom_value)
    new_height = int(image_depth.height * zoom_value)
    resized_image = image_depth.resize((new_width, new_height), resample=Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(resized_image)
    image_label.config(image=photo_image)
    image_label.image = photo_image
    image_label.current_width = new_width
    image_label.current_height = new_height
    if current_zoom.get() == '1':
        image_label.place(x=3, y=0)

def toggle_mode(mode_type, event=None):
    global saved_vars, menu_open
    current_mode = min_var.get()
    
    # Se estamos no modo normal ('no') e queremos entrar em um modo especial
    if current_mode == 'no':
        # Salva o estado atual
        saved_vars = {
            'position': position_var.get(),
            'depth': depth_var.get(),
            'mode': mode_var.get(),
            'size': size_var.get(),
            'limp': limp_var.get(),
            'view': view_var.get(),
            'mode_size': mode_size_var.get()
        }
        min_var.set(mode_type)
        update_image()
    # Se já estamos em um modo especial
    elif current_mode in ['min', 'percent', 'eq1', 'eq2', 'eq3', 'eq1-7', 'eq2-7', 'eq3-7']:
        # Se pressionamos a mesma tecla do modo atual, volta ao normal
        if current_mode == mode_type or mode_type == 'reverse':
            # Restaura o estado salvo
            position_var.set(saved_vars.get('position'))
            depth_var.set(saved_vars.get('depth'))
            mode_var.set(saved_vars.get('mode'))
            size_var.set(saved_vars.get('size'))
            limp_var.set(saved_vars.get('limp'))
            view_var.set(saved_vars.get('view'))
            mode_size_var.set(saved_vars.get('mode_size'))
            min_var.set('no')
            update_image()
        else:
            # Alterna diretamente para o novo modo especial
            min_var.set(mode_type)
            update_image()
    if mode_type == 'reverse':
        min_var.set('no')
        update_image()
        toggle_toggle(event)
    if mode_type == 'min':
        toggle_toggle(event)
    if mode_type == 'percent':
        toggle_toggle(event)
        

def toggle_limp_mode(event=None):
    limp_var.set('False') if limp_var.get() == 'True' else limp_var.set('True')
    update_image()

def navigate_depth(direcao):
    atual = depth_var.get()
    try:
        idx = depths.index(atual)
        if direcao == 'up':
            novo_idx = (idx - 1) % len(depths) 
        else:  # 'down'
            novo_idx = (idx + 1) % len(depths)  
        depth_var.set(depths[novo_idx])
        update_image()
    except ValueError:
        depth_var.set('100')  # fallback
        update_image()

def navigate_position(direction):
    current = position_var.get()
    try:
        idx = positions.index(current)
        if direction == 'left':
            new_idx = (idx - 1) % len(positions)
        else:  # 'right'
            new_idx = (idx + 1) % len(positions)
        position_var.set(positions[new_idx])
        update_image()
    except ValueError:
        position_var.set('EP')  # fallback
        update_image()

def change_zoom_on_button(direction):
    zoom_values_local = [1, 1.344, 2.0]
    current_zoom_index = zoom_values_local.index(float(current_zoom.get()))
    idx = current_zoom_index
    if direction == '+' and idx < len(zoom_values_local) - 1:
        idx += 1
    elif direction == '-' and idx > 0:
        idx -= 1
    current_zoom.set(zoom_values_local[idx])
    if current_zoom.get() == '1':
        update_image()
        image_label.place(x=0, y=0)
    else:
        update_image()
        image_label.place(x=0, y=0)

root = tk.Tk()
try:
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        print(f"Ícone não encontrado: {icon_path}")
except Exception as e:
    print(f"Erro ao definir o ícone: {e}")

popup_menu_frame = None
menu_open = False
click_outside_bound = False
toggle_button = None

def toggle_pop_up_menu(event=None):
    global popup_menu_frame, menu_open, click_outside_bound, toggle_button
    
    if menu_open and not popup_menu_frame:
        return

    # Se já aberto -> fecha
    if menu_open and popup_menu_frame and popup_menu_frame.winfo_exists():
        popup_menu_frame.destroy()
        popup_menu_frame = None
        menu_open = False
        return

    # Abre o menu
    menu_width = 561
    menu_height = 33
    x_target = root.winfo_width() - menu_width
    y_target = 645  # ajuste conforme seu layout

    popup_menu_frame = tk.Frame(root, width=menu_width, height=menu_height,
                                bg="black", relief="raised", bd=2)
    popup_menu_frame.place(x=x_target, y=y_target)
    popup_menu_frame.bind("<Button-1>", lambda e: "break")  # evita fechar ao clicar dentro
    menu_open = True

    # Conteúdo do menu (adapte)
    tk.Label(popup_menu_frame,
             bg="black").place(x=10, y=8)
    help_button = tk.Button(popup_menu_frame, text="?", font=('Tahoma', 20, 'bold'),
                            background='yellow', 
                            command=lambda: [show_instructions(), popup_menu_frame.destroy()])
    help_button.place(x=0, y=0, width=55, height=30)

    check_button_list = {
        'NORMAL': 'reverse', 'Heat 1': 'eq1', 'Heat 2': 'eq2', 'Heat 3': 'eq3',
        'Color 1': 'eq1-7', 'Color 2': 'eq2-7', 'Color 3': 'eq3-7', 'Range %': 'percent', 'Data 1': 'min'
    }

    gap = 1
    buttons_per_row = 10  # total de colunas

    for idx, (btn_text, mode_type) in enumerate(check_button_list.items()):
        row = (idx + 1) // buttons_per_row
        col = (idx + 1) % buttons_per_row
        x = col * (55 + gap)
        y = row * (30 + gap)
        if idx == 0:
            bcl = 'White'
        elif 0 < idx < 4:
            bcl = '#F4B000'
        elif 3 < idx < 7:
            bcl = '#07F598'
        elif idx == 7:
            bcl = '#1147F5'
        elif idx == 8:
            bcl = '#F73E90'
        elif idx in [9, 10]:
            bcl = '#F54E07'
        else:
            bcl = 'darkgray'
        tk.Button(popup_menu_frame, text=btn_text, background=bcl,
                command=lambda mt=mode_type: toggle_mode(mt)) \
            .place(x=x, y=y, width=55, height=30)

    def click_outside(e):
        if not menu_open:
            return
        x, y = e.x_root, e.y_root

        mx1 = popup_menu_frame.winfo_rootx(); my1 = popup_menu_frame.winfo_rooty()
        mx2 = mx1 + popup_menu_frame.winfo_width(); my2 = my1 + popup_menu_frame.winfo_height()
        if mx1 <= x <= mx2 and my1 <= y <= my2:
            return

        if toggle_button:
            bx1 = toggle_button.winfo_rootx(); by1 = toggle_button.winfo_rooty()
            bx2 = bx1 + toggle_button.winfo_width(); by2 = by1 + toggle_button.winfo_height()
            if bx1 <= x <= bx2 and by1 <= y <= by2:
                return

        toggle_pop_up_menu()

    if not click_outside_bound:
        root.bind("<Button-1>", click_outside, add="+")
        click_outside_bound = True

    steps = 15
    start_x = root.winfo_width()
    dx = (x_target - start_x) / steps
    step = 0
    def slide_in():
        nonlocal step
        if popup_menu_frame and popup_menu_frame.winfo_exists():
            if step < steps:
                new_x = int(start_x + dx * (step + 1))
                popup_menu_frame.place(x=new_x, y=y_target)
                step += 1
                root.after(12, slide_in)
            else:
                popup_menu_frame.place(x=x_target, y=y_target)
    slide_in()

def toggle_toggle(event=None):
    global menu_open
    menu_open = True
    toggle_pop_up_menu(event)
    menu_open = False

root.title("PFM - 0.95")
root.geometry("1366x707+0+0")
image_label = tk.Label(root)
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_closing)
image_label.pack()

positions = ['EP', 'MP', 'LJ', 'HJ', 'CO', 'BU', 'SB', 'BB']
depths = ['100', '80', '60', '50', '40', '35', '30', '25', '20', '17', '14', '12', '10', '9', '8', '7', '6', '5', '4', '3', '2']
mode_size = {
    'RR1': ['raise-raise', 'low'],
    'RR2': ['raise-raise', 'high'],
    'R/S': ['raise-shove', None],
    'CR1': ['call-raise', 'low'],
    'CR2': ['call-raise', 'low-med'],
    'CR3': ['call-raise', 'med'],
    'CR4': ['call-raise', 'med-high'],
    'C/S': ['call-shove', None] 
}
limps = {'wl': 'True', 'nl': 'False'}
views = {'Rk': 'results', 'AP': 'results_inf', 'Mx': 'results_rnk', '68': 'results_bc1', '36': 'results_bc2', '04': 'results_bc3', 'Th': 'results_thr'}
positions_offset = {'EP': (0, 0), 'MP': (344, 0), 'LJ': (688, 0), 'HJ': (1032, 0), 'CO': (0, 339), 'BU': (344, 339), 'SB': (688, 339), 'BB': (1032, 339)}
# positions_offset = {'EP': (0, 0), 'MP': (328, 0), 'LJ': (656, 0), 'HJ': (984, 0), 'CO': (0, 339), 'BU': (328, 339), 'SB': (656, 339), 'BB': (984, 339)}
zoom_btn = ['+', '-']

position_var = tk.StringVar(value='EP')
depth_var = tk.StringVar(value='100')
mode_var = tk.StringVar(value='raise-raise')
size_var = tk.StringVar(value='low')
limp_var = tk.StringVar(value='True')
view_var = tk.StringVar(value='results')
mode_size_var = tk.StringVar(value='RR1')
min_var = tk.StringVar(value='no')
current_zoom = tk.StringVar(value=1)
saved_vars = {}

btn_width = 25
btn_height = 25
spacing = 6

rect = tk.Canvas(root, width=1366, height=27, bg='white', highlightthickness=0)
rect.place(x=0, y=680)
rect.create_rectangle(0, 0, 1366, 27, fill="#F0F0F0", outline="")

for p, pos in enumerate(positions):
    color_selected = '#ff0000' if pos == 'EP' else '#ff8000' if pos == 'MP' else '#8000ff' if pos == 'LJ' else '#ff00ff' if pos == 'HJ' else '#00e673' if pos == 'CO' else '#99e600' if pos == 'BU' else '#0080ff' if pos == 'SB' else '#00e6e6'
    tk.Radiobutton(root, text=pos, variable=position_var, value=pos, indicatoron=False, selectcolor=color_selected, background= '#e6e6e6').place(x= 5 + (p * (btn_width + 2)), y=680, width=btn_width, height=btn_height)

prev = spacing + (len(positions) * (btn_width + 2)) + 5
for d, dpt in enumerate(depths):
    tk.Radiobutton(root, text=dpt, variable=depth_var, value=dpt, indicatoron=False, selectcolor='#77dd77', background='#d0f0c0').place(x= prev + (d * (btn_width + 2)), y=680, width=btn_width, height=btn_height)

prev2 = prev + spacing + (len(depths) * (btn_width + 2))
for m, key in enumerate(mode_size):
    tk.Radiobutton(root, text=key, variable=mode_size_var, value=key, 
                   command=lambda k=key: update_mode_size(k), indicatoron=False, selectcolor='#b39ddb', background='#f3f0ff').place(x= prev2 + (m * (btn_width + 2)), y=680, width=btn_width, height=btn_height)

prev3 = prev2 + spacing + (len(mode_size) * (btn_width + 2))
for l, (key, val) in enumerate(limps.items()):
    tk.Radiobutton(root, text=key, variable=limp_var, value=val, indicatoron=False, selectcolor='#ffb347', background='#ffe5b4').place(x= prev3 + (l * (btn_width + 2)), y=680, width=btn_width, height=btn_height)

prev4 = prev3 + spacing + (len(limps.items()) * (btn_width + 2))
for v, (key, val) in enumerate(views.items()):
    tk.Radiobutton(root, text=key, variable=view_var, value=val, indicatoron=False, selectcolor='#7bd0db', background='#d0faff').place(x= prev4 + (v * (btn_width + 2)), y=680, width=btn_width, height=btn_height)

prev5 = prev4 + spacing + (len(views.items()) * (btn_width + 2))
for z, zm in enumerate(zoom_btn):
    tk.Button(root, text=zm, command=lambda x=zm:change_zoom_on_button(x), background='lightgray').place(x= prev5 + (z * (btn_width + 2)), y=680, width=btn_width, height=btn_height)

prev6 = prev5 + spacing + (len(zoom_btn) * (btn_width + 2))
toggle_button = tk.Button(root, text='☰', command=toggle_pop_up_menu, foreground='white', background='black')
toggle_button.place(x= prev6 , y=680, width=btn_width, height=btn_height)

for var in [position_var, depth_var, mode_var, size_var, limp_var, view_var]:
    var.trace_add("write", update_image)

root.bind("<MouseWheel>", on_mouse_wheel)
image_label.bind("<ButtonPress-1>", on_click)
image_label.bind("<B1-Motion>", on_drag)
root.bind("<Escape>", lambda event: toggle_mode('reverse', event))
root.bind("<minus>", lambda event: toggle_mode('min', event))
root.bind("<'>", lambda event: toggle_mode('eq1', event))
root.bind("<Key-1>", lambda event: toggle_mode('eq2', event))
root.bind("<Key-2>", lambda event: toggle_mode('eq3', event))
root.bind("<=>", lambda event: toggle_mode('eq1-7', event))
root.bind("<Key-[>", lambda event: toggle_mode('eq2-7', event))
root.bind("<Key-]>", lambda event: toggle_mode('eq3-7', event))
root.bind("<Key-q>", lambda event: toggle_mode('percent', event))
root.bind('<Key-r>', lambda event: (mode_size_var.set('RR1'), update_mode_size('RR1')))
root.bind('<Key-e>', lambda event: (mode_size_var.set('RR2'), update_mode_size('RR2')))
root.bind('<Key-t>', lambda event: (mode_size_var.set('R/S'), update_mode_size('R/S')))
root.bind('<Key-a>', lambda event: (mode_size_var.set('CR1'), update_mode_size('CR1')))
root.bind('<Key-s>', lambda event: (mode_size_var.set('CR2'), update_mode_size('CR2')))
root.bind('<Key-d>', lambda event: (mode_size_var.set('CR3'), update_mode_size('CR3')))
root.bind('<Key-f>', lambda event: (mode_size_var.set('CR4'), update_mode_size('CR4')))
root.bind('<Key-c>', lambda event: (mode_size_var.set('CR1'), update_mode_size('CR1')))
root.bind('<Key-x>', lambda event: (mode_size_var.set('C/S'), update_mode_size('C/S')))
root.bind('<Key-3>', lambda event: (position_var.set('EP')))
root.bind('<Key-4>', lambda event: (position_var.set('MP')))
root.bind('<Key-5>', lambda event: (position_var.set('LJ')))
root.bind('<Key-6>', lambda event: (position_var.set('HJ')))
root.bind('<Key-7>', lambda event: (position_var.set('CO')))
root.bind('<Key-8>', lambda event: (position_var.set('BU')))
root.bind('<Key-9>', lambda event: (position_var.set('SB')))
root.bind('<Key-0>', lambda event: (position_var.set('BB')))
root.bind('<Key-y>', lambda event: (depth_var.set('100')))
root.bind('<Key-u>', lambda event: (depth_var.set('40')))
root.bind('<Key-i>', lambda event: (depth_var.set('20')))
root.bind('<Key-o>', lambda event: (depth_var.set('10')))
root.bind('<Key-p>', lambda event: (depth_var.set('6')))
root.bind('<Key-/>', lambda event: (view_var.set('results')))
root.bind('<Key-;>', lambda event: (view_var.set('results_inf')))
root.bind('<Key-.>', lambda event: (view_var.set('results_rnk')))
root.bind('<Key-,>', lambda event: (view_var.set('results_bc1')))
root.bind('<Key-m>', lambda event: (view_var.set('results_bc2')))
root.bind('<Key-n>', lambda event: (view_var.set('results_bc3')))
root.bind('<Key-b>', lambda event: (view_var.set('results_thr')))
root.bind('<Key-j>', lambda event: (limp_var.set('False')))
root.bind('<Key-l>', lambda event: (limp_var.set('True')))
root.bind('<Key-k>', lambda event: (toggle_limp_mode(event)))
root.bind('<Key-z>', lambda event: (current_zoom.set(2), image_label.place(x=0, y=0), update_image()))
root.bind('<Key-\\>', lambda event: (current_zoom.set(1), image_label.place(x=3, y=0), update_image()))
root.bind('<Key-F1>', lambda event: (show_instructions()))
root.bind('<Key-Up>', lambda event: navigate_depth('up'))
root.bind('<Key-Down>', lambda event: navigate_depth('down'))
root.bind('<Left>', lambda event: navigate_position('left'))
root.bind('<Right>', lambda event: navigate_position('right'))

if __name__ == "__main__":
    update_image()
    root.mainloop()
