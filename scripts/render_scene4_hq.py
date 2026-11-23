from playwright.sync_api import sync_playwright
from pathlib import Path

html_scene4_hq = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; }
  body { width: 1920px; height: 1080px; overflow: hidden; background: #000; }
  canvas { width: 1920px; height: 1080px; display: block; }
</style>
</head>
<body>
<canvas id="c" width="1920" height="1080"></canvas>
<script>
  const c = document.getElementById("c");
  const ctx = c.getContext("2d");

  // ==========================================
  // 1. CINEMATIC TWILIGHT SKY & VOLUMETRIC GLOW
  // ==========================================
  const skyGrad = ctx.createLinearGradient(0, 0, 0, 680);
  skyGrad.addColorStop(0.0, "#0c0214");
  skyGrad.addColorStop(0.2, "#1a0624");
  skyGrad.addColorStop(0.4, "#3d0a32");
  skyGrad.addColorStop(0.6, "#78143a");
  skyGrad.addColorStop(0.8, "#bd2e3a");
  skyGrad.addColorStop(0.92, "#f06c3a");
  skyGrad.addColorStop(1.0, "#ffb86c");
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, 1920, 680);

  // Volumetric Sunburst / Sunset Glow behind castle
  const sunGlow = ctx.createRadialGradient(960, 480, 20, 960, 480, 550);
  sunGlow.addColorStop(0.0, "rgba(255, 240, 200, 0.75)");
  sunGlow.addColorStop(0.25, "rgba(255, 170, 90, 0.5)");
  sunGlow.addColorStop(0.6, "rgba(210, 60, 80, 0.25)");
  sunGlow.addColorStop(1.0, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = sunGlow;
  ctx.fillRect(0, 0, 1920, 680);

  // Soft atmospheric clouds
  function drawCloud(cx, cy, rx, ry, col) {
    ctx.save();
    ctx.filter = "blur(18px)";
    ctx.fillStyle = col;
    ctx.beginPath();
    ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
  drawCloud(350, 320, 260, 70, "rgba(240, 110, 80, 0.4)");
  drawCloud(620, 260, 320, 80, "rgba(180, 50, 90, 0.45)");
  drawCloud(1380, 280, 340, 85, "rgba(190, 60, 90, 0.45)");
  drawCloud(1650, 340, 280, 75, "rgba(240, 120, 80, 0.4)");

  // ==========================================
  // 2. GRAND GOTHIC FANTASY CASTLE (QUEEN OF HEARTS)
  // ==========================================
  // Mountain silhouettes behind castle
  ctx.fillStyle = "#16051f";
  ctx.beginPath();
  ctx.moveTo(0, 560);
  ctx.lineTo(380, 430);
  ctx.lineTo(720, 510);
  ctx.lineTo(960, 450);
  ctx.lineTo(1250, 520);
  ctx.lineTo(1600, 420);
  ctx.lineTo(1920, 550);
  ctx.lineTo(1920, 600);
  ctx.lineTo(0, 600);
  ctx.fill();

  // Helper for shaded 3D towers with conical roofs
  function drawTower(x, baseY, width, height, roofHeight, hasFlag=true) {
    ctx.save();
    // Tower body gradient (left light, right shadow)
    const bodyGrad = ctx.createLinearGradient(x - width/2, 0, x + width/2, 0);
    bodyGrad.addColorStop(0, "#4a1228");
    bodyGrad.addColorStop(0.3, "#731d3e");
    bodyGrad.addColorStop(0.7, "#3b0c1e");
    bodyGrad.addColorStop(1, "#1a040d");
    ctx.fillStyle = bodyGrad;
    ctx.fillRect(x - width/2, baseY - height, width, height);

    // Battlements on top
    const bW = width / 5;
    for (let i = 0; i < 5; i += 2) {
      ctx.fillRect(x - width/2 + i * bW, baseY - height - 12, bW, 14);
    }

    // Glowing arched windows
    for (let wy = baseY - height + 40; wy < baseY - 30; wy += 55) {
      const winGrad = ctx.createRadialGradient(x, wy, 2, x, wy, 12);
      winGrad.addColorStop(0, "#fff5cc");
      winGrad.addColorStop(0.6, "#ffaa33");
      winGrad.addColorStop(1, "#7a1a08");
      ctx.fillStyle = winGrad;
      ctx.beginPath();
      ctx.arc(x, wy, 7, Math.PI, 0);
      ctx.rect(x - 7, wy, 14, 14);
      ctx.fill();
    }

    // Roof cone gradient
    const roofGrad = ctx.createLinearGradient(x - width*0.55, 0, x + width*0.55, 0);
    roofGrad.addColorStop(0, "#821a28");
    roofGrad.addColorStop(0.35, "#ba283b");
    roofGrad.addColorStop(0.75, "#520c17");
    roofGrad.addColorStop(1, "#26040a");
    ctx.fillStyle = roofGrad;
    ctx.beginPath();
    ctx.moveTo(x - width * 0.58, baseY - height);
    ctx.lineTo(x, baseY - height - roofHeight);
    ctx.lineTo(x + width * 0.58, baseY - height);
    ctx.closePath();
    ctx.fill();

    // Gold finial & heart motif
    ctx.fillStyle = "#f5c842";
    ctx.beginPath();
    ctx.arc(x, baseY - height - roofHeight - 4, 4, 0, Math.PI*2);
    ctx.fill();

    // Red Queen Banner / Flag
    if (hasFlag) {
      ctx.fillStyle = "#e01b38";
      ctx.beginPath();
      ctx.moveTo(x, baseY - height - roofHeight - 4);
      ctx.lineTo(x + 24, baseY - height - roofHeight - 14);
      ctx.lineTo(x + 18, baseY - height - roofHeight - 6);
      ctx.lineTo(x + 26, baseY - height - roofHeight + 2);
      ctx.lineTo(x, baseY - height - roofHeight + 6);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();
  }

  // Main Castle Complex
  // Center Keep
  const keepGrad = ctx.createLinearGradient(840, 0, 1080, 0);
  keepGrad.addColorStop(0, "#33081b");
  keepGrad.addColorStop(0.35, "#5c1332");
  keepGrad.addColorStop(0.8, "#2e0617");
  keepGrad.addColorStop(1, "#12020a");
  ctx.fillStyle = keepGrad;
  ctx.fillRect(850, 280, 220, 260);

  // Large Grand Spire
  drawTower(960, 480, 68, 260, 160, true);
  // Symmetrical flank towers
  drawTower(880, 500, 46, 210, 110, true);
  drawTower(1040, 500, 46, 210, 110, true);
  drawTower(800, 520, 36, 170, 90, false);
  drawTower(1120, 520, 36, 170, 90, false);
  drawTower(730, 540, 30, 140, 75, false);
  drawTower(1190, 540, 30, 140, 75, false);

  // Castle Entrance Arch & Giant Glowing Heart Stained-Glass
  const heartGlow = ctx.createRadialGradient(960, 410, 10, 960, 410, 45);
  heartGlow.addColorStop(0, "#ffffff");
  heartGlow.addColorStop(0.4, "#ff3366");
  heartGlow.addColorStop(0.85, "#990022");
  heartGlow.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = heartGlow;
  ctx.beginPath();
  ctx.arc(960, 410, 45, 0, Math.PI*2);
  ctx.fill();

  // Heart symbol
  ctx.fillStyle = "#ff1a48";
  function drawHeart(hx, hy, s) {
    ctx.beginPath();
    ctx.moveTo(hx, hy + s * 0.7);
    ctx.bezierCurveTo(hx - s, hy, hx - s * 1.2, hy - s * 0.7, hx, hy - s * 0.25);
    ctx.bezierCurveTo(hx + s * 1.2, hy - s * 0.7, hx + s, hy, hx, hy + s * 0.7);
    ctx.fill();
  }
  drawHeart(960, 405, 22);

  // Atmospheric distance haze over castle base
  const hazeGrad = ctx.createLinearGradient(0, 470, 0, 550);
  hazeGrad.addColorStop(0, "rgba(220, 90, 60, 0)");
  hazeGrad.addColorStop(0.7, "rgba(240, 120, 70, 0.45)");
  hazeGrad.addColorStop(1, "rgba(180, 40, 50, 0.7)");
  ctx.fillStyle = hazeGrad;
  ctx.fillRect(650, 470, 620, 80);

  // ==========================================
  // 3. PERSPECTIVE CHECKERED MARBLE COURTYARD FLOOR
  // ==========================================
  const horizonY = 530;
  const numRows = 24;
  const numCols = 26;
  const vpX = 960;

  for (let r = 0; r < numRows; r++) {
    const t0 = Math.pow(r / numRows, 2.7);
    const t1 = Math.pow((r + 1) / numRows, 2.7);
    const y0 = horizonY + t0 * (1080 - horizonY);
    const y1 = horizonY + t1 * (1080 - horizonY);

    for (let c_idx = -numCols/2; c_idx < numCols/2; c_idx++) {
      const spread0 = (t0 + 0.045);
      const spread1 = (t1 + 0.045);
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

      const depth = 0.35 + 0.65 * t1;
      if (isCrimson) {
        // Deep royal crimson marble with specular highlight
        const tileGrad = ctx.createLinearGradient(x0_l, y0, x1_r, y1);
        tileGrad.addColorStop(0, `rgb(${Math.round(140*depth)}, ${Math.round(10*depth)}, ${Math.round(25*depth)})`);
        tileGrad.addColorStop(0.4, `rgb(${Math.round(200*depth)}, ${Math.round(20*depth)}, ${Math.round(42*depth)})`);
        tileGrad.addColorStop(1, `rgb(${Math.round(110*depth)}, ${Math.round(8*depth)}, ${Math.round(20*depth)})`);
        ctx.fillStyle = tileGrad;
      } else {
        // Polished white marble reflecting warm sunset gold
        const tileGrad = ctx.createLinearGradient(x0_l, y0, x1_r, y1);
        tileGrad.addColorStop(0, `rgb(${Math.round(250*depth)}, ${Math.round(242*depth)}, ${Math.round(230*depth)})`);
        tileGrad.addColorStop(0.5, `rgb(${Math.round(255*depth)}, ${Math.round(248*depth)}, ${Math.round(240*depth)})`);
        tileGrad.addColorStop(1, `rgb(${Math.round(230*depth)}, ${Math.round(220*depth)}, ${Math.round(210*depth)})`);
        ctx.fillStyle = tileGrad;
      }
      ctx.fill();

      // Subtle tile bevel border
      ctx.strokeStyle = "rgba(40, 5, 12, 0.35)";
      ctx.lineWidth = Math.max(1, t1 * 2.2);
      ctx.stroke();
    }
  }

  // ==========================================
  // 4. LUSH TOPIARY HEDGE MAZES (LEFT & RIGHT WINGS)
  // ==========================================
  function drawLushHedge(startX, width, isLeft) {
    ctx.save();
    // Base hedge gradient
    const hGrad = ctx.createLinearGradient(startX, 0, startX + width, 0);
    if (isLeft) {
      hGrad.addColorStop(0, "#081c0e");
      hGrad.addColorStop(0.4, "#0f3318");
      hGrad.addColorStop(0.85, "#1b5228");
      hGrad.addColorStop(1, "#0d2b14");
    } else {
      hGrad.addColorStop(0, "#0d2b14");
      hGrad.addColorStop(0.15, "#1b5228");
      hGrad.addColorStop(0.6, "#0f3318");
      hGrad.addColorStop(1, "#081c0e");
    }
    ctx.fillStyle = hGrad;
    ctx.fillRect(startX, 320, width, 760);

    // Rich multi-layered foliage texture
    for (let i = 0; i < 900; i++) {
      const fx = startX + Math.random() * width;
      const fy = 320 + Math.random() * 760;
      const fr = 10 + Math.random() * 22;
      const randC = Math.random();
      if (randC > 0.65) {
        ctx.fillStyle = "rgba(45, 115, 55, 0.45)"; // highlight leaf
      } else if (randC > 0.3) {
        ctx.fillStyle = "rgba(22, 65, 32, 0.5)"; // midtone
      } else {
        ctx.fillStyle = "rgba(8, 28, 14, 0.55)"; // deep shadow
      }
      ctx.beginPath();
      ctx.arc(fx, fy, fr, 0, Math.PI * 2);
      ctx.fill();
    }

    // Topiary heart finials trimmed out of top hedge
    ctx.fillStyle = "#164722";
    const hx = isLeft ? startX + width * 0.72 : startX + width * 0.28;
    drawHeart(hx, 280, 52);
    // Gold ornamental crown on heart topiary
    ctx.fillStyle = "#f5c842";
    ctx.beginPath();
    ctx.arc(hx, 240, 8, 0, Math.PI*2);
    ctx.fill();

    ctx.restore();
  }
  drawLushHedge(-60, 520, true);
  drawLushHedge(1460, 520, false);

  // ==========================================
  // 5. GRAND ROYAL PALACE GATE (CRIMSON & GOLD FILIGREE)
  // ==========================================
  // Marble Gate Pillars
  function drawMarblePillar(px) {
    const pilGrad = ctx.createLinearGradient(px - 45, 0, px + 45, 0);
    pilGrad.addColorStop(0, "#380e18");
    pilGrad.addColorStop(0.3, "#781c30");
    pilGrad.addColorStop(0.7, "#99243d");
    pilGrad.addColorStop(1, "#260810");
    ctx.fillStyle = pilGrad;
    ctx.fillRect(px - 40, 340, 80, 420);

    // Beveled capital & base
    ctx.fillStyle = "#e0b038";
    ctx.fillRect(px - 50, 322, 100, 20);
    ctx.fillRect(px - 46, 745, 92, 18);
    // Gold Heart Finial atop pillar
    ctx.fillStyle = "#f7d25a";
    drawHeart(px, 290, 32);
    // Glowing ruby gem in center of heart
    ctx.fillStyle = "#ff113a";
    drawHeart(px, 292, 16);
  }
  drawMarblePillar(510);
  drawMarblePillar(1410);

  // Wrought Iron Arches with Heart Filigree
  ctx.save();
  ctx.strokeStyle = "#8c1628";
  ctx.lineWidth = 12;
  ctx.beginPath();
  ctx.arc(960, 520, 450, Math.PI, Math.PI * 2);
  ctx.stroke();

  ctx.strokeStyle = "#e8b835";
  ctx.lineWidth = 5;
  ctx.beginPath();
  ctx.arc(960, 520, 435, Math.PI, Math.PI * 2);
  ctx.stroke();

  // Vertical gate spears with heart heads
  for (let gx = 560; gx <= 1360; gx += 48) {
    if (Math.abs(gx - 960) < 65) continue; // center ceremonial opening
    const spearGrad = ctx.createLinearGradient(gx - 4, 0, gx + 4, 0);
    spearGrad.addColorStop(0, "#330812");
    spearGrad.addColorStop(0.5, "#7a1428");
    spearGrad.addColorStop(1, "#1f040a");
    ctx.fillStyle = spearGrad;
    ctx.fillRect(gx - 4, 520, 8, 220);

    // Golden Spear Heart Tips
    ctx.fillStyle = "#f5c842";
    drawHeart(gx, 514, 9);
  }
  ctx.restore();

  // ==========================================
  // 6. LUSH ROSE BUSHES & DRIPPING RED PAINT (KEY STORY ELEMENT)
  // ==========================================
  // Detailed organic rose petals
  function drawDetailedRose(x, y, radius, outerColor, innerColor, isHalfPainted=false) {
    ctx.save();
    // Rose base shadow
    ctx.fillStyle = "rgba(10, 0, 5, 0.4)";
    ctx.beginPath();
    ctx.arc(x + 2, y + 4, radius, 0, Math.PI * 2);
    ctx.fill();

    // Outer petals
    ctx.fillStyle = isHalfPainted ? "#f7f7f7" : outerColor;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();

    // Petal whorls
    for (let p = 0; p < 7; p++) {
      const angle = (p / 7) * Math.PI * 2;
      const px = x + Math.cos(angle) * radius * 0.4;
      const py = y + Math.sin(angle) * radius * 0.4;
      ctx.fillStyle = isHalfPainted ? "#eaeaea" : innerColor;
      ctx.beginPath();
      ctx.arc(px, py, radius * 0.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Center bud
    ctx.fillStyle = isHalfPainted ? "#ffffff" : "#ffe6ea";
    ctx.beginPath();
    ctx.arc(x, y, radius * 0.25, 0, Math.PI * 2);
    ctx.fill();

    // If Half-Painted: Dripping Crimson Red Paint!
    if (isHalfPainted) {
      // Paint overlay over top-right half
      ctx.fillStyle = "#d1112e";
      ctx.beginPath();
      ctx.arc(x, y, radius, Math.PI * 0.7, Math.PI * 1.95);
      ctx.closePath();
      ctx.fill();

      // Dripping wet paint drips down petals
      ctx.fillStyle = "#b80922";
      ctx.fillRect(x - radius * 0.35, y + radius * 0.1, 5, 24);
      ctx.fillRect(x + radius * 0.15, y + radius * 0.3, 4, 32);
      ctx.fillRect(x - radius * 0.05, y + radius * 0.2, 3.5, 18);

      // Rounded droplet ends
      ctx.beginPath();
      ctx.arc(x - radius * 0.35 + 2.5, y + radius * 0.1 + 24, 3.5, 0, Math.PI * 2);
      ctx.arc(x + radius * 0.15 + 2, y + radius * 0.3 + 32, 3, 0, Math.PI * 2);
      ctx.fill();

      // Wet paint gloss shine
      ctx.fillStyle = "rgba(255, 255, 255, 0.45)";
      ctx.beginPath();
      ctx.arc(x + radius * 0.3, y - radius * 0.3, 3, 0, Math.PI*2);
      ctx.fill();
    }
    ctx.restore();
  }

  function drawRoseBushCluster(cx, cy, scale) {
    // Deep green foliage cluster
    for (let i = 0; i < 35; i++) {
      const lx = cx + (Math.random() - 0.5) * 190 * scale;
      const ly = cy + (Math.random() - 0.5) * 140 * scale;
      ctx.fillStyle = Math.random() > 0.5 ? "#123d1d" : "#0d2b14";
      ctx.beginPath();
      ctx.ellipse(lx, ly, 22 * scale, 12 * scale, Math.random() * 3, 0, Math.PI * 2);
      ctx.fill();
    }

    // Crimson red roses
    for (let r = 0; r < 11; r++) {
      const rx = cx + (Math.random() - 0.5) * 160 * scale;
      const ry = cy + (Math.random() - 0.5) * 110 * scale;
      drawDetailedRose(rx, ry, (16 + Math.random() * 6) * scale, "#d91432", "#87081a", false);
    }

    // Half-painted white roses dripping paint
    for (let w = 0; w < 5; w++) {
      const wx = cx + (Math.random() - 0.5) * 140 * scale;
      const wy = cy + (Math.random() - 0.5) * 95 * scale;
      drawDetailedRose(wx, wy, (18 + Math.random() * 5) * scale, "#ffffff", "#e0e0e0", true);
    }
  }

  // Draw Rose Bushes along the hedge bases
  drawRoseBushCluster(380, 680, 1.35);
  drawRoseBushCluster(230, 780, 1.55);
  drawRoseBushCluster(440, 850, 1.45);

  drawRoseBushCluster(1540, 680, 1.35);
  drawRoseBushCluster(1690, 780, 1.55);
  drawRoseBushCluster(1480, 850, 1.45);

  // Abandoned Wooden Paint Bucket & Paint Splatter on Checkered Tiles
  function drawPaintBucketSetup(bx, by) {
    ctx.save();
    // Red paint spill puddle on checkered tiles
    ctx.fillStyle = "#c40c27";
    ctx.beginPath();
    ctx.ellipse(bx + 25, by + 50, 48, 16, 0.2, 0, Math.PI * 2);
    ctx.fill();

    // Spilled droplet splatters
    for (let i = 0; i < 8; i++) {
      const sx = bx + 25 + (Math.random() - 0.5) * 90;
      const sy = by + 50 + (Math.random() - 0.5) * 28;
      ctx.beginPath();
      ctx.arc(sx, sy, 3 + Math.random() * 3.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Wooden Bucket
    const bGrad = ctx.createLinearGradient(bx - 32, 0, bx + 32, 0);
    bGrad.addColorStop(0, "#4a2d16");
    bGrad.addColorStop(0.4, "#7a4a24");
    bGrad.addColorStop(0.8, "#573419");
    bGrad.addColorStop(1, "#2e1a0b");
    ctx.fillStyle = bGrad;
    ctx.beginPath();
    ctx.moveTo(bx - 30, by);
    ctx.lineTo(bx + 30, by);
    ctx.lineTo(bx + 22, by + 52);
    ctx.lineTo(bx - 22, by + 52);
    ctx.closePath();
    ctx.fill();

    // Iron bands
    ctx.strokeStyle = "#1a120c";
    ctx.lineWidth = 4;
    ctx.stroke();

    // Fresh red paint overflowing top
    ctx.fillStyle = "#d6112c";
    ctx.beginPath();
    ctx.ellipse(bx, by, 29, 9, 0, 0, Math.PI * 2);
    ctx.fill();

    // Drips down bucket wood
    ctx.fillRect(bx + 6, by + 5, 8, 30);
    ctx.fillRect(bx - 14, by + 4, 6, 20);

    // Paintbrush resting in bucket
    ctx.strokeStyle = "#a36e3c";
    ctx.lineWidth = 7;
    ctx.beginPath();
    ctx.moveTo(bx - 38, by - 20);
    ctx.lineTo(bx + 32, by + 34);
    ctx.stroke();

    // Wet red bristle tip
    ctx.strokeStyle = "#d6112c";
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(bx + 28, by + 28);
    ctx.lineTo(bx + 40, by + 42);
    ctx.stroke();
    ctx.restore();
  }
  drawPaintBucketSetup(580, 890);

  // ==========================================
  // 7. THEATRICAL LIGHTING & PROSCENIUM CURTAIN VIGNETTE
  // ==========================================
  // Rich Velvet Drapes at edges
  const drapeL = ctx.createLinearGradient(0, 0, 160, 0);
  drapeL.addColorStop(0.0, "#240106");
  drapeL.addColorStop(0.4, "#590914");
  drapeL.addColorStop(0.85, "#800e1e");
  drapeL.addColorStop(1.0, "rgba(128, 14, 30, 0)");
  ctx.fillStyle = drapeL;
  ctx.fillRect(0, 0, 160, 1080);

  const drapeR = ctx.createLinearGradient(1920, 0, 1760, 0);
  drapeR.addColorStop(0.0, "#240106");
  drapeR.addColorStop(0.4, "#590914");
  drapeR.addColorStop(0.85, "#800e1e");
  drapeR.addColorStop(1.0, "rgba(128, 14, 30, 0)");
  ctx.fillStyle = drapeR;
  ctx.fillRect(1760, 0, 160, 1080);

  // Theatrical Golden Spotlight Vignette
  const spotGrad = ctx.createRadialGradient(960, 680, 320, 960, 680, 980);
  spotGrad.addColorStop(0.0, "rgba(255, 230, 190, 0.08)");
  spotGrad.addColorStop(0.65, "rgba(0, 0, 0, 0.12)");
  spotGrad.addColorStop(1.0, "rgba(0, 0, 0, 0.68)");
  ctx.fillStyle = spotGrad;
  ctx.fillRect(0, 0, 1920, 1080);
</script>
</body>
</html>
"""

def main():
    dest_path = Path("assets/images/scene4_rosegarden.png")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.set_content(html_scene4_hq)
        page.screenshot(path=str(dest_path))
        browser.close()
    print(f"Generated High-Quality Scene 4: {dest_path} (1920x1080)")

if __name__ == "__main__":
    main()
