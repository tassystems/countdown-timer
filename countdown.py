import pygame
import sys
import math
import os

# =====================================================
# RASPBERRY PI HEADLESS & GRAPHICS OPTIMIZATION
# =====================================================
os.environ["SDL_FBDEV"] = "/dev/fb0"
os.environ["SDL_NOMOUSE"] = "1" 

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

if WIDTH <= 0 or HEIGHT <= 0:
    WIDTH, HEIGHT = 1024, 768

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.mouse.set_visible(False)
pygame.display.set_caption("24U Countdown")

clock = pygame.time.Clock()

# =====================================================
# COLORS & THEME
# =====================================================
BG = (8, 10, 20)
WHITE = (245, 245, 250)
GRAY = (100, 110, 130)

CYAN = (0, 210, 255)
ORANGE = (255, 140, 0)
RED = (255, 50, 70)
GOLD = (255, 200, 50)
GOLD_LIGHT = (255, 235, 150)
GOLD_DARK = (190, 140, 20)

# =====================================================
# DUAL FONTS LOADING & TARGET WIDTH INITIALIZATION
# =====================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TIMER_FONT_PATH = os.path.join(SCRIPT_DIR, "timer_font.otf")
TEXT_FONT_PATH = os.path.join(SCRIPT_DIR, "text_font.ttf")

# Fixed ui sizing metrics
TITLE_SIZE = max(28, int(HEIGHT * 0.055))
MENU_SIZE = max(22, int(HEIGHT * 0.042))
SMALL_SIZE = max(8, int(HEIGHT * 0.014)) 

# Target width calculation (90% of screen width)
TARGET_TIMER_WIDTH = int(WIDTH * 0.80)

def load_scaled_timer_font(font_path, target_width):
    """Iteratively finds the exact font size needed to fill the target pixel width."""
    test_size = 20
    sample_text = "00:00:00"
    
    # Quick rough approximation step to limit loop passes
    if font_path and os.path.exists(font_path):
        font = pygame.font.Font(font_path, test_size)
    else:
        font = pygame.font.SysFont("monospace", test_size, bold=True)
        
    current_w = font.size(sample_text)[0]
    estimated_size = int(test_size * (target_width / current_w))
    
    # Exact calibration loop
    for size in range(estimated_size + 5, estimated_size - 15, -1):
        if font_path and os.path.exists(font_path):
            test_font = pygame.font.Font(font_path, size)
        else:
            test_font = pygame.font.SysFont("monospace", size, bold=True)
            
        if test_font.size(sample_text)[0] <= target_width:
            return test_font
            
    return test_font

# Initialize fonts safely
TIMER_FONT = load_scaled_timer_font(TIMER_FONT_PATH, TARGET_TIMER_WIDTH)

if os.path.exists(TEXT_FONT_PATH):
    TITLE_FONT = pygame.font.Font(TEXT_FONT_PATH, TITLE_SIZE)
    MENU_FONT = pygame.font.Font(TEXT_FONT_PATH, MENU_SIZE)
    SMALL_FONT = pygame.font.Font(TEXT_FONT_PATH, SMALL_SIZE)
else:
    TITLE_FONT = pygame.font.SysFont("monospace", TITLE_SIZE, bold=True)
    MENU_FONT = pygame.font.SysFont("monospace", MENU_SIZE, bold=True)
    SMALL_FONT = pygame.font.SysFont("monospace", SMALL_SIZE, bold=True)

# Total event baseline (24 Hours in seconds = 86,400)
BASELINE_24H_SECS = 24 * 60 * 60

# =====================================================
# HELPERS
# =====================================================
def format_time(s):
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02}:{m:02}:{sec:02}"


def pulse(speed=4):
    return (math.sin(pygame.time.get_ticks() / 1000 * speed) + 1) / 2


def timer_color(seconds):
    if seconds <= 60: return RED
    elif seconds <= 600: return ORANGE
    return WHITE


def center_text(font, text, color, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))


def draw_bg():
    screen.fill(BG)


def check_global_quit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()

# =====================================================
# PROCEDURAL ANIMATIONS (TROPHY & MICRO LED)
# =====================================================
def draw_trophy(cx, cy, scale=1.0):
    w = lambda val: int(val * scale)
    
    bowl_poly = [
        (cx - w(60), cy - w(50)), (cx + w(60), cy - w(50)),
        (cx + w(55), cy + w(10)), (cx + w(30), cy + w(50)),
        (cx - w(30), cy + w(50)), (cx - w(55), cy + w(10))
    ]
    stem_poly = [
        (cx - w(12), cy + w(50)), (cx + w(12), cy + w(50)),
        (cx + w(8), cy + w(85)), (cx - w(8), cy + w(85))
    ]
    base_poly = [
        (cx - w(45), cy + w(85)), (cx + w(45), cy + w(85)),
        (cx + w(55), cy + w(110)), (cx - w(55), cy + w(110))
    ]

    pygame.draw.polygon(screen, GOLD, bowl_poly)
    pygame.draw.polygon(screen, GOLD_DARK, stem_poly)
    pygame.draw.polygon(screen, GOLD_DARK, base_poly)
    pygame.draw.ellipse(screen, GOLD_LIGHT, (cx - w(60), cy - w(60), w(120), w(20)))
    pygame.draw.arc(screen, GOLD, (cx - w(85), cy - w(40), w(40), w(60)), math.pi/2, 3*math.pi/2, w(8))
    pygame.draw.arc(screen, GOLD, (cx + w(45), cy - w(40), w(40), w(60)), -math.pi/2, math.pi/2, w(8))


def draw_mini_led(cx, cy, scale=1.0):
    base_radius = int(4.5 * scale)
    pulse_mod = pulse(5)
    glow_intensity = int(110 + (145 * pulse_mod))
    
    led_color = (0, glow_intensity, int(glow_intensity * 0.2))
    border_color = (25, 35, 50)
    
    pygame.draw.circle(screen, border_color, (cx, cy), base_radius + max(1, int(1.5 * scale)))
    pygame.draw.circle(screen, led_color, (cx, cy), base_radius)
    pygame.draw.circle(screen, (210, 255, 220), (cx - int(1 * scale), cy - int(1 * scale)), int(1.5 * scale))

# =====================================================
# INTERFACE STATES
# =====================================================
def menu():
    options = ["START 24H", "TIJD AANPASSEN", "EXIT"]
    selected = 0

    while True:
        draw_bg()
        center_text(TITLE_FONT, "24U TIMER", CYAN, int(HEIGHT * 0.1))

        for i, opt in enumerate(options):
            color = GOLD if i == selected else WHITE
            prefix = "> " if i == selected else "  "
            txt = MENU_FONT.render(prefix + opt, True, color)
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, int(HEIGHT * 0.35) + i * int(HEIGHT * 0.09)))

        center_text(SMALL_FONT, "PIJLTJES: NAVIGEER  |  ENTER: KIES", GRAY, int(HEIGHT * 0.85))
        pygame.display.flip()

        for e in pygame.event.get():
            check_global_quit(e)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    if selected == 0: return BASELINE_24H_SECS
                    if selected == 1: return custom_time()
                    pygame.quit()
                    sys.exit()
        clock.tick(60)


def custom_time():
    h, m, s = 24, 0, 0
    selected = 0 

    while True:
        draw_bg()
        center_text(TITLE_FONT, "TIJD INSTELLEN (HH:MM:SS)", GRAY, int(HEIGHT * 0.1))

        h_color = GOLD if selected == 0 else WHITE
        m_color = GOLD if selected == 1 else WHITE
        s_color = GOLD if selected == 2 else WHITE

        h_surf = TIMER_FONT.render(f"{h:02}", True, h_color)
        colon1 = TIMER_FONT.render(":", True, WHITE)
        m_surf = TIMER_FONT.render(f"{m:02}", True, m_color)
        colon2 = TIMER_FONT.render(":", True, WHITE)
        s_surf = TIMER_FONT.render(f"{s:02}", True, s_color)

        total_width = h_surf.get_width() + colon1.get_width() + m_surf.get_width() + colon2.get_width() + s_surf.get_width()
        start_x = WIDTH // 2 - total_width // 2
        y_pos = HEIGHT // 2 - h_surf.get_height() // 2

        screen.blit(h_surf, (start_x, y_pos))
        start_x += h_surf.get_width()
        screen.blit(colon1, (start_x, y_pos))
        start_x += colon1.get_width()
        screen.blit(m_surf, (start_x, y_pos))
        start_x += m_surf.get_width()
        screen.blit(colon2, (start_x, y_pos))
        start_x += colon2.get_width()
        screen.blit(s_surf, (start_x, y_pos))

        hint = SMALL_FONT.render("LINKS/RECHTS: SELECTEER  |  OMHOOG/BENEDEN: AANPASSSEN  |  ENTER: START", True, GRAY)
        hint_y = int(HEIGHT * 0.85) if h_surf.get_height() + y_pos < int(HEIGHT * 0.8) else int(HEIGHT * 0.9)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, hint_y))

        pygame.display.flip()

        for e in pygame.event.get():
            check_global_quit(e)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT: selected = (selected - 1) % 3
                elif e.key == pygame.K_RIGHT: selected = (selected + 1) % 3
                elif e.key == pygame.K_UP:
                    if selected == 0: h = min(99, h + 1)
                    elif selected == 1: m = (m + 1) % 60
                    else: s = (s + 1) % 60
                elif e.key == pygame.K_DOWN:
                    if selected == 0: h = max(0, h - 1)
                    elif selected == 1: m = (m - 1) % 60
                    else: s = (s - 1) % 60
                elif e.key == pygame.K_RETURN:
                    return max(1, h * 3600 + m * 60 + s)
        clock.tick(60)


def wait_screen(seconds):
    while True:
        draw_bg()
        color = timer_color(seconds)

        txt = TIMER_FONT.render(format_time(seconds), True, color)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - txt.get_height() // 2))

        pulse_val = int(pulse(4) * 135)
        msg = SMALL_FONT.render("DRUK ENTER OM DE KLOK TE STARTEN", True, (120 + pulse_val, 180, 255))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, int(HEIGHT * 0.83)))

        pygame.display.flip()

        for e in pygame.event.get():
            check_global_quit(e)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
        clock.tick(60)


# =====================================================
# COUNTDOWN RUNTIME STATE
# =====================================================
def countdown(total_seconds):
    start_ticks = pygame.time.get_ticks()
    target_time_ms = total_seconds * 1000

    render_scale = HEIGHT / 768.0

    while True:
        elapsed_ms = pygame.time.get_ticks() - start_ticks
        remaining_ms = max(0, target_time_ms - elapsed_ms)
        seconds_left = math.ceil(remaining_ms / 1000)

        # Reverse progress evaluation tracking matching 24h milestone baseline targets
        secs_already_walked = BASELINE_24H_SECS - seconds_left
        pct_completed = (secs_already_walked / BASELINE_24H_SECS) * 100
        pct_completed = max(0.0, min(100.0, pct_completed))

        draw_bg()
        color = timer_color(seconds_left)

        # Primary Clock Render (Dynamically takes exactly 90% horizontal screen footprint)
        txt = TIMER_FONT.render(format_time(seconds_left), True, color)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - txt.get_height() // 2))

        # --- MICRO STATUS PANEL (SMALL_SIZE) ---
        led_x = int(WIDTH * 0.04)
        led_y = int(HEIGHT * 0.96)
        draw_mini_led(led_x, led_y, scale=render_scale)

        status_surf = SMALL_FONT.render("Running...", True, GRAY)
        screen.blit(status_surf, (led_x + int(12 * render_scale), led_y - status_surf.get_height() // 2))

        pct_str = f"{pct_completed:.2f}%"
        pct_surf = SMALL_FONT.render(pct_str, True, GRAY)
        screen.blit(pct_surf, (WIDTH - int(WIDTH * 0.04) - pct_surf.get_width(), led_y - pct_surf.get_height() // 2))

        if seconds_left <= 3600 and seconds_left > 600:
            if int(pygame.time.get_ticks() / 300) % 2 == 0:
                warn = MENU_FONT.render("LAATSTE UUR INGEZET...", True, GRAY)
                screen.blit(warn, (WIDTH // 2 - warn.get_width() // 2, int(HEIGHT * 0.83)))
        
        if seconds_left <= 600 and seconds_left > 60:
            if int(pygame.time.get_ticks() / 300) % 2 == 0:
                warn = MENU_FONT.render("LAATSTE 10 MINUTEN...", True, ORANGE)
                screen.blit(warn, (WIDTH // 2 - warn.get_width() // 2, int(HEIGHT * 0.83)))

        if seconds_left <= 60:
            if int(pygame.time.get_ticks() / 300) % 2 == 0:
                warn = MENU_FONT.render("DE LAATSTE MINUUT...", True, RED)
                screen.blit(warn, (WIDTH // 2 - warn.get_width() // 2, int(HEIGHT * 0.83)))

        pygame.display.flip()

        if remaining_ms <= 0:
            break

        for e in pygame.event.get():
            check_global_quit(e)

        clock.tick(60)

    victory()


def victory():
    ticker_x = WIDTH
    msg = "BEDANKT VOOR JULLIE STEUN TIJDENS DEZE 24U!   "
    txt = MENU_FONT.render(msg, True, WHITE)
    
    trophy_scale = (HEIGHT / 768) * 1.2

    while True:
        draw_bg()
        center_text(TITLE_FONT, "PROFICIAT!!!", GOLD, int(HEIGHT * 0.08))

        draw_trophy(WIDTH // 2, int(HEIGHT * 0.35), scale=trophy_scale)

        if int(pygame.time.get_ticks() / 400) % 2 == 0:
            zero_txt = TIMER_FONT.render("00:00:00", True, GOLD_LIGHT)
            screen.blit(zero_txt, (WIDTH // 2 - zero_txt.get_width() // 2, int(HEIGHT * (2/3)) - zero_txt.get_height() // 2))

        screen.blit(txt, (ticker_x, int(HEIGHT * 0.90)))
        ticker_x -= 3 

        if ticker_x < -txt.get_width():
            ticker_x = WIDTH

        pygame.display.flip()

        for e in pygame.event.get():
            check_global_quit(e)
        clock.tick(60)


# =====================================================
# MAIN RUNTIME ENTRY
# =====================================================
while True:
    total = menu()
    wait_screen(total)
    countdown(total)