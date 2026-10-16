import sys, shutil

arq = sys.argv[1] if len(sys.argv) > 1 else "mundozinho.html"
shutil.copy(arq, arq + ".bak")
s = open(arq, encoding="utf-8").read()
erros = []

def sub(old, new):
    global s
    if s.count(old) != 1:
        erros.append(f"{s.count(old)}x encontrado: {old[:80]}")
        return
    s = s.replace(old, new)

if "PATCH-V14-SONS" in s:
    print("Os sons já foram instalados neste arquivo (PATCH-V14-SONS). Nada a fazer.")
    sys.exit(0)

BLOCO = r"""/* ===== PATCH-V14-SONS: áudio procedural (Web Audio API) — não usa arquivos de som ===== */
const SOM = (() => {
  // >>> volumes: 0 = mudo · 1 = normal · 2 = dobro. Tecla M liga/desliga tudo <<<
  const CFG = { mestre: .8, ambiente: 1, vento: 1, chuva: 1, trovao: 1, turbina: 1, gerador: 1, cooler: 1, dc: 1, passos: 1, efeitos: 1 };
  let ctx = null, saida = null, branco = null, marrom = null, bus = null, mudo = false;
  const V = {}, S = { int: 0, passo: 0, portao: false, tTrovao: 20, tPassaro: 4 };
  const HUMS = [{ x: 7.7, z: -7.5, r: 16, v: 1 }, { x: -96, z: -10, r: 45, v: 1.6 }];   // transformador do galpão e subestação da CEMIG
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const queda = (d, r) => { const k = clamp(1 - d / r); return k * k; };
  const rnd = (a, b) => a + Math.random() * (b - a);
  const alvo = (p, v, t = .2) => { if (isFinite(v)) p.setTargetAtTime(v, ctx.currentTime, t); };
  const N = {
    fonte: b => { const s = ctx.createBufferSource(); s.buffer = b; s.loop = true; s.start(0, Math.random() * 2); return s; },
    filtro: (t, f, q = .7) => { const n = ctx.createBiquadFilter(); n.type = t; n.frequency.value = f; n.Q.value = q; return n; },
    ganho: (v = 0) => { const g = ctx.createGain(); g.gain.value = v; return g; },
    osc: (t, f) => { const o = ctx.createOscillator(); o.type = t; o.frequency.value = f; o.start(); return o; },
    pan: () => ctx.createStereoPanner()
  };
  const liga = (...n) => { for (let i = 0; i < n.length - 1; i++) n[i].connect(n[i + 1]); return n[n.length - 1]; };
  const dentroDC = () => { const lx = player.pos.x - galpao.px, lz = player.pos.z - galpao.pz; return lx > -10.3 && lx < galpao.xDir + .3 && Math.abs(lz) < 11.3 && player.pos.y < 5; };
  const dentroCasa = () => Math.abs(player.pos.x + 28) < 3.8 && Math.abs(player.pos.z + 12) < 3.4;
  const panDe = (x, z) => { const dx = x - player.pos.x, dz = z - player.pos.z, d = Math.hypot(dx, dz) || 1; return clamp((dx * Math.cos(player.yaw) - dz * Math.sin(player.yaw)) / d, -1, 1) * .85; };

  // ---------- sons curtos ----------
  function posicional(x, z, raio) {            // devolve um nó de entrada com volume por distância + estéreo
    const g = N.ganho(queda(Math.hypot(player.pos.x - x, player.pos.z - z), raio)), p = N.pan();
    p.pan.value = panDe(x, z); liga(g, p, bus.ef); return g;
  }
  function rajada(dest, o) {                   // ruído filtrado com envelope
    const { buf = branco, tipo = 'bandpass', f = 1000, f2 = null, q = 1, dur = .2, vol = .3, ata = .004, t0 = 0 } = o;
    const t = ctx.currentTime + t0 + .01, s = ctx.createBufferSource(), fl = N.filtro(tipo, f, q), g = ctx.createGain();
    s.buffer = buf; s.loop = true;
    if (f2) { fl.frequency.setValueAtTime(f, t); fl.frequency.exponentialRampToValueAtTime(f2, t + dur); }
    g.gain.setValueAtTime(.0001, t); g.gain.linearRampToValueAtTime(vol, t + ata); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
    liga(s, fl, g, dest); s.start(t, Math.random() * 2); s.stop(t + dur + .05);
  }
  function nota(dest, o) {
    const { tipo = 'sine', f = 440, f2 = null, dur = .15, vol = .2, ata = .005, t0 = 0 } = o;
    const t = ctx.currentTime + t0 + .01, os = ctx.createOscillator(), g = ctx.createGain();
    os.type = tipo; os.frequency.setValueAtTime(f, t); if (f2) os.frequency.exponentialRampToValueAtTime(f2, t + dur);
    g.gain.setValueAtTime(.0001, t); g.gain.linearRampToValueAtTime(vol, t + ata); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
    liga(os, g, dest); os.start(t); os.stop(t + dur + .05);
  }

  function passo(correndo) {
    const P = player.pos, d = bus.passos, k = (correndo ? 1.1 : 1) * rnd(.85, 1.15), v = correndo ? .7 : .5;
    const sup = P.y > 4.5 ? 'metal' : dentroCasa() ? 'madeira'
      : dentroDC() ? ((P.x - galpao.px < -3 && P.z - galpao.pz < -5) ? 'carpete' : 'concreto')
      : Math.abs(P.z - 1) < 3 ? 'asfalto' : Math.abs(P.z - 1) < 5 ? 'concreto' : 'grama';
    if (sup === 'grama') { rajada(d, { buf: marrom, tipo: 'lowpass', f: 700 * k, dur: .12, vol: .9 * v }); rajada(d, { tipo: 'highpass', f: 3500, dur: .07, vol: .04 * v }); }
    else if (sup === 'asfalto' || sup === 'concreto') { rajada(d, { f: 1800 * k, q: 1.3, dur: .05, vol: .18 * v }); nota(d, { f: 95 * k, f2: 60, dur: .08, vol: .14 * v }); }
    else if (sup === 'madeira') { nota(d, { f: 170 * k, f2: 100, dur: .1, vol: .15 * v }); rajada(d, { f: 600, dur: .06, vol: .08 * v }); }
    else if (sup === 'metal') { rajada(d, { f: 2600, q: 4, dur: .07, vol: .12 * v }); nota(d, { tipo: 'triangle', f: 520 * k, f2: 480, dur: .18, vol: .03 * v }); nota(d, { f: 110, f2: 70, dur: .08, vol: .1 * v }); }
    else rajada(d, { buf: marrom, tipo: 'lowpass', f: 500, dur: .09, vol: .5 * v });
  }

  function portaoSom(abre) {
    const d = posicional(galpao.px, galpao.pz + 11.2, 55), T = 1.5;
    nota(d, { tipo: 'square', f: 900, dur: .1, vol: .08 }); nota(d, { tipo: 'square', f: 1200, dur: .1, vol: .06, t0: .13 });         // bip do botão
    rajada(d, { buf: marrom, f: abre ? 120 : 260, f2: abre ? 320 : 110, q: 1.2, dur: T, vol: 1.1, ata: .15, t0: .25 });               // rolo de aço
    rajada(d, { tipo: 'highpass', f: 2200, q: .5, dur: T, vol: .07, ata: .1, t0: .25 });                                              // lâminas
    nota(d, { tipo: 'sawtooth', f: abre ? 150 : 250, f2: abre ? 260 : 130, dur: T, vol: .05, t0: .25 });                              // motor
    rajada(d, { buf: marrom, tipo: 'lowpass', f: 220, dur: .35, vol: 1.2, ata: .002, t0: .25 + T });                                  // batida final
    nota(d, { f: 90, f2: 45, dur: .3, vol: .35, t0: .25 + T });
  }
  function partida(x, z) {
    const d = posicional(x, z, 75);
    nota(d, { tipo: 'sawtooth', f: 38, f2: 95, dur: 1.1, vol: .1 }); rajada(d, { buf: marrom, tipo: 'lowpass', f: 450, dur: 1.1, vol: .9, ata: .05 });
    for (let i = 0; i < 4; i++) rajada(d, { buf: marrom, tipo: 'lowpass', f: 300, dur: .12, vol: .9, t0: 1 + i * .1 });
  }
  function parada(x, z) {
    const d = posicional(x, z, 75);
    nota(d, { tipo: 'sawtooth', f: 70, f2: 18, dur: 1.2, vol: .09 }); rajada(d, { buf: marrom, tipo: 'lowpass', f: 400, f2: 80, dur: 1.2, vol: .7 });
  }
  function trovao() {
    const mu = 1 - .45 * S.int, b = bus.trovao;
    rajada(b, { tipo: 'highpass', f: 1500, dur: .18, vol: .35 * mu, ata: .002 });
    rajada(b, { buf: marrom, tipo: 'lowpass', f: 1200, f2: 70, dur: 4.5, vol: 2.4 * mu, ata: .08 });
    rajada(b, { buf: marrom, tipo: 'lowpass', f: 300, f2: 60, dur: 3, vol: 1.4 * mu, ata: .6, t0: 1.2 });
  }
  function passaro(vol) {
    const p = N.pan(); p.pan.value = rnd(-.8, .8); p.connect(bus.ef);
    const base = rnd(2300, 3600), n = 2 + Math.floor(Math.random() * 3);
    for (let i = 0; i < n; i++) nota(p, { f: base * rnd(.9, 1.1), f2: base * rnd(1.1, 1.5), dur: .09, vol: .04 * vol * CFG.ambiente, t0: i * .13 });
  }
  function tique() {                            // HD/ventoinha estalando no data center
    const p = N.pan(); p.pan.value = rnd(-.7, .7); p.connect(bus.ef);
    rajada(p, { f: 2800, q: 3, dur: .015, vol: .05 });
  }

  // ---------- reações a ações do jogador (F), pelo texto da mira ----------
  const AC = {
    porta: () => { nota(bus.ef, { tipo: 'sawtooth', f: 180, f2: 110, dur: .4, vol: .05 }); rajada(bus.ef, { buf: marrom, tipo: 'lowpass', f: 300, dur: .22, vol: .8 }); rajada(bus.ef, { buf: marrom, tipo: 'lowpass', f: 250, dur: .2, vol: .9, t0: .5 }); },
    geladeira: () => { rajada(bus.ef, { buf: marrom, tipo: 'lowpass', f: 220, dur: .14, vol: 1 }); rajada(bus.ef, { f: 1500, dur: .15, vol: .07, t0: .04 }); },
    tv: () => { rajada(bus.ef, { tipo: 'highpass', f: 3000, dur: .3, vol: .07 }); nota(bus.ef, { f: 15600, dur: .5, vol: .012 }); },
    luz: () => { rajada(bus.ef, { f: 2500, q: 2, dur: .025, vol: .35 }); rajada(bus.ef, { f: 1800, q: 2, dur: .02, vol: .2, t0: .06 }); },
    ventilador: () => { rajada(bus.ef, { f: 2200, q: 2, dur: .02, vol: .3 }); nota(bus.ef, { tipo: 'sawtooth', f: 70, f2: 130, dur: .9, vol: .02, t0: .05 }); rajada(bus.ef, { buf: marrom, f: 300, f2: 700, dur: .9, vol: .5, t0: .05 }); },
    beber: () => { for (let i = 0; i < 4; i++) nota(bus.ef, { f: rnd(280, 450), f2: rnd(600, 900), dur: .09, vol: .07, t0: i * .11 }); rajada(bus.ef, { f: 900, q: 2, dur: .5, vol: .05 }); },
    imprimir: () => { for (let i = 0; i < 8; i++) rajada(bus.ef, { f: 1800, q: 4, dur: .09, vol: .14, t0: i * .13 }); nota(bus.ef, { tipo: 'sawtooth', f: 120, dur: 1.1, vol: .03 }); },
    cozinhar: () => { for (let i = 0; i < 4; i++) rajada(bus.ef, { f: 3000, q: 3, dur: .015, vol: .25, t0: i * .08 }); rajada(bus.ef, { buf: marrom, tipo: 'lowpass', f: 450, dur: .35, vol: .8, t0: .3 }); },
    fogão: () => AC.cozinhar(),
    servir: () => { nota(bus.ef, { f: 2400, dur: .18, vol: .05 }); nota(bus.ef, { f: 3100, dur: .14, vol: .04, t0: .08 }); rajada(bus.ef, { buf: marrom, tipo: 'lowpass', f: 400, dur: .12, vol: .5 }); },
    comer: () => { for (let i = 0; i < 3; i++) rajada(bus.ef, { tipo: 'highpass', f: 1500, dur: .06, vol: .25, t0: i * .14 }); },
    sentar: () => { rajada(bus.ef, { buf: marrom, tipo: 'lowpass', f: 400, dur: .25, vol: .6 }); rajada(bus.ef, { f: 900, dur: .2, vol: .05 }); },
    deitar: () => AC.sentar(),
    'caixa de correio': () => { nota(bus.ef, { tipo: 'sawtooth', f: 400, f2: 700, dur: .25, vol: .03 }); rajada(bus.ef, { f: 2000, dur: .08, vol: .15, t0: .22 }); },
    terminal: () => { nota(bus.ef, { tipo: 'square', f: 660, dur: .06, vol: .04 }); nota(bus.ef, { tipo: 'square', f: 990, dur: .08, vol: .04, t0: .07 }); }
  };
  function acao(rot) {
    if (!ctx || !rot) return;
    const r = String(rot).toLowerCase(), k = Object.keys(AC).find(k => r.includes(k));
    if (k) AC[k]();
  }
  // reações às mensagens do jogo (hud.toast)
  function toast(m) {
    if (!ctx) return;
    const t = String(m).toLowerCase(), E = bus.ef;
    if (/insuficiente|sem (rack|baia|refriger|combust)|sem .* no invent|baixo|cheio|inválid/.test(t)) { nota(E, { tipo: 'square', f: 180, dur: .12, vol: .08 }); nota(E, { tipo: 'square', f: 140, dur: .16, vol: .08, t0: .12 }); }
    else if (/evolu[ií]d/.test(t)) [523, 659, 784, 1047].forEach((f, i) => nota(E, { tipo: 'triangle', f, dur: .14, vol: .09, t0: i * .07 }));
    else if (/ampliado/.test(t)) { rajada(E, { buf: marrom, tipo: 'lowpass', f: 250, dur: 1.2, vol: 1.2 }); [392, 523, 659].forEach((f, i) => nota(E, { tipo: 'triangle', f, dur: .3, vol: .07, t0: i * .12 })); }
    else if (/instalad/.test(t)) { rajada(E, { buf: marrom, tipo: 'lowpass', f: 320, dur: .16, vol: 1 }); nota(E, { f: 1800, dur: .1, vol: .03, t0: .03 }); for (let i = 0; i < 3; i++) rajada(E, { f: 2400, q: 3, dur: .02, vol: .15, t0: .12 + i * .05 }); }
    else if (/removid/.test(t)) { rajada(E, { f: 1200, f2: 400, dur: .2, vol: .12 }); nota(E, { f: 500, f2: 200, dur: .1, vol: .08 }); }
    else if (/comprad|vendeu/.test(t)) { nota(E, { f: 1568, dur: .08, vol: .07 }); nota(E, { f: 2093, dur: .25, vol: .07, t0: .08 }); rajada(E, { tipo: 'highpass', f: 5000, dur: .12, vol: .05, t0: .05 }); }
    else if (/pronta/.test(t)) nota(E, { f: 1320, dur: .7, vol: .09 });
    else if (/gasolina/.test(t)) { rajada(E, { buf: marrom, f: 300, f2: 500, dur: .6, vol: .9 }); nota(E, { f: 800, f2: 1000, dur: .2, vol: .03, t0: .5 }); }
  }
  function ui(tipo) {
    if (!ctx) return;
    if (tipo) { nota(bus.ef, { f: 440, f2: 660, dur: .09, vol: .035 }); nota(bus.ef, { f: 660, f2: 880, dur: .09, vol: .03, t0: .06 }); }
    else nota(bus.ef, { f: 800, dur: .04, vol: .035 });
  }

  // ---------- vozes contínuas ----------
  function construir() {
    V.vento = { f: N.filtro('lowpass', 500), g: N.ganho(0) }; liga(N.fonte(marrom), V.vento.f, V.vento.g, saida);
    V.chuva = { f: N.filtro('lowpass', 7500), g: N.ganho(0), gg: N.ganho(0) };
    liga(N.fonte(branco), N.filtro('highpass', 800), V.chuva.f, V.chuva.g, saida);
    liga(N.fonte(marrom), N.filtro('lowpass', 260), V.chuva.gg, saida);
    V.grilo = { g: N.ganho(0) };
    const am1 = N.ganho(.5), l1 = N.ganho(.5), am2 = N.ganho(.5), l2 = N.ganho(.5);
    liga(N.osc('sine', 17), l1, am1.gain); liga(N.osc('sine', 2.6), l2, am2.gain);
    liga(N.osc('sine', 4300), am1); liga(N.osc('sine', 4650), am1); liga(am1, am2, V.grilo.g, saida);
    V.tur = [0, 1].map(() => { const v = { f: N.filtro('bandpass', 260, .9), am: N.ganho(0), pan: N.pan() }; liga(N.fonte(marrom), v.f, v.am, v.pan, saida); return v; });
    V.ger = [0, 1].map(() => {
      const v = { am: N.ganho(0), pan: N.pan(), o1: N.osc('sawtooth', 45), o2: N.osc('square', 22), lfo: N.osc('sine', 14), lg: N.ganho(0) };
      liga(v.o1, N.filtro('lowpass', 320), v.am); liga(v.o2, N.filtro('lowpass', 160), v.am); liga(N.fonte(marrom), N.filtro('lowpass', 800), v.am);
      liga(v.lfo, v.lg, v.am.gain); liga(v.am, v.pan, saida); return v;
    });
    V.hum = { am: N.ganho(0), pan: N.pan() };
    const hf = N.filtro('lowpass', 500);
    [[60, .6], [120, 1], [240, .35]].forEach(([f, g]) => liga(N.osc('sine', f), N.ganho(g), hf)); liga(hf, V.hum.am, V.hum.pan, saida);
    V.dc = { lp: N.filtro('lowpass', 500), out: N.ganho(0), low: N.ganho(.5), hiss: N.ganho(0), hf: N.filtro('bandpass', 2400, .45), hum: N.ganho(0) };
    liga(N.fonte(marrom), N.filtro('lowpass', 650), V.dc.low, V.dc.lp); liga(N.fonte(branco), V.dc.hf, V.dc.hiss, V.dc.lp);
    liga(N.osc('sine', 120), V.dc.hum, V.dc.lp); N.osc('sine', 180).connect(V.dc.hum); liga(V.dc.lp, V.dc.out, saida);
    V.cool = { f: N.filtro('bandpass', 320, .8), am: N.ganho(0), lg: N.ganho(0), lfo: N.osc('sine', 3.6), pan: N.pan() };
    liga(N.fonte(marrom), V.cool.f, V.cool.am); liga(N.fonte(branco), N.filtro('bandpass', 1400, .5), N.ganho(.12), V.cool.am);
    liga(V.cool.lfo, V.cool.lg, V.cool.am.gain); liga(V.cool.am, V.cool.pan, saida);
  }

  function iniciar() {
    if (ctx) { if (ctx.state === 'suspended') ctx.resume(); return; }
    const AC_ = window.AudioContext || window.webkitAudioContext; if (!AC_) return;
    ctx = new AC_();
    const comp = ctx.createDynamicsCompressor();
    saida = N.ganho(mudo ? 0 : CFG.mestre); liga(saida, comp, ctx.destination);
    const n = ctx.sampleRate * 3;
    branco = ctx.createBuffer(1, n, ctx.sampleRate); marrom = ctx.createBuffer(1, n, ctx.sampleRate);
    const a = branco.getChannelData(0), b = marrom.getChannelData(0); let u = 0;
    for (let i = 0; i < n; i++) { const w = Math.random() * 2 - 1; a[i] = w; u = (u + .02 * w) / 1.02; b[i] = u * 3.5; }
    bus = { ef: N.ganho(CFG.efeitos), passos: N.ganho(CFG.passos), trovao: N.ganho(CFG.trovao) };
    liga(bus.ef, saida); liga(bus.passos, saida); liga(bus.trovao, saida);
    construir();
    if (ctx.state === 'suspended') ctx.resume();
  }
  addEventListener('keydown', e => {
    if (e.code === 'KeyM' && !e.repeat) { mudo = !mudo; if (saida) alvo(saida.gain, mudo ? 0 : CFG.mestre, .05); hud.toast(mudo ? '🔇 Som desligado (M)' : '🔊 Som ligado (M)'); }
  });
  document.addEventListener('visibilitychange', () => { if (ctx) document.hidden ? ctx.suspend() : ctx.resume(); });

  // ---------- atualização por quadro ----------
  function atualizar(dt) {
    if (!ctx || ctx.state !== 'running') return;
    const P = player.pos, rain = clima.intensidade, D = distrito;
    const dcIn = dentroDC(), cIn = dentroCasa();
    S.int += ((dcIn || cIn ? 1 : 0) - S.int) * Math.min(1, dt * 4);
    const ext = 1 - S.int, abafa = 1 - .6 * S.int;
    const noite = clamp(LAMP.matBrilho.opacity / .9), dia = 1 - noite, vt = vento();

    // vento, chuva, trovão, grilos, pássaros
    alvo(V.vento.g.gain, CFG.ambiente * CFG.vento * .11 * vt * (.25 + .75 * ext));
    alvo(V.vento.f.frequency, 330 + 280 * vt + 250 * rain);
    alvo(V.chuva.g.gain, CFG.chuva * .3 * rain * (1 - .5 * S.int));
    alvo(V.chuva.f.frequency, 7500 - 6200 * S.int);
    alvo(V.chuva.gg.gain, CFG.chuva * .5 * rain * (1 - .3 * S.int));
    if (rain > .6) { S.tTrovao -= dt; if (S.tTrovao <= 0) { S.tTrovao = rnd(14, 42); trovao(); } }
    alvo(V.grilo.g.gain, CFG.ambiente * .018 * noite * ext * (1 - rain));
    if (dia > .5 && rain < .2 && ext > .5) { S.tPassaro -= dt; if (S.tPassaro <= 0) { S.tPassaro = rnd(2, 7); passaro(ext * dia); } }

    // turbinas eólicas: "uush" no ritmo das pás (as 2 mais próximas)
    const tur = [];
    for (const l of D.lotes) if (l.turbinasObjs) for (const o of l.turbinasObjs) {
      const x = o.mesh.position.x, z = o.mesh.position.z, d = Math.hypot(P.x - x, P.z - z);
      if (d < 80) tur.push({ o, x, z, d });
    }
    tur.sort((a, b) => a.d - b.d);
    V.tur.forEach((v, i) => {
      const s = tur[i]; if (!s) { alvo(v.am.gain, 0, .15); return; }
      const rz = s.o.rotor.rotation.z, w = clamp(Math.abs(rz - (s.o._rz ?? rz)) / Math.max(dt, .001), 0, 12);
      s.o._rz = rz; s.o._w = (s.o._w || 0) + (w - (s.o._w || 0)) * .2;
      const pulso = .5 + .5 * Math.cos(-rz * 3), amp = .25 + .75 * pulso * pulso;
      alvo(v.am.gain, CFG.turbina * 1.3 * queda(s.d, 75) * abafa * amp * clamp(s.o._w / 1.5), .03);
      alvo(v.f.frequency, 200 + s.o._w * 55); v.pan.pan.value = panDe(s.x, s.z);
    });

    // geradores a gasolina: motor "chug-chug" (partida/parada detectadas pela geração do lote)
    const ger = [];
    for (const l of D.lotes) if (l.uso === 'gerador') {
      const kw = l.kw(), on = kw > 0;
      if (on !== !!l._som) { l._som = on; (on ? partida : parada)(l.x, l.z); }
      if (on) ger.push({ x: l.x, z: l.z, kw, d: Math.hypot(P.x - l.x, P.z - l.z) });
    }
    ger.sort((a, b) => a.d - b.d);
    V.ger.forEach((v, i) => {
      const s = ger[i]; if (!s) { alvo(v.am.gain, 0, .1); alvo(v.lg.gain, 0, .1); return; }
      const base = CFG.gerador * .3 * queda(s.d, 60) * abafa, f0 = 36 + s.kw * .5;
      alvo(v.am.gain, base); alvo(v.lg.gain, base * .5); alvo(v.o1.frequency, f0); alvo(v.o2.frequency, f0 / 2); alvo(v.lfo.frequency, 10 + s.kw * .25);
      v.pan.pan.value = panDe(s.x, s.z);
    });

    // zumbido elétrico dos transformadores
    let hs = { k: 0, x: 0, z: 0 };
    for (const h of HUMS) { const k = queda(Math.hypot(P.x - h.x, P.z - h.z), h.r) * h.v; if (k > hs.k) hs = { k, x: h.x, z: h.z }; }
    alvo(V.hum.am.gain, CFG.ambiente * .06 * hs.k * abafa); V.hum.pan.pan.value = panDe(hs.x, hs.z);

    // refrigeradores do terraço: hélices (velocidade e nº dependem do nível)
    let nivel = 0, soma = 0, perto = null, dm = 1e9;
    for (const c of COOLERS) {
      const x = galpao.px + c.grp.position.x, z = galpao.pz + c.grp.position.z, d = Math.hypot(P.x - x, P.z - z, P.y + 1.6 - 5.9);
      nivel += queda(d, 38) * c.vel / 2.2; soma += c.vel; if (d < dm) { dm = d; perto = { x, z }; }
    }
    if (perto) {
      const vm = soma / COOLERS.length, muff = dcIn ? .5 : 1, base = CFG.cooler * .22 * clamp(nivel) * muff;
      alvo(V.cool.am.gain, base); alvo(V.cool.lg.gain, base * .35); alvo(V.cool.lfo.frequency, 3.6 * vm); alvo(V.cool.f.frequency, 260 + vm * 90);
      V.cool.pan.pan.value = panDe(perto.x, perto.z);
    } else alvo(V.cool.am.gain, 0);

    // data center: ventoinhas dos racks, zumbido grave e HDs; mais alto na sala de racks, abafado fora
    const bai = totalBaias(), nr = racks.length, calor = clamp(cargaTermica() / Math.max(coolingTotal(), 3));
    const lx = P.x - galpao.px, lz = P.z - galpao.pz;
    const dRet = Math.hypot(Math.max(-10.3 - lx, 0, lx - galpao.xDir - .3), Math.max(Math.abs(lz) - 11.3, 0));
    const noSala = dcIn ? ((lx > -2 && lz > -3.6 && lz < 8) ? 1 : .45) : queda(dRet, 22) * .3;
    alvo(V.dc.out.gain, clamp(.12 + nr * .06 + bai * .012) * noSala * CFG.dc);
    alvo(V.dc.hiss.gain, bai > 0 ? .1 + .1 * calor : .03); alvo(V.dc.hum.gain, .05);
    alvo(V.dc.hf.frequency, 2000 + 1500 * calor); alvo(V.dc.lp.frequency, dcIn ? 12000 : 550);
    if (dcIn && noSala === 1 && bai > 0 && Math.random() < Math.min(14, bai * .35) * dt) tique();

    // portão
    if (galpao.portaoAberto !== S.portao) { S.portao = galpao.portaoAberto; portaoSom(S.portao); }

    // passos (no ritmo do balanço da câmera)
    const pn = Math.floor(player.bob * 3.2 / Math.PI);
    if (pn !== S.passo) { S.passo = pn; if (Math.hypot(player.vel.x, player.vel.z) > .6 && player.gravidade.noChao && !player.sentado) passo(Math.hypot(player.vel.x, player.vel.z) > 6.5); }
  }
  return { iniciar, atualizar, acao, toast, ui };
})();
ATUALIZAVEIS.push(dt => SOM.atualizar(dt));
{ const _t = hud.toast; hud.toast = m => { _t(m); SOM.toast(m); }; }
{ const _a = Modal.abrir; Modal.abrir = h => { _a(h); SOM.ui(1); }; }
document.addEventListener('click', e => { if (e.target.closest && e.target.closest('.btn, .slot, .hot-slot')) SOM.ui(0); });
['pointerdown', 'keydown', 'click'].forEach(ev => addEventListener(ev, () => SOM.iniciar(), { passive: true }));
"""

# 1) injeta o sistema de som logo depois da criação da interação (hud, player, galpão etc. já existem)
sub("const interacao = criarInteracao({ camera, scene, hud });",
    "const interacao = criarInteracao({ camera, scene, hud });\n" + BLOCO)

# 2) ao apertar F, toca o som da ação (porta, geladeira, TV, interruptor, cadeira...)
sub("if (alvoF) alvoF.userData.interagir();",
    "if (alvoF) { const _rot = txt(alvoF.userData.rotulo); alvoF.userData.interagir(); if (typeof SOM !== 'undefined') SOM.acao(_rot); }")

if erros:
    print("ATENÇÃO — não aplicado (arquivo NÃO salvo):")
    for e in erros: print(" -", e)
    sys.exit(1)

open(arq, "w", encoding="utf-8").write(s)
print("OK! Sons instalados. Backup em", arq + ".bak")