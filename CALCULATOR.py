import tkinter as tk
import math

# --- Safe math environment ---
safe_dict = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "log": math.log10, "ln": math.log,
    "sqrt": math.sqrt,
    "pi": math.pi, "e": math.e,
    "pow": pow
}

expression = ""
history = []
dark_mode = True
scientific_mode = True

# --- Theme Colors ---
def get_theme():
    if dark_mode:
        return {"bg":"#1e1e1e","fg":"#ffffff","btn":"#2d2d2d","op":"#ff9500"}
    else:
        return {"bg":"#f4f4f4","fg":"#000000","btn":"#ffffff","op":"#ff9500"}

# --- Functions ---
def press(val):
    global expression
    expression += str(val)
    display_var.set(expression)

def clear():
    global expression
    expression = ""
    display_var.set("")

def calculate():
    global expression
    try:
        result = str(eval(expression, {"__builtins__": None}, safe_dict))
        history.append(f"{expression} = {result}")
        display_var.set(result)
        expression = result
    except:
        display_var.set("Error")
        expression = ""

def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)

def toggle_mode():
    global scientific_mode
    scientific_mode = not scientific_mode
    build_buttons()

def open_history():
    hist_win = tk.Toplevel(root)
    hist_win.title("History")
    hist_win.geometry("300x400")
    t = tk.Text(hist_win)
    t.pack(fill="both", expand=True)
    for item in history:
        t.insert(tk.END, item + "\n")

def open_settings():
    def toggle_theme():
        global dark_mode
        dark_mode = not dark_mode
        apply_theme()

    win = tk.Toplevel(root)
    win.title("Settings")
    tk.Button(win, text="Toggle Light/Dark", command=toggle_theme).pack(pady=10)

# --- UI ---
root = tk.Tk()
root.title("Calculator")
root.geometry("420x600")
root.resizable(False, False)

display_var = tk.StringVar()

display = tk.Entry(root, textvariable=display_var,
                   font=("Arial", 20), justify="right")
display.pack(fill="both", padx=10, pady=10, ipady=15)

top_bar = tk.Frame(root)
top_bar.pack(fill="x")

tk.Button(top_bar, text="Mode", command=toggle_mode).pack(side="left")
tk.Button(top_bar, text="History", command=open_history).pack(side="left")
tk.Button(top_bar, text="Settings", command=open_settings).pack(side="right")

btn_frame = tk.Frame(root)
btn_frame.pack(expand=True, fill="both")

# --- Button Builder ---
def build_buttons():
    for widget in btn_frame.winfo_children():
        widget.destroy()

    theme = get_theme()

    basic = [
        ("7","8","9","/"),
        ("4","5","6","*"),
        ("1","2","3","-"),
        ("0",".","%","+")
    ]

    scientific = [
        ("sin(","cos(","tan(","sqrt("),
        ("log(","ln(","pow(","pi"),
        ("asin(","acos(","atan(","e")
    ]

    layout = scientific + basic if scientific_mode else basic

    for row in layout:
        row_frame = tk.Frame(btn_frame, bg=theme["bg"])
        row_frame.pack(expand=True, fill="both")

        for btn in row:
            color = theme["op"] if btn in "+-*/" else theme["btn"]
            tk.Button(
                row_frame, text=btn,
                bg=color, fg=theme["fg"],
                font=("Arial", 12),
                command=lambda x=btn: press(x)
            ).pack(side="left", expand=True, fill="both", padx=1, pady=1)

    # Bottom row (Enter last)
    bottom = tk.Frame(btn_frame)
    bottom.pack(fill="both")

    tk.Button(bottom, text="Clear", command=clear).pack(side="left", expand=True, fill="both")
    tk.Button(bottom, text="⌫", command=backspace).pack(side="left", expand=True, fill="both")
    tk.Button(bottom, text="Enter", bg=theme["op"], command=calculate)\
        .pack(side="left", expand=True, fill="both")

def apply_theme():
    theme = get_theme()
    root.configure(bg=theme["bg"])
    display.configure(bg=theme["btn"], fg=theme["fg"])
    build_buttons()

# --- Keyboard ---
def key_input(event):
    key = event.char
    if key in "0123456789+-*/().":
        press(key)
    elif key == "\r":
        calculate()
    elif key == "\x08":
        backspace()

root.bind("<Key>", key_input)

# Init
apply_theme()
root.mainloop()