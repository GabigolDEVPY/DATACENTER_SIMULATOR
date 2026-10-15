#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch: VISUAL FUTURISTA das evoluções (Painel Solar, Turbina, Gerador, Refrigerador).

Uso:
    python melhorar_evolucoes.py                      -> lê index.html, grava index_corrigido.html
    python melhorar_evolucoes.py meu.html saida.html  -> caminhos personalizados

Rode DEPOIS do patch do gerador a gasolina (funciona sem ele, mas as luzes do reator do gerador
só acompanham o liga/desliga se aquele patch estiver aplicado).

O que muda:
  PAINEL SOLAR   nv1 células com grade e moldura de alumínio · nv2 grade neon + inversor com LED
                 · nv3 vidro negro, moldura neon, varredura de energia, anéis no poste e brilho no chão.
  TURBINA        nv1 base reforçada · nv2 anéis de luz subindo a torre, pontas das pás iluminadas,
                 cone na hélice e luz de aviso · nv3 anel-duto neon em volta do rotor, halo de pás,
                 anéis violeta na torre e pulso de energia no chão.
  GERADOR        nv1 chapa, venezianas e painel digital · nv2 pintura grafite, faixas neon, anéis no escape
                 · nv3 carcaça preta cromada, reator com anéis giratórios (acelera quando ligado), antena,
                 tiras neon e brilho sob a base.
  REFRIGERADOR   nv1 grade e fluxo de ar frio · nv2 cinto neon + indicadores · nv3 colar criogênico
                 · nv4 aletas grafite com borda neon · nv5 tubos de líquido refrigerante
                 · nv6 segundo rotor, núcleo holográfico com órbitas e marca no piso.
"""
import sys
import pathlib

ENTRADA = sys.argv[1] if len(sys.argv) > 1 else "index.html"
SAIDA = sys.argv[2] if len(sys.argv) > 2 else "index_corrigido.html"
MARCA = "PATCH-EVOLUCOES-VISUAIS"

# ---------------------------------------------------------------------------
# 1) Substitui aplicarVisualEvolucao (painel / gerador / turbina) por um despachante
# ---------------------------------------------------------------------------
APLICAR_JS = r"""function aplicarVisualEvolucao(mesh, nivel, tipo) {
    // visual futurista das evoluções: ver o bloco FX (perto do refrigerador de teto)
    if (!mesh) return;
    nivel = Math.max(1, Math.min(3, nivel || 1));
    if (tipo === 'painel') FX.painel(mesh, nivel);
    else if (tipo === 'gerador') FX.gerador(mesh, nivel);
    else if (tipo === 'turbina') FX.turbina(mesh, nivel);
  }"""

# ---------------------------------------------------------------------------
# 2) Infraestrutura de efeitos (global) + novo aplicarNivelCooler
# ---------------------------------------------------------------------------
FX_JS = r"""/* PATCH-EVOLUCOES-VISUAIS */
// ===== EVOLUÇÕES FUTURISTAS (painel · gerador · turbina · refrigerador) =====
// Todo o visual das evoluções vive neste bloco. Cores e níveis ficam nas tabelas de cada função.
const FX = (() => {
  const PI = Math.PI;
  const T = { t: 0 };
  const lista = [];                                   // { obj, fn } — o efeito some sozinho quando o objeto sai do mundo
  const reg = (obj, fn) => lista.push({ obj, fn });

  // ---------- materiais e peças ----------
  const neon = (cor, k = 1.2) => new THREE.MeshStandardMaterial({ color: 0x0a0e13, emissive: cor, emissiveIntensity: k, roughness: .35, metalness: .4 });
  const metal = (cor, m = .8, r = .3) => new THREE.MeshStandardMaterial({ color: cor, metalness: m, roughness: r });
  const vidro = (cor, op, emi = 0x000000, k = 0) => new THREE.MeshStandardMaterial({ color: cor, metalness: .9, roughness: .08, transparent: true, opacity: op, emissive: emi, emissiveIntensity: k, depthWrite: false });
  const aditivo = (cor, op) => new THREE.MeshBasicMaterial({ color: cor, transparent: true, opacity: op, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });

  const tela = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; };
  const tex = c => { const t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t; };
  const GLOW = (() => {
    const [c, x] = tela(64, 64), g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.3, 'rgba(255,255,255,.45)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = g; x.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  })();

  // toda peça decorativa fica "transparente" para a mira (não atrapalha o F / G)
  const peca = (pai, geo, mat, x = 0, y = 0, z = 0, sombra = false) => {
    const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = sombra;
    m.raycast = () => {}; pai.add(m); return m;
  };
  const caixa = (pai, w, h, d, mat, x, y, z, s) => peca(pai, new THREE.BoxGeometry(w, h, d), mat, x, y, z, s);
  const anel = (pai, R, tubo, mat, x, y, z, plano = true, seg = 40) => {
    const m = peca(pai, new THREE.TorusGeometry(R, tubo, 8, seg), mat, x, y, z);
    if (plano) m.rotation.x = PI / 2;                 // plano = deitado; senão fica de pé (olhando para +z)
    return m;
  };
  const brilho = (pai, cor, esc, op, x = 0, y = 0, z = 0) => {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: cor, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false, opacity: op }));
    s.scale.setScalar(esc); s.position.set(x, y, z); s.raycast = () => {}; pai.add(s); return s;
  };

  // materiais compartilhados que pulsam (um único update por frame para todos os equipamentos)
  const P = {
    torre2: [0, 1, 2, 3, 4, 5].map(() => neon(0x3adfff, .6)),
    torre3: [0, 1, 2, 3, 4, 5].map(() => neon(0xa58bff, .6)),
    ponta: neon(0x3adfff, 1.5), faixa: neon(0x3adfff, 1.3), anel: neon(0x6fe9ff, 1.4),
    aviso: neon(0xff3b30, 1.5), avisoCiano: neon(0x3adfff, 1.5), led: neon(0x3dff7c, 1.2),
    base: neon(0x3dffd0, 1.2), fluido: neon(0x3adfff, 1.4), nucleo: neon(0xbff6ff, 1.5), violeta: neon(0x8a7bff, 1.5)
  };
  ATUALIZAVEIS.push(dt => {
    const t = (T.t += dt);
    P.torre2.forEach((m, i) => { m.emissiveIntensity = .25 + 1.3 * Math.max(0, Math.sin(t * 2.6 - i * .8)); });
    P.torre3.forEach((m, i) => { m.emissiveIntensity = .3 + 1.5 * Math.max(0, Math.sin(t * 3.4 - i * .8)); });
    P.faixa.emissiveIntensity = 1.0 + .5 * Math.sin(t * 2.2);
    P.anel.emissiveIntensity = 1.2 + .5 * Math.sin(t * 3);
    P.ponta.emissiveIntensity = 1.3 + .5 * Math.sin(t * 6);
    const pisca = Math.sin(t * 4.5) > .55 ? 2.4 : .12;
    P.aviso.emissiveIntensity = pisca; P.avisoCiano.emissiveIntensity = pisca;
    P.led.emissiveIntensity = .8 + .6 * Math.max(0, Math.sin(t * 3));
    P.base.emissiveIntensity = 1.0 + .5 * Math.sin(t * 2.6 + 1);
    P.fluido.emissiveIntensity = 1.0 + .7 * Math.sin(t * 5);
    P.nucleo.emissiveIntensity = 1.2 + .6 * Math.sin(t * 4);
    P.violeta.emissiveIntensity = 1.2 + .5 * Math.sin(t * 2.8);
    for (let i = lista.length - 1; i >= 0; i--) {
      const e = lista[i];
      if (!e.obj.parent) { lista.splice(i, 1); continue; }
      e.fn(dt, t);
    }
  });

  // ---------- texturas (geradas uma vez por nível) ----------
  const cache = {};
  const texPainel = nv => cache['p' + nv] || (cache['p' + nv] = (() => {
    const W = 512, H = 256, cols = 8, rows = 5, cw = W / cols, ch = H / rows;
    const [c1, a] = tela(W, H), [c2, b] = tela(W, H);
    const fundo = [['#1a2d52', '#0c1a38'], ['#103266', '#071a3f'], ['#080c18', '#020409']][nv - 1];
    const g = a.createLinearGradient(0, 0, W, H); g.addColorStop(0, fundo[0]); g.addColorStop(1, fundo[1]);
    a.fillStyle = g; a.fillRect(0, 0, W, H);
    b.fillStyle = '#000'; b.fillRect(0, 0, W, H);
    const barras = (ctx, cor) => {                    // barras coletoras dentro de cada célula
      ctx.strokeStyle = cor; ctx.lineWidth = 1;
      for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) for (let k = 1; k <= 3; k++) {
        ctx.beginPath(); ctx.moveTo(i * cw + k * cw / 4, j * ch + 4); ctx.lineTo(i * cw + k * cw / 4, (j + 1) * ch - 4); ctx.stroke();
      }
    };
    barras(a, nv === 3 ? 'rgba(108,243,255,.20)' : 'rgba(150,180,230,.22)');
    const linha = ['#7d93bf', '#52b8ff', '#6cf3ff'][nv - 1];
    const grade = (ctx, cor, lw) => {
      ctx.strokeStyle = cor; ctx.lineWidth = lw;
      for (let i = 0; i <= cols; i++) { ctx.beginPath(); ctx.moveTo(i * cw, 0); ctx.lineTo(i * cw, H); ctx.stroke(); }
      for (let j = 0; j <= rows; j++) { ctx.beginPath(); ctx.moveTo(0, j * ch); ctx.lineTo(W, j * ch); ctx.stroke(); }
    };
    grade(a, linha, nv === 1 ? 2 : 3);
    if (nv >= 2) {
      grade(b, linha, 3);
      const sh = a.createLinearGradient(0, 0, W, H);   // reflexo diagonal no vidro
      sh.addColorStop(0, 'rgba(255,255,255,0)'); sh.addColorStop(.5, 'rgba(120,200,255,.10)'); sh.addColorStop(1, 'rgba(255,255,255,0)');
      a.fillStyle = sh; a.fillRect(0, 0, W, H);
    }
    if (nv === 3) barras(b, 'rgba(108,243,255,.35)');
    return { map: tex(c1), emi: tex(c2) };
  })());

  const texDisp = nv => cache['d' + nv] || (cache['d' + nv] = (() => {
    const [c, x] = tela(512, 160);
    const cor = ['#ffb347', '#3adfff', '#b9a6ff'][nv - 1], kw = [10, 15, 22][nv - 1];
    x.fillStyle = '#04080c'; x.fillRect(0, 0, 512, 160);
    x.strokeStyle = cor; x.lineWidth = 4; x.strokeRect(6, 6, 500, 148);
    x.fillStyle = cor; x.textAlign = 'left';
    x.font = '600 28px "Segoe UI", Arial, sans-serif'; x.fillText('GERADOR', 26, 46);
    x.font = '800 84px "Segoe UI", Arial, sans-serif'; x.fillText('NV ' + nv, 26, 128);
    x.textAlign = 'right'; x.font = '800 66px "Segoe UI", Arial, sans-serif'; x.fillText(kw + ' kW', 486, 112);
    x.textAlign = 'left';
    for (let i = 0; i < 3; i++) { x.globalAlpha = i < nv ? 1 : .2; x.fillRect(330 + i * 52, 30, 44, 14); }
    x.globalAlpha = 1;
    return tex(c);
  })());

  // =====================================================================
  // PAINEL SOLAR (grupo: placa inclinada + poste)
  // =====================================================================
  function painel(mesh, nv) {
    const u = mesh.userData;
    if (!u._fxP) {
      const placa = mesh.children.find(c => c.isMesh && Math.abs(c.rotation.x) > .1);
      if (!placa) return;
      u._fxP = placa;
      // as duas barras soltas do modelo antigo saem; entra uma moldura de verdade, presa à placa
      mesh.children.filter(c => c.isMesh && c.geometry.parameters && c.geometry.parameters.width === 2.25)
        .forEach(c => { mesh.remove(c); c.geometry.dispose(); });
      const mold = metal(0x9aa4b4, .9, .3); mold.emissive.setHex(0x3adfff);
      u._fxMold = mold;
      [[2.28, .1, .05, 0, .775], [2.28, .1, .05, 0, -.775], [.05, .1, 1.6, 1.115, 0], [.05, .1, 1.6, -1.115, 0]]
        .forEach(([w, h, d, x, z]) => caixa(placa, w, h, d, mold, x, 0, z));
    }
    const placa = u._fxP;
    const C = [null,
      { emi: 0,  met: .5,  rug: .28, mold: 0x9aa4b4, ek: 0 },
      { emi: .9, met: .7,  rug: .18, mold: 0xc4d0e0, ek: .35 },
      { emi: 1.3, met: .85, rug: .08, mold: 0x141a21, ek: 1.7 }][nv];
    const tx = texPainel(nv), pm = placa.material;
    pm.map = tx.map; pm.emissiveMap = tx.emi; pm.color.set(0xffffff); pm.emissive.set(0xffffff);
    pm.emissiveIntensity = C.emi; pm.metalness = C.met; pm.roughness = C.rug; pm.needsUpdate = true;
    u._fxMold.color.setHex(C.mold); u._fxMold.emissiveIntensity = C.ek;

    if (nv >= 2 && !u._fx2) {                          // inversor com LED no poste
      u._fx2 = 1;
      caixa(mesh, .3, .22, .16, metal(0x2a3342, .7, .4), 0, .3, .15, true);
      caixa(mesh, .18, .03, .01, P.led, 0, .35, .235);
    }
    if (nv >= 3 && !u._fx3) {                          // anéis no poste, varredura de energia, halo e marca no chão
      u._fx3 = 1;
      [.12, .48].forEach(y => anel(mesh, .095, .018, P.anel, 0, y, 0));
      anel(mesh, .95, .03, P.anel, 0, .1, 0, true, 48);
      peca(mesh, new THREE.CircleGeometry(.95, 40), aditivo(0x3adfff, .10), 0, .095, 0).rotation.x = -PI / 2;
      brilho(mesh, 0x5fe8ff, 3.4, .16, 0, .95, 0);
      const varre = peca(placa, new THREE.PlaneGeometry(2.1, .16), aditivo(0x8ff7ff, .4), 0, .052, 0);
      varre.rotation.x = -PI / 2;
      const fase = Math.random();
      reg(mesh, (dt, t) => {
        const k = (t * .45 + fase) % 1;
        varre.position.z = -.7 + k * 1.4; varre.material.opacity = .5 * Math.sin(PI * k);
      });
    }
  }

  // =====================================================================
  // GERADOR (corpo 3 x 1.6 x 1.6; medidor de combustível fica embaixo à esquerda da frente)
  // =====================================================================
  function gerador(mesh, nv) {
    const u = mesh.userData;
    if (!u._fxG) {
      const corpo = mesh.children.find(c => c.isMesh && c.geometry.parameters && c.geometry.parameters.width === 3 && c.geometry.parameters.height === 1.6);
      if (!corpo) return;
      u._fxG = corpo;
      const esc = metal(0x0e1013, .6, .5);
      caixa(mesh, 3.04, .06, 1.64, metal(0x1a1d22, .7, .4), 0, 1.83, 0, true);                            // chapa do teto
      [-1, 1].forEach(s => { for (let k = 0; k < 6; k++) caixa(mesh, .03, .07, 1.2, esc, s * 1.505, .55 + k * .2, 0); });   // venezianas
      for (let k = 0; k < 5; k++) caixa(mesh, .8, .04, .02, esc, .75, .5 + k * .12, .81);                  // grade frontal
      u._fxTela = peca(mesh, new THREE.PlaneGeometry(1.3, .4), new THREE.MeshBasicMaterial({ color: 0xffffff }), -.35, 1.42, .812);
    }
    const corpo = u._fxG;
    const C = [null, { cor: 0xd98e04, m: .3, r: .6 }, { cor: 0x2d3a4b, m: .6, r: .38 }, { cor: 0x12161c, m: .85, r: .22 }][nv];
    corpo.material.color.setHex(C.cor); corpo.material.metalness = C.m; corpo.material.roughness = C.r;
    const tm = u._fxTela.material; tm.map = texDisp(nv); tm.needsUpdate = true;

    if (nv >= 2 && !u._fx2) {                          // faixas neon em volta do corpo + anéis no escape
      u._fx2 = 1;
      caixa(mesh, 3.03, .05, 1.63, P.faixa, 0, 1.7, 0);
      caixa(mesh, 3.03, .05, 1.63, P.faixa, 0, .3, 0);
      anel(mesh, .18, .03, P.anel, 1, 1.95, 0);
      anel(mesh, .18, .03, P.anel, 1, 2.55, 0);
    }
    if (nv >= 3 && !u._fx3) {                          // reator com anéis giratórios, antena, tiras neon, brilho no chão
      u._fx3 = 1;
      const aco = metal(0x242a32, .85, .3);
      [-1, 1].forEach(s => caixa(mesh, .05, 1.4, .05, P.violeta, s * 1.52, 1.0, .82));
      peca(mesh, new THREE.CylinderGeometry(.22, .3, .4, 14), aco, -.6, 2.06, 0, true);
      const nucleoMat = neon(0xbff6ff, 1.5);
      peca(mesh, new THREE.SphereGeometry(.26, 18, 14), nucleoMat, -.6, 2.55, 0);
      const halo = brilho(mesh, 0x6fe9ff, 2.4, .5, -.6, 2.55, 0);
      const r1 = anel(mesh, .52, .03, P.anel, -.6, 2.55, 0, false);
      const r2 = anel(mesh, .6, .025, P.ponta, -.6, 2.55, 0, false);
      peca(mesh, new THREE.CylinderGeometry(.03, .03, .9, 6), aco, -1.3, 2.3, -.5);
      peca(mesh, new THREE.SphereGeometry(.07, 10, 8), P.avisoCiano, -1.3, 2.78, -.5);
      const sub = peca(mesh, new THREE.CircleGeometry(2.35, 40), aditivo(0x3adfff, .1), 0, .095, 0);
      sub.rotation.x = -PI / 2;
      let ang = 0, vr = .2;
      reg(mesh, (dt, t) => {
        const lig = !!u.ligado;                        // u.ligado é atualizado pelo gerador (liga/desliga)
        vr += ((lig ? 1 : .15) - vr) * Math.min(1, dt * 2);
        ang += dt * vr;
        r1.rotation.set(ang * 2.2, .6, 0); r2.rotation.set(1.1, ang * -1.7, .3);
        nucleoMat.emissiveIntensity = lig ? 1.3 + .7 * Math.sin(t * 9) : .45 + .15 * Math.sin(t * 2);
        halo.material.opacity = (lig ? .55 : .15) * (.8 + .2 * Math.sin(t * 9));
        sub.material.opacity = lig ? .22 + .1 * Math.sin(t * 3) : .06;
      });
    }
  }

  // =====================================================================
  // TURBINA EÓLICA (torre r .34→.16, 11 m; nacela em y 11.1; rotor em z 1.1)
  // =====================================================================
  const rT = y => .34 - .18 * (y / 11);               // raio da torre na altura y
  function turbina(mesh, nv) {
    const u = mesh.userData;
    if (!u._fxT) {
      const rotor = mesh.children.find(c => c.isGroup);
      if (!rotor) return;
      u._fxT = rotor;
      u._fxOrig = []; mesh.traverse(c => { if (c.isMesh) u._fxOrig.push(c); });   // peças originais (para o acabamento por nível)
      peca(mesh, new THREE.CylinderGeometry(.62, .72, .18, 18), metal(0x2a3038, .8, .35), 0, .09, 0, true);   // flange da base
    }
    const rotor = u._fxT, cy = 11.1;
    const C = [null, { m: 0, r: .6 }, { m: .45, r: .3 }, { m: .7, r: .18 }][nv];
    u._fxOrig.forEach(c => { c.material.metalness = C.m; c.material.roughness = C.r; });

    if (nv >= 2 && !u._fx2) {                          // anéis de luz subindo a torre, pontas das pás, cone e aviso
      u._fx2 = 1;
      u._fxAneis = [1.3, 3.0, 4.7, 6.4, 8.1, 9.8].map((y, i) => anel(mesh, rT(y) + .015, .035, P.torre2[i], 0, y, 0, true, 28));
      rotor.children.filter(c => c.isGroup).forEach(p => caixa(p, .44, .26, .14, P.ponta, 0, 4.7, 0));
      const cone = peca(rotor, new THREE.ConeGeometry(.28, .75, 16), metal(0xdfe6ee, .6, .25), 0, 0, .35);
      cone.rotation.x = PI / 2;
      anel(rotor, .3, .025, P.anel, 0, 0, .02, false);
      caixa(mesh, .5, .03, 1.2, P.faixa, 0, 11.46, 0);
      peca(mesh, new THREE.SphereGeometry(.09, 10, 8), P.aviso, 0, 11.56, -.7);
    }
    if (nv >= 3 && !u._fx3) {                          // anel-duto neon, halo das pás, glow e pulso no chão
      u._fx3 = 1;
      u._fxAneis.forEach((m, i) => { m.material = P.torre3[i]; });
      anel(mesh, 5.15, .07, P.anel, 0, cy, .75, false, 80);
      anel(mesh, 4.95, .025, P.ponta, 0, cy, .75, false, 80);
      const estai = metal(0x20252c, .85, .3);
      [90, 210, 330].forEach(d => {
        const a = d * PI / 180;
        const s = caixa(mesh, 4.65, .05, .05, estai, Math.cos(a) * 2.775, cy + Math.sin(a) * 2.775, .75);
        s.rotation.z = a;
      });
      anel(rotor, 4.72, .03, aditivo(0x6fe9ff, .35), 0, 0, 0, false, 80);
      peca(rotor, new THREE.CircleGeometry(4.75, 56), aditivo(0x6fe9ff, .045), 0, 0, -.02);
      brilho(mesh, 0x6fe9ff, 9, .10, 0, cy, .6);
      const pulso = anel(mesh, 1, .03, aditivo(0x6fe9ff, .5), 0, .1, 0, true, 40);
      const fase = Math.random();
      reg(mesh, (dt, t) => {
        const k = (t * .5 + fase) % 1;
        pulso.scale.setScalar(.8 + k * 2.6); pulso.material.opacity = .55 * (1 - k);
      });
    }
  }

  // =====================================================================
  // REFRIGERADOR DE TETO (6 níveis; o.nivel, o.grp, o.flags, o.matC, o.matP, o.mkRotor)
  // =====================================================================
  function cooler(o) {
    const nv = o.nivel, f = o.flags, grp = o.grp, R = COOLER_RAIO;
    if (!f.fx1) {                                      // nv1: aro, grade em estrela, LED e fluxo de ar frio
      f.fx1 = 1;
      const claro = metal(0xcfd6de, .8, .3), esc = metal(0x1b1f25, .8, .4);
      anel(grp, R, .05, claro, 0, .52, 0, true, 40);
      for (let k = 0; k < 3; k++) { const e = caixa(grp, R * 1.9, .014, .035, esc, 0, .68, 0); e.rotation.y = k * PI / 3; }
      caixa(grp, .12, .05, .02, P.led, 0, .3, R * 1.03);
      const fluxo = [0, 1, 2].map(() => anel(grp, R * .75, .025, aditivo(0x9be8ff, 0), 0, .8, 0, true, 40));
      reg(grp, (dt, t) => {
        fluxo.forEach((r, i) => {
          const k = (t * .55 + i / 3) % 1;
          r.position.y = .85 + k * 1.5; r.scale.setScalar(1 - .35 * k);
          r.material.opacity = (.10 + .04 * o.nivel) * Math.sin(PI * k);   // mais forte a cada nível
        });
      });
    }
    if (nv >= 2 && !f.fx2) {                           // nv2: cinto neon na base + indicadores
      f.fx2 = 1;
      anel(grp, R * 1.06, .028, P.base, 0, .18, 0, true, 40);
      [45, 135, 225, 315].forEach(d => {
        const a = d * PI / 180;
        const m = caixa(grp, .06, .22, .02, P.base, Math.cos(a) * R * 1.03, .32, Math.sin(a) * R * 1.03);
        m.rotation.y = PI / 2 - a;
      });
    }
    if (nv >= 3 && !f.fx3) {                           // nv3: colar criogênico de vidro
      f.fx3 = 1;
      anel(grp, R, .09, vidro(0x5aa9e6, .55, 0x1a6aff, .7), 0, .46, 0, true, 40);
    }
    o.matP.emissive.setHex(0x2ab8ff);                  // pás começam a brilhar a partir do nv3
    o.matP.emissiveIntensity = nv >= 3 ? .1 + .12 * (nv - 3) : 0;
    if (nv >= 4 && !f.fx4) {                           // nv4: aletas grafite com borda neon
      f.fx4 = 1;
      o.matC.color.setHex(0x23282f); o.matC.metalness = .85; o.matC.roughness = .3;
      const aleta = metal(0x2a3038, .85, .3);
      for (let i = 0; i < 12; i++) {
        const a = i / 12 * PI * 2, x = Math.cos(a) * (R + .1), z = Math.sin(a) * (R + .1);
        const fin = caixa(grp, .05, .38, .3, aleta, x, .27, z, true); fin.rotation.y = -a;
        const borda = caixa(grp, .056, .03, .3, P.base, x, .47, z); borda.rotation.y = -a;
      }
    }
    if (nv >= 5 && !f.fx5) {                           // nv5: tubos de líquido refrigerante (entre as aletas)
      f.fx5 = 1;
      const aco = metal(0x2a3038, .85, .3);
      [15, 195].forEach(d => {
        const a = d * PI / 180, c = Math.cos(a), s = Math.sin(a), rr = R + .5;
        const br = caixa(grp, .5, .08, .08, aco, c * (R + .22), .38, s * (R + .22)); br.rotation.y = -a;
        peca(grp, new THREE.CylinderGeometry(.075, .075, 1.1, 12), vidro(0x9fe8ff, .28), c * rr, .62, s * rr);
        peca(grp, new THREE.CylinderGeometry(.04, .04, 1.05, 8), P.fluido, c * rr, .62, s * rr);
        [.05, 1.18].forEach(y => peca(grp, new THREE.CylinderGeometry(.1, .1, .1, 12), aco, c * rr, y, s * rr, true));
        peca(grp, new THREE.SphereGeometry(.09, 10, 8), P.avisoCiano, c * rr, 1.27, s * rr);
      });
      o.grade.material = neon(0x3adfff, .9);
    }
    if (nv >= 6 && !f.fx6) {                           // nv6: 2º rotor, núcleo holográfico com órbitas, marca no piso
      f.fx6 = 1;
      peca(grp, new THREE.CylinderGeometry(.06, .06, .5, 8), o.matC, 0, .85, 0);
      o.rotor2 = o.mkRotor(1.1, R * .8);
      const cy = 1.75;
      peca(grp, new THREE.CylinderGeometry(.012, .012, .5, 6), P.nucleo, 0, 1.4, 0);
      peca(grp, new THREE.SphereGeometry(.14, 16, 12), P.nucleo, 0, cy, 0);
      brilho(grp, 0x9ff3ff, 1.9, .5, 0, cy, 0);
      const r1 = anel(grp, .3, .02, P.anel, 0, cy, 0, false), r2 = anel(grp, .44, .018, P.ponta, 0, cy, 0, false);
      peca(grp, new THREE.CylinderGeometry(.025, .025, .7, 6), o.matC, R * .9, 1.0, 0);
      peca(grp, new THREE.SphereGeometry(.08, 10, 8), P.avisoCiano, R * .9, 1.4, 0);
      anel(grp, R * 1.25, .03, P.anel, 0, .03, 0, true, 56);
      peca(grp, new THREE.CircleGeometry(R * 1.25, 48), aditivo(0x3adfff, .08), 0, .025, 0).rotation.x = -PI / 2;
      reg(grp, (dt, t) => { r1.rotation.set(t * 2, .5, 0); r2.rotation.set(1.2, t * -1.5, .4); });
    }
  }

  return { painel, gerador, turbina, cooler };
})();

function aplicarNivelCooler(o) {
  o.vel = 1 + (o.nivel - 1) * .45;                     // ventilador mais rápido a cada nível
  FX.cooler(o);
}

"""


def trocar_bloco(html, inicio, fim, novo, nome, usar_comentario=None):
    """Troca o texto entre `inicio` (inclusive) e `fim` (exclusive) por `novo`."""
    i = html.find(inicio)
    if i == -1:
        sys.exit(f"Não encontrei {nome} no HTML (o arquivo mudou?). Nada foi alterado.")
    if usar_comentario:                               # leva junto o comentário logo acima da função, se existir
        c = html.rfind(usar_comentario, 0, i)
        if c != -1 and i - c < 200:
            i = c
    j = html.find(fim, i)
    if j == -1 or j < i:
        sys.exit(f"Não encontrei o fim de {nome}. Nada foi alterado.")
    return html[:i] + novo + html[j:]


def main():
    caminho = pathlib.Path(ENTRADA)
    if not caminho.exists():
        sys.exit(f"Arquivo não encontrado: {ENTRADA}")
    html = caminho.read_text(encoding="utf-8")

    if MARCA in html:
        sys.exit("Este HTML já tem o patch de evoluções visuais aplicado. Nada a fazer.")

    # 1) painel / gerador / turbina
    html = trocar_bloco(
        html,
        "function aplicarVisualEvolucao(mesh, nivel, tipo) {",
        "function abrirModalEvoluir(obj, tipo, getKw, aplicarEvo) {",
        APLICAR_JS + "\n\n  ",
        "aplicarVisualEvolucao",
    )

    # 2) refrigerador + infraestrutura de efeitos
    html = trocar_bloco(
        html,
        "function aplicarNivelCooler(o) {",
        "function abrirModalCooler(obj) {",
        FX_JS,
        "aplicarNivelCooler",
        usar_comentario="// Cada evolução acrescenta uma peça visual nova",
    )

    # 3) o gerador avisa quando liga/desliga (reator acelera). Precisa do patch de gasolina.
    antigo = "on = v; obj.on = v;"
    if html.count(antigo) == 1:
        html = html.replace(antigo, "on = v; obj.on = v; g.userData.ligado = v;")
    else:
        print("Aviso: não achei o liga/desliga do gerador a gasolina; o reator do nv3 ficará em modo 'desligado'.")

    pathlib.Path(SAIDA).write_text(html, encoding="utf-8")
    print(f"Pronto! Arquivo gerado: {SAIDA}")


if __name__ == "__main__":
    main()