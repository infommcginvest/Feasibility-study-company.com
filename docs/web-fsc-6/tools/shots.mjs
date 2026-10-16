// WEB-FSC-6 look gate: desktop 1440 and mobile 390 full-page screenshots plus an overflow test.
// node docs/web-fsc-6/tools/shots.mjs <base-url> <out-dir> <url-path> [<url-path> ...]
// Starts chrome-headless-shell with a DevTools port, drives it over CDP (Node's built-in WebSocket),
// and prints one JSON line per page and width: scrollWidth, innerWidth, page-level overflow (true/false),
// and the wide tables that scroll inside their own wrapper.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const [base, outDir, ...paths] = process.argv.slice(2);
const SHELL = join(homedir(), 'Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell');
if (!existsSync(SHELL)) { console.error('headless shell not found', SHELL); process.exit(2); }
mkdirSync(outDir, { recursive: true });
const port = 9300 + Math.floor(Math.random() * 500);
const proc = spawn(SHELL, [`--remote-debugging-port=${port}`, '--no-first-run', '--hide-scrollbars', `--user-data-dir=${join(outDir, '.profile')}`, 'about:blank'], { stdio: 'ignore' });
const killer = setTimeout(() => { proc.kill('SIGKILL'); console.error('timeout'); process.exit(3); }, 600000);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function target() {
  for (let i = 0; i < 50; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/json/list`);
      const list = await r.json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch (e) { /* not up yet */ }
    await sleep(200);
  }
  throw new Error('no devtools target');
}

const ws = new WebSocket(await target());
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let seq = 0;
const pending = new Map();
const waiters = [];
ws.addEventListener('message', (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  else if (msg.method) { for (const w of waiters.splice(0)) w(msg); }
});
const send = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++seq;
  const t = setTimeout(() => reject(new Error('cdp timeout ' + method)), 60000);
  pending.set(id, (m) => { clearTimeout(t); m.error ? reject(new Error(JSON.stringify(m.error))) : resolve(m.result); });
  ws.send(JSON.stringify({ id, method, params }));
});
await send('Page.enable');
await send('Runtime.enable');

async function shoot(path, width, label) {
  const height = width > 800 ? 900 : 844;
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 800 });
  const loaded = new Promise((r) => { const f = (m) => { if (m.method === 'Page.loadEventFired') r(); else waiters.push(f); }; waiters.push(f); });
  await send('Page.navigate', { url: base.replace(/\/$/, '') + path });
  await Promise.race([loaded, sleep(20000)]);
  await sleep(1200);
  const probe = await send('Runtime.evaluate', { returnByValue: true, expression: `(() => {
    const de = document.documentElement;
    const wide = [...document.querySelectorAll('table')].filter(t => t.scrollWidth > t.parentElement.clientWidth + 1)
      .map(t => ({cls: t.className, table: t.scrollWidth, box: t.parentElement.clientWidth, scrolls: getComputedStyle(t.parentElement).overflowX}));
    const over = [...document.body.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && !e.closest('.data-table-wrap,.monitor-wrap,.mega-panel'); })
      .slice(0, 5).map(e => e.tagName + '.' + e.className);
    return {scrollWidth: de.scrollWidth, innerWidth, height: de.scrollHeight, pageOverflow: de.scrollWidth > innerWidth + 1, wideTables: wide, offenders: over};
  })()` });
  const info = probe.result.value;
  await send('Emulation.setDeviceMetricsOverride', { width, height: Math.min(info.height, 16000), deviceScaleFactor: 1, mobile: width < 800 });
  await sleep(500);
  const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  const name = (path.replace(/^\/|\/$/g, '').replace(/\//g, '_') || 'home') + `-${label}.png`;
  writeFileSync(join(outDir, name), Buffer.from(shot.data, 'base64'));
  console.log(JSON.stringify({ path, width, file: name, ...info }));
}

try {
  for (const p of paths) { await shoot(p, 1440, 'desktop-1440'); await shoot(p, 390, 'mobile-390'); }
} finally {
  clearTimeout(killer);
  ws.close();
  proc.kill('SIGKILL');
}
