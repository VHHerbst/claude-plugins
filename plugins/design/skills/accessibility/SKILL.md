---
name: accessibility
description: Auditoria de acessibilidade WCAG de um ecrã, componente ou fluxo, feita por tarefa e não por checklist. Usa quando alguém pedir "auditoria de acessibilidade", "WCAG", "isto é acessível?", "a11y", "contraste", "navegação por teclado", "leitor de ecrã", ou antes de entregar um produto a cliente que exija conformidade.
---

# Accessibility

A pergunta não é "cumpre os critérios?". É **"esta pessoa consegue fazer o que veio
fazer?"**.

Um ecrã pode passar em quarenta critérios e continuar impossível de usar só com o
teclado, porque o foco desaparece a meio. E um ecrã pode falhar um critério de
contraste num rodapé decorativo sem que isso afete ninguém.

Auditar por tarefa apanha o primeiro caso. Auditar por checklist só apanha o segundo.

---

## 0. O que ferramenta nenhuma apanha

Antes de começar, tem isto presente para saberes onde gastar o esforço: as
ferramentas automáticas apanham à volta de **um terço** dos problemas reais. Detetam
contraste, `alt` em falta e alguns erros de marcação.

**Não detetam** — e é aqui que a auditoria vale:

- ordem de tabulação ilógica
- foco que desaparece ou fica preso dentro de um modal
- `alt` que existe mas descreve a aparência em vez da função
- mensagem de erro que aparece visualmente mas nunca é anunciada
- ação que só existe em `hover`
- rótulo que faz sentido a ver o ecrã e nenhum a ouvi-lo

Se o projeto tiver `axe`, `lighthouse` ou equivalente, corre-o para limpar o
trivial — e depois **audita a sério**.

## 1. Percorrer a tarefa por três caminhos

Escolhe a tarefa principal do ecrã e completa-a três vezes:

**Só com teclado.** Tab, Shift+Tab, Enter, Espaço, Escape, setas. Nada de rato.
- Consegues chegar a tudo o que é interativo?
- **Vês sempre onde estás?** Foco invisível é o problema mais comum e o mais fácil
  de corrigir.
- A ordem faz sentido, ou salta para o rodapé a meio do formulário?
- Abriste um modal — o foco entrou lá? Fica preso lá dentro? Ao fechar, volta ao
  sítio de onde veio?
- Há armadilhas: sítios onde entras e não sais sem rato?

**Sem ver o ecrã.** Lê a página como um leitor de ecrã a leria: só a estrutura, os
rótulos e o que é anunciado.
- Os cabeçalhos formam um índice que se percebe, sem saltar de `h1` para `h4`?
- Cada campo tem rótulo associado — não é `placeholder` a fazer de rótulo?
- Botões só com ícone: têm nome acessível que diz **o que fazem**, não o que
  parecem? (`Fechar`, não `Cruz`.)
- Quando aparece um erro, ou um resultado carrega, isso é **anunciado**?
- Imagens decorativas estão marcadas como decorativas, em vez de terem descrição a
  ler em voz alta?

**Com dificuldade de visão ou motora.**
- Contraste: **4.5:1** texto normal, **3:1** texto grande e elementos de interface
  (bordas de campos, ícones que dizem algo).
- Alvos de toque com pelo menos **24px**, e espaçados o suficiente para não se
  acertar no errado.
- Nada depende **só** de cor para dizer o que quer dizer — o estado de erro precisa
  de mais que ficar vermelho.
- O texto aumenta até 200% sem partir o layout nem cortar conteúdo.
- Há movimento? Respeita `prefers-reduced-motion`?

## 2. Classificar por impacto real

- **Impede** — há gente que simplesmente não consegue completar a tarefa. Formulário
  que não se submete por teclado, modal sem saída, campo sem rótulo num passo
  obrigatório.
- **Dificulta** — consegue-se, com esforço a mais: contraste fraco no texto que
  importa, foco pouco visível, ordem estranha.
- **Não conforme** — falha o critério sem impacto prático: contraste num rodapé
  decorativo, `alt` numa imagem que ninguém precisa de ver.

Se o cliente exige conformidade formal (concurso público, contrato), a terceira
coluna também entra no orçamento — mas continua a ser a última a corrigir.

## 3. Cada achado com prova e com a correção

```
| Impacto | O quê | Onde | Critério | Correção |
|---|---|---|---|---|
| Impede | Modal não devolve o foco ao fechar; teclado volta ao topo | Modal de confirmação | 2.4.3 | Guardar o elemento que abriu e devolver-lhe o foco no onClose |
```

Cita o critério WCAG quando existir, mas **o critério nunca substitui a explicação
do dano**. "Falha 1.4.3" não convence ninguém a corrigir. "O valor total do carrinho
não se lê com o ecrã ao sol" convence.

## 4. Entregar

Ordena por impacto. Fecha com:

> **Impede alguém de comprar / submeter / concluir:** sim / não — e o quê.

E diz explicitamente **o que não conseguiste testar** — leitor de ecrã real, zoom em
dispositivo verdadeiro, utilizadores com deficiência. Uma auditoria que finge ter
coberto tudo é pior que uma auditoria honesta e parcial.

---

## Antes de entregares a auditoria

1. Completei a tarefa só com teclado, do princípio ao fim?
2. Verifiquei o que acontece ao foco quando modais abrem e fecham?
3. Verifiquei que erros e mudanças de estado são anunciados, não só mostrados?
4. Os rótulos dizem a **função**, não a aparência?
5. Cada achado tem a correção concreta, não só o número do critério?
6. Disse o que ficou por testar?

Se alguma resposta for "não", ainda é uma checklist.

O que sair daqui e for para implementar passa pelo `/design:handoff`; o que já
estiver em produção, pelo `/ops:sniper`.
