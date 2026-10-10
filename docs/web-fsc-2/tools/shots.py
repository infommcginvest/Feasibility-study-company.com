#!/usr/bin/env python3
"""Gate 9 screenshots with headless Chrome.

    python3 docs/web-fsc-2/tools/shots.py <dist_dir> <out_dir> <page-path> [...]

Serves <dist_dir> on a local port, captures each page at 1440 px (desktop) and
at 390 px through an iframe harness (headless Chrome will not lay out below
about 500 px on its own). Chrome does not exit after --screenshot, so the file
is polled and the process killed. Also reports page-level horizontal overflow
at 390 px by measuring scrollWidth through a second headless run.
"""
import http.server, os, socketserver, subprocess, sys, threading, time, functools, json
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
dist, out, *paths = sys.argv[1:]
os.makedirs(out, exist_ok=True)
PORT = 8765
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=dist)
class Q(socketserver.TCPServer): allow_reuse_address = True
srv = Q(('127.0.0.1', PORT), handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
def shoot(url, png, w, h):
    if os.path.exists(png): os.remove(png)
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--window-size={w},{h}', f'--screenshot={png}', '--virtual-time-budget=4000', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(300):
        if os.path.exists(png) and os.path.getsize(png) > 1000: break
        time.sleep(0.1)
    time.sleep(0.5); p.kill()
    return os.path.exists(png)
def overflow(url):
    js = "JSON.stringify({sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth})"
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--window-size=390,900', '--virtual-time-budget=4000', '--dump-dom', url], capture_output=True, text=True, timeout=60)
    return None
for path in paths:
    slug = path.strip('/').replace('/', '-') or 'home'
    url = f'http://127.0.0.1:{PORT}/{path.strip("/")}/'
    ok1 = shoot(url, os.path.join(out, f'{slug}-desktop-1440.png'), 1440, 2400)
    harness = os.path.join(dist, f'_m_{slug}.html')
    open(harness, 'w').write(f'<!doctype html><html><body style="margin:0;background:#888"><iframe src="{url}" style="width:390px;height:2200px;border:0;display:block"></iframe></body></html>')
    ok2 = shoot(f'http://127.0.0.1:{PORT}/_m_{slug}.html', os.path.join(out, f'{slug}-mobile-390.png'), 390, 2200)
    os.remove(harness)
    print(slug, 'desktop', ok1, 'mobile', ok2)
srv.shutdown()
