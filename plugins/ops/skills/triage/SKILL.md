---
name: triage
description: Triagem de dívida técnica — audita uma base de código e devolve os problemas ordenados por quanto custam de facto, não por quão feios são. Usa quando alguém pedir "auditoria da base de código", "dívida técnica", "o que é que devíamos refatorar", "faz triage", "por onde começamos a arrumar isto", ou quando um projeto está lento de mexer e ninguém sabe explicar porquê.
---

# Triage

Triagem no campo de batalha não é tratar quem está pior. É separar quem morre se
não for já, de quem aguenta, de quem não se salva — e gastar as mãos que temos onde
mudam o resultado.

Auditoria de dívida técnica é a mesma coisa. Uma lista de sessenta coisas feias não
é triagem: é rendição com formatação bonita. Ninguém vai fazer sessenta coisas.

**A regra que separa isto de uma lista de queixas:** código feio que funciona, que
está estável e que não bloqueia nada não é dívida — é código feio. Dívida é o que
**já te cobrou juros**: tempo perdido, bug repetido, entrega adiada.

---

## 0. Definir o teatro de operações

Nunca corras isto contra um repositório inteiro sem foco — sai uma lista que
ninguém lê.

Pergunta, ou infere do pedido, **um** destes âmbitos:

- um módulo ou pasta (`src/modules/comercial`)
- um fluxo de negócio (o funil, o agendamento, a faturação)
- os ficheiros que a equipa mais mexeu nos últimos 90 dias

Diz qual escolheste antes de começar. Faz uma todo list.

## 1. Recolher sinais objetivos, não opiniões

Antes de qualquer agente julgar seja o que for, junta factos. Isto é o que separa
uma triagem de um desabafo:

```bash
# churn: onde é que a equipa gasta tempo de facto
git log --since="6 months ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -30

# ficheiros grandes de mais para o que fazem
git ls-files | xargs wc -l 2>/dev/null | sort -rn | head -30

# correções repetidas no mesmo sítio: sintoma clássico de dívida real
git log --since="6 months ago" --oneline --grep="fix\|corrige\|hotfix" -i | head -40
```

**Um ficheiro com muito churn e muitos "fix" é o alvo número um.** É ali que a
equipa está a sangrar tempo, mesmo que o código pareça aceitável.

## 2. Auditar — agentes em paralelo, um por eixo

Cada agente recebe o âmbito, os sinais do passo 1, e o `AGENTS.md` / `CLAUDE.md`.
Devolve achados com **ficheiro, linha e evidência**.

- **#1 — Duplicação com divergência.** Não é a duplicação em si: é a cópia que já
  se afastou do original. Duas versões da mesma regra de negócio a dar respostas
  diferentes é um bug à espera de data.
- **#2 — Acoplamento que trava a próxima feature.** O que é que não se consegue
  mudar sem tocar em cinco sítios? Prova com um exemplo concreto do backlog.
- **#3 — Falhas silenciosas acumuladas.** `catch` vazio, erro engolido, `.single()`
  sem tratar vazio, valor por omissão que mascara falha.
- **#4 — Base de dados.** Migrações no git que ninguém correu, policies RLS
  esquecidas ou permissivas de mais, índices em falta em queries quentes, funções
  duplicadas com hardening só numa delas, views sem o prefixo do projeto.
- **#5 — Configuração e produção.** Env vars obrigatórias que não existem em todos
  os ambientes, segredos em código, dados fictícios no bundle, feature flags mortas
  há meses, Edge Functions no repo que nunca foram deployadas.
- **#6 — Documentação desalinhada.** `docs/features/` e `AGENTS.md` que descrevem
  um comportamento que o código já não tem. Documentação errada é pior que
  documentação nenhuma: manda a próxima pessoa na direção errada com confiança.

## 3. O teste dos juros

Para **cada** achado, responde a isto antes de o classificares:

> Quando é que isto custou tempo a alguém, ou partiu alguma coisa, nos últimos seis
> meses? Aponta o commit, o incidente ou a entrega atrasada.

Se não consegues apontar nada, e também não consegues mostrar que bloqueia algo que
está no plano, **o achado é T3**. Sem discussão e sem pena.

## 4. Classificar

- **T1 — sangra agora.** Está a causar dano neste momento, mesmo que ninguém tenha
  reparado: perda silenciosa de dados, RLS que expõe dados de outro cliente,
  segredo exposto, bug latente num fluxo em uso.
- **T2 — dói e piora.** Já cobrou juros e vai cobrar outra vez. Entra na próxima
  janela de trabalho, com data.
- **T3 — fica.** Feio, estável, não bloqueia. **Não tocar.** Existe na lista só
  para a equipa parar de o discutir em cada sprint.

Se tudo te parecer T1, a triagem falhou — volta ao passo 3.

## 5. Cada item tem de caber num PR

"Refatorar o módulo comercial" não é um item de triagem, é um desejo. Parte até cada
linha ser algo que uma pessoa faz e entrega sem bloquear mais ninguém.

Se não cabe num PR, ou está mal partido, ou é uma decisão de arquitetura — e nesse
caso o sítio é o `/ops:doctrine`, não aqui.

## 6. Entregar

Uma tabela por prioridade. Sem prosa à volta.

```
### Triagem — <âmbito> — <data>

**T1 — sangra agora**

| O quê | Onde | Evidência | Custo |
|---|---|---|---|
| <uma linha> | ficheiro:linha | <commit / incidente> | <horas> |

**T2 — dói e piora** ...

**T3 — fica** ...
```

Fecha com **as três primeiras coisas a fazer, por ordem, e porquê é essa ordem**.
Se a equipa só ler uma linha, é esta.

Se o projeto seguir o nosso padrão de documentação, oferece-te para gravar o
relatório em `docs/plans/triagem-<âmbito>-<data>.md` — mas **pergunta antes de
escrever ficheiros no repositório**.

---

## O que não entra na triagem

- estilo, formatação, nomes de variáveis — isso é linter, não é dívida
- falta de testes em abstrato; só entra se houver um bug que testes teriam apanhado
- "isto devia usar a biblioteca X" sem um custo concreto do que está lá
- reescritas totais — nunca são um item de triagem
- problemas que a mudança em curso vai resolver na mesma

---

## Antes de entregares a triagem

1. Disse qual foi o âmbito?
2. Cada T1 e T2 tem evidência apontada — commit, incidente ou entrega atrasada?
3. Cada item cabe num PR?
4. A lista de T3 existe e está explicitamente marcada como "não tocar"?
5. Disse quais são as três primeiras, por ordem?

Se alguma resposta for "não", ainda é uma lista de queixas.

Quando um item T1 for para execução num sistema em uso, o modo de trabalho é o
`/ops:sniper`.
