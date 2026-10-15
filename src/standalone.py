# wraps the built page into a self-contained index.html for static hosting (Netlify)
SITE_URL = 'https://playlateral.com'        # your live address, e.g. 'https://handoff.netlify.app' (makes link previews work everywhere)
GOATCOUNTER = 'handoff'     # your GoatCounter code, e.g. 'handoff' for handoff.goatcounter.com (turns on visitor stats)
s = open('out/gridiron-handoff.html').read()
i = s.index('</style>') + len('</style>')
img = (SITE_URL.rstrip('/') + '/' if SITE_URL else '') + 'og-image.png'
desc = 'Link two NFL players through the teams, jersey numbers and colleges they share. A new puzzle every day, plus trivia and Ball Knowledge.'
icon = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 120 120%22%3E%3Cg stroke=%22%233b1f0f%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cpath d=%22M48 92l-6 16M72 92l6 16%22 stroke-width=%225%22 fill=%22none%22/%3E%3Cpath d=%22M33 110h14M73 110h14%22 stroke-width=%227%22/%3E%3Cpath d=%22M28 66C18 72 14 80 13 88%22 stroke-width=%225%22 fill=%22none%22/%3E%3Ccircle cx=%2213%22 cy=%2290%22 r=%227.5%22 fill=%22%23fff%22 stroke-width=%223.5%22/%3E%3Cg class=%22wave%22%3E%3Cpath d=%22M92 54C102 46 106 36 106 26%22 stroke-width=%225%22 fill=%22none%22/%3E%3Ccircle cx=%22106%22 cy=%2221%22 r=%227.5%22 fill=%22%23fff%22 stroke-width=%223.5%22/%3E%3C/g%3E%3Cg transform=%22rotate%28-14 60 64%29%22%3E%3Cpath d=%22M14 64C26 30 94 30 106 64C94 98 26 98 14 64Z%22 fill=%22%239a5a32%22 stroke-width=%224%22/%3E%3Cpath d=%22M27 44Q22 64 27 84M93 44Q98 64 93 84%22 stroke=%22%23f3eadf%22 stroke-width=%225%22 fill=%22none%22/%3E%3Cpath d=%22M46 41H74M52 36V46M60 36V46M68 36V46%22 stroke=%22%23f3eadf%22 stroke-width=%223.5%22/%3E%3Cellipse cx=%2249%22 cy=%2261%22 rx=%228%22 ry=%229.5%22 fill=%22%23fff%22 stroke-width=%223%22/%3E%3Cellipse cx=%2271%22 cy=%2261%22 rx=%228%22 ry=%229.5%22 fill=%22%23fff%22 stroke-width=%223%22/%3E%3Ccircle cx=%2251%22 cy=%2263%22 r=%224%22 fill=%22%231d1d1d%22 stroke=%22none%22/%3E%3Ccircle cx=%2273%22 cy=%2263%22 r=%224%22 fill=%22%231d1d1d%22 stroke=%22none%22/%3E%3Ccircle cx=%2252.5%22 cy=%2261.5%22 r=%221.4%22 fill=%22%23fff%22 stroke=%22none%22/%3E%3Ccircle cx=%2274.5%22 cy=%2261.5%22 r=%221.4%22 fill=%22%23fff%22 stroke=%22none%22/%3E%3Cpath d=%22M49 76Q60 86 71 76%22 stroke-width=%223.5%22 fill=%22%235a1d10%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E'
meta = f'''<meta name="description" content="{desc}">
<meta name="theme-color" content="#1d2024">
<link rel="icon" href="{icon}"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Lateral">
<meta property="og:title" content="Lateral: the NFL connection game"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
{f'<meta property="og:url" content="{SITE_URL}">' if SITE_URL else ''}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Lateral: the NFL connection game">
<meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{img}">
{f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>' if GOATCOUNTER else ''}'''
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + meta + '\n<style>html{-webkit-text-size-adjust:100%}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        + s[:i] + '\n</head>\n<body>\n' + s[i:] + '\n</body>\n</html>\n')
open('../site/index.html', 'w').write(page)
print('standalone written', len(page) // 1024, 'KB | site url:', SITE_URL or '(not set)', '| goatcounter:', GOATCOUNTER or '(not set)')
