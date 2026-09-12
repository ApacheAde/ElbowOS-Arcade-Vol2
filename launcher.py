#!/usr/bin/env python3
"""ElbowOS Arcade Vol. 2 — colourful game launcher."""

import importlib
import sys

import pygame

W, H = 880, 620
BG = (12, 16, 36)
GOLD = (255, 210, 70)
CYAN = (80, 230, 255)
WHITE = (240, 244, 255)
PINK = (255, 90, 160)

GAMES = [
    ("1", "Pipe Jumper", "Mario-style platformer (original, not an emulator)", "games.pipe_jumper"),
    ("2", "Blackjack Table", "Casino twenty-one", "games.blackjack_table"),
    ("3", "Neon Slots", "Three-reel slot machine", "games.neon_slots"),
    ("4", "Memory Match", "Colour pair card game", "games.memory_match"),
    ("5", "Street Craps", "Dice table", "games.craps_table"),
    ("6", "Neon Breakout", "Brick breaker", "games.neon_breakout"),
    ("7", "Star Blaster", "Space shooter", "games.star_blaster"),
]


def run_module(modname):
    pygame.quit()
    mod = importlib.import_module(modname)
    importlib.reload(mod)
    mod.main()
    pygame.init()


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("ElbowOS Arcade Vol. 2")
    clock = pygame.time.Clock()
    titlef = pygame.font.SysFont("consolas", 36, bold=True)
    font = pygame.font.SysFont("consolas", 22)
    small = pygame.font.SysFont("consolas", 16)

    rows = []
    for i, (key, name, desc, mod) in enumerate(GAMES):
        rows.append((pygame.Rect(80, 130 + i * 56, 720, 48), key, name, desc, mod))

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                for _, key, _, _, mod in rows:
                    if e.unicode == key:
                        run_module(mod)
                        screen = pygame.display.set_mode((W, H))
                        pygame.display.set_caption("ElbowOS Arcade Vol. 2")
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for rect, _, _, _, mod in rows:
                    if rect.collidepoint(e.pos):
                        run_module(mod)
                        screen = pygame.display.set_mode((W, H))
                        pygame.display.set_caption("ElbowOS Arcade Vol. 2")

        screen.fill(BG)
        t = titlef.render("ELBOWOS ARCADE  VOL. 2", True, GOLD)
        screen.blit(t, t.get_rect(center=(W // 2, 48)))
        screen.blit(small.render("https://x.com/ElbowOS    click a row or press 1-7", True, CYAN), (80, 88))
        for rect, key, name, desc, _ in rows:
            pygame.draw.rect(screen, (28, 40, 84), rect, border_radius=10)
            pygame.draw.rect(screen, CYAN, rect, 2, border_radius=10)
            screen.blit(font.render(f"{key}  {name}", True, WHITE), (rect.x + 16, rect.y + 4))
            screen.blit(small.render(desc, True, PINK), (rect.x + 48, rect.y + 26))
        pygame.display.flip()


if __name__ == "__main__":
    main()
