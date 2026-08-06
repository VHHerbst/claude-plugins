---
name: start
description: Primeiro passo da construção de uma plataforma própria de automação de conversas (um ManyChat teu). Levanta o que já existe, decide o âmbito honesto da primeira versão, escolhe canal e stack, e escreve o plano com os passos. Usa quando alguém disser "quero construir o meu manychat", "criar uma plataforma de chatbot", "automação de WhatsApp própria", "começar o chatbot", ou pedir por onde começar num projeto destes.
---

# Start

Vais construir uma plataforma de automação de conversas — o que o ManyChat, o
Manychat-like ou o Chatfuel fazem, mas tua, com a tua base de dados e sem
mensalidade por contacto.

Este comando não escreve código nenhum. Faz a única coisa que decide se o projeto
chega ao fim: **cortar o âmbito antes de começar**.

Toda a gente que desiste a meio de um projeto destes desistiu pelo mesmo motivo —
tentou construir o construtor visual de fluxos na primeira semana.

---

## 1. Ver o que já existe

Antes de perguntar seja o que for, **lê o projeto**:

- há base de dados? Supabase, Postgres, outra coisa? Já tem tabelas de contactos?
- há frontend? Que stack — Vite+React, Next?
- há alguma integração de mensagens já feita, mesmo que meia?
- há `AGENTS.md` ou `docs/features/` com convenções a respeitar?

Se o repositório já tem metade disto, o plano parte daí. **Nunca proponhas começar
do zero num projeto que já anda.**

## 2. As quatro perguntas que definem tudo

Pergunta, e não avances sem resposta:

**1. Que canal, primeiro?** Um só.
- **WhatsApp não oficial** (Evolution API, Z-API): barato, rápido, e **o número pode
  ser banido**. Serve para começar e para volumes pequenos.
- **WhatsApp Cloud API** (Meta, oficial): não bane, mas exige verificação de negócio,
  templates aprovados e paga-se por conversa.
- **Instagram Direct** (Meta Graph): o identificador do contacto é o PSID, e só
  podes iniciar conversa dentro da janela de 24h.

**2. Quem usa a plataforma?** Só tu, a tua equipa, ou clientes teus com contas
separadas? Se for a terceira, é multi-tenant — e isso muda o modelo de dados todo,
desde a primeira tabela. **Decidir isto depois custa uma reescrita.**

**3. O que faz a versão que vai para o ar primeiro?** Uma frase. Por exemplo:
"responde automaticamente a quem escreve fora de horas e regista o contacto".

**4. Quem escreve os fluxos?** Tu, no código? Ou uma pessoa não técnica, num ecrã?
Se for a segunda, o construtor visual é obrigatório — mas continua a não ser o
primeiro passo.

## 3. O corte

Escreve o plano por fases, e sê duro na primeira:

**Fase 1 — recebe e responde.** Uma conversa entra, fica guardada, e uma resposta
automática simples sai. Sem construtor, sem condições, sem campanhas. **Isto tem de
estar no ar antes de qualquer outra coisa ser construída.**

**Fase 2 — fluxos a sério.** Motor com estado, condições, esperas, guardar respostas
no contacto.

**Fase 3 — construtor.** O ecrã onde uma pessoa desenha o fluxo sem código.

**Fase 4 — campanhas.** Envio para muitos, com opt-out e limites.

A ordem não é negociável, e a razão é simples: **a fase 1 é a única que prova que o
canal funciona de verdade**. Tudo o resto assenta nela. Construir o motor antes de
receber uma mensagem real é construir em cima de uma suposição.

## 4. Escrever o plano

Grava em `docs/plans/chatbot-plano.md` — **pergunta antes de criar ficheiros**:

```markdown
# Plataforma de conversas — plano

- **Canal:** <qual, e porquê esse>
- **Multi-tenant:** sim / não
- **Primeira versão faz:** <uma frase>
- **Fluxos escritos por:** <quem>

## Estado
- [ ] Fase 1 — recebe e responde   (`/chatbot:schema`, `/chatbot:channel`)
- [ ] Fase 2 — motor de fluxos     (`/chatbot:engine`)
- [ ] Fase 3 — construtor          (`/chatbot:builder`)
- [ ] Fase 4 — campanhas           (`/chatbot:dispatch`)
- [ ] No ar                        (`/chatbot:launch`)

## Decisões tomadas
<data — o quê — porquê>
```

**Este ficheiro é a memória do projeto.** Os comandos seguintes leem-no para saber
onde vais — mas nunca confiam nele sozinho: confirmam sempre no sistema real se a
tabela existe, se o webhook responde. Um `[x]` numa lista não é prova de nada.

## 5. Entregar

Diz o plano em voz de pessoa, e **avisa do que vai correr mal**:

- se escolheu WhatsApp não oficial, o número pode ser banido — não uses o número
  pessoal, e não faças envios em massa antes da fase 4
- se escolheu multi-tenant, o isolamento entre clientes tem de estar na primeira
  migração, não numa depois
- se escolheu Meta, a aprovação demora dias — começa o pedido **hoje**, em paralelo
  com a fase 1

Fecha com **o próximo comando a correr**: `/chatbot:schema`.

---

## Antes de dar o plano por feito

1. Li o que já existe no projeto, em vez de assumir folha em branco?
2. As quatro perguntas estão respondidas — canal, multi-tenant, primeira versão,
   quem escreve fluxos?
3. A fase 1 é mesmo pequena, ou disfarcei o construtor lá dentro?
4. Avisei do risco de banimento e do prazo de aprovação da Meta?
5. O plano está escrito num ficheiro, não só nesta conversa?

Se alguma resposta for "não", o projeto vai encalhar na semana três.
