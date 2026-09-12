#!/usr/bin/env python3
"""Street Craps — colourful dice table."""

import random
import sys

import pygame

W, H = 920, 600
FELT = (16, 102, 48)
GOLD = (230, 190, 60)
WHITE = (250, 250, 250)
RED = (200, 40, 40)
NAVY = (16, 24, 40)


def roll():
    return random.randint(1, 6), random.randint(1, 6)


def pip_positions(n):
    c = (0.5, 0.5)
    spots = {
        1: [c],
        2: [(0.28, 0.28), (0.72, 0.72)],
        3: [(0.28, 0.28), c, (0.72, 0.72)],
        4: [(0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72)],
        5: [(0.28, 0.28), (0.72, 0.28), c, (0.28, 0.72), (0.72, 0.72)],
        6: [(0.28, 0.25), (0.72, 0.25), (0.28, 0.5), (0.72, 0.5), (0.28, 0.75), (0.72, 0.75)],
    }
    return spots[n]


def draw_die(surf, value, x, y, size=110):
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surf, WHITE, rect, border_radius=16)
    pygame.draw.rect(surf, GOLD, rect, 3, border_radius=16)
    for px, py in pip_positions(value):
        pygame.draw.circle(surf, NAVY, (int(x + px * size), int(y + py * size)), size // 12)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Street Craps — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 34, bold=True)

    bank, bet = 300, 10
    point = None
    dice = (1, 1)
    msg = "Come-out roll: 7 or 11 win, 2/3/12 lose"
    rolling = 0

    btn = pygame.Rect(360, 500, 200, 54)
    minus = pygame.Rect(80, 500, 90, 54)
    plus = pygame.Rect(750, 500, 90, 54)

    def resolve(a, b):
        nonlocal point, bank, msg
        s = a + b
        if point is None:
            if s in (7, 11):
                bank += bet
                msg = f"{s} — natural! You win ${bet}"
            elif s in (2, 3, 12):
                bank -= bet
                msg = f"{s} — craps. Lost ${bet}"
            else:
                point = s
                msg = f"Point is {point}. Roll it again before a 7."
        else:
            if s == point:
                bank += bet
                msg = f"Hit the point {point}! Won ${bet}"
                point = None
            elif s == 7:
                bank -= bet
                msg = "Seven-out. Lost the point."
                point = None
            else:
                msg = f"Rolled {s}. Point remains {point}."

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and rolling == 0:
                if btn.collidepoint(e.pos) and bank >= bet:
                    rolling = 18
                elif minus.collidepoint(e.pos):
                    bet = max(5, bet - 5)
                elif plus.collidepoint(e.pos):
                    bet = min(bank, bet + 5)

        if rolling:
            dice = roll()
            rolling -= 1
            if rolling == 0:
                resolve(*dice)

        screen.fill(NAVY)
        pygame.draw.rect(screen, FELT, (40, 40, 840, 420), border_radius=20)
        pygame.draw.rect(screen, GOLD, (40, 40, 840, 420), 4, border_radius=20)
        screen.blit(big.render("STREET CRAPS", True, GOLD), (320, 60))
        screen.blit(font.render(f"Bank ${bank}   Bet ${bet}   Point {point or '-'}", True, WHITE), (70, 120))
        screen.blit(font.render(msg, True, GOLD), (70, 160))
        draw_die(screen, dice[0], 280, 230)
        draw_die(screen, dice[1], 520, 230)
        total = dice[0] + dice[1]
        screen.blit(big.render(str(total), True, WHITE), (440, 360))

        pygame.draw.rect(screen, RED, btn, border_radius=10)
        screen.blit(font.render("ROLL", True, WHITE), font.render("ROLL", True, WHITE).get_rect(center=btn.center))
        pygame.draw.rect(screen, GOLD, minus, border_radius=10)
        pygame.draw.rect(screen, GOLD, plus, border_radius=10)
        screen.blit(font.render("-5", True, NAVY), font.render("-5", True, NAVY).get_rect(center=minus.center))
        screen.blit(font.render("+5", True, NAVY), font.render("+5", True, NAVY).get_rect(center=plus.center))
        pygame.display.flip()


if __name__ == "__main__":
    main()
