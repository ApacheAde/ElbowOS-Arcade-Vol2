#!/usr/bin/env python3
"""Pipe Jumper — original side-scroller in the plumber-platformer style.
Not an emulator and does not load ROMs or Nintendo assets."""

import random
import sys

import pygame

W, H = 960, 540
GRAVITY = 0.55
JUMP = -11.5
SPEED = 5.2
SKY = (92, 168, 255)
HILL = (56, 196, 88)
DIRT = (168, 92, 36)
PIPE = (40, 180, 64)
COIN = (255, 214, 40)
ENEMY = (196, 92, 28)
PLAYER = (236, 48, 48)
FLAG = (48, 220, 96)
WHITE = (255, 255, 255)
NAVY = (16, 24, 48)


class Actor:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.alive = True

    def draw(self, surf, cam):
        r = self.rect.move(-cam, 0)
        pygame.draw.rect(surf, self.color, r, border_radius=6)
        return r


def make_world():
    ground = []
    x = 0
    while x < 4200:
        w = random.choice([220, 280, 340, 400])
        ground.append(pygame.Rect(x, 460, w, 80))
        x += w + random.choice([0, 0, 70, 110])
    pipes = [pygame.Rect(520, 380, 54, 80), pygame.Rect(1180, 340, 54, 120),
             pygame.Rect(1980, 360, 54, 100), pygame.Rect(2680, 330, 54, 130)]
    coins = [pygame.Rect(random.randint(80, 3900), random.choice([300, 340, 380]), 18, 18)
             for _ in range(28)]
    foes = [Actor(random.randint(400, 3600), 428, 32, 32, ENEMY) for _ in range(9)]
    for f in foes:
        f.vx = random.choice([-1.6, 1.6])
    flag = pygame.Rect(4000, 220, 16, 240)
    return ground, pipes, coins, foes, flag


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pipe Jumper — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 42, bold=True)

    ground, pipes, coins, foes, flag = make_world()
    p = Actor(60, 380, 34, 44, PLAYER)
    cam = 0
    score = 0
    lives = 3
    won = False
    dead = False

    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w) and p.on_ground and not dead and not won:
                    p.vy = JUMP
                    p.on_ground = False
                if e.key == pygame.K_r:
                    return main()

        keys = pygame.key.get_pressed()
        if not dead and not won:
            p.vx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                p.vx = -SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                p.vx = SPEED
            p.vy += GRAVITY
            p.rect.x += int(p.vx)
            p.rect.y += int(p.vy)
            p.on_ground = False
            solids = ground + pipes
            for s in solids:
                if p.rect.colliderect(s):
                    if p.vy >= 0 and p.rect.bottom - s.top < 28:
                        p.rect.bottom = s.top
                        p.vy = 0
                        p.on_ground = True
                    elif p.vy < 0:
                        p.rect.top = s.bottom
                        p.vy = 0
                    else:
                        if p.vx > 0:
                            p.rect.right = s.left
                        elif p.vx < 0:
                            p.rect.left = s.right
            if p.rect.top > H + 40:
                lives -= 1
                if lives <= 0:
                    dead = True
                else:
                    p.rect.topleft = (max(40, p.rect.x - 180), 200)
                    p.vy = 0

            for c in coins[:]:
                if p.rect.colliderect(c):
                    coins.remove(c)
                    score += 10

            for f in foes:
                if not f.alive:
                    continue
                f.rect.x += int(f.vx)
                if random.random() < 0.008:
                    f.vx *= -1
                if p.rect.colliderect(f.rect):
                    if p.vy > 0 and p.rect.bottom - f.rect.top < 22:
                        f.alive = False
                        p.vy = JUMP * 0.55
                        score += 25
                    else:
                        lives -= 1
                        p.rect.topleft = (max(40, p.rect.x - 160), 200)
                        p.vy = 0
                        if lives <= 0:
                            dead = True

            if p.rect.colliderect(flag):
                won = True
                score += 200

        cam = max(0, p.rect.centerx - 280)

        screen.fill(SKY)
        for i in range(8):
            hx = (i * 280 - cam * 0.3) % (W + 280) - 80
            pygame.draw.ellipse(screen, (70, 210, 110), (hx, 390, 260, 140))
        for g in ground:
            r = g.move(-cam, 0)
            pygame.draw.rect(screen, HILL, r)
            pygame.draw.rect(screen, DIRT, (r.x, r.y + 18, r.w, r.h - 18))
        for pipe in pipes:
            r = pipe.move(-cam, 0)
            pygame.draw.rect(screen, PIPE, r, border_radius=4)
            pygame.draw.rect(screen, (30, 140, 50), (r.x - 6, r.y, r.w + 12, 18), border_radius=4)
        for c in coins:
            pygame.draw.ellipse(screen, COIN, c.move(-cam, 0))
        for f in foes:
            if f.alive:
                r = f.draw(screen, cam)
                pygame.draw.circle(screen, WHITE, (r.x + 10, r.y + 10), 4)
                pygame.draw.circle(screen, WHITE, (r.x + 22, r.y + 10), 4)
        fr = flag.move(-cam, 0)
        pygame.draw.rect(screen, (230, 230, 230), fr)
        pygame.draw.polygon(screen, FLAG, [(fr.right, fr.y + 8), (fr.right + 54, fr.y + 28), (fr.right, fr.y + 48)])
        pr = p.draw(screen, cam)
        pygame.draw.rect(screen, (40, 80, 200), (pr.x + 6, pr.y + 18, 22, 16))
        pygame.draw.rect(screen, (255, 210, 160), (pr.x + 8, pr.y + 4, 18, 14), border_radius=4)

        hud = font.render(f"SCORE {score}   LIVES {lives}   [R] restart   [ESC] quit", True, NAVY)
        screen.blit(hud, (16, 12))
        if won:
            t = big.render("COURSE CLEAR!", True, (255, 240, 80))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2)))
        if dead:
            t = big.render("GAME OVER — press R", True, (255, 70, 70))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2)))

        pygame.display.flip()
        _ = dt


if __name__ == "__main__":
    main()
