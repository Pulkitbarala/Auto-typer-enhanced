import re
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pynput.keyboard import Controller, Key
import keyboard as kb
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys
import os

# -----------------------------
# Auto Typer Pro by Pulkit Barala
# -----------------------------

# Initialize controller
keyboard_controller = Controller()

# Typing speed delays
CHAR_DELAY_SLOW = 0.08
CHAR_DELAY_MEDIUM = 0.04
CHAR_DELAY_FAST = 0.02

current_speed = CHAR_DELAY_MEDIUM
is_typing = False
hidden = False

# Tray icon image
def create_image():
    image = Image.new('RGB', (64, 64), color=(52, 58, 64))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 24, 48, 40), fill="white")
    return image

# Safe typing function
def safe_type_text(text, char_delay):
    global is_typing
    is_typing = True
    try:
        for char in text:
            if not is_typing:
                break
            if char == '\n':
                keyboard_controller.press(Key.enter)
                keyboard_controller.release(Key.enter)
            elif char == '\t':
                keyboard_controller.press(Key.tab)
                keyboard_controller.release(Key.tab)
            else:
                keyboard_controller.type(char)
            time.sleep(char_delay)
    finally:
        is_typing = False
        update_status("✅ Typing completed!")

# Threaded typing start
def start_typing_thread(text, delay_time=4):
    if not text.strip():
        update_status("❌ No text to type!")
        return

    def typing_task():
        update_status(f"⏳ Starting in {delay_time} seconds...")
        time.sleep(delay_time)
        if is_typing:
            return
        update_status(f"⌨️ Typing {len(text)} characters...")
        safe_type_text(text, current_speed)

    threading.Thread(target=typing_task, daemon=True).start()

# Typing modes
def paste_normal():
    text = text_area.get("1.0", tk.END + "-1c")
    start_typing_thread(text, 4)

def paste_quick():
    text = text_area.get("1.0", tk.END + "-1c")
    start_typing_thread(text, 1)

def paste_single_line():
    text = re.sub(r'\n', ' ', text_area.get("1.0", tk.END + "-1c"))
    start_typing_thread(text, 4)

def paste_single_line_quick():
    text = re.sub(r'\n', ' ', text_area.get("1.0", tk.END + "-1c"))
    start_typing_thread(text, 1)

def paste_line_by_line():
    text = text_area.get("1.0", tk.END + "-1c")
    lines = text.strip().split('\n')
    full_text = '\n'.join(lines)
    start_typing_thread(full_text, 4)

def paste_line_by_line_quick():
    text = text_area.get("1.0", tk.END + "-1c")
    lines = text.strip().split('\n')
    full_text = '\n'.join(lines)
    start_typing_thread(full_text, 1)

# Control functions
def stop_typing():
    global is_typing
    is_typing = False
    update_status("🛑 Typing stopped!")

def set_speed_slow():
    global current_speed
    current_speed = CHAR_DELAY_SLOW
    update_status("🐌 Speed set to SLOW")

def set_speed_medium():
    global current_speed
    current_speed = CHAR_DELAY_MEDIUM
    update_status("⚖ Speed set to MEDIUM")

def set_speed_fast():
    global current_speed
    current_speed = CHAR_DELAY_FAST
    update_status("🚀 Speed set to FAST")

def update_status(message):
    status_var.set(message)
    root.update_idletasks()

def update_char_count(*args):
    try:
        text = text_area.get("1.0", tk.END + "-1c")
        chars = len(text)
        lines = text.count('\n') + (1 if text else 0)
        words = len(text.split()) if text.strip() else 0
        char_count_var.set(f"📝 {chars} chars, {lines} lines")
        word_count_var.set(f"📄 {words} words")
    except:
        pass

def clear_text():
    text_area.delete("1.0", tk.END)
    update_char_count()
    update_status("🗑️ Text cleared")

def paste_from_clipboard():
    try:
        clipboard_text = root.clipboard_get()
        text_area.insert(tk.INSERT, clipboard_text)
        update_char_count()
        update_status("📋 Text pasted from clipboard")
    except:
        update_status("❌ Clipboard empty")

# Preview popup
def preview_typing():
    preview = tk.Toplevel(root)
    preview.title("Typing Preview")
    preview.geometry("600x300")
    tk.Label(preview, text="Typing Preview:", font=("Segoe UI", 10, "bold")).pack()
    preview_text = tk.Text(preview, wrap="word", font=("Consolas", 10))
    preview_text.insert("1.0", text_area.get("1.0", tk.END))
    preview_text.config(state="disabled")
    preview_text.pack(expand=True, fill="both", padx=10, pady=10)
    ttk.Button(preview, text="✅ Start Typing", command=lambda: [preview.destroy(), paste_normal()]).pack(pady=10)

# Tray control
def toggle_window():
    global hidden
    if hidden:
        root.after(0, root.deiconify)
    else:
        root.after(0, root.withdraw)
    hidden = not hidden

def tray_exit():
    icon.stop()
    root.destroy()
    sys.exit()

def run_tray():
    icon.run()

# Init UI
root = tk.Tk()
root.title("Auto Typer Pro - by Pulkit Barala")
root.geometry("850x600")
root.configure(bg="#f8f9fa")

# Text Area
text_area = tk.Text(root, font=("Consolas", 11), bg="white", fg="#212529", wrap="word")
text_area.pack(expand=True, fill="both", padx=10, pady=(10, 0))
text_area.bind('<KeyRelease>', update_char_count)
text_area.bind('<Button-1>', update_char_count)

# Stats
status_frame = tk.Frame(root, bg="#f8f9fa")
status_frame.pack(fill="x", padx=10, pady=5)
char_count_var = tk.StringVar(value="📝 0 chars, 0 lines")
word_count_var = tk.StringVar(value="📄 0 words")

tk.Label(status_frame, textvariable=char_count_var, bg="#f8f9fa", fg="#6c757d").pack(side="left")
tk.Label(status_frame, textvariable=word_count_var, bg="#f8f9fa", fg="#6c757d").pack(side="left", padx=(20, 0))

# Controls
controls = tk.Frame(root, bg="#f8f9fa")
controls.pack(fill="x", padx=10, pady=10)

for text, command in [
    ("▶ Type All", paste_normal),
    ("⚡ Quick", paste_quick),
    ("📄 Single Line", paste_single_line),
    ("⚡ Single Line Quick", paste_single_line_quick),
    ("📋 Line by Line", paste_line_by_line),
    ("⚡ Line by Line Quick", paste_line_by_line_quick),
    ("🔍 Preview", preview_typing),
    ("🛑 Stop", stop_typing),
    ("🗑️ Clear", clear_text),
    ("📋 Paste", paste_from_clipboard)
]:
    ttk.Button(controls, text=text, command=command).pack(side="left", padx=5)

# Speed buttons
speed_controls = tk.Frame(root, bg="#f8f9fa")
speed_controls.pack(fill="x", padx=10)

for name, func in [
    ("🐌 Slow", set_speed_slow),
    ("⚖ Medium", set_speed_medium),
    ("🚀 Fast", set_speed_fast)
]:
    ttk.Button(speed_controls, text=name, command=func).pack(side="left", padx=5, pady=5)

# Status bar
status_var = tk.StringVar(value="💡 Ready")
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief="sunken", anchor="w", bg="#343a40", fg="white")
status_bar.pack(side="bottom", fill="x")

# Shortcuts
kb.add_hotkey("ctrl+6", paste_quick)
kb.add_hotkey("ctrl+7", paste_single_line_quick)
kb.add_hotkey("ctrl+8", paste_line_by_line_quick)
kb.add_hotkey("ctrl+shift+s", stop_typing)
kb.add_hotkey("ctrl+shift+h", toggle_window)

# Tray
icon = pystray.Icon("AutoTyper", create_image(), "Auto Typer Pro", menu=pystray.Menu(
    item('Show/Hide', toggle_window),
    item('Stop Typing', stop_typing),
    item('Exit', tray_exit)
))
threading.Thread(target=run_tray, daemon=True).start()

# Start app
root.mainloop()
