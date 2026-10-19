#!/usr/bin/env python3
import sys, re, shutil, os

CSS = r"""
    /* ===== PATCH: inventário 10x8 sem scroll + hotbar visível no inventário ===== */
    .painel-inv { width: min(920px, 96vw) !important; max-height: 96vh !important; }
    .painel-inv .grade {
      display: grid !important;
      grid-template-columns: repeat(10, min(64px, 7.2vh)) !important;
      grid-auto-rows: min(64px, 7.2vh) !important;
      justify-content: center !important;
      align-content: start !important;
      gap: 6px !important;
      padding: 14px 18px !important;
      max-height: none !important;
      overflow-x: hidden !important;
      overflow-y: auto !important;
      scrollbar-width: none !important;
    }
    .painel-inv .grade::-webkit-scrollbar { display: none !important; }
    .painel-inv .slot {
      width: 100% !important; height: 100% !important; min-width: 0 !important;
      flex-shrink: initial !important;
    }
    .painel-inv .slot svg { width: 55% !important; height: 55% !important; }
    body:has(#inventario:not(.oculto)) #hotbar {
      opacity: 1 !important; pointer-events: auto !important; z-index: 25 !important;
    }
"""

FUMACA = r"""  // ---- fumacinha fria saindo dos difusores (só com refrigeração instalada) ----
  {
    const cvF = document.createElement('canvas'); cvF.width = cvF.height = 64;
    const cxF = cvF.getContext('2d'), grF = cxF.createRadialGradient(32, 32, 0, 32, 32, 32);
    grF.addColorStop(0, 'rgba(255,255,255,.9)'); grF.addColorStop(.5, 'rgba(255,255,255,.35)'); grF.addColorStop(1, 'rgba(255,255,255,0)');
    cxF.fillStyle = grF; cxF.fillRect(0, 0, 64, 64);
    const texF = new THREE.CanvasTexture(cvF);
    const fumos = [];
    xs.forEach(x => zs.forEach(z => {
      for (let i = 0; i < 3; i++) {
        const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: texF, color: 0xbdefff, transparent: true, opacity: 0, depthWrite: false, fog: false }));
        sp.raycast = () => {}; sp.visible = false; grp.add(sp);
        fumos.push({ sp, x, z, t: i / 3 + Math.random() * .1, vel: .22 + Math.random() * .08, dx: (Math.random() - .5) * .5, dz: (Math.random() - .5) * .5 });
      }
    }));
    ATUALIZAVEIS.push(dt => {
      const k = Math.min(1, coolingTotal() / 8);
      fumos.forEach(f => {
        if (k <= 0) { f.sp.visible = false; return; }
        f.t = (f.t + dt * f.vel) % 1;
        const u = f.t;
        f.sp.visible = true;
        f.sp.position.set(f.x + f.dx * u, 3.6 - u * 1.1, f.z + f.dz * u);
        f.sp.scale.setScalar(.35 + u * .9);
        f.sp.material.opacity = .5 * k * Math.sin(Math.PI * u);
      });
    });
  }

  """


def main():
    if len(sys.argv) != 2:
        print("Uso: python corrigir.py arquivo.html")
        sys.exit(1)
    src = sys.argv[1]
    if not os.path.isfile(src):
        print(f"Erro: arquivo não encontrado: {src}")
        sys.exit(1)
    try:
        with open(src, "r", encoding="utf-8", newline="") as f:
            html = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    base, ext = os.path.splitext(src)
    bak = base + ".bak" + ext
    out = base + "_corrigido" + ext
    try:
        if not os.path.exists(bak):
            shutil.copy2(src, bak)
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        sys.exit(1)

    # 1) fumaça fria nos difusores
    m = re.search(r"[ \t]*// ---- animacao: o fluxo e o brilho dependem da refrigeracao instalada ----", html)
    if not m:
        print("Erro: trecho de animação do dutoClima não encontrado.")
        sys.exit(1)
    html = html[:m.start()] + FUMACA + html[m.start():].lstrip(" \t") if False else html[:m.start()] + FUMACA + html[m.start():]

    # 2) inventário com 80 slots (10x8)
    html, n = re.subn(
        r"const total = Math\.max\(16, Math\.ceil\(\(pilhas\.length \+ 1\) / 8\) \* 8\);",
        "const total = Math.max(80, Math.ceil(pilhas.length / 10) * 10);",
        html, count=1)
    if n != 1:
        print("Erro: trecho do inventário (total de slots) não encontrado.")
        sys.exit(1)

    # 3) CSS
    idx = html.find("</style>")
    if idx < 0:
        print("Erro: </style> não encontrado.")
        sys.exit(1)
    html = html[:idx] + CSS + "  " + html[idx:]

    try:
        with open(out, "w", encoding="utf-8", newline="") as f:
            f.write(html)
    except Exception as e:
        print(f"Erro ao gravar saída: {e}")
        sys.exit(1)
    print(f"OK: {out}\nBackup: {bak}")


if __name__ == "__main__":
    main()