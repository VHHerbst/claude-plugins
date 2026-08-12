---
name: isolate
description: Isolamento de avaria em sistema a correr — confirma que há mesmo avaria, separa o teu código da plataforma e dos dados, e devolve a camada culpada com a prova que a acusa, antes de alguém abrir um ficheiro. Usa quando algo que funcionava deixou de funcionar, quando alguém disser "isto está partido", "deu erro em produção", "parou de entrar", "o cliente diz que não recebeu", "não aparece nada", ou quando a única pista for um silêncio — nenhuma mensagem, nenhuma marcação, nenhum registo novo.
---

# Isolate

Uma avaria em produção não se corrige: primeiro isola-se. A diferença entre uma hora
e um dia perdido está quase sempre na primeira decisão — em que camada se acredita
que está o problema. Quem começa a ler código antes de saber isso está a procurar
debaixo do candeeiro.

Isto não é revisão (`/ops:recon`) nem priorização (`/ops:triage`). Aqui há uma coisa
concreta que não funciona, e o objetivo é dizer **qual a camada culpada e com que
prova** — não emendar.

---

## 0. Confirma que há avaria

Antes de tudo: **o sintoma existe?**

Ausência de atividade não é sintoma. "Não entraram mensagens hoje", "ninguém marcou",
"a sincronia não correu" — nada disto é uma avaria enquanto não souberes que **devia**
ter havido tráfego. Pergunta o que se fez, quando, e o que se esperava ver.

Um relato tem sempre três partes, e a maioria chega com uma só:

1. **o que se fez** — a ação concreta, com hora;
2. **o que aconteceu** — a mensagem de erro, o ecrã, o silêncio;
3. **o que se esperava** — sem isto não há avaria, há expectativa.

Investigar a partir de uma premissa que ninguém verificou custa o dobro: gasta-se o
tempo, e ainda se altera configuração de produção para resolver um problema que não
existia.

## 1. Preserva a prova antes de mexer

**A primeira alteração apaga a prova.** Configuração sobrescrita, contentor
reiniciado, ficheiro substituído — depois disso já não se sabe se o que lá estava era
a causa ou já estava certo.

Antes de tocar em seja o que for, guarda o estado atual: copia o valor, tira o
screenshot, corre a query e guarda a saída. Vale sobretudo para o que **não tem
leitura** — há painéis onde se escreve a configuração e não se consegue voltar a
lê-la. Escrever por cima aí é apagar a única cópia.

## 2. Corta pelo meio, não pelo princípio

Um pedido atravessa camadas. Não as sigas por ordem: parte-as ao meio e vê de que
lado está o problema. Cada corte elimina metade.

O corte mais rentável é quase sempre **entre o que é teu e o que não é**:

| Camada | Pergunta que a ilibra ou acusa |
| --- | --- |
| Quem envia | o pedido chegou sequer a sair? |
| Rede e entrada | o webhook do fornecedor ainda aponta para nós? |
| Runtime | o processo arranca, ou nem isso? |
| Configuração | as credenciais chegam ao processo? |
| Código | com a entrada certa, faz o que devia? |
| Dados | a linha existe, e com que forma? |
| Interface | o ecrã está a mostrar o que a base tem? |

Um ecrã desatualizado é a explicação mais comum e a menos suspeitada. Sessão
expirada, cache, aba aberta desde ontem — a página mostra o estado de ontem e não
avisa. Confirma na base antes de acreditares no que vês.

## 3. Prova de vida por camada

Cada camada tem uma pergunta que se responde em segundos, sem efeitos secundários.
Faz a pergunta; não deduzas a resposta.

- **Arrancar não é funcionar.** Um serviço que responde `200` pode estar sem
  credenciais nenhumas. Precisas de um caminho que **use a credencial** e devolva
  resposta observável — uma verificação de webhook que só devolve o desafio se a
  chave for lida, um endpoint de estado, um caso de erro que só ocorre com a
  configuração certa.
- **"Está no painel" não é estar no processo.** A resposta é `env | grep -c '^PREFIXO_'`
  dentro do contentor, não a captura de ecrã do painel.
- **O que a plataforma diz sobre si própria não conta.** "Up to date", "Deployed",
  "Ativo" — descrevem o registo dela, não o artefacto que está a atender.

Quando a prova real implica disparar algo para uma pessoa — mandar uma mensagem,
criar uma marcação, cobrar — **não testes no cliente**. Procura o caminho que passa
pelo mesmo código e pela mesma credencial sem tocar em ninguém.

## 4. Depois de mexer em infraestrutura, varre tudo

Se o que mudou foi o contentor, o painel ou o runtime — e não uma linha de código —
o dano não fica onde puseste as mãos. Varre **todos** os endpoints, não só aquele em
que mexeste.

Para isso tens de saber de antemão que resposta significa "vivo". Num serviço com
autenticação, um `401` é boa notícia: significa que arrancou. O que procuras é o erro
de arranque.

É uma varredura destas que encontra o que desapareceu sem ninguém pedir.

## 5. Pergunta quem dá pela falta

Há caminhos que só gente de fora usa: o formulário público, o webhook de entrada, a
sincronização automática, o email de convite. Ninguém da equipa passa por lá — por
isso, **quando param, não há queixa. Há silêncio, e o silêncio lê-se como "está tudo
bem".**

Ao fechar o isolamento, diz há quanto tempo aquilo estava assim e quem teria dado por
isso. Uma marcação pelo site pode estar morta há dias sem uma única chamada de
cliente.

E procura onde as falhas ficam escritas sem avisar ninguém: tabelas de log, `status =
'falhou'`, execuções vermelhas num painel que ninguém abre. É lá que está a contagem
do estrago.

## 6. Entregar

```
Isolamento — <sistema> — <data>

SINTOMA        o que se fez, o que aconteceu, o que se esperava
CAMADA         onde está o problema
PROVA          o comando ou query que o demonstra, e a saída
DESDE QUANDO   e quem teria dado por isso
ESTRAGO        o que já aconteceu enquanto esteve assim
NÃO É          as camadas que ilibaste, e como
```

O campo **NÃO É** vale tanto como o resto. Sem ele, a próxima pessoa repete o
caminho todo.

---

## O que não é isolamento

- **Corrigir.** Isolar termina quando a camada está identificada com prova. A correção
  é outro pedido, e em produção segue o `/ops:sniper`.
- **Adivinhar pela última alteração.** "Foi o último deploy" é hipótese, não
  conclusão. Vale como ordem de investigação, nunca como resposta.
- **Aceitar o relato como diagnóstico.** Quem reporta viu um sítio. O mesmo erro
  costuma estar nos caminhos automáticos, onde não há ninguém a olhar.
- **Culpar o código primeiro.** É a camada que mais se lê e a que menos falha sozinha
  em sistemas que já funcionavam. Alguma coisa mudou — normalmente à volta dele.

## Antes de dares o isolamento por fechado

1. Confirmei que houve mesmo avaria, ou parti de uma ausência?
2. Guardei a prova antes de alterar o que quer que fosse?
3. A camada que acuso tem uma prova que a acusa, ou só uma suspeita?
4. Disse quais as camadas que ilibei?
5. Sei desde quando, e quem daria por isso?
6. Contei o estrago, ou só descrevi a causa?

Se alguma resposta for "não", ainda não isolaste — ainda estás a palpitar.
