const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [name, w] of [['tip_desk', 1280], ['tip_phone', 400]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    const src = require('fs').readFileSync('/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/artifact/alife_lab.html', 'utf8');
    await p.setContent('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>' + src + '</body></html>');
    await p.waitForTimeout(800);
    for (const id of ['v-ch', 'v-p']) {
      const el = await p.$(`#${id} .plot`); await el.scrollIntoViewIfNeeded(); const bb = await el.boundingBox();
      await p.mouse.move(bb.x + bb.width * 0.55, bb.y + bb.height / 2); await p.waitForTimeout(200);
      const v = await p.$(`#${id}`); await v.screenshot({ path: `${name}_${id}.png` });
    }
    await p.close();
  }
  await b.close();
})();
