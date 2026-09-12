#!/usr/bin/env python3
"""Star Blaster — colourful top-down space shooter."""

import random
import sys

import pygame

W, H = 900, 640
BG = (6, 8, 22)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Star Blaster — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 40, bold=True)

    ship = pygame.Rect(W // 2 - 16, H - 70, 32, 36)
    bullets = []
    enemies = []
    stars = [(random.randint(0, W), random.randint(0, H), random.randint(1, 3)) for _ in range(70)]
    spawn = 0
    score = 0
    lives = 3
    cooldown = 0
    alive = True

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
                if e.key == pygame.K_r:
                    return main()

        keys = pygame.key.get_pressed()
        if alive:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ship.x -= 7
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ship.x += 7
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                ship.y -= 6
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                ship.y += 6
            ship.clamp_ip(pygame.Rect(8, 40, W - 16, H - 48))
            cooldown = max(0, cooldown - 1)
            if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and cooldown == 0:
                bullets.append(pygame.Rect(ship.centerx - 3, ship.y - 12, 6, 14))
                cooldown = 10

            for b in bullets:
                b.y -= 11
            bullets = [b for b in bullets if b.bottom > 0]

            spawn += 1
            if spawn >= max(18, 48 - score // 80):
                spawn = 0
                enemies.append(pygame.Rect(random.randint(20, W - 50), -36, 36, 28))

            for en in enemies:
                en.y += 3 + score // 200
            for en in enemies[:]:
                if en.top > H:
                    enemies.remove(en)
                    lives -= 1
                    if lives <= 0:
                        alive = False

            for b in bullets[:]:
                hit = b.collidelist(enemies)
                if hit != -1:
                    enemies.pop(hit)
                    bullets.remove(b)
                    score += 15
                    break

            if ship.collidelist(enemies) != -1:
                idx = ship.collidelist(enemies)
                enemies.pop(idx)
                lives -= 1
                if lives <= 0:
                    alive = False

        screen.fill(BG)
        for i, (sx, sy, r) in enumerate(stars):
            sy = (sy + r) % H
            stars[i] = (sx, sy, r)
            pygame.draw.circle(screen, (180, 200, 255), (sx, int(sy)), r)
        pygame.draw.polygon(screen, (80, 220, 255), [
            (ship.centerx, ship.y),
            (ship.left, ship.bottom),
            (ship.centerx, ship.bottom - 10),
            (ship.right, ship.bottom),
        ])
        pygame.draw.rect(screen, (255, 180, 40), (ship.centerx - 4, ship.bottom - 4, 8, 10))
        for b in bullets:
            pygame.draw.rect(screen, (255, 240, 80), b, border_radius=2)
        for en in enemies:
            pygame.draw.rect(screen, (255, 70, 110), en, border_radius=6)
            pygame.draw.rect(screen, (255, 180, 200), (en.x + 8, en.y + 8, 20, 10))

        screen.blit(font.render(f"SCORE {score}   LIVES {lives}   arrows move  SPACE fire  [R] restart", True, (220, 230, 255)), (12, 10))
        if not alive:
            t = big.render("SHIP DOWN — press R", True, (255, 90, 90))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2)))
        pygame.display.flip()


if __name__ == "__main__":
    main()
