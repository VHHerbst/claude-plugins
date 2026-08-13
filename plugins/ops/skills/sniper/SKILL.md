---
name: sniper
description: Modo de trabalho obrigatório para alterações em sistemas que já estão em produção com utilizadores reais. Usa quando o pedido envolver alterar código, RPCs, migrações SQL, fluxos ou ecrãs de um projeto em uso (bigone-ops-hub, klc-bigone, nexxorhub, cr-clinic, febracised, galp-galen…), ou quando alguém disser "protocolo sniper", "modo sniper", "sem erros" ou "isto está em produção".
---

# Protocolo Sniper

Trabalhamos em sistemas que a equipa está a usar **neste momento**. Um erro publicado
não é um bug — é uma venda atrasada, uma reunião perdida, um cliente à espera.
Não temos o luxo de tentar duas vezes.

Aplica todas as regras abaixo, sem exceção.

---

## 1. Ler antes de escrever

Lê o corpo atual da RPC, do componente ou da policy **antes** de a alterares.
Nunca reproduzas de memória.

Confirma qual é a versão **mais recente** de uma função: pode haver hardening
posterior noutra migração que ainda não viste. A última migração que menciona a
função ganha — não a primeira que encontraste.

**A base viva manda sobre o repositório.** A linhagem de migrações é uma hipótese
sobre o schema, não o schema. Antes de escreveres SQL ou código que referencia uma
coluna, função ou tabela, pergunta à base a correr — uma query custa menos que ler
três migrações.

**E conta quantas cópias existem da regra que vais corrigir.** Quando o defeito está
numa regra de negócio — formato de telefone, preço, duração, permissão — procura o
padrão no repositório inteiro. As Edge Functions não partilham imports com o
frontend, por isso guardam sempre a sua própria cópia: corriges o ecrã, e o envio do
servidor continua errado onde ninguém o vê falhar.

## 2. Migrações não são corridas por ti

Escreves o SQL **idempotente** e entregas. Quem tem acesso corre-o no Supabase
SQL Editor.

- Migrações de **enum** ficam num ficheiro isolado e correm **antes** das que as usam.
- Ficheiros de migração empurrados para o git **não correm sozinhos**. A Lovable
  não os aplica. Se ninguém correu o SQL à mão, a base de dados não mudou.

**SQL que mexe em dados já gravados entrega-se em três partes, por esta ordem:**

1. a query que **conta** quantas linhas apanha;
2. o `select` que mostra a coluna proposta ao lado da atual;
3. o `update` — **comentado**, para quem corre descomentar depois de conferir.

Num sistema em uso não há undo. Uma condição mal medida corrige o alvo e estraga o
que estava ao lado, e ninguém dá por isso até a pessoa errada se queixar.

## 3. Commits cirúrgicos

`git add` **apenas** dos ficheiros que tocaste. **Nunca `git add -A`.**

Costuma haver outra sessão de Claude Code a trabalhar em paralelo no mesmo
working tree. Um `add -A` leva o trabalho de outra pessoa à boleia e ninguém
percebe até rebentar.

## 4. Trio verde antes de dar por feito

O CI corre em Node 20. Corre o mesmo localmente:

```bash
nvm use 20 && npx tsc --noEmit && TZ=UTC npx vitest run && npx vite build
```

O `TZ=UTC` dá paridade com o CI — sem ele, testes com datas passam na tua
máquina e falham lá.

## 5. Verificar na ground truth, nunca num sinal intermédio

Um `200 OK` não é prova. `ok: true` não é prova. Testes a passar não são prova.
`tsc` sem erros não é prova. **"Está configurado no painel" também não é prova** — há
plataformas onde o que defines no painel nunca chega ao processo.

**Arrancar não é funcionar.** Um serviço pode responder `200` sem uma única
credencial. Precisas de um caminho que **use** a credencial e devolva resposta
observável — senão estás a testar que o ficheiro existe.

**Prova** é: o registo apareceu na tabela, o card mudou de coluna no ecrã, o
bundle servido em produção contém o código novo. Vai ver no sítio final.

Uma mudança tem quase sempre **mais do que uma ground truth**. Escreve os efeitos que
devia produzir — a resposta que o utilizador vê, a linha na tabela, a entrada no log —
e verifica-os todos. O efeito visível é o que menos falha e o que mais engana: um bot
pode responder em quatro segundos com o passo seguinte a falhar em todas as execuções.

Quando a prova só se observa disparando algo para uma pessoa real, **não testes no
cliente**: procura o caminho que passa pelo mesmo código e pela mesma credencial sem
tocar em ninguém.

Se não conseguires ver o resultado final, di-lo em vez de assumir.

## 6. Ordem de rollout pensada

- Estado/campo novo que ficaria **invisível ou partido** se chegasse antes do
  ecrã → **frontend primeiro, migração depois**.
- Mudança sem risco de invisibilidade → **migração primeiro, frontend depois**.

Decide a ordem *antes* de entregar, e escreve-a na entrega.

## 7. Guardar não é publicar — sabe qual é o botão

Push, save e merge não ativam nada. Cada plataforma tem o seu passo de ativação:
descobre qual é o dela **antes** de dares por feito, e diz na entrega quem o carrega.

- **Lovable** — o **Publish**. Enquanto ninguém carregar, o que está no GitHub não
  existe para os utilizadores.
- **n8n** — **Publicar**. Guardar cria um rascunho e a versão antiga continua a
  atender. Confirma que a versão ativa é a nova.
- **Edge Functions self-hosted** — não há deploy automático nenhum. O ficheiro tem de
  ir parar ao contentor.
- **Migrações** — alguém corre o SQL à mão. Ver a regra 2.

E o contrário também é verdade: **o que está no ar pode sair do ar sem ninguém tocar
no código.** O que vive só na camada de escrita de um contentor — ficheiros copiados à
mão, credenciais escritas com `sed` — não é um deploy, é uma configuração à espera de
desaparecer: basta a infraestrutura recriar o serviço. Num painel gerido, **"Reiniciar"
é seguro, "Implantar" recria e apaga.**

E **nunca escrevas direto no destino.** Um `>` ou um `sed -i` sobre um ficheiro que
está bom destrói-o quando o passo anterior falha — basta um download falhado para a
mensagem de erro ficar por cima de um webhook em produção. Escreve num sítio
temporário e move só em caso de sucesso.

## 8. Fechar cada bloco com resumo por-pessoa

Quem pediu tem de conseguir ler só a sua linha. Organiza por pessoa
(Diana / Nathalia / Wesley / Rita / Hélder…), e para cada pedido diz o estado:

- **feito e publicado**
- **feito, falta publicar**
- **feito, falta correr a migração**
- **feito no código, falta corrigir os dados já gravados**
- **em falta** — e porquê

Um defeito que **escreveu dados errados** tem três partes: a causa, os dados torcidos
e o estrago já feito. Corrigir a causa fecha uma — dizer "corrigido" com as outras
duas por tratar é encerrar um incidente que continua a correr.

E acrescenta uma linha sempre que a mudança traga um comportamento que, visto de fora,
é indistinguível de uma avaria: **o que vai acontecer, que é de propósito, e como se
desfaz.** Uma guarda que cala o bot assim que um humano responde está a fazer o que
devia — para a equipa é "o bot morreu".

Sem jargão técnico. A pessoa quer saber se já pode usar.

## 9. Superfície nova = checklist transversal

Sempre que acrescentas um passo ou estado a um fluxo, verifica **na mesma
entrega**:

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

## 10. Não prometas o que não verificaste

Se ficou a meio, diz o que ficou e porquê. Se não conseguiste testar, diz que
não testaste.

Uma entrega honesta e incompleta custa uma hora. Uma entrega falsamente completa
custa um dia e a confiança da equipa.

## 11. Não troques um automatismo por atenção humana

Se a mudança faz o sistema deixar de responder porque "a equipa trata disso", tem de
levar a rede junto: a pessoa tem N minutos de prioridade e, se ninguém pegar, o
automatismo entra.

**Silêncio incondicional à espera de que alguém esteja a olhar não se publica.** Uma
guarda dessas durou um dia numa clínica: o cliente pediu preços a meio da tarde e
ficou uma hora sem resposta.

## 12. Desligar também é uma entrega

Parar de usar um fornecedor não o cala. Enquanto a conta e os fluxos existirem do
outro lado, ele continua a disparar — e esse lado não é teu.

**O desligamento que se aguenta é o do receptor:** o teu webhook responde com uma
recusa nomeada, não escreve nada, e leva a data no próprio ficheiro. Depois confirmas
na tabela que parou. "Já ninguém usa aquilo" não é desligar — uma integração dada como
substituída continuou semanas a injetar mensagens antigas em conversas de clientes.

## 13. Escrita bloqueada não dá erro — dá zero linhas

Com RLS, um `update` ou `delete` que **não casa com nenhuma policy** não falha: afeta
zero linhas. O PostgREST devolve `200`, o `error` vem `null`, e o código que só olha ao
`error` anuncia sucesso sem ter escrito nada.

É a falha mais cara que há, porque **o utilizador é treinado a desconfiar de si próprio**:
clica, lê "guardado com sucesso", vê o registo na mesma, e clica outra vez. Um gestor de
agência cancelou a mesma venda **três vezes** e o sistema concordou as três — o papel dele
tinha sido acrescentado ao ecrã anos depois da policy ter sido escrita.

Portanto:

- **Transições de estado vão por RPC `SECURITY DEFINER`** que devolve `{ok, erro}`, e o
  frontend **valida o `ok`** — não o `error`. A recusa passa a ser uma frase que chega ao
  ecrã em vez de silêncio.
- Se um `update` direto for mesmo inevitável, encadeia `.select()` e confirma que voltaram
  linhas. `.single()` também serve: com zero linhas devolve erro.
- **A permissão que a UI mostra tem de existir na base.** Ao acrescentar um papel a um
  ecrã, procura a policy ou a guarda da RPC que o cobre. Se não existir, ele vê o botão e
  a ação não acontece — e ninguém repara enquanto ninguém com esse papel tentar.

O mesmo raciocínio vale para leitura: uma tabela protegida por RLS devolve **lista vazia**,
não erro. Derivar hierarquia ou permissões no browser a partir de uma tabela que o
utilizador não pode ler produz um ecrã vazio sem uma única mensagem — resolve no servidor,
com RPC.

---

## Antes de dizer "está feito", responde a isto

1. Li o código atual antes de o mudar?
2. O `git add` levou só os meus ficheiros?
3. O trio verde passou em Node 20?
4. Vi o resultado no sítio final, ou só num `200 OK`?
5. Disse claramente o que falta — publicar, migração, dados por corrigir?
6. O resumo está por pessoa, em linguagem que ela entende?
7. Se o defeito escreveu dados errados, disse quantos e o que se perdeu?
8. Avisei do que vai parecer avaria e não é?
9. As escritas confirmam que escreveram — `ok` da RPC ou linhas devolvidas — em vez de confiarem na ausência de erro?
10. Todo o papel que vê o botão tem policy ou guarda que o deixa agir?

Se alguma resposta for "não", ainda não está feito.
