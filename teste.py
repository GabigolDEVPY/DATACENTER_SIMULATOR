#!/usr/bin/env python3
import sys, re, shutil, os

HELPERS = r"""const PRECO_SERVIDOR = {};   // preços vindos do Django, chave 'tipo:id'
const EQUIPADOS_SRV = new Set();   // itens do servidor (energia/cooler) instalados no mundo: não voltam ao inventário na sincronização
const NIVEL_SRV = {};              // nível evoluído localmente de itens do servidor, chave 'tipo:id'
const chaveSrv = it => (it && it.djangoId !== undefined && it.djangoId !== null) ? it.tipo + ':' + it.djangoId : null;
function marcarEquipado(it) {
  const k = chaveSrv(it); if (!k) return;
  EQUIPADOS_SRV.add(k);
  if (API.equiparEnergia) apiFetch(API.equiparEnergia, { data: { id: it.djangoId, type: it.tipo } });
}
function devolverItem(tipo, nivel, srvId) {
  const extra = {};
  if (srvId !== undefined && srvId !== null) {
    const k = tipo + ':' + srvId;
    EQUIPADOS_SRV.delete(k);
    NIVEL_SRV[k] = nivel;
    extra.djangoId = srvId; extra.servidor = true;
    if (PRECO_SERVIDOR[k] !== undefined) extra.preco = PRECO_SERVIDOR[k];
    if (API.desequiparEnergia) apiFetch(API.desequiparEnergia, { data: { id: srvId, type: tipo } });
  }
  inventario.adicionarItem({ ...ITENS[tipo], tipo, qtd: 1, nivel, ...extra });
}"""

ALIASES = r"""
  Object.assign(TIPO_SRV, {
    solar: 'painel', panel: 'painel', solar_panel: 'painel', painel_solar: 'painel',
    wind: 'turbina', wind_turbine: 'turbina', turbine: 'turbina', eolica: 'turbina', turbina_eolica: 'turbina',
    generator: 'gerador', gasoline_generator: 'gerador',
    ceiling_cooler: 'cooler', roof_cooler: 'cooler', ceilingcooler: 'cooler', refrigerador: 'cooler'
  });"""


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

    if "EQUIPADOS_SRV" in html:
        print("Erro: este arquivo já contém a correção.")
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

    def sub(pattern, repl, label, count=1, flags=0):
        nonlocal html
        html, n = re.subn(pattern, lambda m: m.expand(repl) if False else repl_fn(m, repl), html, count=0 if count == 0 else count, flags=flags)
        if n < 1 or (count and n != count):
            print(f"Erro: trecho não encontrado ({label}): {n} ocorrência(s), esperado {count}.")
            sys.exit(1)

    def repl_fn(m, repl):
        # suporta \1 manualmente, sem interpretar outros escapes
        return re.sub(r"\\(\d)", lambda g: m.group(int(g.group(1))), repl)

    # 1) helpers globais
    sub(r"const PRECO_SERVIDOR = \{\};[^\n]*", HELPERS, "PRECO_SERVIDOR")

    # 2) API (hooks opcionais no backend)
    sub(r"inventario: '/user/inventory/',",
        "inventario: '/user/inventory/',\n  equiparEnergia: null, desequiparEnergia: null,   // opcional: URLs para persistir equipar/desequipar",
        "API.inventario")

    # 3) tipos vindos do servidor (aliases + normalização)
    sub(r"(const TIPO_SRV = \{[^\n]*\};)", "\\1" + ALIASES, "TIPO_SRV")
    sub(r"String\(s\.type \|\| s\.tipo \|\| ''\)\.toLowerCase\(\)",
        "String(s.type || s.tipo || '').toLowerCase().replace(/[\\s-]+/g, '_')", "normalização type")

    # 4) sincronização: não recriar no inventário o que já está instalado
    sub(r"const item = montarItemServidor\(s\);\s*if \(!item\) return;",
        "const item = montarItemServidor(s);\n        if (!item) return;\n"
        "        { const k = chaveSrv(item); if (k) { if (EQUIPADOS_SRV.has(k)) return; if ((NIVEL_SRV[k] || 0) > (item.nivel || 1)) item.nivel = NIVEL_SRV[k]; } }",
        "sincronizarComServidor")

    # 5) vaga do lote: passa o item do inventário para o construtor
    sub(r"ordenarVagasLote\(l\); construir\(x, z, recriar, nivel\);",
        "ordenarVagasLote(l); marcarEquipado(it); construir(x, z, recriar, Math.min(NIVEL_MAX, nivel), it);",
        "vaga.construir")
    sub(r"\(x, z, recriar, nivelIni\) =>", "(x, z, recriar, nivelIni, itSrv) =>", "construtores", count=3)

    # 6) remoção (G): devolve o item do servidor com o mesmo id/nível
    sub(r"inv\.adicionarItem\(\{ \.\.\.ITENS\.(painel|turbina|gerador), tipo: '(?:painel|turbina|gerador)', qtd: 1, nivel: obj\.nivel \}\);",
        "devolverItem('\\1', obj.nivel, itSrv && itSrv.djangoId);", "remover energia", count=3)

    # 7) cooler de teto
    sub(r"criarCoolerTeto\(g, x, z, nivel\);",
        "marcarEquipado(it); criarCoolerTeto(g, x, z, Math.min(COOLER.max, nivel), it);", "vaga cooler")
    sub(r"function criarCoolerTeto\(g, x, z, nivelInicial = 1\) \{",
        "function criarCoolerTeto(g, x, z, nivelInicial = 1, itSrv = null) {", "criarCoolerTeto")
    sub(r"inventario\.adicionarItem\(\{ \.\.\.ITENS\.cooler, tipo: 'cooler', qtd: 1, nivel: obj\.nivel \}\);",
        "devolverItem('cooler', obj.nivel, itSrv && itSrv.djangoId);", "remover cooler")

    try:
        with open(out, "w", encoding="utf-8", newline="") as f:
            f.write(html)
    except Exception as e:
        print(f"Erro ao gravar saída: {e}")
        sys.exit(1)
    print(f"OK: {out}\nBackup: {bak}")


if __name__ == "__main__":
    main()