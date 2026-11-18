const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const preview = process.argv[2] === 'preview';
  const fps = 30, dur = 34;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve('index.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  if (preview) {
    for (const t of [3.5, 9.8, 13, 22, 27.8, 32.5]) {
      await p.evaluate(t => seek(t), t);
      await p.screenshot({ path: `prev_${t}.jpg`, type: 'jpeg', quality: 70 });
    }
    await b.close(); return;
  }
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', 'silent.mp4'], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < fps * dur; i++) {
    await p.evaluate(t => seek(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
})();
