#!/usr/bin/env python3
"""Neon Blackjack — casino table in full colour."""

import random
import sys

import pygame

W, H = 960, 600
GREEN = (12, 92, 48)
FELT = (18, 118, 62)
GOLD = (232, 186, 64)
WHITE = (250, 250, 250)
RED = (210, 36, 48)
BLACK = (22, 22, 28)
NAVY = (20, 36, 72)

SUITS = ["S", "H", "D", "C"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUIT_COLOR = {"S": BLACK, "C": BLACK, "H": RED, "D": RED}
SUIT_MARK = {"S": "SP", "C": "CL", "H": "HT", "D": "DI"}


def deck():
    d = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(d)
    return d


def value(hand):
    total, aces = 0, 0
    for r, _ in hand:
        if r == "A":
            total += 11
            aces += 1
        elif r in "JQK":
            total += 10
        else:
            total += int(r)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def draw_card(surf, card, x, y, font, hidden=False):
    rect = pygame.Rect(x, y, 78, 110)
    pygame.draw.rect(surf, WHITE, rect, border_radius=8)
    pygame.draw.rect(surf, GOLD, rect, 2, border_radius=8)
    if hidden:
        pygame.draw.rect(surf, NAVY, rect.inflate(-12, -12), border_radius=6)
        return
    r, s = card
    color = SUIT_COLOR[s]
    surf.blit(font.render(r, True, color), (x + 8, y + 8))
    surf.blit(font.render(SUIT_MARK[s], True, color), (x + 8, y + 40))


def button(surf, rect, label, font, active=True):
    c = GOLD if active else (90, 90, 90)
    pygame.draw.rect(surf, c, rect, border_radius=8)
    pygame.draw.rect(surf, WHITE, rect, 2, border_radius=8)
    t = font.render(label, True, BLACK)
    surf.blit(t, t.get_rect(center=rect.center))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Blackjack — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 36, bold=True)
    cardf = pygame.font.SysFont("consolas", 22, bold=True)

    bank = 500
    bet = 25
    dck = deck()
    player, dealer = [], []
    phase = "bet"
    msg = "Place a bet, then DEAL"
    hide = True

    def deal():
        nonlocal dck, player, dealer, phase, hide, bank, msg
        if bank < bet:
            msg = "Not enough chips"
            return
        if len(dck) < 20:
            dck = deck()
        bank -= bet
        player = [dck.pop(), dck.pop()]
        dealer = [dck.pop(), dck.pop()]
        hide = True
        phase = "play"
        if value(player) == 21:
            settle()
        else:
            msg = "HIT or STAND"

    def settle():
        nonlocal phase, hide, bank, msg
        hide = False
        phase = "settle"
        while value(dealer) < 17:
            dealer.append(dck.pop())
        pv, dv = value(player), value(dealer)
        if pv > 21:
            msg = "BUST — dealer wins"
        elif dv > 21 or pv > dv:
            win = bet * 2
            if pv == 21 and len(player) == 2:
                win = int(bet * 2.5)
                msg = "BLACKJACK!"
            else:
                msg = "You win!"
            bank += win
        elif pv == dv:
            bank += bet
            msg = "Push"
        else:
            msg = "Dealer wins"

    buttons = {
        "deal": pygame.Rect(40, 520, 120, 48),
        "hit": pygame.Rect(180, 520, 120, 48),
        "stand": pygame.Rect(320, 520, 120, 48),
        "m5": pygame.Rect(520, 520, 80, 48),
        "p5": pygame.Rect(620, 520, 80, 48),
        "m25": pygame.Rect(720, 520, 90, 48),
        "p25": pygame.Rect(830, 520, 90, 48),
    }

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                if buttons["deal"].collidepoint(pos) and phase != "play":
                    deal()
                elif buttons["hit"].collidepoint(pos) and phase == "play":
                    player.append(dck.pop())
                    if value(player) >= 21:
                        settle()
                elif buttons["stand"].collidepoint(pos) and phase == "play":
                    settle()
                elif phase != "play":
                    if buttons["m5"].collidepoint(pos):
                        bet = max(5, bet - 5)
                    if buttons["p5"].collidepoint(pos):
                        bet = min(bank, bet + 5)
                    if buttons["m25"].collidepoint(pos):
                        bet = max(5, bet - 25)
                    if buttons["p25"].collidepoint(pos):
                        bet = min(bank, bet + 25)

        screen.fill(GREEN)
        pygame.draw.ellipse(screen, FELT, (40, 40, 880, 430))
        pygame.draw.ellipse(screen, GOLD, (40, 40, 880, 430), 4)
        screen.blit(big.render("BLACKJACK", True, GOLD), (380, 56))
        screen.blit(font.render(f"Bank ${bank}   Bet ${bet}", True, WHITE), (40, 16))
        screen.blit(font.render(msg, True, GOLD), (40, 480))

        screen.blit(font.render(f"Dealer  {'' if hide else value(dealer)}", True, WHITE), (80, 120))
        for i, c in enumerate(dealer):
            draw_card(screen, c, 80 + i * 90, 150, cardf, hidden=(hide and i == 1))
        screen.blit(font.render(f"You  {value(player) if player else ''}", True, WHITE), (80, 290))
        for i, c in enumerate(player):
            draw_card(screen, c, 80 + i * 90, 320, cardf)

        button(screen, buttons["deal"], "DEAL", font, phase != "play")
        button(screen, buttons["hit"], "HIT", font, phase == "play")
        button(screen, buttons["stand"], "STAND", font, phase == "play")
        button(screen, buttons["m5"], "-5", font, phase != "play")
        button(screen, buttons["p5"], "+5", font, phase != "play")
        button(screen, buttons["m25"], "-25", font, phase != "play")
        button(screen, buttons["p25"], "+25", font, phase != "play")
        pygame.display.flip()


if __name__ == "__main__":
    main()
