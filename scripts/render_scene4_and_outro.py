from playwright.sync_api import sync_playwright
from pathlib import Path

html_scene4 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; }
  body { width: 1920px; height: 1080px; overflow: hidden; background: #000; }
  canvas { width: 1920px; height: 1080px; }
</style>
</head>
<body>
<canvas id="c" width="1920" height="1080"></canvas>
<script>
  const c = document.getElementById("c");
  const ctx = c.getContext("2d");

  // 1. Dramatic Sky
  const sky = ctx.createLinearGradient(0, 0, 0, 620);
  sky.addColorStop(0, "#100318");
  sky.addColorStop(0.25, "#2e0838");
  sky.addColorStop(0.5, "#68103d");
  sky.addColorStop(0.75, "#b82e38");
  sky.addColorStop(0.9, "#e86a38");
  sky.addColorStop(1.0, "#fca25e");
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, 1920, 620);

  // Soft glowing theatrical clouds
  function drawCloud(x, y, rad, color) {
    const g = ctx.createRadialGradient(x, y, rad*0.2, x, y, rad);
    g.addColorStop(0, color);
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(x, y, rad, 0, Math.PI*2);
    ctx.fill();
  }
  drawCloud(400, 250, 220, "rgba(235, 120, 90, 0.45)");
  drawCloud(1500, 220, 260, "rgba(220, 90, 110, 0.4)");
  drawCloud(960, 320, 300, "rgba(255, 180, 100, 0.5)");

  // 2. Distant Royal Fantasy Castle Silhouette
  ctx.fillStyle = "#1e0926";
  function drawCastle() {
    ctx.fillRect(840, 320, 240, 260);
    drawSpire(960, 480, 360, 45, 120);
    drawSpire(870, 500, 280, 35, 90);
    drawSpire(1050, 500, 280, 35, 90);
    drawSpire(780, 520, 220, 30, 80);
    drawSpire(1140, 520, 220, 30, 80);
    for (let bx = 840; bx < 1080; bx += 20) {
      ctx.fillRect(bx, 310, 12, 18);
    }
    ctx.fillStyle = "#ff2a55";
    drawHeart(960, 280, 16);
    ctx.fillStyle = "#1e0926";
  }

  function drawSpire(x, baseY, h, w, roofH) {
    ctx.beginPath();
    ctx.moveTo(x - w/2, baseY);
    ctx.lineTo(x - w*0.4, baseY - h);
    ctx.lineTo(x + w*0.4, baseY - h);
    ctx.lineTo(x + w/2, baseY);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(x - w*0.45, baseY - h);
    ctx.lineTo(x, baseY - h - roofH);
    ctx.lineTo(x + w*0.45, baseY - h);
    ctx.fill();
    ctx.fillStyle = "#f5c542";
    ctx.beginPath();
    ctx.arc(x, baseY - h - roofH - 4, 4, 0, Math.PI*2);
    ctx.fill();
    ctx.fillStyle = "#1e0926";
  }

  function drawHeart(x, y, s) {
    ctx.beginPath();
    ctx.moveTo(x, y + s*0.6);
    ctx.bezierCurveTo(x - s, y, x - s*1.1, y - s*0.6, x, y - s*0.2);
    ctx.bezierCurveTo(x + s*1.1, y - s*0.6, x + s, y, x, y + s*0.6);
    ctx.fill();
  }
  drawCastle();

  // 3. Perspective Checkered Courtyard (Red & White Marble)
  const horizonY = 560;
  const numRows = 22;
  const numCols = 26;
  const vpX = 960;

  for (let r = 0; r < numRows; r++) {
    const t0 = Math.pow(r / numRows, 2.5);
    const t1 = Math.pow((r + 1) / numRows, 2.5);
    const y0 = horizonY + t0 * (1080 - horizonY);
    const y1 = horizonY + t1 * (1080 - horizonY);

    for (let c_idx = -numCols/2; c_idx < numCols/2; c_idx++) {
      const spread0 = (t0 + 0.05);
      const spread1 = (t1 + 0.05);
      const x0_l = vpX + (c_idx * 165) * spread0;
      const x0_r = vpX + ((c_idx + 1) * 165) * spread0;
      const x1_l = vpX + (c_idx * 165) * spread1;
      const x1_r = vpX + ((c_idx + 1) * 165) * spread1;

      const isCrimson = (Math.abs(r + c_idx)) % 2 === 0;
      ctx.beginPath();
      ctx.moveTo(x0_l, y0);
      ctx.lineTo(x0_r, y0);
      ctx.lineTo(x1_r, y1);
      ctx.lineTo(x1_l, y1);
      ctx.closePath();

      const brightness = 0.35 + 0.65 * t1;
      if (isCrimson) {
        ctx.fillStyle = `rgb(${Math.round(170 * brightness)}, ${Math.round(18 * brightness)}, ${Math.round(32 * brightness)})`;
      } else {
        ctx.fillStyle = `rgb(${Math.round(245 * brightness)}, ${Math.round(238 * brightness)}, ${Math.round(230 * brightness)})`;
      }
      ctx.fill();
      ctx.strokeStyle = "rgba(25, 0, 5, 0.35)";
      ctx.lineWidth = Math.max(1, t1 * 2);
      ctx.stroke();
    }
  }

  // 4. Grand Manicured Hedge Maze Topiaries
  function drawHedgeArch(startX, width, isLeft) {
    const hedgeGrad = ctx.createLinearGradient(startX, 0, startX + width, 0);
    if (isLeft) {
      hedgeGrad.addColorStop(0, "#0a2210");
      hedgeGrad.addColorStop(0.5, "#12381b");
      hedgeGrad.addColorStop(1, "#1b4a25");
    } else {
      hedgeGrad.addColorStop(0, "#1b4a25");
      hedgeGrad.addColorStop(0.5, "#12381b");
      hedgeGrad.addColorStop(1, "#0a2210");
    }
    ctx.fillStyle = hedgeGrad;
    ctx.fillRect(startX, 360, width, 720);

    for (let i = 0; i < 400; i++) {
      const hx = startX + Math.random() * width;
      const hy = 360 + Math.random() * 720;
      const hr = 8 + Math.random() * 16;
      ctx.fillStyle = Math.random() > 0.4 ? "rgba(30, 85, 42, 0.35)" : "rgba(10, 35, 16, 0.4)";
      ctx.beginPath();
      ctx.arc(hx, hy, hr, 0, Math.PI*2);
      ctx.fill();
    }

    ctx.fillStyle = "#1b4a25";
    const heartX = isLeft ? startX + width * 0.7 : startX + width * 0.3;
    drawHeart(heartX, 330, 48);
  }
  drawHedgeArch(-40, 480, true);
  drawHedgeArch(1480, 480, false);

  // 5. Grand Crimson & Wrought-Iron Palace Gates
  function drawPillar(px) {
    const pilGrad = ctx.createLinearGradient(px - 35, 0, px + 35, 0);
    pilGrad.addColorStop(0, "#4a1520");
    pilGrad.addColorStop(0.5, "#852438");
    pilGrad.addColorStop(1, "#2d0c14");
    ctx.fillStyle = pilGrad;
    ctx.fillRect(px - 35, 380, 70, 400);
    ctx.fillStyle = "#e8b835";
    ctx.fillRect(px - 45, 365, 90, 18);
    drawHeart(px, 335, 26);
  }
  drawPillar(520);
  drawPillar(1400);

  ctx.strokeStyle = "#c42338";
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.arc(960, 540, 400, Math.PI, Math.PI*2);
  ctx.stroke();
  ctx.strokeStyle = "#f0c040";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(960, 540, 385, Math.PI, Math.PI*2);
  ctx.stroke();

  for (let gx = 560; gx <= 1360; gx += 44) {
    if (Math.abs(gx - 960) < 60) continue;
    ctx.strokeStyle = "#50101c";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(gx, 540);
    ctx.lineTo(gx, 720);
    ctx.stroke();
    ctx.fillStyle = "#f0c040";
    drawHeart(gx, 536, 7);
  }

  // 6. Lush Rose Bushes with Crimson Red & Half-Painted White Roses
  function drawRoseBush(cx, cy, scale) {
    for (let i = 0; i < 25; i++) {
      const lx = cx + (Math.random() - 0.5) * 160 * scale;
      const ly = cy + (Math.random() - 0.5) * 120 * scale;
      ctx.fillStyle = "#14421e";
      ctx.beginPath();
      ctx.ellipse(lx, ly, 18*scale, 10*scale, Math.random()*3, 0, Math.PI*2);
      ctx.fill();
    }

    for (let r = 0; r < 9; r++) {
      const rx = cx + (Math.random() - 0.5) * 140 * scale;
      const ry = cy + (Math.random() - 0.5) * 100 * scale;
      drawRose(rx, ry, 16 * scale, "#d6112c", "#850012");
    }

    for (let w = 0; w < 4; w++) {
      const wx = cx + (Math.random() - 0.5) * 130 * scale;
      const wy = cy + (Math.random() - 0.5) * 90 * scale;
      drawHalfPaintedRose(wx, wy, 17 * scale);
    }
  }

  function drawRose(x, y, rad, outerCol, innerCol) {
    ctx.fillStyle = outerCol;
    ctx.beginPath();
    ctx.arc(x, y, rad, 0, Math.PI*2);
    ctx.fill();
    ctx.fillStyle = innerCol;
    ctx.beginPath();
    ctx.arc(x, y, rad * 0.55, 0, Math.PI*2);
    ctx.fill();
    ctx.fillStyle = "#fff";
    ctx.globalAlpha = 0.25;
    ctx.beginPath();
    ctx.arc(x - rad*0.2, y - rad*0.2, rad*0.25, 0, Math.PI*2);
    ctx.fill();
    ctx.globalAlpha = 1.0;
  }

  function drawHalfPaintedRose(x, y, rad) {
    ctx.fillStyle = "#fdfdfd";
    ctx.beginPath();
    ctx.arc(x, y, rad, 0, Math.PI*2);
    ctx.fill();
    ctx.fillStyle = "#e0dede";
    ctx.beginPath();
    ctx.arc(x, y, rad * 0.6, 0, Math.PI*2);
    ctx.fill();
    
    ctx.fillStyle = "#d6112c";
    ctx.beginPath();
    ctx.arc(x, y, rad, Math.PI*0.8, Math.PI*1.9);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.rect(x - rad*0.3, y + rad*0.2, 4, 18);
    ctx.rect(x + rad*0.2, y + rad*0.4, 3, 24);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x - rad*0.3 + 2, y + rad*0.2 + 18, 3, 0, Math.PI*2);
    ctx.arc(x + rad*0.2 + 1.5, y + rad*0.4 + 24, 2.5, 0, Math.PI*2);
    ctx.fill();
  }

  drawRoseBush(360, 680, 1.3);
  drawRoseBush(240, 780, 1.5);
  drawRoseBush(420, 840, 1.4);
  drawRoseBush(1560, 680, 1.3);
  drawRoseBush(1680, 780, 1.5);
  drawRoseBush(1500, 840, 1.4);

  // Wooden paint bucket & brush
  function drawPaintBucket(bx, by) {
    ctx.fillStyle = "#6e4420";
    ctx.beginPath();
    ctx.moveTo(bx - 26, by);
    ctx.lineTo(bx + 26, by);
    ctx.lineTo(bx + 20, by + 46);
    ctx.lineTo(bx - 20, by + 46);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = "#2b221a";
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.fillStyle = "#d6112c";
    ctx.beginPath();
    ctx.ellipse(bx, by, 25, 8, 0, 0, Math.PI*2);
    ctx.fill();
    ctx.fillRect(bx + 8, by + 4, 6, 26);
    ctx.beginPath();
    ctx.ellipse(bx + 16, by + 46, 32, 10, 0.2, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle = "#996335";
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(bx - 35, by - 14);
    ctx.lineTo(bx + 28, by + 28);
    ctx.stroke();
    ctx.strokeStyle = "#d6112c";
    ctx.lineWidth = 7;
    ctx.beginPath();
    ctx.moveTo(bx + 24, by + 24);
    ctx.lineTo(bx + 35, by + 35);
    ctx.stroke();
  }
  drawPaintBucket(560, 880);

  // Theatrical Stage Framing: Crimson Velvet Drapes
  const drapeGradL = ctx.createLinearGradient(0, 0, 140, 0);
  drapeGradL.addColorStop(0, "#2e0208");
  drapeGradL.addColorStop(0.5, "#690b17");
  drapeGradL.addColorStop(0.85, "#911322");
  drapeGradL.addColorStop(1, "rgba(145, 19, 34, 0)");
  ctx.fillStyle = drapeGradL;
  ctx.fillRect(0, 0, 140, 1080);

  const drapeGradR = ctx.createLinearGradient(1920, 0, 1780, 0);
  drapeGradR.addColorStop(0, "#2e0208");
  drapeGradR.addColorStop(0.5, "#690b17");
  drapeGradR.addColorStop(0.85, "#911322");
  drapeGradR.addColorStop(1, "rgba(145, 19, 34, 0)");
  ctx.fillStyle = drapeGradR;
  ctx.fillRect(1780, 0, 140, 1080);

  // Soft atmospheric spotlight vignette
  const spotGrad = ctx.createRadialGradient(960, 680, 350, 960, 680, 950);
  spotGrad.addColorStop(0, "rgba(255, 230, 200, 0.08)");
  spotGrad.addColorStop(0.7, "rgba(0, 0, 0, 0.15)");
  spotGrad.addColorStop(1, "rgba(0, 0, 0, 0.65)");
  ctx.fillStyle = spotGrad;
  ctx.fillRect(0, 0, 1920, 1080);
</script>
</body>
</html>
"""

html_outro = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; }
  body { width: 1920px; height: 1080px; overflow: hidden; background: #050106; font-family: 'Georgia', serif; }
  canvas { width: 1920px; height: 1080px; }
</style>
</head>
<body>
<canvas id="c" width="1920" height="1080"></canvas>
<script>
  const c = document.getElementById("c");
  const ctx = c.getContext("2d");

  // Background dark velvet
  const bg = ctx.createRadialGradient(960, 540, 100, 960, 540, 900);
  bg.addColorStop(0, "#240713");
  bg.addColorStop(0.5, "#120209");
  bg.addColorStop(1, "#050104");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, 1920, 1080);

  // Theatrical Drapes
  const dL = ctx.createLinearGradient(0, 0, 220, 0);
  dL.addColorStop(0, "#3d040e");
  dL.addColorStop(0.5, "#780d1e");
  dL.addColorStop(1, "rgba(120, 13, 30, 0)");
  ctx.fillStyle = dL;
  ctx.fillRect(0, 0, 220, 1080);

  const dR = ctx.createLinearGradient(1920, 0, 1700, 0);
  dR.addColorStop(0, "#3d040e");
  dR.addColorStop(0.5, "#780d1e");
  dR.addColorStop(1, "rgba(120, 13, 30, 0)");
  ctx.fillStyle = dR;
  ctx.fillRect(1700, 0, 220, 1080);

  const dT = ctx.createLinearGradient(0, 0, 0, 160);
  dT.addColorStop(0, "#3d040e");
  dT.addColorStop(0.7, "#6b0a19");
  dT.addColorStop(1, "rgba(107, 10, 25, 0)");
  ctx.fillStyle = dT;
  ctx.fillRect(0, 0, 1920, 160);

  // Golden Theatrical Filigree Frame
  ctx.strokeStyle = "#d4af37";
  ctx.lineWidth = 4;
  ctx.strokeRect(180, 120, 1560, 840);
  ctx.strokeStyle = "#f5df82";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(196, 136, 1528, 808);

  function drawCorner(x, y, flipX, flipY) {
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(flipX ? -1 : 1, flipY ? -1 : 1);
    ctx.strokeStyle = "#f5df82";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(45, 45, 30, Math.PI, Math.PI*1.5);
    ctx.stroke();
    ctx.fillStyle = "#f5df82";
    ctx.beginPath();
    ctx.arc(32, 32, 6, 0, Math.PI*2);
    ctx.fill();
    ctx.restore();
  }
  drawCorner(180, 120, false, false);
  drawCorner(1740, 120, true, false);
  drawCorner(180, 960, false, true);
  drawCorner(1740, 960, true, true);

  // Center Spotlight
  const spot = ctx.createRadialGradient(960, 520, 50, 960, 520, 480);
  spot.addColorStop(0, "rgba(255, 235, 175, 0.35)");
  spot.addColorStop(0.6, "rgba(255, 215, 130, 0.12)");
  spot.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = spot;
  ctx.beginPath();
  ctx.arc(960, 520, 480, 0, Math.PI*2);
  ctx.fill();

  for (let i = 0; i < 90; i++) {
    const gx = 700 + Math.random() * 520;
    const gy = 320 + Math.random() * 400;
    const gr = 1 + Math.random() * 2.5;
    ctx.fillStyle = `rgba(255, 230, 150, ${0.2 + Math.random()*0.5})`;
    ctx.beginPath();
    ctx.arc(gx, gy, gr, 0, Math.PI*2);
    ctx.fill();
  }

  // Titles
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  ctx.font = "italic 36px Georgia, serif";
  ctx.fillStyle = "#d4af37";
  ctx.fillText("Alice in Wonderland", 960, 420);

  ctx.shadowColor = "rgba(245, 215, 110, 0.9)";
  ctx.shadowBlur = 35;
  ctx.font = "bold 115px 'Georgia', serif";
  ctx.fillStyle = "#fffdf0";
  ctx.fillText("THE END", 960, 530);

  ctx.shadowBlur = 10;
  ctx.fillStyle = "#fce492";
  ctx.fillText("THE END", 960, 530);
  ctx.shadowBlur = 0;

  ctx.strokeStyle = "#d4af37";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(800, 620);
  ctx.lineTo(1120, 620);
  ctx.stroke();
  ctx.fillStyle = "#d4af37";
  ctx.beginPath();
  ctx.arc(960, 620, 6, 0, Math.PI*2);
  ctx.fill();

  ctx.font = "26px Georgia, serif";
  ctx.fillStyle = "rgba(235, 210, 150, 0.85)";
  ctx.fillText("Curtain Call & Final Bow", 960, 670);
</script>
</body>
</html>
"""

def main():
    dest_dir = Path("assets/images")
    dest_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        p1 = browser.new_page(viewport={"width": 1920, "height": 1080})
        p1.set_content(html_scene4)
        p1.screenshot(path=str(dest_dir / "scene4_rosegarden.png"))
        p1.close()
        print("Generated scene4_rosegarden.png (1920x1080)")

        p2 = browser.new_page(viewport={"width": 1920, "height": 1080})
        p2.set_content(html_outro)
        p2.screenshot(path=str(dest_dir / "outro_the_end.png"))
        p2.close()
        print("Generated outro_the_end.png (1920x1080)")

        browser.close()

if __name__ == "__main__":
    main()
