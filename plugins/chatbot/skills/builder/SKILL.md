---
name: builder
description: O ecrã onde uma pessoa sem código desenha os fluxos de conversa, e a caixa de entrada para atendimento humano. Usa depois do /chatbot:engine, ou quando alguém pedir "o construtor de fluxos", "editor visual", "arrastar os blocos", "a minha cliente quer montar sozinha", "caixa de entrada das conversas".
---

# Builder

Aqui é onde a maior parte destes projetos morre — não por ser difícil, mas por ser
construído cedo de mais e grande de mais. Um editor de nós ligados por setas é
trabalho a sério, e não vale nada enquanto o motor não correr fluxos reais.

Se chegaste aqui com o `/chatbot:engine` a funcionar de verdade, a boa notícia é
esta: **o construtor não tem lógica nenhuma.** É um editor do `jsonb` que o motor já
sabe correr.

---

## 1. A versão que já serve

Antes de construíres uma tela com arrastar e largar, pergunta se isto não chega:

**Uma lista ordenada de passos.** Cada passo é um cartão — tipo de nó, conteúdo, e
para onde vai a seguir. Adicionar, apagar, reordenar.

Cobre a maior parte dos fluxos que as pessoas fazem de facto, constrói-se numa
fração do tempo, e funciona no telemóvel — coisa que um canvas de nós não faz.

Só vais para a tela livre quando alguém tiver mesmo um fluxo com ramificações a mais
para uma lista. E aí já sabes como são os fluxos reais, em vez de imaginares.

## 2. Se for mesmo a tela

- Usa uma biblioteca de fluxos já feita. Escrever arrastar-e-largar do zero é semanas
  que não estão no plano.
- Guarda a posição dos nós no `jsonb` do fluxo, **num sítio que o motor ignora**. A
  aparência não pode contaminar a execução.
- Auto-guardar rascunho. Publicar é um ato à parte, e cria versão nova.

## 3. As coisas que o construtor tem de impedir

Um construtor que deixa criar um fluxo inválido está a empurrar o erro para o
telemóvel de um cliente. Antes de deixar publicar:

- **nó sem saída** — a conversa fica pendurada e a pessoa nunca mais tem resposta
- **ciclo sem condição de saída** — mensagens em espiral até ao banimento
- **nó órfão** — ninguém lá chega; provavelmente foi engano
- **atributo usado antes de ser recolhido** — `{{nome}}` num texto antes da pergunta
  que guarda o nome sai literalmente assim para o cliente

Mostra o problema **no nó**, em linguagem de pessoa. `n7 sem seguinte` não é uma
mensagem de erro — "Este passo não leva a lado nenhum: a conversa fica sem resposta"
é.

## 4. Testar sem gastar um cliente

**Um botão de testar comigo.** Corre o fluxo contra o teu próprio contacto, no canal
real. É a funcionalidade que mais confiança dá a quem monta os fluxos, e a mais
esquecida.

Mostra também, ao lado, o que a pessoa vai ver — a pré-visualização da mensagem com
as variáveis substituídas.

## 5. A caixa de entrada

O construtor sem caixa de entrada é meia plataforma. É onde alguém vê as conversas a
acontecer e entra quando é preciso.

O mínimo: lista de conversas por atividade recente, a conversa aberta com o
histórico, escrever como humano, e **um botão bem visível de assumir a conversa** —
que cala a automação, como o motor já garante.

Dois detalhes que decidem se é usável: dizer **quem** está a atender (senão duas
pessoas respondem ao mesmo cliente) e mostrar **quanto falta da janela de 24h**, para
não se escrever uma resposta que vai ser recusada.

## 6. Provar

Pede a alguém que não construiu isto para montar um fluxo simples sem ajuda, e fica
calado a ver. Onde essa pessoa hesitar, é onde está o problema — não onde tu achas.

Se quiseres a crítica estruturada do ecrã antes de o dar por bom, é o
`/design:critique`. O texto dos botões e dos erros é o `/design:copy`.

Próximo comando: `/chatbot:dispatch`.

---

## Antes de dares o construtor por feito

1. Considerei a lista de passos antes de partir para a tela?
2. A posição visual dos nós é ignorada pelo motor?
3. Publicar cria versão nova, sem mexer na que está a correr?
4. As validações impedem nó sem saída, ciclo, órfão e variável por recolher?
5. Há testar comigo, no canal real?
6. A caixa de entrada mostra quem está a atender e a janela de 24h?
7. Vi uma pessoa não técnica montar um fluxo sem eu falar?

Se a 7 for "não", ainda não sabes se o construtor serve.
