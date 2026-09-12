#!/usr/bin/env python3
"""Neon Slots — three-reel casino machine (shape symbols, no emoji fonts)."""

import random
import sys

import pygame

W, H = 800, 640
BG = (18, 8, 36)
PINK = (255, 70, 160)
CYAN = (40, 230, 255)
GOLD = (255, 210, 60)
WHITE = (255, 255, 255)
PURPLE = (86, 40, 160)
NAVY = (20, 20, 28)

SYMBOLS = [
    ("CHERRY", (255, 70, 90), 4),
    ("LEMON", (255, 220, 60), 5),
    ("BELL", (255, 190, 50), 8),
    ("STAR", (255, 240, 140), 10),
    ("GEM", (80, 220, 255), 15),
    ("SEVEN", (255, 60, 80), 25),
]


def payout(reels, bet):
    names = [r[0] for r in reels]
    if names[0] == names[1] == names[2]:
        return bet * reels[0][2]
    if names[0] == names[1] or names[1] == names[2] or names[0] == names[2]:
        return bet
    return 0


def draw_symbol(surf, item, box, font):
    name, color, _ = item
    pygame.draw.rect(surf, (30, 16, 60), box, border_radius=16)
    pygame.draw.rect(surf, CYAN, box, 3, border_radius=16)
    pygame.draw.circle(surf, color, box.center, 38)
    pygame.draw.circle(surf, WHITE, box.center, 38, 2)
    t = font.render(name, True, WHITE)
    surf.blit(t, t.get_rect(center=(box.centerx, box.bottom - 28)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Slots — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    small = pygame.font.SysFont("consolas", 16, bold=True)
    big = pygame.font.SysFont("consolas", 40, bold=True)

    bank, bet = 200, 5
    reels = [SYMBOLS[0], SYMBOLS[1], SYMBOLS[2]]
    spinning = 0
    msg = "Click SPIN"
    last_win = 0

    spin_btn = pygame.Rect(300, 520, 200, 56)
    minus = pygame.Rect(80, 520, 80, 56)
    plus = pygame.Rect(640, 520, 80, 56)

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and spinning == 0:
                if spin_btn.collidepoint(e.pos) and bank >= bet:
                    bank -= bet
                    spinning = 28
                    msg = "Good luck..."
                    last_win = 0
                elif minus.collidepoint(e.pos):
                    bet = max(1, bet - 1)
                elif plus.collidepoint(e.pos):
                    bet = min(25, min(max(1, bank), bet + 1))

        if spinning:
            reels = [random.choice(SYMBOLS) for _ in range(3)]
            spinning -= 1
            if spinning == 0:
                last_win = payout(reels, bet)
                bank += last_win
                msg = f"WIN ${last_win}!" if last_win else "No luck — spin again"

        screen.fill(BG)
        pygame.draw.rect(screen, PURPLE, (70, 70, 660, 380), border_radius=24)
        pygame.draw.rect(screen, GOLD, (70, 70, 660, 380), 4, border_radius=24)
        title = big.render("NEON SLOTS", True, PINK)
        screen.blit(title, title.get_rect(center=(W // 2, 40)))
        for i, item in enumerate(reels):
            box = pygame.Rect(110 + i * 200, 140, 170, 220)
            draw_symbol(screen, item, box, small)

        screen.blit(font.render(f"Bank ${bank}    Bet ${bet}    Last win ${last_win}", True, GOLD), (80, 470))
        screen.blit(font.render(msg, True, CYAN), (80, 492))

        pygame.draw.rect(screen, PINK, spin_btn, border_radius=10)
        t = font.render("SPIN", True, WHITE)
        screen.blit(t, t.get_rect(center=spin_btn.center))
        pygame.draw.rect(screen, GOLD, minus, border_radius=10)
        pygame.draw.rect(screen, GOLD, plus, border_radius=10)
        t = font.render("-BET", True, NAVY)
        screen.blit(t, t.get_rect(center=minus.center))
        t = font.render("+BET", True, NAVY)
        screen.blit(t, t.get_rect(center=plus.center))
        pygame.display.flip()


if __name__ == "__main__":
    main()
