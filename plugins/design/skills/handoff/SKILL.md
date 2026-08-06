---
name: handoff
description: Transforma um design em especificação que um programador consegue implementar sem adivinhar — estados, casos limite, tokens e o que reutilizar do design system que já existe. Usa quando alguém pedir "handoff", "specs para o dev", "passa isto para desenvolvimento", "o que o programador precisa de saber", partilhar um ficheiro ou link de Figma para implementar, ou quando um design ficar aprovado e for preciso construí-lo.
---

# Handoff

Um handoff não falha nos pixels. Falha no **"e quando não houver nada?"**, no
**"e se o nome for enorme?"**, no **"e enquanto está a carregar?"**.

O programador que recebe um design incompleto não pára para perguntar — ele decide.
E as decisões que ele tomar às três da tarde de uma sexta-feira passam a fazer parte
do produto para sempre.

Especificar é responder às perguntas antes de elas serem feitas.

---

## 0. Ler o que já existe antes de especificar seja o que for

Isto é o passo que mais handoffs saltam e o que causa mais estrago.

Procura no projeto, **antes** de escrever uma linha de spec:

- o design system ou biblioteca de componentes (`components/ui`, `Button`, `Card`…)
- os tokens já definidos — cores, espaçamentos, tipografia, raios, sombras
- um ecrã parecido já implementado

> **Um handoff que ignora o que já existe cria o sétimo botão do produto.** Se o
> design usa um azul que não está nos tokens, ou um espaçamento fora da escala, a
> especificação tem de dizer isso explicitamente: **é intencional e entra no design
> system, ou é engano e usa-se o que já lá está?** Essa pergunta é tua, não do dev.

## 1. O que o dev precisa de receber

### Estrutura
Do exterior para o interior: o que é fixo, o que estica, o que quebra. Um layout
descrito em pixels absolutos não sobrevive ao primeiro ecrã diferente.

### Comportamento por breakpoint
Não chega dizer "responsivo". O que acontece à tabela no telemóvel — vira cartões,
faz scroll horizontal, esconde colunas? **Escolhe.** Se não escolheres, escolhe o
dev.

### Estados de cada componente interativo
A lista mínima, sem exceções:

`default` · `hover` · `focus (visível ao teclado)` · `active` · `disabled` ·
`loading` · `erro`

Se um estado não estiver desenhado, diz o que fazer nele. "Não especificado" é uma
resposta honesta; o silêncio não é.

### Estados de cada ecrã

- **vazio** — primeira vez, e vazio por filtro (são diferentes: um ensina, o outro
  oferece limpar o filtro)
- **a carregar** — skeleton, spinner, ou nada
- **erro** — de rede, de permissão, de validação
- **sem permissão** — o que este papel não pode ver, e se o vê desativado ou não vê
  de todo

### Conteúdo real, não Lorem
Especifica com o pior conteúdo verdadeiro: o nome de empresa mais comprido que
existe na base de dados, o valor com mais dígitos, a lista com um item e a lista com
quinhentos. **Onde corta, onde quebra a linha, onde aparece reticências.**

### Interação e movimento
O que é imediato, o que espera resposta do servidor, o que é otimista. Duração e
easing das transições que importam. Se houver movimento, o que acontece com
`prefers-reduced-motion`.

### Acessibilidade que só o design responde
Ordem de tabulação quando não é a óbvia, o que é anunciado a leitores de ecrã em
ícones sem texto, e para onde vai o foco depois de fechar um modal.

## 2. A secção que quase todos saltam

Uma lista de **"o que acontece quando…"**, com as perguntas concretas deste ecrã:

- ... a lista está vazia porque o utilizador é novo?
- ... a lista está vazia porque o filtro não deu resultados?
- ... o pedido falha a meio da submissão?
- ... a pessoa não tem permissão para a ação que está visível?
- ... o valor é zero, negativo, ou nulo?
- ... a pessoa abre isto em duas abas ao mesmo tempo?

Escreve as que se aplicam. Esta secção é a diferença entre "implementei o design" e
"o ecrã funciona".

## 3. Marcar o que ficou por decidir

Nunca entregues um handoff com buracos silenciosos. Faz uma secção
**"Por decidir"** com as perguntas em aberto e **quem as responde**.

Uma pergunta explícita atrasa uma hora. Uma pergunta implícita vira uma decisão
errada que se descobre em produção.

## 4. Entregar

```
### Handoff — <ecrã> — <data>

**Reutiliza:** <componentes e tokens existentes>
**Novo no design system:** <o que é mesmo novo, e porquê>

#### Estrutura
#### Breakpoints
#### Componentes e estados
#### Estados do ecrã
#### O que acontece quando…
#### Acessibilidade
#### Por decidir — <pergunta> → <quem responde>
```

Se o projeto seguir o nosso padrão de documentação, oferece-te para gravar em
`docs/features/`, mas **pergunta antes de escrever ficheiros no repositório**.

---

## Antes de entregares o handoff

1. Li o design system e os tokens do projeto antes de especificar?
2. Cada componente interativo tem os sete estados, ou diz explicitamente o que fazer
   nos que faltam?
3. Cada ecrã tem vazio, a carregar, erro e sem permissão?
4. Especifiquei com o pior conteúdo real, não com Lorem?
5. A secção "o que acontece quando…" existe e é deste ecrã, não genérica?
6. O que ficou por decidir está escrito, com dono?

Se alguma resposta for "não", o dev vai decidir por ti.

Depois de implementado, quem verifica é o `/ops:recon`. A conformidade WCAG é o
`/design:accessibility`.
