# Walk for a Cause — Countdown Timer
## Headless Raspberry Pi 3B+ Setup Guide (pygame / framebuffer)

---

### Why pygame / headless?
- Runs directly on the framebuffer — **no desktop, no Xorg, no browser needed**
- Boots in ~15 seconds instead of ~45 seconds with a full desktop
- Uses less RAM and CPU, leaving more headroom on the Pi 3B+
- Full control over every pixel, perfectly centred at any resolution

---

### 1. Flash a headless OS

Use **Raspberry Pi OS Lite (64-bit)** — no desktop environment.
Flash with Raspberry Pi Imager, enable SSH in settings if you want to configure remotely.

---

### 2. Install dependencies

SSH in or connect a keyboard, then:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pygame fonts-freefont-ttf python3-pip
```

That's it — `python3-pygame` on Raspberry Pi OS Lite already includes
SDL2 with framebuffer support. No X11 needed.

---

### 3. Copy the script

```bash
# From your PC:
scp countdown_timer.py pi@raspberrypi.local:/home/pi/

# Or via USB stick — mount and copy manually
```

---

### 4. Test it manually

```bash
python3 /home/pi/countdown_timer.py
```

You should see the menu on the HDMI display immediately.

**Controls:**
| Key | Action |
|-----|--------|
| ← → | Switch between Hours / Minutes / Seconds |
| ↑ ↓ | Increase / Decrease selected value |
| R | Reset to 24:00:00 |
| Enter / Space | Confirm on menu — Start on timer screen |
| Esc | Back to menu (from timer) |
| Any key / click | Exit (from finished screen) |

---

### 5. Auto-launch on boot

Create a systemd service so the timer starts automatically when the Pi boots:

```bash
sudo nano /etc/systemd/system/countdown.service
```

Paste this content:

```ini
[Unit]
Description=Walk for a Cause Countdown Timer
After=multi-user.target

[Service]
User=pi
Group=pi
Environment=SDL_VIDEODRIVER=fbcon
Environment=SDL_FBDEV=/dev/fb0
Environment=SDL_AUDIODRIVER=dummy
ExecStart=/usr/bin/python3 /home/pi/countdown_timer.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable countdown.service
sudo systemctl start countdown.service
```

Check status:
```bash
sudo systemctl status countdown.service
```

---

### 6. HDMI resolution

If your TV shows a wrong resolution or black bars, force 1080p in `/boot/config.txt`:

```bash
sudo nano /boot/config.txt
```

Add or uncomment:
```
hdmi_force_hotplug=1
hdmi_group=1
hdmi_mode=16        # 1080p 60Hz
# hdmi_mode=4       # 720p 60Hz (use this for older TVs)
```

Reboot after changes.

---

### 7. Prevent screen blanking

The Pi console blanks the screen after 10 minutes. Disable it:

```bash
sudo nano /boot/cmdline.txt
```

Add to the end of the existing single line (do not add a new line):
```
consoleblank=0
```

---

### 8. Permissions for framebuffer

The `pi` user normally has framebuffer access, but if you get a permission error:
```bash
sudo usermod -aG video pi
```
Then reboot.

---

### Troubleshooting

| Problem | Fix |
|---------|-----|
| Black screen | Check `hdmi_force_hotplug=1` in `/boot/config.txt` |
| Font looks wrong | Run `sudo apt install fonts-freefont-ttf` |
| `No module named pygame` | Run `sudo apt install python3-pygame` |
| Screen goes blank mid-event | Add `consoleblank=0` to cmdline.txt |
| Wrong resolution | Set `hdmi_mode` in `/boot/config.txt` |
