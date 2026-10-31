const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const f = 'file:///tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/artifact/alife_lab.html';
  const src = require('fs').readFileSync(f.slice(7), 'utf8');
  const html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + src + '</body></html>';
  require('fs').writeFileSync('/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/artifact/_preview.html', html);
  for (const [name, w, scheme] of [['desk_light', 1280, 'light'], ['desk_dark', 1280, 'dark'], ['phone', 400, 'light']]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto('file:///tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/artifact/_preview.html');
    await p.waitForTimeout(800);
    const sw = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
    // hover the challenge chart
    const box = await p.$('#v-ch .plot'); const bb = await box.boundingBox();
    await p.mouse.move(bb.x + bb.width * 0.6, bb.y + bb.height / 2);
    await p.screenshot({ path: `${name}.png`, fullPage: true });
    console.log(name, 'scroll', sw, 'errors', errs);
    await p.close();
  }
  await b.close();
})();
