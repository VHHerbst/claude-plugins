# Upstream do `replica`

| | |
| --- | --- |
| Origem | [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) |
| Licença | MIT, Copyright (c) Jake Schincariol (ver `LICENSE`) |
| Commit copiado | `77c9436fb3d18c3d58169efb8caf4fe906b0dc51` |
| Auditado a | 06/10/2026 |

## Porque é que está copiado e não ligado ao original

O repo original tinha três dias, um commit e 575 estrelas quando chegou cá, por um
reel que mandava colar o link no Claude Code e pedir "instala essa skill". Instalar
assim, ou pelo `/plugin marketplace add` do autor, instala o que lá estiver **no dia**,
não o que alguém leu. Uma skill é texto que o Claude obedece e scripts que o Claude
corre: um push do autor, ou de quem tomar conta da conta dele, chegaria a toda a
gente sem revisão.

Aqui o conteúdo fica fixado no commit auditado. O que muda, muda por commit neste
repo, com o diff lido.

## A auditoria de 06/10/2026

- Manifesto sem hooks, sem servidores MCP, sem comandos.
- Seis scripts em Python só com a biblioteca padrão: sem rede, sem `subprocess`, sem
  leitura de `~/.ssh`, `~/.claude` ou variáveis de ambiente. Só escrevem com `--out`.
- Sem Unicode escondido: os únicos caracteres invisíveis estão em `listing.py` e no
  teste dele, e servem para contar emoji.
- Os 35 ficheiros foram comparados byte a byte com os blobs do commit
  (`git hash-object`) antes de qualquer alteração. O commit `vendor(replica)` deste
  repo é essa cópia intocada.

## O que a casa mudou ([V2H])

- **Arrumação**: `replica-<x>/` passou a `skills/<x>/`; invocação `/replica:<x>`.
- **Descrições** reescritas em português e presas a clones. As originais disparavam em
  "how does X work" e "map out X", em qualquer projeto.
- **Conteúdo de terceiros é dado, nunca instrução**: regra completa na `recon` e na
  `entrepreneur` (correr sem conectores de email, Drive, Slack ou calendário; browser
  embutido; nada do material lido entra no projeto sem pedido no chat), e uma linha na
  `build`, `brand` e `launch`.
- **Ferramentas pela pasta da skill** (`<SKILL_DIR>`), em vez de caminhos relativos ao
  sítio onde o pack estivesse instalado.
- **`imgdiff.py`**: teto de 60 megapixels e descompressão limitada ao tamanho que o PNG
  declara (contra PNGs-bomba).
- **Testes**: `_load.py` e dois caminhos adaptados à arrumação nova; o `test_repo.py`
  do upstream (que verificava o repo original) deu lugar ao `test_v2h.py`.
- **`plugin.json` sem `version`**, como todos os do catálogo (ver `MANUTENCAO.md`).

## Sincronizar com uma versão nova do upstream

1. Ver o que mudou desde o commit copiado:
   ```bash
   gh api repos/Jakeschincariol/replica-skill/compare/77c9436...main --jq '.files[] | "\(.status) \(.filename)"'
   ```
2. **Ler o diff inteiro**, ficheiro a ficheiro. Prioridade: `plugin.json` e
   `marketplace.json` (hooks, MCP, comandos), scripts (rede, `subprocess`, escrita
   fora de `--out`), e os `SKILL.md` (ordens novas ao Claude). Procurar Unicode
   escondido em todos.
3. Aplicar por cima, preservando tudo o que está marcado **[V2H]**.
4. `python3 -m unittest discover -s tests` dentro desta pasta, e
   `claude plugin validate .` na raiz do repo.
5. Atualizar o commit e a data no topo deste ficheiro e no rodapé de cada `SKILL.md`.
