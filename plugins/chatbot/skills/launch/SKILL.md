---
name: launch
description: Pôr a plataforma de conversas no ar e mantê-la de pé — o que verificar antes, o que monitorizar depois, e como saber que partiu antes de o cliente ligar. Usa no fim da construção, ou quando alguém pedir "pôr no ar", "lançar o chatbot", "checklist antes de publicar", "está tudo pronto?", "as mensagens deixaram de chegar".
---

# Launch

Uma plataforma de conversas falha de uma forma particular: **em silêncio**. Não há
página em baixo, não há erro no ecrã. As mensagens simplesmente deixam de chegar, e
descobre-se dois dias depois, quando um cliente pergunta porque é que ninguém lhe
respondeu.

Tudo o que este comando faz é resolver isso: garantir que **tu sabes antes do
cliente**.

---

## 1. Antes de abrir a alguém

**As credenciais.** Todas em variáveis de ambiente, e presentes em **todos** os
ambientes onde o código corre. Um `throw` numa variável que só existe em local
rebenta o deploy inteiro no primeiro arranque em produção — verifica que existem
antes de as tornares obrigatórias.

**O que está no ar é o teu código.** Em plataformas onde as funções servidor precisam
de deploy explícito, guardar não é deployar. Confirma no endpoint de produção, não no
repositório.

**As migrações correram.** Todas, por ordem. Ficheiro no git não é tabela na base de
dados. Vai ver a tabela.

**A RLS está ligada e restringe.** Não basta existir a policy: tenta ler dados de
outro cliente com as credenciais de um, e confirma que **não vês nada**. Uma policy
mal escrita não dá erro — dá resultados.

**Nada de dados fictícios no que foi publicado.** Nem escondidos atrás de uma flag: a
flag falha em silêncio e o cache guarda o que lá estava.

**Um fluxo real, de ponta a ponta, com telemóvel.** A pessoa escreve, o fluxo corre,
a resposta chega, a conversa fica na caixa de entrada. Se não fizeste isto hoje, não
está pronto.

## 2. O que monitorizar

Três sinais chegam para saber que está vivo:

**Mensagens recebidas na última hora.** Se um canal que costuma receber dezenas
recebe zero, o webhook caiu ou a instância desligou. **Este é o alarme mais
importante da plataforma**, e é o que ninguém põe.

**Taxa de falha de envio.** A subir significa bloqueio a começar. Age no aviso, não
no banimento.

**Execuções de fluxo presas.** `flow_runs` em `em_espera` com `retomar_em` já
passado há muito é a tarefa periódica que morreu.

Para cada um: um limite, e alguém avisado. Um gráfico que ninguém olha não é
monitorização.

## 3. O que vai partir, e o plano para cada

Escreve isto **antes** de acontecer, não durante:

- **a instância não oficial desliga** → quem repõe, e o que o cliente vê enquanto
  isso
- **o token da Meta expira** → quando expira, e quem renova
- **o número é banido** → há número alternativo? o histórico das conversas
  sobrevive?
- **a base de dados fica sem espaço** → as mensagens crescem depressa; decide agora o
  que se arquiva e quando

Nenhum destes é hipótese remota. São todos "quando", não "se".

## 4. Entregar a quem vai usar

Quem recebe a plataforma não quer saber de nada disto. Quer saber três coisas:

- o que já pode fazer hoje
- o que ainda não faz — dito explicitamente, para não descobrir sozinho
- a quem liga quando não funciona

E fica sempre escrito o que ficou por fazer. **Uma entrega honesta e incompleta custa
uma hora; uma entrega falsamente completa custa a confiança.**

## 5. Depois do lançamento

O que vier a seguir já não é construção, é manutenção — e aí o modo de trabalho muda:
mexer nisto passa a ser `/ops:sniper`, porque a partir de agora há gente a usar. A
revisão do que se muda é `/ops:recon`. Quando a lista de "arranjar um dia destes"
crescer, é `/ops:triage`.

Se construíres um segundo produto que repita metade disto — webhooks, filas, canais —
**é aí que se extrai a disciplina comum para um plugin próprio**. Não antes: com um
exemplo só, a abstração é adivinhação.

---

## Antes de dizer que está no ar

1. As variáveis existem em todos os ambientes?
2. O que responde em produção é o código novo — verificado no endpoint?
3. Todas as migrações correram, confirmado na base de dados?
4. Tentei ver dados de outro cliente e **não** consegui?
5. Não há dados fictícios no que foi publicado?
6. Corri um fluxo completo com telemóvel real, hoje?
7. Há alarme para "zero mensagens recebidas na última hora"?
8. Disse ao cliente o que ainda não faz?

Se alguma resposta for "não", ainda não está no ar — está publicado, que é diferente.
