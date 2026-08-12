---
name: doctrine
description: Doutrina — escreve e mantém as decisões de arquitetura do projeto (ADRs) em docs/adr/, incluindo as alternativas rejeitadas e o gatilho que reabre a discussão. Usa quando alguém pedir "documenta esta decisão", "porque é que fizemos assim", "ADR", "decisão de arquitetura", "escreve a doutrina", quando for preciso explicar uma escolha técnica a um cliente ou a outro dev, ou quando uma decisão antiga estiver a ser substituída.
---

# Doctrine

Doutrina militar não é o registo do que aconteceu — isso é o relatório. Doutrina é a
decisão escrita **para quem chegou depois**, para que não se volte a discutir o que
já foi decidido, e para se saber quando é que a decisão deixou de valer.

Um ADR serve exatamente para isso. E quase todos falham no mesmo ponto: registam a
escolha e esquecem-se de escrever **o que foi rejeitado e porquê**. Meses depois
alguém propõe a alternativa rejeitada, ninguém se lembra da razão, e discute-se tudo
outra vez do zero.

Duas secções fazem a diferença entre um ADR útil e um ADR decorativo:
**alternativas rejeitadas** e **gatilho de revisão**.

---

## 0. Isto é mesmo uma decisão de arquitetura?

Poluir o `docs/adr/` é pior que não o ter: quando lá está tudo, ninguém lê nada.

Escreve o ADR só se as **três** forem verdade:

1. **É caro de reverter.** Mudar de ideias daqui a seis meses custa dias, não uma
   hora.
2. **Atravessa mais que um módulo.** Afeta como outras partes do sistema são
   escritas.
3. **Houve alternativa real.** Alguém podia legitimamente ter escolhido outra coisa.

Se falha alguma, não é doutrina. É uma nota de implementação — o sítio é o
`docs/features/` ou um comentário no código. **Diz isso e não escrevas o ADR.**

### Exceção: o que já se tentou e correu mal

Se o que reprovou o teste foi **uma coisa que se tentou e a produção rejeitou**, a
nota não é "não resultou". Leva o que um ADR leva — a data, o dano concreto, e a
condição em que valeria a pena tentar outra vez. Sem isso, alguém volta a propor a
mesma ideia daqui a três meses e ninguém se lembra porque é que saiu.

## 1. Encontrar onde vive a doutrina

Procura, por esta ordem: `docs/adr/`, `docs/decisions/`, `docs/plans/`, ou o que o
`AGENTS.md` mandar. **Segue a convenção que já lá está** — numeração, formato de
nome, idioma. Não impunhas um formato novo a um projeto que já tem um.

Se não existir nada, cria `docs/adr/` e começa em `0001`.

## 2. Ler o que já foi decidido

Lê os ADRs existentes **antes** de escrever. Duas coisas podem acontecer:

- **Esta decisão substitui uma anterior.** Marca a antiga como
  `Substituída por 00XX` e liga as duas. **Nunca apagues nem reescrevas um ADR
  antigo** — a decisão errada de ontem é o contexto que explica a de hoje.
- **Esta decisão contradiz uma anterior sem dar por isso.** Para. Isto é o achado
  mais valioso que esta skill produz. Levanta a contradição antes de escrever seja
  o que for.

## 3. Escrever

Título é a **decisão**, não o tema. `0007 — Um schema Supabase por projeto`, e não
`0007 — Organização da base de dados`. Quem lê o índice tem de perceber o que foi
decidido sem abrir o ficheiro.

```markdown
# 0007 — Um schema Supabase por projeto

- **Estado:** aceite
- **Data:** 2026-08-06
- **Decidiram:** Vitor, <quem mais>

## Contexto

O que era verdade quando decidimos — restrições reais, não teoria. O que estava a
doer, o que estava a bloquear, o que já se tinha tentado.

## Decisão

No imperativo, uma frase se possível. "Cada projeto vive no seu próprio schema, com
views em `public` prefixadas pelo nome do projeto."

## Alternativas rejeitadas

**Tudo em `public` com prefixo nas tabelas** — descartado porque <razão concreta>.

**Uma instância Supabase por projeto** — descartado porque <razão concreta>.

## Consequências

O que passa a ser mais fácil, e — obrigatoriamente — **o que passa a custar mais**.
Um ADR sem custos escritos não foi pensado até ao fim.

## Gatilho de revisão

O que teria de mudar para reabrirmos isto. "Se o PostgREST self-hosted passar a
expor schemas não-`public` sem workaround, esta decisão deixa de ser necessária."
```

**Contexto no passado, decisão no presente, consequências no futuro.** Se te
apanhares a escrever "vamos avaliar" ou "poderá ser interessante", ainda não há
decisão — o estado é `proposta`, e diz isso a quem pediu.

## 4. ADR retroativo

Escrever a doutrina de uma decisão que já foi tomada há meses é legítimo e muitas
vezes é o mais valioso — é o que permite explicar a um cliente ou a um dev novo
porque é que o sistema é como é.

Duas regras nesse caso:

- **A data é a da decisão original**, não a de hoje. Encontra-a no git.
- **Não inventes as alternativas.** Se não descobriste o que foi ponderado na
  altura, escreve `Não registado` em vez de reconstruir uma discussão que talvez
  nunca tenha acontecido. Doutrina inventada é pior que doutrina em falta.

## 5. Ligar

Um ADR que ninguém encontra não existe. Na mesma entrega:

- entrada no índice (`docs/adr/README.md`), com título e estado
- link a partir do `AGENTS.md` quando a decisão afeta como se escreve código
- link a partir do `docs/features/` relevante

## 6. Entregar

Mostra o ADR escrito e diz explicitamente:

- que ficheiros criaste ou alteraste
- se algum ADR anterior ficou marcado como substituído
- se encontraste alguma contradição com doutrina existente

Como qualquer alteração ao repositório: **pergunta antes de escrever ficheiros** se
o pedido não foi claramente para os criar.

---

## Antes de entregares a doutrina

1. Passou nos três testes do passo 0 — caro de reverter, atravessa módulos, havia
   alternativa?
2. As alternativas rejeitadas estão escritas **com a razão**?
3. As consequências incluem o que passa a custar mais?
4. Há gatilho de revisão?
5. Segui a numeração e o formato que o projeto já usava?
6. Liguei a partir do índice e do `AGENTS.md`?

Se alguma resposta for "não", ainda é uma nota, não é doutrina.
