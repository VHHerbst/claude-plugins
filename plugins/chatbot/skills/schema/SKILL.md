---
name: schema
description: Modelo de dados da plataforma de conversas — contactos, conversas, mensagens, fluxos e execuções — com isolamento por cliente e RLS desde a primeira migração. Usa depois do /chatbot:start, ou quando alguém pedir "as tabelas do chatbot", "modelo de dados das conversas", "schema do manychat", "como guardo as mensagens".
---

# Schema

O modelo de dados é a única parte deste projeto que **não dá para corrigir depois em
silêncio**. Quando houver cem mil mensagens guardadas e três clientes a usar, mudar a
forma como o contacto é identificado deixa de ser uma migração e passa a ser um fim
de semana perdido.

Duas decisões têm de estar certas à primeira: **como se identifica um contacto** e
**como se separam os clientes**.

---

## 1. A identidade do contacto

A mesma pessoa pode escrever-te por WhatsApp e por Instagram, e o identificador é
diferente em cada canal — número de telefone num, PSID no outro. E o PSID **é
diferente por cada página**: a mesma pessoa tem PSIDs distintos em duas páginas tuas.

Portanto: **o identificador do canal nunca é a chave primária do contacto.**

```
contacts            id, tenant_id, nome, atributos (jsonb), criado_em
contact_channels    id, contact_id, canal, external_id, UNIQUE(canal, external_id)
```

Assim a mesma pessoa junta-se depois sem perder histórico. Se puseres o número de
telefone como chave do contacto, no dia em que ligares o Instagram tens a mesma
pessoa duas vezes e nenhuma forma limpa de as unir.

`atributos` em `jsonb` é o que o ManyChat chama campos personalizados — o que o fluxo
recolhe e guarda. Não crias uma coluna por cada coisa que perguntas.

## 2. O isolamento

Se a plataforma serve clientes teus, **`tenant_id` entra em todas as tabelas na
primeira migração** e a RLS é escrita ao mesmo tempo. Não "depois, quando houver
clientes". Depois significa nunca, e significa o dia em que um cliente vê as
conversas do outro.

Segue a convenção da casa: schema próprio do projeto, e o que tiver de ser exposto em
`public` vai com o prefixo do projeto. Confirma qual é a convenção **lendo o projeto**,
não de memória.

Escreve as policies com a função de autorização que o projeto já usa — e confirma em
que schema ela vive de facto na base de dados viva, que pode não ser onde a migração
antiga a criou.

**Não te esqueças do `DELETE`.** É a policy que mais falta, e a falta dela só aparece
quando alguém tenta apagar e nada acontece — ou pior, quando apaga o que não era dele.

## 3. As tabelas

```
contacts            quem é a pessoa (acima)
contact_channels    por onde se fala com ela (acima)

conversations       contact_id, canal, estado (aberta/fechada/humano),
                    ultima_mensagem_em, janela_expira_em
messages            conversation_id, direcao (entrada/saida), tipo, conteudo,
                    external_id UNIQUE, estado (enviada/entregue/lida/falhou),
                    erro, criado_em

flows               nome, versao, publicado, definicao (jsonb)
flow_runs           flow_id, contact_id, no_atual, variaveis (jsonb),
                    estado (a_correr/em_espera/terminado/falhou), retomar_em
```

Três pontos que parecem detalhe e não são:

**`external_id UNIQUE` em `messages`.** Os webhooks repetem-se — a Meta e as APIs
não oficiais reentregam o mesmo evento quando não recebem `200` depressa. Sem esta
restrição, respondes duas vezes à mesma mensagem e o cliente vê a plataforma a
gaguejar.

**`janela_expira_em` na conversa.** No Instagram e no WhatsApp oficial só podes
iniciar contacto dentro de 24h desde a última mensagem da pessoa. Guardar isto é o
que impede a plataforma de tentar enviar o que vai ser recusado.

**`retomar_em` no `flow_runs`.** É o que faz uma espera de 2 horas dentro de um fluxo
funcionar sem um processo a dormir agarrado à memória.

## 4. Índices que vais precisar

Não são otimização prematura — são as queries que a plataforma faz a toda a hora:

- `messages (conversation_id, criado_em DESC)` — abrir uma conversa
- `conversations (tenant_id, ultima_mensagem_em DESC)` — a caixa de entrada
- `flow_runs (estado, retomar_em)` — quem tem de acordar agora
- `contact_channels (canal, external_id)` — já vem do `UNIQUE`

## 5. Entregar

Migração **idempotente**, e enums em ficheiro separado que corre **antes**.

E diz claramente: **ficheiros de migração no git não correm sozinhos.** Alguém tem de
os aplicar. Enquanto isso não acontecer, a base de dados não mudou — por muito verde
que esteja o deploy.

Fecha com o próximo comando: `/chatbot:channel`.

---

## Antes de dares o schema por feito

1. O identificador do canal está numa tabela à parte, e não é a chave do contacto?
2. Se é multi-tenant, `tenant_id` e RLS entraram **nesta** migração?
3. Há policy de `DELETE`?
4. `messages.external_id` é `UNIQUE`?
5. A conversa guarda quando expira a janela de 24h?
6. A migração é idempotente e os enums estão isolados?
7. Disse a quem entrega que ainda falta **correr** o SQL?

Se alguma resposta for "não", ainda não está feito.
