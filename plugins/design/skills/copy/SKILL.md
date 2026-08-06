---
name: copy
description: Escreve e revê o texto de interface — botões, rótulos, estados vazios, mensagens de erro, confirmações e ecrãs de onboarding. Usa quando alguém pedir "UX copy", "o texto deste ecrã", "escreve as mensagens", "melhora este botão", "mensagem de erro", "estado vazio", ou quando um fluxo estiver desenhado e faltar o que lá está escrito.
---

# Copy

O texto de uma interface não é conteúdo. **É interface.** Um botão mal escrito falha
exatamente como um botão mal colocado: a pessoa hesita, carrega no errado, ou desiste.

E escreve-se para o pior momento — não para quem está descansado a explorar o
produto, mas para quem está com pressa, já se enganou uma vez, e está a ler no
telemóvel enquanto faz outra coisa.

---

## 0. Duas decisões antes de escrever a primeira palavra

**A variante do português.** PT-PT ou PT-BR. Não é detalhe: *ecrã* e *tela*,
*utilizador* e *usuário*, *guardar* e *salvar*, *telemóvel* e *celular*. Misturar as
duas no mesmo produto faz o produto parecer montado à pressa por várias pessoas — que
foi exatamente o que aconteceu.

Descobre qual é a do projeto lendo o que já lá está, e **segue essa**. Se o produto
serve os dois mercados, isso é uma decisão de arquitetura, não de copy — vai para o
`/ops:doctrine`.

**O tratamento.** Tu ou você, e o mesmo do princípio ao fim.

## 1. As palavras são as da pessoa, não as do sistema

O utilizador não sabe o que é uma *policy*, um *registo*, uma *entidade*, um *lead*
ou um *card*. Ele sabe o que é um cliente, uma proposta, uma marcação.

Traduz sempre do sistema para o negócio. Se não consegues traduzir um termo, é sinal
de que o conceito não devia estar exposto ali.

## 2. Regras por tipo de texto

### Botões
**Verbo da ação, na primeira pessoa de quem carrega.** `Guardar alterações`,
`Enviar proposta`, `Marcar consulta`.

Nunca `OK`, `Confirmar`, `Continuar` — obrigam a ler a caixa toda para saber o que
vai acontecer. Se o botão sozinho não diz o que faz, está mal escrito.

Num par de botões, o secundário diz o que faz, não `Cancelar`: `Manter rascunho`.

### Mensagens de erro
Três coisas, por esta ordem: **o que falhou**, **porquê em linguagem de pessoa**, **o
que fazer agora**.

- Nunca `Ops!`, nunca `Algo correu mal`, nunca um pedido de desculpa em vez de uma
  saída.
- Nunca o texto do erro técnico. `PGRST116` não é uma mensagem.
- Se a culpa é do sistema, assume sem drama e diz quando voltar a tentar.
- Se a culpa é do preenchimento, diz **qual campo** e **o que se espera** — não
  "dados inválidos".

> `Não foi possível guardar: a data da consulta é anterior a hoje. Escolhe uma data
> futura.`

### Estados vazios
É o ecrã que a pessoa vê **na primeira vez**. É a melhor oportunidade de ensinar o
produto — não a desperdices com um desenho bonito e "Nada por aqui".

Diz o que aparece aqui quando houver, porque é útil, e dá a ação para o primeiro.

E distingue: vazio **de novo** ensina; vazio **por filtro** oferece limpar o filtro.
São textos diferentes.

### Confirmações destrutivas
Diz **o que se perde** e se **dá para voltar atrás**. O botão nomeia o estrago:
`Apagar 12 contactos`, não `Confirmar`.

Se a ação é reversível, diz — poupa o susto e a chamada ao suporte.

### Sucesso
Confirma o que aconteceu **e o que se segue**. `Proposta enviada. O cliente recebe
por email e ficas a saber quando abrir.`

Sucesso que só diz "Guardado com sucesso" desperdiça o único momento em que a pessoa
está a olhar e tranquila.

### Rótulos de campo
O rótulo diz o que é; o texto de ajuda diz o formato ou a razão. **Nunca uses
`placeholder` como rótulo** — desaparece quando se escreve, e quem volta a rever o
formulário já não sabe o que preencheu.

## 3. Cortar

Escreve, depois tira metade. Quase sempre sobra:

- "Por favor", "simplesmente", "basta", "apenas"
- explicar o óbvio: `Clique aqui para...`
- o produto a falar de si: `O nosso sistema irá processar...`
- exclamações. Uma interface entusiasmada a meio de um erro é irritante.

Teste final: **lê em voz alta.** Se não dizes assim a um colega, não escrevas assim
no ecrã.

## 4. Entregar

Tabela com o texto atual e o proposto, e **a razão** — sem a razão, é troca de gosto
por gosto:

```
| Onde | Está | Fica | Porquê |
|---|---|---|---|
| Botão do modal | Confirmar | Apagar 12 contactos | Diz o estrago; sozinho já se percebe |
```

Se o texto for para vários sítios (email, notificação, ecrã), verifica que dizem
todos a mesma coisa. Copy inconsistente entre canais é o que faz uma pessoa achar
que fez duas ações quando fez uma.

---

## Antes de entregares o copy

1. Confirmei a variante do português e o tratamento com o que já existe no produto?
2. Cada botão diz o que faz sem ser preciso ler o resto?
3. Cada erro diz o que fazer a seguir?
4. Os estados vazios ensinam, em vez de decorar?
5. Tirei o "por favor", os "simplesmente" e as exclamações?
6. Li em voz alta?

Se alguma resposta for "não", ainda é texto, não é interface.

Se ao escrever descobrires que o ecrã precisa de uma explicação comprida para se
perceber, o problema não é o texto — é o desenho. Isso é `/design:critique`.
