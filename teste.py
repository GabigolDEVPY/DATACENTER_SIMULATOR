#!/usr/bin/env python3
import sys
import shutil
from pathlib import Path

SYNC_CALL = "try { if (typeof inventario !== 'undefined' && inventario && inventario.sincronizar) inventario.sincronizar(); } catch (e) {}"

TROCAS = [
    (
        "  function fechar() {\n"
        "    root.innerHTML = '';\n"
        "    root.classList.remove('visivel');\n"
        "    if (rendererDom) rendererDom.requestPointerLock();\n"
        "  }",
        "  function fechar() {\n"
        "    root.innerHTML = '';\n"
        "    root.classList.remove('visivel');\n"
        "    if (rendererDom) rendererDom.requestPointerLock();\n"
        "    " + SYNC_CALL + "\n"
        "  }",
        "Modal.fechar()",
    ),
    (
        "  let sincronizando = false;\n"
        "  async function sincronizarComServidor() {\n"
        "    if (sincronizando) return;\n"
        "    sincronizando = true;",
        "  let sincronizando = false, pendente = false;\n"
        "  async function sincronizarComServidor() {\n"
        "    if (sincronizando) { pendente = true; return; }\n"
        "    sincronizando = true;",
        "guarda de sincronização",
    ),
    (
        "    } finally {\n"
        "      sincronizando = false;\n"
        "    }\n"
        "  }",
        "    } finally {\n"
        "      sincronizando = false;\n"
        "      if (pendente) { pendente = false; sincronizarComServidor(); }\n"
        "    }\n"
        "  }",
        "reexecução pendente",
    ),
    (
        "saldo: () => saldo, ganhar, gastar, vender, get aberto() { return aberto; } };",
        "saldo: () => saldo, ganhar, gastar, vender, sincronizar: sincronizarComServidor, get aberto() { return aberto; } };",
        "retorno do inventário",
    ),
]


def main():
    if len(sys.argv) != 2:
        print("Uso: python corrigir.py arquivo.html", file=sys.stderr)
        sys.exit(1)

    origem = Path(sys.argv[1])
    if not origem.is_file():
        print(f"Erro: arquivo não encontrado: {origem}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(origem, "r", encoding="utf-8", newline="") as f:
            texto = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}", file=sys.stderr)
        sys.exit(1)

    crlf = "\r\n" in texto
    if crlf:
        texto = texto.replace("\r\n", "\n")

    if "sincronizarComServidor" not in texto:
        print("Erro: a sincronização do inventário com o servidor não existe neste arquivo.", file=sys.stderr)
        sys.exit(1)

    for antigo, novo, nome in TROCAS:
        n = texto.count(antigo)
        if n != 1:
            print(f"Erro: âncora '{nome}' encontrada {n} vez(es) (esperado 1). Arquivo já corrigido ou diferente.", file=sys.stderr)
            sys.exit(1)
        texto = texto.replace(antigo, novo)

    if crlf:
        texto = texto.replace("\n", "\r\n")

    destino = origem.with_name(origem.stem + "_corrigido" + origem.suffix)
    backup = origem.with_name(origem.name + ".bak")

    try:
        if not backup.exists():
            shutil.copy2(origem, backup)
        with open(destino, "w", encoding="utf-8", newline="") as f:
            f.write(texto)
    except Exception as e:
        print(f"Erro ao gravar arquivos: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {destino}")
    print(f"Backup: {backup}")


if __name__ == "__main__":
    main()