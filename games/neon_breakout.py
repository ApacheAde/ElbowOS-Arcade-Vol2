#!/usr/bin/env python3
"""Neon Breakout — colourful brick-breaker."""

import sys

import pygame

W, H = 900, 640
BG = (10, 12, 28)
PADDLE = (80, 230, 255)
BALL = (255, 230, 80)
COLORS = [
    (255, 70, 110),
    (255, 140, 50),
    (255, 220, 60),
    (80, 220, 120),
    (70, 160, 255),
    (180, 90, 255),
]


def build_bricks():
    bricks = []
    for row in range(6):
        for col in range(11):
            bricks.append(pygame.Rect(30 + col * 76, 70 + row * 32, 70, 24))
    return bricks


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Breakout — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 40, bold=True)

    paddle = pygame.Rect(W // 2 - 60, H - 40, 120, 16)
    ball = pygame.Rect(W // 2 - 8, H - 70, 16, 16)
    vx, vy = 4.2, -4.8
    bricks = build_bricks()
    lives, score = 3, 0
    running = True
    won = False

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
                if e.key == pygame.K_r:
                    return main()

        keys = pygame.key.get_pressed()
        if running:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                paddle.x -= 9
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                paddle.x += 9
            paddle.x = max(10, min(W - paddle.w - 10, paddle.x))
            ball.x += int(vx)
            ball.y += int(vy)
            if ball.left <= 0 or ball.right >= W:
                vx *= -1
            if ball.top <= 0:
                vy *= -1
            if ball.colliderect(paddle) and vy > 0:
                vy *= -1
                offset = (ball.centerx - paddle.centerx) / (paddle.w / 2)
                vx = max(-7, min(7, vx + offset * 2.2))
            hit = ball.collidelist(bricks)
            if hit != -1:
                bricks.pop(hit)
                vy *= -1
                score += 10
                if abs(vx) < 8:
                    vx *= 1.02
                    vy *= 1.02
            if not bricks:
                running = False
                won = True
            if ball.top > H:
                lives -= 1
                ball.topleft = (paddle.centerx - 8, H - 70)
                vx, vy = 4.2, -4.8
                if lives <= 0:
                    running = False

        screen.fill(BG)
        for i, b in enumerate(bricks):
            pygame.draw.rect(screen, COLORS[i // 11 % len(COLORS)], b, border_radius=4)
        pygame.draw.rect(screen, PADDLE, paddle, border_radius=8)
        pygame.draw.ellipse(screen, BALL, ball)
        screen.blit(font.render(f"SCORE {score}   LIVES {lives}   arrows move   [R] restart", True, (220, 230, 255)), (16, 16))
        if won:
            t = big.render("FIELD CLEARED!", True, (255, 220, 70))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2)))
        elif not running:
            t = big.render("GAME OVER — press R", True, (255, 90, 90))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2)))
        pygame.display.flip()
        _ = dt


if __name__ == "__main__":
    main()
