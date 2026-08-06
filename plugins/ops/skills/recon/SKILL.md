---
name: recon
description: Reconhecimento de terreno antes de avançar — revisão de código multi-agente com filtro de confiança, para pull requests do GitHub ou para o diff local. Usa quando alguém pedir "revê este PR", "revisão de código", "code review", "faz recon", "vê se isto tem bugs antes de publicar", ou passar um número/URL de pull request. Cobre também os eixos próprios da V2H — RLS e migrações Supabase, env vars obrigatórias, dados fictícios em produção e documentação por atualizar.
---

# Recon

Reconhecimento é ir ver o terreno **antes** de avançar. Não se dispara nada aqui: o
resultado é um relatório de quem observou, para quem decide.

Uma revisão só vale se **o que reportas for verdade**. Vinte observações plausíveis
valem menos que três confirmadas: quem lê deixa de confiar e passa a ignorar tudo —
e a partir daí o recon deixou de servir para o que existe.

Por isso esta revisão tem duas metades — **encontrar** e **duvidar**. A segunda é a
que interessa.

---

## 0. Determinar o alvo

Por esta ordem:

1. Se veio um número ou URL de PR no pedido → é esse.
2. Se a branch atual tem PR aberto (`gh pr view`) → é esse.
3. Caso contrário → **diff local** contra a branch base (`git diff main...HEAD`,
   mais `git diff` e `git diff --staged` se houver trabalho por commitar).

Diz qual dos três estás a rever antes de começar. Faz uma todo list.

Usa sempre `gh` para falar com o GitHub — nunca web fetch.

## 1. Elegibilidade

Um agente Haiku verifica se o PR (a) está fechado, (b) é draft, (c) não precisa de
revisão — automático, ou trivial e obviamente correto — ou (d) já tem uma revisão
tua. Se sim, **para aqui** e diz porquê.

Para diff local, salta este passo.

## 2. Recolher as regras do projeto

Um agente Haiku devolve **caminhos** (não conteúdos) de:

- `CLAUDE.md` e `AGENTS.md` na raiz e nas pastas tocadas pela mudança
- `docs/features/` e `docs/plans/` relacionados com o que mudou

Os `docs/features/` interessam por uma razão específica: **isto já pode ter sido
resolvido antes**. Uma correção que ignora a solução documentada é uma regressão,
não uma correção.

## 3. Resumo da mudança

Um agente Haiku lê o PR/diff e devolve um resumo do que a mudança faz. Todos os
agentes seguintes recebem este resumo.

## 4. Encontrar — 8 agentes Sonnet em paralelo

Cada um devolve uma lista de problemas e, para cada um, **o motivo pelo qual foi
levantado** (adesão ao AGENTS.md, bug, contexto histórico, policy…).

- **#1 — Regras do projeto.** Conformidade com `CLAUDE.md` / `AGENTS.md`. Lembra-te
  que estes ficheiros são guias de escrita: nem tudo se aplica em revisão.
- **#2 — Bugs óbvios.** Lê **só** o diff, sem ir buscar contexto extra. Bugs
  grandes. Ignora nitpicks.
- **#3 — Histórico.** `git blame` e histórico das linhas mexidas. Este código já foi
  assim antes e foi mudado por alguma razão?
- **#4 — PRs anteriores.** PRs que tocaram nestes ficheiros e os comentários que lá
  ficaram — a mesma observação costuma aplicar-se outra vez.
- **#5 — Comentários no código.** Os comentários existentes avisavam de algo que
  esta mudança quebra?
- **#6 — Falhas silenciosas.** `catch` vazio, erro engolido, `.single()` sem tratar
  o vazio, promessa sem `await`, valor por omissão que mascara falha, `ok: true`
  devolvido sem se ter confirmado nada. **Uma falha que ninguém vê é pior que um
  crash.**
- **#7 — Supabase e base de dados.** Só se a mudança tocar SQL, RPCs, policies ou
  queries:
  - migração **idempotente**? enum em ficheiro isolado e a correr **antes** de quem
    o usa?
  - RLS: policy nova deixa passar o que não devia? `DELETE` sem policy? função de
    autorização no schema certo (na BD viva pode estar em `private`, não em
    `public`)?
  - isolamento por schema respeitado, e views/RPCs em `public` com o prefixo do
    projeto?
  - `user_id` usado onde o correto é cruzar por email (pode estar stale)?
  - a migração está no git mas **ninguém a correu** — o Lovable não aplica.
- **#8 — Produção e configuração.**
  - `throw` em env var ausente que ainda não existe em todos os ambientes de deploy
  - dados fictícios/mock a entrar no bundle, mesmo atrás de flag
  - segredos, chaves ou tokens em código
  - Edge Function alterada que precisa de **deploy explícito** — guardar não é
    deployar
  - `docs/features/` / `AGENTS.md` por atualizar no mesmo commit

## 5. Duvidar — um agente Haiku por problema

Cada agente recebe o PR, a descrição do problema e a lista de ficheiros do passo 2,
e devolve um **score de 0 a 100** de confiança em que o problema é real. Quando o
problema foi levantado por causa de um `CLAUDE.md`/`AGENTS.md`, o agente tem de
confirmar que o ficheiro diz **mesmo** aquilo.

Dá esta rubrica ao agente **literalmente**:

- **0** — Nada confiante. É falso positivo que não sobrevive a um olhar atento, ou é
  um problema pré-existente.
- **25** — Pouco confiante. Pode ser real, pode ser falso positivo; o agente não
  conseguiu verificar. Se for estilístico, não está explicitamente escrito no
  `CLAUDE.md`/`AGENTS.md`.
- **50** — Moderadamente confiante. Verificou-se que é real, mas pode ser nitpick ou
  raro na prática. Face ao resto do PR, não é importante.
- **75** — Muito confiante. O agente confirmou, e é muito provável que aconteça na
  prática. A abordagem atual do PR é insuficiente. É importante e afeta
  diretamente o funcionamento, ou está explicitamente escrito no
  `CLAUDE.md`/`AGENTS.md`.
- **100** — Certeza absoluta. O agente confirmou e as provas são diretas: acontece,
  e com frequência.

## 6. Filtrar

**Fora tudo abaixo de 80.** Se não sobrar nada, diz que está limpo e para.

Não compenses um PR limpo a inventar observações. "Não encontrei nada acima de 80"
é um resultado legítimo e útil.

## 7. Reverificar elegibilidade

Só para PR: repete o passo 1 — entretanto pode ter sido fechado ou já revisto.

## 8. Entregar

**Por omissão, o resultado vai para o chat.** Comentar num PR é publicar em nome do
utilizador: só o fazes se ele **pedir explicitamente** nesta conversa. Se achares
que vale a pena comentar, pergunta primeiro.

Formato, com exatamente estas regras:

- breve
- sem emojis
- **cada problema com link e citação** — ficheiro e linhas, com SHA completo
  (`https://github.com/<org>/<repo>/blob/<sha40>/caminho#L13-L17`). Nada de `HEAD`,
  nada de construir o SHA com bash.
- se citas o `AGENTS.md`, **linka o `AGENTS.md`**

```
### Revisão

3 problemas encontrados:

1. <descrição breve> (AGENTS.md diz "<...>")

<link com sha completo e intervalo de linhas>
```

E fecha com a linha que interessa a quem vai publicar:

> **Bloqueia publicação:** sim / não — e porquê.

---

## Falsos positivos — não reportes isto

- problemas **pré-existentes**, em linhas que o autor não mexeu
- o que parece bug mas não é
- nitpicks que um sénior não levantaria
- o que o linter, o typechecker ou o compilador apanham — imports errados, erros de
  tipo, formatação, newlines. **Não corras o build nem o typecheck**: isso corre à
  parte no CI, e no fluxo de entrega é o trio verde do Protocolo Sniper.
- qualidade genérica — falta de testes, documentação pobre, "segurança" em abstrato
  — a não ser que esteja escrito no `AGENTS.md`
- regras do `AGENTS.md` explicitamente silenciadas no código (ex.: comentário de
  lint ignore)
- mudanças de comportamento que são claramente intencionais e fazem parte do
  objetivo do PR

---

## Antes de entregares a revisão

1. Disse qual foi o alvo — PR ou diff local?
2. Cada problema passou pelo agente de dúvida e ficou acima de 80?
3. Cada problema tem link com SHA completo e citação?
4. Verifiquei se `docs/features/` já resolvia isto antes?
5. Disse se bloqueia publicação?
6. Não comentei no GitHub sem o utilizador pedir?

Se alguma resposta for "não", ainda não está pronta.

Quando o recon apanhar algo numa mudança que vai para um sistema em uso, o passo
seguinte é o `/ops:sniper` — o recon diz o que está mal, o sniper diz como se corrige
sem partir nada. Se o que apanhaste for antigo e não for desta mudança, não o
reportes aqui: vai para o `/ops:triage`.
