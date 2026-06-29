# grid-launcher
Lightweight menu for PostmarketOS devices running niri/hypr/etc
# 📱 Touch Grid Launcher for Linux Mobile

A lightweight, touch-optimized application launcher built with **Python** and **GTK3**. Designed specifically for Wayland compositors (like [Niri](https://github.com/YaLTeR/niri)) and mobile Linux distributions (like [postmarketOS](https://postmarketos.org/)).

If you are tired of desktop-oriented launchers that are hard to use with a finger, this simple grid launcher is for you.

![Python](https://img.shields.io/badge/Python-3.6+-blue)
![GTK3](https://img.shields.io/badge/GTK-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Touch-Friendly UI:** Large 3-column grid layout with generous spacing, perfect for tapping with a finger.
- **Modern Dark Theme:** Beautiful, custom-styled dark UI using GTK CSS.
- **Lightweight:** Built with pure Python and GTK3. No heavy frameworks or web engines.
- **Smart App Detection:** Automatically parses standard `.desktop` files from `/usr/share/applications` and `~/.local/share/applications`.
- **Auto-Close:** The launcher automatically closes when you tap an app to launch it.
- **Scrollable:** Smooth scrolling for devices with many installed apps.

The script was written using AI

## 📦 Requirements

- Python 3
- GTK 3
- PyGObject (`python3-gobject`)

**Install dependencies on Alpine/postmarketOS:**
```bash
sudo apk add python3 py3-gobject3 gtk+3.0

