# main.py
from pygame import *
import math
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "100, 70"

# Initializing modules
init()
font.init()

display.set_caption("Virtual Projectile Motion Lab") 

# Constants
size = width, height = 1200, 650
screen = display.set_mode(size)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
myClock = time.Clock()


# Intializing stuff
mb = [0, 0, 0]
mx, my = 0, 0

# Constant stuff
ground = Rect(0, 550, width - 300, height-550)
menuRect = Rect(width - 300, 0, 300, height)
startRect = Rect(920, 560, 260, 50)

# Text
arial16 = font.SysFont("Arial", 16)
arial24 = font.SysFont("Arial", 24)
arial30 = font.SysFont("Arial", 30)
arial45 = font.SysFont("Arial", 45)

# Projectile buttons
entries = [Rect(1080, 74 + i*45, 100, 24) for i in range(5)]
entries_text = ["5", "5", "45", "9.81", "1"]

# Time
timeRect = Rect(705, 20, 150, 70)

# Info Rects
info_rects = [Rect(915, 340, 120, 20), Rect(1065, 340, 120, 20), Rect(915, 390, 120, 20), Rect(1065, 390, 120, 20),
              Rect(915, 440, 120, 20), Rect(1065, 440, 120, 20), Rect(915, 490, 120, 20), Rect(1065, 490, 120, 20)]

# Ball
b = [40, 300]
bv = [0, 0]

oldx, oldy = 0, 0
dx = 50.6
max_height = 5.63


def get_buttons():
    """
    Get all user inputs.
    """
    keys = key.get_pressed()

    # Mouse info
    global mb
    mb = mouse.get_pressed()
    global mx, my
    mx, my = mouse.get_pos()


def get_scale(h, vi, theta, g):
    global dx, max_height
    dx = (vi*math.sin(math.radians(theta)) + ((vi*math.sin(math.radians(theta))) ** 2 + 2*g*h) ** 0.5) * (vi*math.cos(math.radians(theta))) / g

    max_height = (vi * math.sin(math.radians(theta))) ** 2 / (2*g) + h
    if 0 < dx <= 7:
        out = 1
    elif 7 < dx <= 14:
        out = 2
    elif 14 < dx <= 35:
        out = 5
    elif 35 < dx <= 70:
        out = 10
    elif 70 < dx <= 140:
        out = 20
    elif 140 < dx <= 350:
        out = 50
    elif 350 < dx <= 700:
        out = 100
    elif 700 < dx <= 1400:
        out = 200
    else:
        out = 500

    if 0 < max_height <= 5:
        out1 = 1
    elif 5 < max_height <= 10:
        out1 = 2
    elif 10 < max_height <= 25:
        out1 = 5
    elif 25 < max_height <= 50:
        out1 = 10
    elif 50 < max_height <= 100:
        out1 = 20
    elif 100 < max_height <= 250:
        out1 = 50
    elif 250 < max_height <= 500:
        out1 = 100
    elif 500 < max_height <= 1000:
        out1 = 200
    else:
        out1 = 500

    return max(out, out1)


def data(scale, h, vi, theta, g, m, screen):
    vx = vi * math.cos(math.radians(theta))
    vx_text = arial16.render(str(round(vx, 2)), True, RED)
    screen.blit(vx_text, (975 - vx_text.get_width() // 2, 392))
    vy = vi * math.sin(math.radians(theta)) - g * (passed_time / 1000)
    vy_text = arial16.render(str(round(vy, 2)), True, RED)
    screen.blit(vy_text, (1125 - vy_text.get_width() // 2, 392))
    dx = (b[0] - 40) * scale / 100
    dx_text = arial16.render(str(round(dx, 2)), True, RED)
    screen.blit(dx_text, (975 - dx_text.get_width() // 2, 342))
    dy = (550 - b[1]) * scale / 100
    dy_text = arial16.render(str(round(dy, 2)), True, RED)
    screen.blit(dy_text, (1125 - dy_text.get_width() // 2, 342))
    vtot = (vx ** 2 + vy ** 2) ** 0.5
    vtot_text = arial16.render(str(round(vtot, 2)), True, RED)
    screen.blit(vtot_text, (975 - vtot_text.get_width() // 2, 442))
    angle = math.degrees(math.atan2(vy, vx))
    angle_text = arial16.render(str(round(angle, 2)), True, RED)
    screen.blit(angle_text, (1125 - angle_text.get_width() // 2, 442))
    kinetic_energy = 0.5 * m * vtot ** 2
    kinetic_energy_text = arial16.render(str(round(kinetic_energy, 2)), True, RED)
    screen.blit(kinetic_energy_text, (975 - kinetic_energy_text.get_width() // 2, 492))
    g_energy = m * g * dy
    g_energy_text = arial16.render(str(round(g_energy, 2)), True, RED)
    screen.blit(g_energy_text, (1125 - g_energy_text.get_width() // 2, 492))


def update_p(screen, scale, active, time, is_launching):
    screen.fill((216, 220, 55))

    draw.rect(screen, (190, 225, 245), menuRect)  # Menu rect
    draw.rect(screen, (222, 184, 135), ground)  # Ground rect

    # Border
    draw.line(screen, BLACK, (0, 0), (width, 0), 2)
    draw.line(screen, BLACK, (width-2, 0), (width-2, height), 2)
    draw.line(screen, BLACK, (width, height-2), (0, height-2), 2)
    draw.line(screen, BLACK, (0, height), (0, 0), 2)
    draw.line(screen, BLACK, (width-300, height), (width-300, 0), 2)
    draw.line(screen, BLACK, (900, 300), (1200, 300), 2)

    # x axis
    draw.line(screen, BLACK, (20, 550), (width - 320, 550), 3)
    draw.line(screen, BLACK, (width - 330, 540), (width - 320, 550), 3)
    draw.line(screen, BLACK, (width - 330, 560), (width - 320, 550), 3)
    for i in range(41):
        if i % 5 == 4:
            draw.line(screen, BLACK, (60 + 20 * i, 540), (60 + 20 * i, 560), 2)
            x_num = arial16.render(str((i + 1) // 5 * scale), True, BLACK)
            screen.blit(x_num, (61 + 20*i - x_num.get_width() // 2, 560))
        else:
            draw.line(screen, BLACK, (60 + 20 * i, 545), (60 + 20 * i, 555))
    screen.blit(arial16.render("X (m)", True, BLACK), (850, 520))

    # y axis
    draw.line(screen, BLACK, (40, 15), (40, 570), 3)
    draw.line(screen, BLACK, (30, 25), (40, 15), 3)
    draw.line(screen, BLACK, (50, 25), (40, 15), 3)
    for i in range(26):
        if i % 5 == 4:
            draw.line(screen, BLACK, (30, 530 - 20*i), (50, 530 - 20*i), 2)
            x_num = arial16.render(str((i + 1) // 5 * scale), True, BLACK)
            screen.blit(x_num, (5, 530 - 20*i - x_num.get_height() // 2))
        else:
            draw.line(screen, BLACK, (35, 530 - 20*i), (45, 530 - 20*i))
    screen.blit(arial16.render("Y (m)", True, BLACK), (55, 15))

    screen.blit(arial30.render("Projectile Motion", True, BLACK), (960, 15))
    screen.blit(arial24.render("Initial Height (m)", True, BLACK), (915, 70))
    screen.blit(arial24.render("Initial Speed (m/s)", True, BLACK), (915, 115))
    screen.blit(arial24.render("Angle (°)", True, BLACK), (915, 160))
    screen.blit(arial24.render("Gravity (m/s²)", True, BLACK), (915, 205))
    screen.blit(arial24.render("Mass (kg)", True, BLACK), (915, 250))

    for i in range(len(entries)):
        draw.rect(screen, WHITE, entries[i])
        if entries[i].collidepoint(mx, my) and i != active:
            draw.rect(screen, (100, 100, 100), entries[i], 1)
        if i == active:
            draw.rect(screen, BLUE, entries[i], 1)
            if t % 60 <= 30:
                draw.rect(screen, BLACK, (arial16.render(entries_text[i], True, BLACK).get_width() + 1083, 76 + i * 45, 2, 18))

        screen.blit(arial16.render(entries_text[i], True, BLACK), (1083, 76 + i*45))

    draw.rect(screen, GREEN, startRect)
    launch_text = arial30.render("Launch!", True, BLACK)
    screen.blit(launch_text, (1050 - launch_text.get_width() // 2, 565))

    if startRect.collidepoint(mx, my) and not is_launching:
        draw.rect(screen, RED, startRect, 5)

    draw.rect(screen, (200, 200, 200), timeRect)
    draw.rect(screen, BLACK, timeRect, 2)

    seconds = time // 1000
    mili = time % 1000
    clock = str(seconds) + "." + str(mili)

    screen.blit(arial45.render(clock, True, RED), (715, 27))

    # Info
    for r in info_rects:
        draw.rect(screen, WHITE, r)

    screen.blit(arial16.render("Horizontal Position (m)", True, BLACK), (915, 320))
    screen.blit(arial16.render("Vertical Position (m)", True, BLACK), (1065, 320))
    screen.blit(arial16.render("Horizontal Velocity (m/s)", True, BLACK), (915, 370))
    screen.blit(arial16.render("Vertical Velocity (m/s)", True, BLACK), (1065, 370))
    screen.blit(arial16.render("Total Speed (m/s)", True, BLACK), (915, 420))
    screen.blit(arial16.render("Angle (°)", True, BLACK), (1065, 420))
    screen.blit(arial16.render("Kinetic Energy (J)", True, BLACK), (915, 470))
    screen.blit(arial16.render("Potential Energy (J)", True, BLACK), (1065, 470))

    data(scale, h, vi, theta, g, m, screen)

    # Ball
    draw.circle(screen, RED, (int(b[0]), int(b[1])), 10)

    display.flip()


def launch(scale, h, vi, theta, g):
    b[0] += (bv[0] * 100 / 60 / scale)
    b[1] += (bv[1] * 100 / 60 / scale)
    bv[1] += (g / 60)


def gameloop(screen):
    global active
    global h, vi, theta, g, m, t
    active = None
    running = True
    is_launching = False
    scale = 1
    h = 0
    vi = 0
    theta = 0
    g = 9.81
    m = 0
    t = 0
    global time_started, passed_time
    passed_time = 0
    time_started = False
    start_time = 0
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            if evnt.type == MOUSEBUTTONDOWN:
                for i in range(len(entries)):
                    if entries[i].collidepoint(mx, my):
                        # If input box is clicked toggle its activeness
                        if active == i:
                            active = None
                        else:
                            active = i
                        break
                    else:
                        # If screen is clicked not on input box toggle it off
                        active = None

            if evnt.type == KEYDOWN:
                if active is not None:
                    # Dealing with the inputs of the box
                    if evnt.key == K_RETURN or evnt.key == K_ESCAPE:
                        # Enter exits the input box
                        active = None
                    elif evnt.key == K_BACKSPACE:  # Backspacing the text
                        entries_text[active] = entries_text[active][:-1]
                    else:
                        if len(entries_text[active]) < 8:  # Adding the pressed unicode character to the text
                            if "0" <= evnt.unicode <= "9" or (evnt.unicode == "." and "." not in entries_text[active]):
                                entries_text[active] += evnt.unicode
                            if active == 2 and evnt.unicode == "-" and entries_text[active] == "":
                                entries_text[active] += evnt.unicode
                        else:
                            if "0" <= evnt.unicode <= "9" or (evnt.unicode == "." and "." not in entries_text[active]):
                                entries_text[active] = entries_text[active][:-1] + evnt.unicode
        t += 1
        if not is_launching and startRect.collidepoint(mx, my) and mb[0]:
            is_launching = True
            values = [0, 0, 0, 0, 0]
            time_started = True
            start_time = time.get_ticks()
            passed_time = 0
            for i in range(len(entries_text)):
                try:
                    values[i] = float(entries_text[i])
                    if values[i] < 0 and i != 2:
                        values[i] = 0
                        entries_text[i] = "0"
                    if i == 0 and values[i] > 1000:
                        values[i] = 1000
                        entries_text[i] = "1000"
                    elif i == 1 and values[i] > 250:
                        values[i] = 250
                        entries_text[i] = "250"
                    elif i == 2:
                        if values[i] < -90:
                            values[i] = -90
                            entries_text[i] = "-90"
                        elif 90 < values[i]:
                            values[i] = 90
                            entries_text[i] = "-90"
                    elif i == 3:
                        if values[i] > 100:
                            values[i] = 100
                            entries_text[i] = "100"
                except ValueError:
                    values[i] = 0
                    entries_text[i] = "0"

            h, vi, theta, g, m = values
            scale = get_scale(h, vi, theta, g)
            b[0] = 40
            b[1] = 550 - ((100 * h) / scale)
            bv[0] = vi * math.cos(math.radians(theta))
            bv[1] = -vi * math.sin(math.radians(theta))

        if is_launching:
            launch(scale, h, vi, theta, g)
            if b[1] >= 550:
                b[1] = 550
                is_launching = False
                time_started = False

        if time_started:
            passed_time = time.get_ticks() - start_time
        update_p(screen, scale, active, passed_time, is_launching)

        get_buttons()

        myClock.tick(60)


page = "game"
while page != "exit":
    if page == "game":
        page = gameloop(screen)

quit()
