#!/usr/bin/env python3
"""Memory Match — colourful pair-matching card game."""

import random
import sys
import time

import pygame

W, H = 900, 640
COLS, ROWS = 6, 4
PAD_X, PAD_Y = 30, 90
CW, CH = 130, 120

PALETTE = [
    ((255, 80, 80), "RUBY"),
    ((255, 160, 40), "AMBER"),
    ((255, 220, 50), "GOLD"),
    ((80, 220, 90), "JADE"),
    ((50, 210, 210), "TEAL"),
    ((70, 130, 255), "AZURE"),
    ((170, 90, 255), "VIOLET"),
    ((255, 90, 180), "PINK"),
    ((240, 240, 240), "PEARL"),
    ((255, 110, 70), "CORAL"),
    ((120, 255, 180), "MINT"),
    ((90, 90, 110), "STEEL"),
]


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Memory Match — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    labelf = pygame.font.SysFont("consolas", 16, bold=True)
    big = pygame.font.SysFont("consolas", 36, bold=True)

    faces = PALETTE[:]
    cards = faces + faces
    random.shuffle(cards)
    board = cards
    revealed = [False] * (COLS * ROWS)
    matched = [False] * (COLS * ROWS)
    pick = []
    moves = 0
    freeze_until = 0
    started = time.time()

    def cell(i):
        r, c = divmod(i, COLS)
        return pygame.Rect(PAD_X + c * (CW + 10), PAD_Y + r * (CH + 10), CW, CH)

    while True:
        clock.tick(60)
        now = time.time()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_r:
                    return main()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and now >= freeze_until:
                if len(pick) == 2:
                    continue
                for i in range(len(board)):
                    if cell(i).collidepoint(e.pos) and not revealed[i] and not matched[i]:
                        revealed[i] = True
                        pick.append(i)
                        if len(pick) == 2:
                            moves += 1
                            a, b = pick
                            if board[a][1] == board[b][1]:
                                matched[a] = matched[b] = True
                                pick = []
                            else:
                                freeze_until = now + 0.75
                        break

        if len(pick) == 2 and now >= freeze_until:
            for i in pick:
                if not matched[i]:
                    revealed[i] = False
            pick = []

        screen.fill((18, 22, 48))
        elapsed = int(now - started)
        done = all(matched)
        screen.blit(font.render(f"Moves {moves}   Time {elapsed}s   [R] new board   [ESC] quit", True, (220, 220, 240)), (24, 24))
        if done:
            t = big.render("ALL PAIRS FOUND!", True, (255, 220, 70))
            screen.blit(t, (24, 48))

        for i, (color, name) in enumerate(board):
            r = cell(i)
            if matched[i] or revealed[i]:
                pygame.draw.rect(screen, color, r, border_radius=12)
                pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=12)
                t = labelf.render(name, True, (10, 10, 20))
                screen.blit(t, t.get_rect(center=r.center))
            else:
                pygame.draw.rect(screen, (50, 70, 160), r, border_radius=12)
                pygame.draw.rect(screen, (140, 180, 255), r, 3, border_radius=12)
                t = labelf.render("?", True, (200, 220, 255))
                screen.blit(t, t.get_rect(center=r.center))

        pygame.display.flip()


if __name__ == "__main__":
    main()
