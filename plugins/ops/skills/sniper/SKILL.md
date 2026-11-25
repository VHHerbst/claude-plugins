---
name: sniper
description: Modo de trabalho para alterações em sistemas que já estão em produção com utilizadores reais. Usa quando o pedido envolver alterar código, RPCs, migrações SQL, fluxos ou ecrãs de um projeto em uso (bigone-ops-hub, klc-bigone, nexxorhub, cr-clinic, febracised, galp-galen…), ou quando alguém disser "protocolo sniper", "modo sniper", "sem erros" ou "isto está em produção".
---

# Protocolo Sniper

Trabalhamos em sistemas que a equipa está a usar **neste momento**. Um erro publicado
não é um bug — é uma venda atrasada, uma reunião perdida, um cliente à espera.
Não temos o luxo de tentar duas vezes.

O protocolo tem um **núcleo** que vale sempre e **camadas** que entram conforme o que
a mudança toca. Pedir camadas a mais custa tanto como pedir a menos: um protocolo que
manda recitar regras que não se aplicam ensina a saltar linhas — e depois saltam-se
também as que importam.

## Este ficheiro não repete o projeto

Quando o repositório tem regras próprias — `CLAUDE.md`, `AGENTS.md`, uma skill do
projeto, um `verificar.sh` — **elas ganham**: são mais concretas e foram pagas com
incidentes daquele sistema. Aqui fica o que vale em **todos** os projetos. Não copies
para aqui o que já está escrito lá, e nunca apliques daqui um comando que o projeto
desmente.

---

## Porta de entrada: o que é que esta mudança toca?

Escolhe o nível **antes** de começar e diz qual escolheste na entrega. As camadas são
cumulativas — o N2 leva também a do N1. Na dúvida entre dois níveis, é o de cima.

- **N0 — não muda comportamento em produção.** Docs, testes, estilos, copy, refactor
  sem efeito observável. → só o **núcleo**; entrega em duas linhas, sem checklist.
- **N1 — lê dados ou muda o que o utilizador vê.** Ecrãs, listagens, filtros,
  relatórios, exportações. → + **camada A**.
- **N2 — escreve.** `update`/`insert`/`delete`, RPCs, migrações, permissões, estado
  novo num fluxo. → + **camadas B, C e D**.
- **N3 — sai do código.** Infraestrutura, integrações, automatismos, webhooks,
  desligamentos. → + **camada E** e o anexo `plataformas.md`, na pasta desta skill.

---

# Núcleo — sempre

## 1. Ler antes de escrever, e a base viva manda

Lê o corpo atual da RPC, do componente ou da policy **antes** de a alterares. Nunca
reproduzas de memória.

Confirma qual é a versão **mais recente**: pode haver hardening posterior noutra
migração que ainda não viste. A última migração que menciona a função ganha — não a
primeira que encontraste.

E a linhagem de migrações é uma **hipótese** sobre o schema, não o schema. Antes de
escreveres SQL ou código que referencia uma coluna, função ou tabela, pergunta à base
a correr: uma query custa menos do que ler três migrações.

## 2. Commit cirúrgico

`git add` **apenas** dos ficheiros que tocaste. **Nunca `git add -A`.**

Costuma haver outra sessão de Claude Code a trabalhar em paralelo no mesmo working
tree. Um `add -A` leva o trabalho de outra pessoa à boleia e ninguém percebe até
rebentar.

## 3. O portão do projeto, verde

Corre o portão que **o projeto** define — não um comando que trouxeste de outro. No
`bigone-ops-hub` é `./scripts/verificar.sh`.

Se o projeto não tiver portão: typecheck, testes e build, na versão de Node do CI e
com `TZ=UTC` (sem isso, testes com datas passam na tua máquina e falham lá) — e
confirma a que `tsconfig` o typecheck aponta, porque num repositório com *projects* o
da raiz tem `"files": []` e sai verde sem compilar nada.

A regra por trás é maior do que qualquer comando: **um comando que passa sempre não é
uma verificação.** Antes de aceitar um "OK", pergunta o que teria de acontecer para
ele falhar.

## 4. Prova na ground truth, nunca num sinal intermédio

Um `200 OK` não é prova. `ok: true` não é prova. Testes a passar, `tsc` limpo e "está
configurado no painel" também não. **Arrancar não é funcionar** — um serviço responde
`200` sem uma única credencial; precisas de um caminho que **use** a credencial e
devolva resposta observável.

**Prova** é: o registo apareceu na tabela, o card mudou de coluna no ecrã, o bundle
servido em produção contém o código novo.

E há quase sempre **mais do que uma ground truth**. Escreve os efeitos que a mudança
devia produzir — o que o utilizador vê, a linha na tabela, a entrada no log — e
verifica-os todos. O efeito visível é o que menos falha e o que mais engana: um bot
responde em quatro segundos com o passo seguinte a falhar em todas as execuções.

Quando a prova só se observa disparando algo para uma pessoa real, **não testes no
cliente**: procura o caminho que passa pelo mesmo código e pela mesma credencial sem
tocar em ninguém. Se não conseguires ver o resultado final, di-lo em vez de assumir.

## 5. Guardar não é publicar

Push, save e merge não ativam nada. Cada plataforma tem o seu passo de ativação:
descobre qual é o dela **antes** de dares por feito, e diz na entrega quem o carrega.
Os passos de cada uma estão em `plataformas.md`.

## 6. Não prometas o que não verificaste

Se ficou a meio, diz o que ficou e porquê. Se não conseguiste testar, diz que não
testaste.

Uma entrega honesta e incompleta custa uma hora. Uma entrega falsamente completa custa
um dia e a confiança da equipa.

---

# Camada A — Leitura e ecrãs (N1+)

**Ler tem falso-sucesso.** Uma tabela travada por RLS devolve **lista vazia**, não
erro: `error` vem a `NULL` e o ecrã fica em branco sem dizer porquê. Destructura
sempre o `error` — `const { data } = await supabase.rpc(...)` esconde RPCs partidas.
Quando o vazio for legítimo, diz isso em voz alta no código.

**Permissões e hierarquia não se resolvem no browser.** Derivar chefias ou papéis a
partir de uma tabela que o utilizador não pode ler produz um ecrã vazio sem uma única
mensagem. Resolve no servidor, com RPC `SECURITY DEFINER`.

**Conta quantas cópias existem da regra que vais corrigir.** Quando o defeito está numa
regra de negócio — formato de telefone, preço, duração, permissão — procura o padrão no
repositório inteiro. As Edge Functions não partilham imports com o frontend, por isso
guardam sempre a sua própria cópia: corriges o ecrã, e o envio do servidor continua
errado onde ninguém o vê falhar.

# Camada B — Escrita e permissões (N2+)

**Escrita bloqueada não dá erro — dá zero linhas.** Com RLS, um `update` ou `delete`
que não casa com nenhuma policy não falha: afeta zero linhas, o PostgREST devolve
`200`, o `error` vem `null`, e o código que só olha ao `error` anuncia sucesso sem ter
escrito nada.

É a falha mais cara que há, porque **o utilizador é treinado a desconfiar de si
próprio**: clica, lê "guardado com sucesso", vê o registo na mesma, e clica outra vez.
Um gestor de agência cancelou a mesma venda **três vezes** e o sistema concordou as três.

- **Transições de estado vão por RPC `SECURITY DEFINER`** que devolve `{ok, erro}`, e o
  frontend **valida o `ok`** — não o `error`. A recusa passa a ser uma frase que chega
  ao ecrã em vez de silêncio.
- Se um `update` direto for mesmo inevitável, encadeia `.select()` e confirma que
  voltaram linhas. `.single()` também serve: com zero linhas devolve erro.
- **A permissão que a UI mostra tem de existir na base.** Ao acrescentar um papel a um
  ecrã, procura a policy ou a guarda da RPC que o cobre. Se não existir, ele vê o botão
  e a ação não acontece — e ninguém repara enquanto ninguém com esse papel tentar.

# Camada C — Base de dados e migrações (N2+)

**As migrações não são corridas por ti.** Escreves o SQL **idempotente** e entregas;
quem tem acesso corre-o. Ficheiros empurrados para o git **não correm sozinhos**: se
ninguém correu o SQL à mão, a base não mudou. Migrações de **enum** ficam num ficheiro
isolado e correm **antes** das que as usam.

**SQL que mexe em dados já gravados entrega-se em três partes, por esta ordem:**

1. a query que **conta** quantas linhas apanha;
2. o `select` que mostra a coluna proposta ao lado da atual;
3. o `update` — **comentado**, para quem corre descomentar depois de conferir.

Num sistema em uso não há undo. Uma condição mal medida corrige o alvo e estraga o que
estava ao lado, e ninguém dá por isso até a pessoa errada se queixar.

**Ordem de rollout, decidida antes de entregar e escrita na entrega:**

- Estado ou campo novo que ficaria **invisível ou partido** se chegasse antes do ecrã →
  **frontend primeiro, migração depois**.
- Mudança sem risco de invisibilidade → **migração primeiro, frontend depois**.

# Camada D — Superfície nova (N2+)

Sempre que acrescentas um passo ou estado a um fluxo, verifica **na mesma entrega**:

- observações / notas
- histórico e auditoria
- labels e badges
- filtros e pesquisas
- permissões por papel
- documentação (`AGENTS.md`, `docs/features/`)
- **quem chama isto** — o ecrã que devia usar a coisa nova já a invoca?

Um estado novo que não aparece nos filtros é um estado que ninguém encontra. E uma
função entregue que nenhum ecrã chama não é meia funcionalidade: é zero, com o
agravante de constar como feita.

# Camada E — Fora do código (N3)

**Não troques um automatismo por atenção humana.** Se a mudança faz o sistema deixar de
responder porque "a equipa trata disso", tem de levar a rede junto: a pessoa tem N
minutos de prioridade e, se ninguém pegar, o automatismo entra. **Silêncio
incondicional à espera de que alguém esteja a olhar não se publica** — uma guarda
dessas durou um dia numa clínica: o cliente pediu preços a meio da tarde e ficou uma
hora sem resposta.

**Desligar também é uma entrega.** Parar de usar um fornecedor não o cala: enquanto a
conta e os fluxos existirem do outro lado, ele continua a disparar — e esse lado não é
teu. O desligamento que se aguenta é o **do receptor**: o teu webhook responde com uma
recusa nomeada, não escreve nada, leva a data no próprio ficheiro, e depois confirmas
na tabela que parou. "Já ninguém usa aquilo" não é desligar — uma integração dada como
substituída continuou semanas a injetar mensagens antigas em conversas de clientes.

O resto — o botão de cada plataforma, o que sobrevive a um redeploy, como escrever num
contentor sem destruir o que lá está — está em `plataformas.md`.

---

# A entrega

**N0 e N1 pequenos:** duas linhas. O que mudou, e o que falta para estar no ar.

**Bloco com vários pedintes:** organiza por pessoa (Diana / Nathalia / Wesley / Rita /
Hélder…), para cada um conseguir ler só a sua linha. Para cada pedido, o estado:

- **feito e publicado**
- **feito, falta publicar**
- **feito, falta correr a migração**
- **feito no código, falta corrigir os dados já gravados**
- **em falta** — e porquê

Um defeito que **escreveu dados errados** tem três partes: a causa, os dados torcidos e
o estrago já feito. Corrigir a causa fecha uma — dizer "corrigido" com as outras duas
por tratar é encerrar um incidente que continua a correr.

E acrescenta uma linha sempre que a mudança traga um comportamento que, visto de fora,
é indistinguível de uma avaria: **o que vai acontecer, que é de propósito, e como se
desfaz.** Uma guarda que cala o bot assim que um humano responde está a fazer o que
devia — para a equipa é "o bot morreu".

Sem jargão técnico. A pessoa quer saber se já pode usar.

---

## Antes de dizer "está feito"

Quatro perguntas, sempre:

1. Li o código atual antes de o mudar — e perguntei à base, em vez de deduzir do repositório?
2. O `git add` levou só os meus ficheiros?
3. O portão do projeto passou — e sei o que teria de acontecer para ele falhar?
4. Vi o resultado no sítio final, e disse o que falta: publicar, migração, dados por corrigir?

Mais uma por camada que tenhas aberto:

- **A** — alguma leitura ignora o `error`, ou devolve vazio sem dizer porquê?
- **B** — as escritas confirmam que escreveram (`ok` da RPC, linhas devolvidas), e todo o papel que vê o botão tem policy que o deixa agir?
- **C** — o `update` em dados gravados foi entregue comentado, depois da contagem?
- **D** — o estado novo aparece nos filtros, no histórico e na documentação?
- **E** — avisei do que vai parecer avaria e não é?

Se alguma resposta for "não", ainda não está feito.
