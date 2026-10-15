# Lateral 🏈

**[playlateral.com](https://playlateral.com)**: a daily NFL connection game.

Connect two NFL players through the teams, jersey numbers and colleges they share. Every link is a lateral. Fastest time wins.

- **Lateral:** a new pair every day, plus Unlimited and a Hard mode with its own daily pair and rule twists
- **Trivia:** name a player's number, team and college in 3 tries
- **Ball Knowledge:** an endless chain on a 30-second play clock
- **Daily rankings:** "faster than X% of players today", with a bell curve of everyone's times

## How it's built
- One static page (`site/index.html`) with roster data on 32,600 players from 1920 to 2025 (nflverse), cleaned and de-duplicated
- 410 hand-checked daily puzzles, each with a verified solution, Hard-mode solution and best route
- `netlify/functions/rank.mjs`: a serverless function that stores one finish time per device per day in Netlify Blobs and returns the player's percentile
- Hosted on Netlify. Every push to `main` deploys automatically.

## Repo layout
- `site/`: what's published (the game page, preview image, icon)
- `netlify/functions/rank.mjs`: the daily-rankings function
- `src/`: build tools and data. `update_season.py 2026` adds a new season's rosters (trades, signings, rookies). `tpl2.html` is the game template; `build2.py` fills in the player data; `standalone.py` writes `site/index.html`; `val.js` checks every puzzle route. Changes here don't trigger a deploy.

```
cd src && PYTHONHASHSEED=0 python3 build2.py && python3 standalone.py && node val.js
npm test                                  # ranking function tests
node tools/devserver.mjs site 100         # local preview with 100 fake players
```

Fan-made. Not affiliated with the NFL. Data: nflverse, College Football Data.
