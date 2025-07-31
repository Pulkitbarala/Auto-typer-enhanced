import re
import time
import threading
import tkinter as tk
from tkinter import *
from pynput.keyboard import Controller, Key
import keyboard as kb

root = Tk()
root.title("Auto Typer Pro - Pulkit Barala")
root.geometry("900x650")
root.minsize(700, 500)
root.configure(bg="#f8f9fa")

COLORS = {
    'bg': '#f8f9fa',
    'primary': '#007bff',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'dark': '#343a40',
    'white': '#ffffff',
    'text': '#212529',
    'muted': '#6c757d'
}

keyboard_controller = Controller()
CHAR_DELAY_SLOW = 0.09
CHAR_DELAY_MEDIUM = 0.05
CHAR_DELAY_FAST = 0.025
current_speed = CHAR_DELAY_SLOW
is_typing = False
typing_thread = None

def update_status(msg):
    status_var.set(msg)
    root.update_idletasks()

def safe_type_text(text, delay):
    global is_typing
    is_typing = True
    try:
        for char in text:
            if not is_typing:
                break
            if char in ['\n', '\r']:
                keyboard_controller.press(Key.enter)
                keyboard_controller.release(Key.enter)
            elif char == '\t':
                keyboard_controller.press(Key.tab)
                keyboard_controller.release(Key.tab)
            else:
                keyboard_controller.type(char)
            time.sleep(delay)
    except Exception as e:
        update_status(f"❌ Error: {e}")
    is_typing = False
    update_status("✅ Typing complete!")

def start_typing(text, delay=4):
    if is_typing:
        update_status("❌ Already typing.")
        return
    if not text.strip():
        update_status("❌ Empty text.")
        return
    def task():
        update_status(f"⏳ Typing in {delay}s...")
        time.sleep(delay)
        safe_type_text(text, current_speed)
    threading.Thread(target=task, daemon=True).start()

def stop_typing():
    global is_typing
    is_typing = False
    update_status("🛑 Typing stopped.")

def update_stats(*args):
    text = text_area.get(1.0, END + "-1c")
    char_count_var.set(f"📝 {len(text)} chars")
    word_count_var.set(f"📄 {len(text.split())} words")

def clear_text():
    text_area.delete(1.0, END)
    update_stats()
    update_status("🗑️ Cleared.")

def paste_clipboard():
    try:
        clip = root.clipboard_get()
        text_area.insert(INSERT, clip)
        update_stats()
        update_status("📋 Clipboard pasted.")
    except:
        update_status("❌ Clipboard empty.")

def paste_normal(): start_typing(text_area.get(1.0, END + "-1c"), 4)
def paste_quick(): start_typing(text_area.get(1.0, END + "-1c"), 1)
def paste_single(): start_typing(re.sub(r'\n', ' ', text_area.get(1.0, END + "-1c")), 4)
def paste_line(): start_typing(text_area.get(1.0, END + "-1c"), 4)
def paste_single_quick(): start_typing(re.sub(r'\n', ' ', text_area.get(1.0, END + "-1c")), 1)
def paste_line_quick(): start_typing(text_area.get(1.0, END + "-1c"), 1)

def type_clipboard_force():
    try:
        clip = root.clipboard_get()
        if clip.strip():
            start_typing(clip, 1)
        else:
            update_status("⚠️ Clipboard empty.")
    except:
        update_status("❌ Cannot access clipboard.")

def set_speed_slow():
    global current_speed
    current_speed = CHAR_DELAY_SLOW
    speed_var.set("SLOW")
    update_status("🐌 Speed: SLOW")

def set_speed_med():
    global current_speed
    current_speed = CHAR_DELAY_MEDIUM
    speed_var.set("MEDIUM")
    update_status("⚡ Speed: MEDIUM")

def set_speed_fast():
    global current_speed
    current_speed = CHAR_DELAY_FAST
    speed_var.set("FAST")
    update_status("🚀 Speed: FAST")

def build_ui():
    global text_area, status_var, speed_var, char_count_var, word_count_var

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    header = Frame(root, bg=COLORS['dark'], height=70)
    header.grid(row=0, column=0, sticky="ew")
    Label(header, text="Auto Typer Pro", bg=COLORS['dark'], fg="white", font=("Segoe UI", 18, "bold")).pack(pady=(10, 0))
    Label(header, text="By Pulkit Barala", bg=COLORS['dark'], fg="#ccc").pack()

    body = Frame(root, bg=COLORS['bg'])
    body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    body.grid_columnconfigure(0, weight=1)
    body.grid_rowconfigure(0, weight=1)

    lf = LabelFrame(body, text="📝 Text Input", font=("Segoe UI", 12, "bold"), bg=COLORS['bg'], fg=COLORS['text'])
    lf.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
    lf.grid_columnconfigure(0, weight=1)
    lf.grid_rowconfigure(0, weight=1)

    text_container = Frame(lf)
    text_container.grid(sticky="nsew", padx=10, pady=10)
    text_container.grid_columnconfigure(0, weight=1)
    text_container.grid_rowconfigure(0, weight=1)

    text_area = Text(text_container, font=("Consolas", 11), wrap=WORD, bg="white", relief=SOLID, undo=True)
    text_area.grid(row=0, column=0, sticky="nsew")
    scrollbar = Scrollbar(text_container, command=text_area.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    text_area['yscrollcommand'] = scrollbar.set
    text_area.bind('<KeyRelease>', update_stats)
    text_area.bind('<Button-1>', update_stats)

    stats = Frame(lf, bg=COLORS['bg'])
    stats.grid(sticky="ew", padx=10)
    char_count_var = StringVar(value="📝 0 chars")
    word_count_var = StringVar(value="📄 0 words")
    Label(stats, textvariable=char_count_var, bg=COLORS['bg'], fg=COLORS['muted']).pack(side=LEFT)
    Label(stats, textvariable=word_count_var, bg=COLORS['bg'], fg=COLORS['muted']).pack(side=LEFT, padx=20)
    Button(stats, text="📋 Paste", command=paste_clipboard, bg=COLORS['info'], fg="white", relief="flat").pack(side=RIGHT)
    Button(stats, text="🗑️ Clear", command=clear_text, bg=COLORS['danger'], fg="white", relief="flat").pack(side=RIGHT, padx=5)

    controls = Frame(body, bg=COLORS['bg'])
    controls.grid(row=1, column=0, sticky="ew", pady=(10, 0))
    for i in range(2): controls.grid_columnconfigure(i, weight=1)

    Button(controls, text="▶ Full Type(from clipboard use ctrl +2)", command=paste_normal, bg=COLORS['primary'], fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    Button(controls, text="⚡ Quick(ctrl + 6)", command=paste_quick, bg="#6f42c1", fg="white").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Button(controls, text="📄 One Line", command=paste_single, bg=COLORS['success'], fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    Button(controls, text="📋 Line-by-line", command=paste_line, bg=COLORS['warning'], fg="white").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    Button(controls, text="🔁 OneLine Quick", command=paste_single_quick, bg=COLORS['success'], fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    Button(controls, text="🔁 Line Quick(ctrl + 8)", command=paste_line_quick, bg=COLORS['warning'], fg="white").grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    Button(controls, text="🛑 Stop(ctrl+shift+S)", command=stop_typing, bg=COLORS['danger'], fg="white").grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    spd = Frame(body, bg=COLORS['bg'])
    spd.grid(row=2, column=0, sticky="ew", pady=5)
    Label(spd, text="Speed:", bg=COLORS['bg'], fg=COLORS['text']).pack(side=LEFT)
    speed_var = StringVar(value="SLOW")
    Label(spd, textvariable=speed_var, bg=COLORS['bg'], fg=COLORS['primary']).pack(side=LEFT, padx=10)
    Button(spd, text="🐌", command=set_speed_slow).pack(side=LEFT, padx=2)
    Button(spd, text="⚡", command=set_speed_med).pack(side=LEFT, padx=2)
    Button(spd, text="🚀", command=set_speed_fast).pack(side=LEFT, padx=2)

    footer = Frame(root, bg=COLORS['dark'], height=30)
    footer.grid(row=2, column=0, sticky="ew")
    status_var = StringVar(value="💡 Ready")
    Label(footer, textvariable=status_var, fg="white", bg=COLORS['dark']).pack(anchor=W, padx=10)

try:
    kb.add_hotkey('ctrl+2', type_clipboard_force)
    kb.add_hotkey('ctrl+6', paste_quick)
    kb.add_hotkey('ctrl+7', paste_single_quick)
    kb.add_hotkey('ctrl+8', paste_line_quick)
    kb.add_hotkey('ctrl+shift+s', stop_typing)
except:
    pass

build_ui()
root.mainloop()
