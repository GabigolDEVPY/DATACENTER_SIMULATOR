#!/usr/bin/env python3
"""
Patch: carrega no mundo os racks e baias que vêm do Django (variável `data`).

Uso:
    python patch_carregar_racks.py caminho/do/template.html

Cria um backup (.bak) e aplica o patch no próprio arquivo. É idempotente.
Formato esperado de data:
    {"racks": [{"id": 1, "name": "Rack 1", "bays": [{"id": 1, "status": false}]}]}
"""
import re
import shutil
import sys

MARCA = "PATCH-DJANGO-RACKS"


def sub(texto, padrao, novo, nome):
    r, n = re.subn(padrao, lambda m: novo, texto, count=1, flags=re.S)
    if n != 1:
        sys.exit(f"ERRO: trecho '{nome}' não encontrado. Patch NÃO aplicado.")
    return r


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "mundozinho.html"
    with open(caminho, encoding="utf-8") as f:
        html = f.read()

    if MARCA in html:
        sys.exit("Patch já aplicado neste arquivo.")

    # 1) Vaga de rack: aceita instalação direta (sem gastar item) e nome vindo do Django
    html = sub(
        html,
        r"v\.userData\.interagir = \(\) => \{\s*const it = inventario\.procurarItem\(i => i\.tipo === 'rack'\);\s*"
        r"if \(!it\) \{[^}]*\}\s*inventario\.removerItem\(i => i === it\); g\.group\.remove\(v\); liberar\(v\);",
        "v.userData.interagir = (gratis, nomeDjango) => {\n"
        "    if (gratis !== true) {\n"
        "      const it = inventario.procurarItem(i => i.tipo === 'rack');\n"
        "      if (!it) { hud.toast('Sem Rack no inventário — compre na Loja do terminal.'); return; }\n"
        "      inventario.removerItem(i => i === it);\n"
        "    }\n"
        "    g.group.remove(v); liberar(v);",
        "vaga de rack (interagir)",
    )
    html = sub(
        html,
        r"nomeBase: proximoNomeRack\(\),",
        "nomeBase: (typeof nomeDjango === 'string' && nomeDjango) ? nomeDjango : proximoNomeRack(),",
        "nomeBase",
    )
    html = sub(
        html,
        r"hud\.toast\('Rack instalado \(vazio\) — instale baias nele\. Aperte G na mira para remover\.'\);",
        "hud.toast('Rack instalado (vazio) — instale baias nele. Aperte G na mira para remover.');\n"
        "    return obj;",
        "retorno do rack",
    )

    # 2) Baia: instalação direta (sem item do inventário)
    html = sub(
        html,
        r"function instalarBaia\(i\) \{\s*if \(baias\[i\]\) return;\s*"
        r"const item = inventario\.procurarItem\(it => it\.tipo === 'baia'\);\s*"
        r"if \(!item\) \{[^}]*\}\s*inventario\.removerItem\(it => it === item\);",
        "function instalarBaia(i, gratis) {\n"
        "    if (baias[i]) return;\n"
        "    if (gratis !== true) {\n"
        "      const item = inventario.procurarItem(it => it.tipo === 'baia');\n"
        "      if (!item) { hud.toast('Sem baias no inventário.'); return; }\n"
        "      inventario.removerItem(it => it === item);\n"
        "    }",
        "instalarBaia",
    )
    html = sub(
        html,
        r"contarBaias\(\) \{ return baias\.filter\(Boolean\)\.length; \},",
        "contarBaias() { return baias.filter(Boolean).length; },\n"
        "    instalarBaiaDireto(i) { instalarBaia(i, true); },\n"
        "    nomeBase,",
        "contarBaias",
    )

    # 3) Carregador: roda uma vez ao iniciar o mundo
    carregador = """const interacao = criarInteracao({ camera, scene, hud });

/* PATCH-DJANGO-RACKS: monta os racks e baias existentes vindos do Django */
function carregarMundoDoDjango() {
  const lista = (typeof data !== 'undefined' && data && Array.isArray(data.racks)) ? data.racks : [];
  if (!lista.length) return;
  const toastOrig = hud.toast;
  hud.toast = () => {};                       // sem spam de avisos no carregamento
  try {
    lista.forEach(rd => {
      const ord = VAGAS_RACK.slice().sort((a, b) => Math.abs(a.z - b.z) > .01 ? a.z - b.z : a.x - b.x);
      const vaga = ord[0];
      if (!vaga) { console.warn('Sem vagas de rack livres para:', rd.name); return; }
      const obj = vaga.v.userData.interagir(true, rd.name || ('Rack ' + rd.id));
      if (!obj) return;
      obj.djangoId = rd.id;
      (rd.bays || []).slice(0, 15).forEach((b, i) => obj.instalarBaiaDireto(i));
    });
  } finally {
    hud.toast = toastOrig;
  }
}
carregarMundoDoDjango();
"""
    html = sub(
        html,
        r"const interacao = criarInteracao\(\{ camera, scene, hud \}\);",
        carregador,
        "criarInteracao",
    )

    shutil.copyfile(caminho, caminho + ".bak")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK! Patch aplicado em {caminho} (backup: {caminho}.bak)")


if __name__ == "__main__":
    main()