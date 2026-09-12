# ElbowOS Arcade Vol. 2

A fresh pack of **standalone full-colour Python 3 games** (pygame).  
Project link: **[https://x.com/ElbowOS](https://x.com/ElbowOS)**

This is **not** a Nintendo / Mario Bros emulator and does not load ROM files.  
`pipe_jumper.py` is an original side-scroller in the classic plumber-platformer style (coins, pipes, stomping critters, flag).

## Games

| File | Genre | Controls |
|---|---|---|
| `games/pipe_jumper.py` | Platformer | A/D or arrows move, Space / W / Up jump, R restart |
| `games/blackjack_table.py` | Casino cards | Click DEAL / HIT / STAND, adjust bet |
| `games/neon_slots.py` | Casino slots | Click SPIN, +/- bet |
| `games/memory_match.py` | Card matching | Click two cards, R new board |
| `games/craps_table.py` | Casino dice | Click ROLL, +/- bet |
| `games/neon_breakout.py` | Arcade | Arrows move paddle |
| `games/star_blaster.py` | Shooter | Arrows move, Space fire |

## Run

```bash
python3 -m pip install -r requirements.txt
python3 launcher.py
```

Or one game:

```bash
python3 games/pipe_jumper.py
```

Needs Python 3.10+ and a desktop display (pygame / SDL).

## Links

- This repo: https://github.com/ApacheAde/ElbowOS-Arcade-Vol2
- ElbowOS on X: https://x.com/ElbowOS

MIT licensed. Original code and placeholder art — no copyrighted sprites or ROMs.
