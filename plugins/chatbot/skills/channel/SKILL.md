---
name: channel
description: Liga um canal real à plataforma de conversas — recebe mensagens por webhook e envia respostas, com WhatsApp (Evolution API, Z-API ou Cloud API da Meta) ou Instagram Direct. Usa depois do /chatbot:schema, ou quando alguém pedir "ligar o WhatsApp", "receber mensagens", "webhook do Instagram", "conectar o canal", "a mensagem não chega".
---

# Channel

Este é o passo em que a plataforma deixa de ser uma ideia. Uma pessoa escreve do
telemóvel dela, e aparece uma linha na tua tabela.

Enquanto isso não acontecer com um telemóvel verdadeiro, **não construas mais nada**.
Tudo o que vier depois assenta aqui.

---

## 1. Receber

O webhook tem uma regra que domina todas as outras: **responde `200` imediatamente e
processa depois.**

Meta e as APIs não oficiais reentregam o evento se demorares — e reentregar significa
responder duas vezes à mesma pessoa. Guardar a mensagem em bruto e devolver `200` tem
de acontecer antes de qualquer lógica de fluxo.

A ordem correta dentro do webhook:

1. **Validar que o pedido é mesmo de quem diz ser.** Na Meta, verifica a assinatura
   `X-Hub-Signature-256` com o teu app secret. Nas não oficiais, um token secreto no
   URL ou no header. **Um webhook aberto é um endpoint que qualquer pessoa usa para
   injetar mensagens na tua plataforma.**
2. **Gravar em bruto**, com o `external_id` do evento.
3. **`200`.**
4. Só então: encontrar ou criar o contacto, encontrar ou abrir a conversa, atualizar
   a janela de 24h, e entregar ao motor.

Se o `external_id` já existir, **para em silêncio**. Não é erro, é o normal.

Na Meta ainda há o passo de verificação inicial: um `GET` com `hub.challenge` que
tens de devolver tal e qual, senão a subscrição nunca fica ativa.

## 2. Enviar

Cada canal tem a sua forma, mas há coisas comuns a todos:

- **Nunca chames a API do canal a partir do frontend.** A chave fica no servidor,
  sempre. Uma chave de Z-API no bundle é uma conta usada por estranhos.
- **Guarda a mensagem de saída antes de enviar**, com estado `a_enviar`. Se a chamada
  falhar a meio, ficas a saber que tentaste.
- **Trata a falha.** Número inválido, fora da janela, template não aprovado,
  rate limit. Cada um destes precisa de comportamento próprio — engolir todos num
  `catch` é a forma mais rápida de teres uma plataforma que "não envia" e ninguém
  sabe porquê.
- **Respeita a janela.** Fora das 24h, no Instagram e no WhatsApp oficial, só passa
  template aprovado. Verifica antes de tentar, não descubras pelo erro.

## 3. As armadilhas de cada canal

**Não oficiais (Evolution, Z-API).** O número pode ser banido, e é. Não uses o teu
número pessoal. Não faças envios em massa daqui. E a instância cai — trata a
desconexão como estado normal do sistema, com reconexão e aviso, não como exceção.

Se a arquitetura do produto é uma instância central e não cada cliente a ligar o seu
número, **isso é decisão de produto e não se contorna com uma opção escondida**.

**WhatsApp Cloud API.** Templates aprovados para qualquer coisa fora da janela, e a
aprovação demora. Números de teste têm limites baixos que enganam: funciona nos
testes e falha no primeiro dia real.

**Instagram Direct.** O `external_id` é o PSID, e é **por página** — a mesma pessoa
tem PSID diferente noutra página tua. A app precisa das permissões
`instagram_manage_messages` e `pages_messaging`, e a conta tem de ser profissional e
ligada a uma página.

## 4. Provar que funciona

Nada disto conta como feito por causa de um `200` nos logs. **Prova é:**

1. Escreveste do teu telemóvel para o número/conta.
2. Apareceu **uma** linha em `messages` — não zero, não duas.
3. O contacto foi criado com o `external_id` certo.
4. A resposta chegou ao telemóvel.
5. Escreveste outra vez e não duplicou nada.

Se estás numa plataforma onde as funções servidor precisam de **deploy explícito**,
confirma que o que está a responder em produção é o teu código novo. Guardar não é
deployar, e um webhook antigo continua a responder `200` sem fazer nada de novo.

## 5. Entregar

Diz o que ficou ligado, com que credenciais (**nome** das variáveis, nunca o valor),
o que falta configurar do lado do fornecedor, e o teste que fizeste com telemóvel
real.

Próximo comando: `/chatbot:engine`.

---

## Antes de dares o canal por ligado

1. O webhook valida a origem — assinatura ou token secreto?
2. Devolve `200` antes de processar?
3. Mensagem repetida é ignorada pelo `external_id`?
4. As chaves estão só no servidor, e o nome delas está documentado?
5. As falhas de envio têm tratamento por tipo, e não um `catch` único?
6. **Testei com um telemóvel a sério e vi a linha na tabela?**

Se a 6 for "não", ainda não está ligado — está por testar.
