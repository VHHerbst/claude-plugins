# Histórico

Mudanças no catálogo, da mais recente para a mais antiga. Cada linha diz **o que
mudou** e **o que aconteceu para termos aprendido isso** — a segunda parte é a que faz
a regra colar.

---

## 2026-08-06 — plugin `chatbot`, a primeira construção guiada

Sete comandos que levam alguém de zero a uma plataforma própria de automação de
conversas — `start`, `schema`, `channel`, `engine`, `builder`, `dispatch`, `launch`.

É o primeiro plugin de outra família: os outros são **disciplinas** (servem sempre,
em qualquer projeto), este é uma **construção** (tem princípio, meio e fim). A ordem
dos comandos é a parte importante, e existe por um motivo — quem desiste destes
projetos desiste sempre no mesmo sítio, a construir o editor visual de fluxos na
primeira semana.

Decisões que ficam registadas:

- **Não se chama `manychat`.** É marca de outra empresa; usá-la no nome sugere
  ligação oficial e vira problema exatamente quando o projeto ganha visibilidade. A
  promessa vive na descrição, onde é referência descritiva.
- **O `comms` como disciplina não foi criado**, de propósito. Extrai-se quando um
  segundo produto repetir o mesmo trabalho — com um exemplo só, a abstração é
  adivinhação.
- Os travões do `dispatch` (opt-out imediato, ritmo, paragem por taxa de falhas) não
  são zelo a mais: o custo do erro ali não é um bug, é o canal de vendas de um
  cliente.

---

## 2026-08-06 — plugin `design`

Cinco comandos que cobrem o ciclo todo, de pesquisar a entregar ao dev:

- `/design:research` — síntese de pesquisa. Separa **o que foi dito**, **o que foi
  observado** e **o que é interpretação tua**; um achado só é padrão com 3 sessões
  independentes, e nada de percentagens com amostra pequena.
- `/design:critique` — crítica ordenada por dano (bloqueia / atrasa / preferência),
  com as preferências à parte e sem peso. Percorre a tarefa, não o ecrã.
- `/design:copy` — texto de interface. Botão diz o que faz, erro diz o que fazer a
  seguir, estado vazio ensina. Fixa PT-PT ou PT-BR e não mistura.
- `/design:accessibility` — auditoria WCAG por tarefa: completar o fluxo só com
  teclado, sem ver, e com dificuldade motora. Diz o que as ferramentas automáticas
  não apanham, que é a maior parte.
- `/design:handoff` — lê o design system **antes** de especificar, sete estados por
  componente, e a secção "o que acontece quando…" que falta em quase todos.

Com isto o catálogo passa a ter **um plugin por caixa de ferramentas**: o designer
instala `design`, o programador instala `ops`, e ninguém carrega comandos que não são
para si.

---

## 2026-08-06 — plugin `ops` e arquitetura de nomes

O catálogo passou a ter uma língua só. Tudo o que é engenharia vive no plugin `ops`,
com os comandos nomeados como operações:

- `/ops:recon` — **novo.** Revisão de PR ou do diff local. Oito agentes a encontrar,
  um agente por achado a duvidar com score 0–100, e só passa acima de 80. Baseado no
  plugin oficial `code-review`, com eixos nossos: falhas silenciosas, RLS e migrações
  Supabase, env vars obrigatórias, mock em produção e docs por atualizar.
- `/ops:sniper` — o Protocolo Sniper, sem alterações às regras. Só mudou de sítio.
- `/ops:triage` — **novo.** Auditoria de dívida técnica ordenada por quanto custa de
  facto. A regra central: código feio que funciona e não bloqueia nada não é dívida.
- `/ops:doctrine` — **novo.** ADRs com as duas secções que quase todos saltam —
  alternativas rejeitadas e gatilho de revisão.

**Porquê a mudança de nomes:** `/protocolo-sniper:protocolo-sniper` gaguejava, e isso
era o sintoma de um plugin construído à volta de uma skill em vez de à volta de uma
disciplina. Com alunos e seguidores a instalar isto, um nome mudado depois custa a
toda a gente — agora custava a cinco pessoas.

O plugin `protocolo-sniper` fica no catálogo como redirecionamento e será removido.
O bloco `renames` do `marketplace.json` faria isto sozinho, mas exige Claude Code
≥ 2.1.193 e rebenta a validação em versões anteriores.

---

## 2026-08-04 — versão inicial

As dez regras de arranque, tiradas do modo de trabalho que já usávamos:

1. Ler antes de escrever
2. Migrações não são corridas por ti
3. Commits cirúrgicos — nunca `git add -A`
4. Trio verde antes de dar por feito
5. Verificar na ground truth, nunca num sinal intermédio
6. Ordem de rollout pensada
7. Código no GitHub não está live
8. Fechar cada bloco com resumo por-pessoa
9. Superfície nova = checklist transversal
10. Não prometas o que não verificaste

---

## Como propor uma alteração

Se apanhaste um erro que uma regra nova teria evitado, diz. A regra melhor é sempre a
que nasce de algo que correu mal a sério — não de teoria.

Fala com o Vitor, ou abre uma issue em `VHHerbst/claude-plugins`.
