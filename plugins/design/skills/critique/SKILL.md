---
name: critique
description: Crítica estruturada de um ecrã, fluxo ou interface, ordenada por quanto atrapalha a pessoa que o vai usar. Usa quando alguém pedir "o que achas deste ecrã", "critica este design", "dá feedback nisto", "isto está bom?", partilhar uma imagem ou link de Figma para avaliação, ou quando um design estiver pronto e faltar uma segunda opinião antes de ir para desenvolvimento.
---

# Critique

Crítica de design não é dizer o que mudarias. É dizer **o que impede a pessoa de
fazer aquilo que veio fazer** — e, só depois disso arrumado, falar de gosto.

A diferença é prática: "eu punha o botão maior" não dá para agir, porque não diz o
problema que resolve. "A ação principal fica abaixo da dobra no telemóvel e 60% dos
utilizadores entram por telemóvel" dá.

---

## 0. Sem contexto não há crítica

Antes de olhar para o ecrã, tens de saber três coisas. Se não vierem no pedido,
**pergunta** — e não continues sem elas:

1. **Quem é a pessoa e o que veio cá fazer?** Uma tarefa concreta, não "usar a app".
2. **Em que momento aparece este ecrã?** Primeira vez? Todos os dias? A meio de
   outra coisa? Com pressa?
3. **Onde é que isto é usado?** Telemóvel de rua com uma mão, ou ecrã grande sentado?

Crítica sem isto é decoração. É o que faz alguém redesenhar um ecrã que já estava
certo para o contexto dele.

Se te derem uma imagem, descreve primeiro o que estás a ver, para o autor poder
corrigir-te se leste mal.

## 1. Percorrer a tarefa, não o ecrã

Não avalies elementos por ordem de tamanho. **Faz o percurso da pessoa**, passo a
passo, e em cada passo pergunta:

- O que é que ela procura agora?
- Isso está visível, ou tem de o descobrir?
- Consegue perceber o que acontece se carregar?
- Se se enganar, percebe que se enganou? Consegue voltar atrás?

A maioria dos problemas reais aparece **entre** os ecrãs, não dentro deles.

## 2. Os seis eixos

Depois do percurso, verifica:

- **Hierarquia.** A coisa mais importante do ecrã é a mais visível? Se fechares os
  olhos e voltares a abrir, onde é que eles caem primeiro?
- **Ação principal.** Há **uma** óbvia? Dois botões com o mesmo peso visual é o
  mesmo que nenhum.
- **Carga.** Quantas decisões estão a ser pedidas ao mesmo tempo? O que podia ser
  decidido depois, ou não ser decidido de todo?
- **Estados.** Vazio, a carregar, erro, sem permissão, lista com um item, lista com
  quinhentos, texto longo, nome comprido. **Um design que só existe no estado
  perfeito não está desenhado.**
- **Consistência.** Faz o mesmo que o resto do produto faz, ou inventa aqui uma
  forma nova de fazer a mesma coisa?
- **Confiança.** No momento em que a pessoa carrega no botão que custa dinheiro,
  apaga algo ou envia ao cliente — ela sabe o que vai acontecer?

## 3. Classificar por dano, não por gosto

- **Bloqueia** — a pessoa não consegue fazer o que veio fazer, ou faz mal sem dar
  por isso.
- **Atrasa** — consegue, mas hesita, erra à primeira, ou tem de aprender.
- **Preferência** — gosto teu. Vai para uma secção à parte, marcada como tal, **sem
  peso nenhum na decisão**.

Ser honesto na terceira coluna é o que faz as outras duas serem levadas a sério. Um
crítico que apresenta preferências como problemas deixa de ser ouvido em ambas.

## 4. Cada ponto com o porquê e uma saída

Nunca escrevas só o problema. Cada linha leva:

- **o que observaste** — no ecrã, sem interpretação
- **quem é afetado e quando**
- **uma saída possível** — uma, não três; e dita como hipótese, não como ordem

Se não consegues explicar a quem é que aquilo faz mal, provavelmente é preferência.
Muda de coluna.

## 5. Entregar

```
### Crítica — <ecrã / fluxo> — <data>

**Contexto assumido:** <quem, a fazer o quê, onde>

**Bloqueia**
1. <observação> — <quem é afetado> — hipótese: <saída>

**Atrasa**
...

**Preferências (sem peso)**
...
```

Começa por **uma frase a dizer o que o design faz bem** — não por educação, mas
porque quem recebe precisa de saber o que **não** deve mexer ao corrigir o resto.

E fecha com a mesma linha do resto do catálogo:

> **Bloqueia desenvolvimento:** sim / não — e porquê.

---

## O que não é crítica

- "eu faria diferente" sem nomear o problema
- comparar com outro produto sem dizer o que ele resolve que este não resolve
- tendências ("isto já não se usa") — a pergunta é se funciona, não se é recente
- reescrever o design em vez de o criticar; se o trabalho é redesenhar, isso é outro
  pedido e diz-se
- pedir mais informação no ecrã sem dizer o que sai para dar lugar

---

## Antes de entregares

1. Sei quem usa isto, para quê e onde — ou perguntei?
2. Percorri a tarefa em vez de comentar elementos soltos?
3. Verifiquei os estados feios: vazio, erro, texto longo, lista enorme?
4. Cada ponto diz a quem faz mal?
5. As preferências estão separadas e marcadas como tal?

Se alguma resposta for "não", ainda é opinião.

Quando a crítica for aceite e o design for para desenvolvimento, o passo seguinte é
o `/design:handoff`. Se o problema for de texto e não de layout, é o `/design:copy`.
