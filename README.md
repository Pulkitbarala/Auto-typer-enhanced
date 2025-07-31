# 🚀 AutoTyper Pro – Advanced Typing Automation Tool

> Built with 💻 by **Pulkit Barala**

---

## 🧠 Features at a Glance

✨ Sleek Modern UI with **Resizable Window**  
🎯 Typing Modes: Full / Quick / Line-by-Line / Single-Line  
📋 **Clipboard Override Mode** – Ctrl+2 types clipboard even if text box has content  
🔍 Typing Preview before execution  
🧰 **System Tray Toggle** – Ctrl+Shift+H to hide/unhide  
⚙️ Customizable Hotkeys *(First-time setup with saved config)*  
🛡️ Works on screen-sharing + in coding editors  
📦 Portable `.EXE` (no install needed)  
📊 Live Character, Word, and Line Count

---

## 🎥 Demo Preview

![AutoTyper Preview](https://via.placeholder.com/800x400?text=Demo+GIF+Here)

---

## 🧩 Modes & Shortcuts

| Shortcut / Button         | Description                                |
|---------------------------|--------------------------------------------|
| ▶ `Type All`              | Normal Typing (delay 4s)                   |
| ⚡ `Quick Typing` (Ctrl+6) | Fast Typing (delay 1s)                     |
| 📄 `Single Line`          | Remove line breaks, type as one line       |
| 📋 `Line-by-Line`         | Type one line at a time                    |
| 🔍 `Preview`              | Show full typed text before running        |
| ⌨ `Ctrl+2`               | Type from clipboard (even if text exists)  |
| ❄ `Ctrl+Shift+H`         | Hide/Restore app from tray                 |
| 🚱 `Ctrl+Shift+S`         | Emergency Stop                             |
| 🗑 `Clear`                | Clear text field                           |

---

## 🛠 Setup Guide

### 🔧 Install Requirements

```bash
pip install pyinstaller pynput pystray pillow keyboard
```

---

### ⚙️ Create `.EXE` File

```bash
pyinstaller autotyper.py --noconsole --onefile
```

Your portable EXE will be inside:

```
dist/AutoTyperPro.exe
```

✅ Double-click and run on any Windows PC — no Python needed!

---

## 🧑‍💻 Tech Stack

- `Tkinter` – GUI  
- `Pynput` – Keyboard Controller  
- `Keyboard` – Hotkeys  
- `Pystray` – System Tray  
- `Pillow` – Tray Icon Image  
- `PyInstaller` – `.EXE` Builder  

---

## 💻 Screenshot Preview

| Dynamic Resizable UI | Tray Mode Active |
|----------------------|------------------|
| ![Resizable UI](https://via.placeholder.com/300x200?text=Resizable+UI) | ![Tray](https://via.placeholder.com/300x200?text=Tray+Icon) |

---

## 🧩 Coming Soon / Enhancements

- 🎨 Theme switcher (dark/light)  
- 🧠 Smart typing speed per content type  
- 💾 Drag-and-drop file support  
- 🛠 Custom hotkeys (first-run setup + display beside UI)  

---

## 🙋‍♂️ Support & Credits

Made with ❤️ by [**Pulkit Barala**](https://github.com/pulkitbarala)

Feel free to fork ⭐ this repo and contribute!

---

## 🔐 Protection Tips

To protect your `.py` code:

1. **Compile to `.pyc` using `compileall`**
2. **Use PyArmor for obfuscation + encryption**
3. **Package with PyInstaller –noconsole –onefile**
