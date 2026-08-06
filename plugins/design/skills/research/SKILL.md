---
name: research
description: Síntese de pesquisa com utilizadores — transforma entrevistas, testes de usabilidade, gravações, tickets de suporte ou respostas de inquérito em achados ordenados por frequência e impacto, separando o que foi dito do que foi observado do que é conclusão tua. Usa quando alguém pedir "sintetiza estas entrevistas", "o que aprendemos com os testes", "análise das respostas", "síntese de pesquisa", ou entregar transcrições e notas de sessões com utilizadores.
---

# Research

Síntese não é resumo. Um resumo encolhe o que foi dito; uma síntese diz **o que é
verdade em várias sessões ao mesmo tempo** — e distingue isso do que aconteceu numa
só.

O erro que estraga quase todas as sínteses é misturar três coisas de peso muito
diferente:

1. **O que a pessoa disse.** Opinião. Ela pode estar enganada sobre si própria.
2. **O que a pessoa fez.** Observação. Vale muito mais.
3. **O que tu concluíste.** Interpretação. Vale o que a evidência a sustentar.

Quando os três aparecem no mesmo parágrafo, a interpretação ganha o peso de facto — e
alguém vai construir uma funcionalidade em cima disso.

**Mantém-nos separados do princípio ao fim.**

---

## 0. Saber o que tens nas mãos

Antes de sintetizar, escreve:

- quantas sessões, de que tipo (entrevista, teste, ticket, inquérito)
- **quem** eram — papel, experiência com o produto
- o que foi perguntado, e se foi perguntado da mesma forma a todos
- quem **não** está representado

Esse último ponto define o que a síntese pode e não pode afirmar. Cinco sessões com
utilizadores avançados não dizem nada sobre quem entra pela primeira vez, e a síntese
tem de o dizer em vez de deixar o leitor assumir.

## 1. Extrair, sem interpretar ainda

Percorre cada sessão e tira, com identificação (`S3`, `S7`) e citação literal quando
for fala:

- **momentos de fricção** — hesitou, voltou atrás, pediu ajuda, desistiu
- **modelos mentais** — as palavras que a pessoa usa para descrever a coisa; se
  chama outra coisa ao que o produto chama, isso é um achado
- **soluções improvisadas** — o Excel paralelo, o grupo de WhatsApp, o papel na
  secretária. **A gambiarra é o pedido de funcionalidade mais fiável que existe**,
  porque custou trabalho a alguém.
- **contradições** — disse que nunca usava e usou; disse que era fácil e demorou
  quatro minutos

Não agrupes nesta fase. Agrupar cedo faz-te ver o padrão que já esperavas.

## 2. Agrupar por problema, não por funcionalidade

Junta por **o que a pessoa estava a tentar fazer** e onde emperrou — não por ecrã
nem por sugestão dada.

Se agrupas por sugestão, o resultado é uma lista de pedidos. Se agrupas por
problema, vês que quatro pedidos diferentes são o mesmo problema — e uma solução
resolve os quatro.

## 3. O teste da evidência

Para cada padrão, antes de o chamares padrão:

> Em quantas sessões **independentes** apareceu? Aponta quais.

- **1 sessão** — é um sinal. Escreve como sinal, com o número da sessão. Nunca "os
  utilizadores acham".
- **2 sessões** — pode ser padrão. Diz que é provisório.
- **3 ou mais** — padrão.

E separa sempre **frequência** de **gravidade**. Uma coisa que aconteceu uma vez e
fez a pessoa perder o trabalho todo é mais importante que uma irritação que aconteceu
cinco vezes. Se juntares as duas num "score", perdes precisamente a informação que
interessa.

**Nunca uses percentagens com menos de 20 sessões.** "60% dos utilizadores" com
cinco pessoas é três pessoas — e escrever assim faz três pessoas parecerem um
mercado.

## 4. Entregar

```
### Síntese — <estudo> — <data>

**Base:** <n> sessões, <perfis>. **Não representado:** <quem falta>.

#### Achados

**1. <O problema, numa frase>**
- **Observado:** o que aconteceu de facto — S2, S5, S7
- **Dito:** "<citação literal>" — S5
- **Interpretação:** <a tua leitura, marcada como tua>
- **Gravidade:** impede / atrasa / irrita
- **O que muda no produto:** <hipótese, uma>

#### Sinais isolados (1 sessão — não são padrão)

#### Contradições por resolver

#### O que esta pesquisa não pode responder
```

As duas últimas secções são as que dão credibilidade ao resto. Uma síntese sem
contradições e sem limites ou teve pouca pesquisa, ou teve pouca honestidade.

Fecha com **as duas coisas a mudar primeiro**, e a razão de serem essas.

---

## O que não entra numa síntese

- pedidos de funcionalidade repetidos como conclusão — o pedido é o dado, não o
  achado
- "os utilizadores querem X" quando o que houve foi uma pessoa a sugerir X
- citações escolhidas para confirmar o que já se pensava; se há citação contra, entra
- números decorativos com amostra pequena
- juntar o que se disse ao telefone com o que se observou em teste, como se fosse a
  mesma coisa

---

## Antes de entregares a síntese

1. Está escrito quantas sessões, com quem, e quem falta?
2. Observado, dito e interpretado estão visualmente separados em cada achado?
3. Cada padrão aponta as sessões concretas onde apareceu?
4. O que apareceu uma vez está marcado como sinal isolado?
5. As contradições estão escritas, em vez de arrumadas?
6. Disse o que esta pesquisa **não** consegue responder?

Se alguma resposta for "não", ainda é um resumo.

O que sair daqui vira desenho, e o desenho passa pelo `/design:critique` antes de ir
para `/design:handoff`.
