#!/usr/bin/env python3
"""
Uso:  python posicao_racks.py index.html
Saída: index_posicao.html
"""
import sys
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("Uso: python posicao_racks.py arquivo.html")

src = Path(sys.argv[1])
html = src.read_text(encoding="utf-8").replace("\r\n", "\n")


def trocar(texto, antigo, novo, nome):
    if texto.count(antigo) != 1:
        sys.exit(f"[ERRO] trecho '{nome}' não encontrado (ou duplicado). Nada foi gravado.")
    print(f"[ok] {nome}")
    return texto.replace(antigo, novo)


# 1) Cada vaga de rack ganha uma position fixa (1, 2, 3...) na ordem de criação.
html = trocar(
    html,
    "const VAGAS_RACK = [];",
    "const VAGAS_RACK = [];\n"
    "const POSICAO_BASE = 1;   // se o servidor começa em 0, mude para 0\n"
    "let VAGA_SEQ = 0;",
    "constantes de position",
)

html = trocar(
    html,
    "function criarVagaRack(g, x, z) {",
    "function criarVagaRack(g, x, z, posFixa) {\n"
    "  const pos = posFixa !== undefined ? posFixa : (POSICAO_BASE + VAGA_SEQ++);",
    "criarVagaRack com position",
)

html = trocar(
    html,
    "VAGAS_RACK.push({ x, z, v, marc }); atualizarVagasRack();",
    "VAGAS_RACK.push({ x, z, v, marc, pos }); atualizarVagasRack();",
    "vaga guarda position",
)

# 2) A vaga visível é sempre a de menor position livre.
html = trocar(
    html,
    """function atualizarVagasRack() {
  const ord = VAGAS_RACK.slice().sort((a, b) => Math.abs(a.z - b.z) > .01 ? a.z - b.z : a.x - b.x);
  ord.forEach((e, i) => { e.v.visible = e.marc.visible = (i === 0); });
}""",
    """function atualizarVagasRack() {
  const ord = VAGAS_RACK.slice().sort((a, b) => a.pos - b.pos);
  ord.forEach((e, i) => { e.v.visible = e.marc.visible = (i === 0); });
}""",
    "vaga visível por position",
)

# 3) Rack instalado sabe sua position; ao remover, a vaga volta com a mesma position.
html = trocar(
    html,
    "aoRemover: () => { const k = racks.indexOf(obj); if (k >= 0) racks.splice(k, 1); criarVagaRack(g, x, z); }",
    "aoRemover: () => { const k = racks.indexOf(obj); if (k >= 0) racks.splice(k, 1); criarVagaRack(g, x, z, pos); }",
    "vaga volta com a mesma position",
)

html = trocar(
    html,
    "    racks.push(obj);",
    "    obj.position = pos;\n    racks.push(obj);",
    "rack guarda position",
)

# 4) Instalar rack: manda id + position.
html = trocar(
    html,
    "apiFetch(API.instalarRack, { data: { id: idSrv } })",
    "apiFetch(API.instalarRack, { data: { id: idSrv, position: pos } })",
    "POST de instalar com position",
)

# 5) Baias: lembra quais slots estavam ocupados ao remover o rack (G) e restaura nos mesmos.
html = trocar(
    html,
    "    contarBaias() { return baias.filter(Boolean).length; },",
    "    contarBaias() { return baias.filter(Boolean).length; },\n"
    "    indicesBaias() { return baias.map((b, i) => b ? i : -1).filter(i => i >= 0); },",
    "indicesBaias",
)

html = trocar(
    html,
    "nome: nomeBase, rackNome: nomeBase, baiasQtd: n,",
    "nome: nomeBase, rackNome: nomeBase, baiasQtd: n, baiasIdx: obj.indicesBaias(),",
    "inventário guarda slots das baias",
)

html = trocar(
    html,
    "const restaurarBaias = novo => { for (let k = 0; k < nBaias; k++) novo.instalarBaiaDireto(k); };",
    "const idxBaias = Array.isArray(it.baiasIdx) ? it.baiasIdx : Array.from({ length: nBaias }, (_, k) => k);\n"
    "    const restaurarBaias = novo => idxBaias.forEach(k => novo.instalarBaiaDireto(k));",
    "restaurar baias nos mesmos slots",
)

# 6) Load da página: racks em ordem de position, baias em ordem de position.
ini = html.find("function carregarMundoDoDjango() {")
fim = html.find("\ncarregarMundoDoDjango();", ini)
if ini < 0 or fim < 0:
    sys.exit("[ERRO] carregarMundoDoDjango não encontrada. Nada foi gravado.")

nova = """function carregarMundoDoDjango() {
  const lista = (typeof data !== 'undefined' && data && Array.isArray(data.racks)) ? data.racks.slice() : [];
  if (!lista.length) return;
  const num = v => { const n = Number(v); return Number.isFinite(n) ? n : Infinity; };
  lista.sort((a, b) => num(a.position) - num(b.position));          // 1, 2, 3...
  const toastOrig = hud.toast;
  hud.toast = () => {};                       // sem spam de avisos no carregamento
  try {
    lista.forEach(rd => {
      // vaga com a mesma position do rack; se não existir/estiver ocupada, usa a menor livre
      let vaga = VAGAS_RACK.find(e => e.pos === Number(rd.position));
      if (!vaga) vaga = VAGAS_RACK.slice().sort((a, b) => a.pos - b.pos)[0];
      if (!vaga) { console.warn('Sem vagas de rack livres para:', rd.name); return; }
      const obj = vaga.v.userData.interagir(true, rd.name || ('Rack ' + rd.id));
      if (!obj) return;
      obj.djangoId = rd.id;
      // baias em ordem de position, cada uma no slot da sua position
      const usados = new Set();
      (rd.bays || []).slice().sort((a, b) => num(a.position) - num(b.position)).forEach(b => {
        let i = Number(b.position) - POSICAO_BASE;
        if (!Number.isInteger(i) || i < 0 || i >= 15 || usados.has(i)) {
          i = -1;
          for (let k = 0; k < 15; k++) if (!usados.has(k)) { i = k; break; }
        }
        if (i < 0) return;
        usados.add(i);
        obj.instalarBaiaDireto(i);
      });
    });
  } finally {
    hud.toast = toastOrig;
  }
}"""
html = html[:ini] + nova + html[fim:]
print("[ok] load por position (racks e baias)")

saida = src.with_name(src.stem + "_posicao" + src.suffix)
saida.write_text(html, encoding="utf-8")
print(f"\nPronto: {saida}")