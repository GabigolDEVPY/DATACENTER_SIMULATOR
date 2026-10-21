#!/usr/bin/env python3
import re
import sys
import shutil
from pathlib import Path


def flex(texto):
    return r"\s*".join(re.escape(t) for t in texto.split())


class Patcher:
    def __init__(self, txt):
        self.txt = txt
        self.falhas = []

    def um(self, nome, antigo, novo):
        r, n = re.subn(flex(antigo), lambda m: novo, self.txt, count=1, flags=re.S)
        if n == 0:
            self.falhas.append(nome)
        else:
            self.txt = r

    def todos(self, nome, antigo, novo):
        r, n = re.subn(flex(antigo), lambda m: novo, self.txt, flags=re.S)
        if n == 0:
            self.falhas.append(nome)
        else:
            self.txt = r

    def regex(self, nome, pat, novo):
        r, n = re.subn(pat, lambda m: novo, self.txt, count=1, flags=re.S)
        if n == 0:
            self.falhas.append(nome)
        else:
            self.txt = r


SPLITS_NOVO = r"""function splitsParede(g, xIni, xFim) {
  const S = g.sala;
  const lados = [[S.zFundo + S.esp / 2 + .13, 0, 1], [S.zFrente - S.esp / 2 - .13, Math.PI, -1]];
  const fontes = [];
  for (let k = 0; ; k++) {
    const x = 1.5 + 4 * k;
    if (x > xFim - .3) break;
    if (x < xIni + .3) continue;
    lados.forEach(([z, ry, dir]) => {
      const u = new THREE.Group(); u.position.set(x, 4.1, z); u.rotation.y = ry; g.group.add(u);
      const add = (geo, mat, px, py, pz) => { const m = new THREE.Mesh(geo, mat); m.position.set(px, py, pz); m.raycast = () => {}; u.add(m); };
      add(ARM.geoSplit, ARM.corpo, 0, 0, 0);
      add(ARM.geoFenda, ARM.escuro, 0, -.07, .125);
      add(ARM.geoLedS, ARM.led, .45, .06, .125);
      fontes.push({ x, z, dir });
    });
  }
  if (!fontes.length) return;

  // ar frio: nuvem macia (partículas com alpha individual), sai da fenda, abre em leque e cai devagar
  const NP = 18, N = fontes.length * NP;
  const pos = new Float32Array(N * 3), alp = new Float32Array(N), siz = new Float32Array(N);
  const rA = new Float32Array(N), rB = new Float32Array(N), rC = new Float32Array(N);
  for (let i = 0; i < N; i++) { rA[i] = Math.random(); rB[i] = Math.random(); rC[i] = Math.random(); }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('aAlpha', new THREE.BufferAttribute(alp, 1));
  geo.setAttribute('aSize', new THREE.BufferAttribute(siz, 1));
  const mat = new THREE.ShaderMaterial({
    uniforms: { uScale: { value: 600 } },
    transparent: true, depthWrite: false,
    vertexShader: `
      attribute float aAlpha; attribute float aSize; uniform float uScale; varying float vA;
      void main() {
        vA = aAlpha;
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = min(aSize * uScale / max(-mv.z, 0.1), 220.0);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      varying float vA;
      void main() {
        vec2 c = gl_PointCoord - 0.5;
        float d = length(c) * 2.0;
        float a = exp(-d * d * 3.2) * smoothstep(1.0, 0.82, d) * vA;
        gl_FragColor = vec4(0.90, 0.96, 1.0, a);
      }`
  });
  const pts = new THREE.Points(geo, mat);
  pts.frustumCulled = false; pts.raycast = () => {}; g.group.add(pts);
  let t = 0;
  ATUALIZAVEIS.push(dt => {
    t += dt;
    let kf = .35;
    try { kf = coolingTotal() > 0 ? 1 : .35; } catch (e) {}
    try { mat.uniforms.uScale.value = window.innerHeight * Math.min(window.devicePixelRatio || 1, 1.5) * .652; } catch (e) {}
    let n = 0;
    fontes.forEach((f, fi) => {
      for (let p = 0; p < NP; p++, n++) {
        const s = (t * .16 + p / NP + rA[n] * .08 + fi * .137) % 1;
        const e = 1 - Math.pow(1 - s, 1.7);
        const leque = (rB[n] - .5) * 2 * (.15 + s * 1.7);
        const sway = Math.sin(t * .9 + rC[n] * 6.28 + s * 3) * .22 * s;
        pos[n * 3]     = f.x + leque + sway;
        pos[n * 3 + 1] = 3.98 - e * .55 - s * s * 1.15 + (rC[n] - .5) * .25 * s;
        pos[n * 3 + 2] = f.z + f.dir * (.18 + e * 3.6);
        siz[n] = .28 + s * 1.5 + rA[n] * .25;
        alp[n] = Math.min(1, s / .1) * Math.pow(1 - s, 1.4) * .30 * kf;
      }
    });
    geo.attributes.position.needsUpdate = true;
    geo.attributes.aAlpha.needsUpdate = true;
    geo.attributes.aSize.needsUpdate = true;
  });
}
"""

FILEIRAS_NOVAS = "[-9.4, -6.1, -2.8, .5, 3.8]"
FILEIRAS_ANT = "[-9.4, -6.9, -4.4, -1.9]"


def aplicar(txt):
    p = Patcher(txt)

    # 5 fileiras, corredores 50% maiores (passo 3,3 m)
    p.todos("fileiras de racks", FILEIRAS_ANT, FILEIRAS_NOVAS)

    # sala de racks ampliada ate perto do portao + porta na parede esquerda alinhada a um corredor
    p.um("SALA",
         "zFrente: 1.0, portaZ0: -3.95, portaZ1: -2.35, esp: .25 }",
         "zFrente: 7.4, portaZ0: -1.95, portaZ1: -.35, esp: .25 }")

    # faixas amarelas nos novos corredores
    p.um("faixas do chao",
         "[-8.15, -5.65, -3.15, -.65].forEach(z => {",
         "[-7.75, -4.45, -1.15, 2.15, 5.6].forEach(z => {")

    # refrigeradores do terraco alinhados com as 5 fileiras
    p.um("vagas cooler",
         "vagasCooler(g, [[1, -8.15], [4.5, -8.15], [8, -8.15], [1, -3.15], [4.5, -3.15], [8, -3.15]]);",
         "vagasCooler(g, [[1, -7.75], [4.5, -7.75], [8, -7.75], [1, -1.15], [4.5, -1.15], [8, -1.15], [1, 5.45], [4.5, 5.45], [8, 5.45]]);")
    p.um("vagas cooler expansao",
         "vagasCooler(galpao, [[xA + 2.5, -8.15], [xA + 7.5, -8.15], [xA + 2.5, -3.15], [xA + 7.5, -3.15]]);",
         "vagasCooler(galpao, [[xA + 2.5, -7.75], [xA + 7.5, -7.75], [xA + 2.5, -1.15], [xA + 7.5, -1.15], [xA + 2.5, 5.45], [xA + 7.5, 5.45]]);")
    p.um("CZS",
         "CZS = [-8.15, -3.15]",
         "CZS = [-7.75, -1.15, 5.45]")
    p.um("offset dos canos do terraco",
         "return cz + (zr >= cz ? 1.3 : -1.3);",
         "return cz + (zr >= cz ? 1.65 : -1.65);")

    # mensagem da expansao
    p.um("toast expansao",
         "4 fileiras de vagas marcadas.",
         "5 fileiras de vagas marcadas.")

    # fumaca mais bonita
    p.regex("splitsParede",
            r"function splitsParede\([^)]*\)\s*\{.*?\n\}\n",
            SPLITS_NOVO)

    return p.txt, p.falhas


def main():
    if len(sys.argv) != 2:
        print("Uso: python corrigir_html_2.py caminho/arquivo.html")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.is_file():
        print(f"Erro: arquivo nao encontrado: {src}")
        sys.exit(1)

    try:
        with open(src, "r", encoding="utf-8", newline="") as f:
            original = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    crlf = "\r\n" in original
    txt = original.replace("\r\n", "\n")

    novo, falhas = aplicar(txt)
    if falhas:
        print("Erro: nao foi possivel aplicar as seguintes correcoes (use o HTML ja corrigido pelo script anterior):")
        for n in falhas:
            print(f"  - {n}")
        print("Nenhum arquivo foi gerado.")
        sys.exit(2)

    if crlf:
        novo = novo.replace("\n", "\r\n")

    try:
        bak = src.with_name(src.name + ".bak")
        if not bak.exists():
            shutil.copy2(src, bak)

        dst = src.with_name(f"{src.stem}_v2{src.suffix}")
        i = 1
        while dst.exists():
            dst = src.with_name(f"{src.stem}_v2_{i}{src.suffix}")
            i += 1

        with open(dst, "w", encoding="utf-8", newline="") as f:
            f.write(novo)
    except Exception as e:
        print(f"Erro ao gravar arquivos: {e}")
        sys.exit(1)

    print(f"Backup: {bak}")
    print(f"Gerado: {dst}")


if __name__ == "__main__":
    main()