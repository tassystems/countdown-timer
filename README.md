
# ⏳ 24U Countdown Timer for Raspberry Pi

A fullscreen Raspberry Pi (3B+ or higher) countdown timer built with Pygame for events.

Features:
- 24-hour default countdown
- Custom HH:MM:SS timer modification (keyboard only)
- Color-coded urgency system
- Real-time percentage progress tracking
- Victory screen with scrolling ticker
- Procedural arcade-style trophy animation
- Optimized for Raspberry Pi headless OS

---

## 🎮 Controls

### Menu
- ↑ / ↓ → Navigate menu
- ENTER → Select
- ESC → Quit

### Custom time
- ← / → → Select field (HH / MM / SS)
- ↑ / ↓ → Adjust value
- ENTER → Confirm

### Timer
- ENTER → Start
- ESC → Exit program

---

## 🖥️ Display Modes

### Countdown states:
- White → Normal time
- Orange → Last 10 minutes
- Red → Final minute (flashing)

### Victory mode:
- Drawn trophy
- Flashing 00:00:00
- Scrolling thank-you ticker

---

## ⚙️ Requirements

- Raspberry Pi 3B+ / 4 / 5
- Raspberry Pi OS (Lite or Full)
- HDMI display
- Keyboard (USB or wireless)
- Python 3.9+

---

## 📦 Dependencies

Install system packages:

```bash
sudo apt update
sudo apt install -y python3 python3-pygame
````

Optional (better performance on Pi):

```bash
sudo apt install -y xserver-xorg xinit
```

---

## 📁 Project Setup

Create a folder:

```bash
mkdir countdown-timer
cd countdown-timer
```

Save your script as:

```
countdown.py
```

---

## 🚀 Running the Program

### Option 1: Direct launch (desktop mode)

```bash
python3 countdown.py
```

---

### Option 2: Headless kiosk boot (recommended)

Edit autostart:

```bash
sudo nano /etc/rc.local
```

Add before `exit 0`:

```bash
python3 /home/pi/countdown-timer/countdown.py &
```

---

### Option 3: Autostart via systemd (best practice)

Create service:

```bash
sudo nano /etc/systemd/system/countdown.service
```

Paste:

```ini
[Unit]
Description=Countdown Timer
After=graphical.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/countdown-timer/countdown.py
Restart=always
User=pi
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
```

Enable it:

```bash
sudo systemctl enable countdown.service
sudo systemctl start countdown.service
```

---

## 🧠 Performance Notes (Raspberry Pi 3B+)

Recommended settings:

* Use HDMI resolution 1024x768 or 720p for smoother performance
* Avoid running other heavy desktop apps
* Disable screensaver:

```bash
xset s off
xset -dpms
xset s noblank
```

---

## 🏁 Behavior Summary

### Start Flow:

Menu → Time Setup → Preview → Countdown

### End Flow:

00:00:00 → Flashing mode → Victory ticker loop

---

## ❤️ Purpose

Designed for:

* Charity walking events
* Public event countdown displays
* Fundraising awareness screens
* Stadium / hall HDMI displays

---

## 📜 License

Free to use for non-commercial charity and public events.


