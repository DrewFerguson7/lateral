# Lateral 🏈

**[playlateral.com](https://playlateral.com)**: a daily NFL connection game.

Connect two NFL players through the teams, jersey numbers and colleges they share. Every link is a lateral. Fastest time wins.

- **Lateral:** a new pair every day, plus Unlimited and a Hard mode with rule twists
- **Trivia:** name a player's number, team and college in 3 tries
- **Ball Knowledge:** an endless chain on a 30-second play clock
- **Daily rankings:** "faster than X% of players today"

## How it's built
- One static page (`index.html`) with roster data on 32,600 players from 1920 to 2025 (nflverse), cleaned and de-duplicated
- 410 hand-checked daily puzzles, each with a verified solution, Hard-mode solution and best route
- `netlify/functions/rank.mjs`: a serverless function that stores one finish time per device per day in Netlify Blobs and returns the player's percentile
- Hosted on Netlify. Every push to `main` deploys automatically.

Run `npm test` to check the ranking function.

Fan-made. Not affiliated with the NFL. Data: nflverse, College Football Data.
