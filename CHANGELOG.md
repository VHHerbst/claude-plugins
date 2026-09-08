# Histórico

Mudanças no catálogo, da mais recente para a mais antiga. Cada linha diz **o que
mudou** e **o que aconteceu para termos aprendido isso** — a segunda parte é a que faz
a regra colar.

---

## 2026-09-08 — o frontend que parecia sempre feito por IA

Skill nova no **`design`**: **`/design:taste`** — direção visual para landing pages,
portfólios e redesigns.

Todos os frontends gerados por IA convergiam para a mesma cara: gradiente roxo, herói
centrado sobre mesh escuro, três cartões de features iguais, Inter + slate-900. Não é
falta de capacidade — é falta de leitura do brief. O modelo salta para a estética
default em vez de perguntar *para quem é isto e com que linguagem*.

A skill obriga a ordem certa: primeiro uma "design read" declarada em uma linha (tipo
de página, audiência, linguagem visual, sistema de design), depois três dials que
governam tudo (variância de layout, intensidade de motion, densidade visual), e só
então código. Adaptada de [taste-skill](https://github.com/Leonxlnx/taste-skill) de
Leonxlnx (MIT, ~457 mil instalações no skills.sh) — o corpo mantém-se em inglês para
não criar deriva em relação ao original.

## 2026-08-13 — a escrita que falha calada, e o utilizador que se culpa

Regra nova no **`ops:sniper`**: *"Escrita bloqueada não dá erro — dá zero linhas."*

Um gestor de agência cancelou a mesma venda **três vezes**. Das três, o sistema
respondeu "cancelada com sucesso". Das três, a venda ficou onde estava. Ele reportou-o
como se fosse um mistério — e a partir dali passou a duvidar do que o ecrã lhe dizia
em todo o resto do módulo.

Não havia bug nenhum no cancelar. O código fazia `update` direto na tabela e verificava
`error`. Só que, com RLS, um `update` que não casa com nenhuma policy **não é erro**:
afeta zero linhas, o PostgREST devolve `200`, o `error` vem `null`. O papel dele tinha
sido acrescentado ao ecrã muito depois de a policy ter sido escrita — a UI dava-lhe o
botão, a base nunca lho tinha dado.

A varredura ao módulo, feita a seguir, encontrou **mais seis** transições com a mesma
forma, e uma segunda cara do mesmo problema: hierarquia calculada no browser a partir de
uma tabela que aquele papel não pode ler. RLS na leitura não dá erro, dá **lista vazia** —
o filtro de coordenador simplesmente não existia para ele, sem uma única mensagem. Foi
reportado três vezes antes de alguém perceber porquê.

A lição que ficou na regra: **ausência de erro não é confirmação**. Transições vão por RPC
que devolve `{ok, erro}` e o frontend valida o `ok`; permissão que a UI mostra tem de
existir na base; e o que depende de tabelas protegidas resolve-se no servidor.

Entraram também duas perguntas no checklist final — sobre escritas que confirmam que
escreveram, e sobre papéis que veem botões sem guarda que os deixe agir.

---

## 2026-08-12 — `ops:isolate`, e o dia que o ensinou

Skill nova: **`/ops:isolate`**. Separar o teu código da plataforma e dos dados **antes**
de abrir um ficheiro. Nasceu de um dia inteiro num CRM em produção onde quase todo o
tempo perdido foi de diagnóstico, não de correção.

O que aconteceu, por ordem:

Investigou-se uma avaria que não existia. "Não entraram mensagens hoje" foi tomado por
sintoma, quando ninguém tinha enviado nenhuma. A investigação levou a alterar
configuração de produção sem motivo — e, como o painel do fornecedor escreve os
webhooks mas não os deixa ler, **a alteração apagou a única prova** de qual era o
estado anterior. Daí as duas primeiras secções da skill: confirmar que há avaria, e
guardar a prova antes de mexer.

Um deploy que escrevia direto no destino apagou um webhook que funcionava: o download
falhou, o `curl` escreveu a mensagem de erro por cima do ficheiro, e o WhatsApp da
clínica ficou morto uma manhã. Está agora na regra 7 do `sniper` — descarregar para um
sítio temporário e mover só em caso de sucesso.

Descobriu-se que oito Edge Functions simplesmente não existiam no servidor, incluindo
as duas da marcação online. Ninguém se tinha queixado porque **só clientes de fora
passam por ali** — o silêncio lia-se como normalidade. É a secção "quem dá pela falta".

E duas tentativas falhadas de guardar credenciais ensinaram que **arrancar não é
funcionar**: uma função pode responder `200` sem uma única credencial carregada, e o
runtime não dá erro nenhum. A prova tem de passar pela credencial.

Nas skills existentes: o `sniper` deixou de falar só de Lovable na regra 7 — "guardar
não é publicar" passou a listar o botão de cada plataforma, e ganhou o inverso, que é
o que está no ar sair do ar sozinho quando vive só na camada de escrita de um
contentor. Ganhou ainda a entrega de SQL em três partes, os estados "faltam os dados"
e "falta medir o que se perdeu", e duas regras novas: não trocar um automatismo por
atenção humana, e desligar uma integração no receptor em vez de assumir que parou.

O `recon` ganhou três eixos de configuração, o `triage` passou a contar o texto que o
próprio sistema mostra como documentação desalinhada, o `doctrine` ganhou o registo do
que já se tentou e a produção rejeitou, e o `chatbot:engine` a distinção entre calar
por handoff e calar por horário.

---

## 2026-08-06 — catálogo público

Licença de uso escrita: **usar sim, redistribuir não**. Instalar, usar em trabalho
pago e adaptar a cópia própria é livre; republicar, partilhar versões alteradas ou
vender não é.

O README passou a ser a montra em vez de documentação interna, e as notas de
manutenção mudaram-se para o [MANUTENCAO.md](MANUTENCAO.md).

O plugin `protocolo-sniper` **foi removido** do catálogo. Existia só para redirecionar
quem o tinha instalado, e como ainda ninguém da equipa tinha chegado a usá-lo, o
catálogo estreia limpo com três plugins.

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
