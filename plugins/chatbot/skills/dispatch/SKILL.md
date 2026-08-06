---
name: dispatch
description: Campanhas e envios para muitos contactos ao mesmo tempo, com segmentação, opt-out, ritmo de envio e proteção contra banimento. Usa depois do /chatbot:builder, ou quando alguém pedir "enviar para todos os contactos", "campanha de WhatsApp", "disparo em massa", "mandar promoção", "o número foi bloqueado".
---

# Dispatch

Esta é a funcionalidade que dá dinheiro e é a que destrói plataformas. Um envio mal
feito não dá um erro: dá um número banido, uma conta desativada, e um cliente sem
canal de vendas na segunda-feira de manhã.

Por isso este passo é o último, e por isso tem mais travões que funcionalidades.

**A regra que resume tudo: a plataforma tem de ser mais cautelosa do que a pessoa que
carrega no botão.** Quem carrega está com pressa e a ver o resultado; quem paga a
conta do banimento é o cliente.

---

## 1. Antes de qualquer código, o consentimento

**Só se envia a quem escreveu primeiro, ou a quem deu consentimento registado.**
Comprar listas ou importar contactos de sítio nenhum é o caminho direto para o
bloqueio — e, em muitos sítios, é ilegal.

Guarda, por contacto: se aceitou receber, quando, e por onde veio. Sem esses três
campos, não há campanha.

**O opt-out é obrigatório e imediato.** Uma palavra ("sair", "parar") que marca o
contacto e **corta na hora**, inclusive uma campanha a meio de ser enviada. Ignorar
um pedido de saída é a denúncia que traz o bloqueio mais depressa que qualquer
volume.

E o opt-out vale para campanhas, não para respostas: se a pessoa escrever depois de
sair, continua a poder ser atendida.

## 2. A janela e os templates

No WhatsApp oficial e no Instagram, fora das 24h só passa **template aprovado**. Não
é uma restrição a contornar — é a regra da plataforma, e contorná-la é o que fecha
contas.

Filtra o público **antes** de enviar: quem está fora da janela e não tem template
aprovado não entra na campanha. Diz isso no ecrã, com números — "1.240 contactos, 310
fora da janela" — para quem carrega saber o que vai acontecer.

## 3. O ritmo

Nunca dispares tudo de uma vez. Uma fila, com:

- **intervalo entre mensagens**, com variação aleatória — envios em intervalos
  exatamente iguais parecem o que são
- **limite por hora e por dia**, configurável e conservador por omissão
- **paragem automática** se as falhas passarem de uma percentagem: é o primeiro sinal
  de bloqueio, e continuar a insistir transforma um aviso num banimento
- **botão de parar**, que pára mesmo — não "no fim do lote"

Nas APIs não oficiais, sê ainda mais lento do que te parece razoável. O canal não te
avisa antes de te banir.

## 4. Cada envio é rastreável

Uma campanha sem registo por contacto é impossível de depurar e impossível de
explicar ao cliente:

```
campaigns          nome, fluxo/template, segmento, estado, criado_por, criado_em
campaign_targets   campaign_id, contact_id, estado (pendente/enviado/entregue/
                   lido/falhou/ignorado), motivo_ignorado, erro, enviado_em
```

O `motivo_ignorado` é a coluna que evita as discussões: fora da janela, sem
consentimento, opt-out, número inválido.

## 5. Ensaiar antes

Duas coisas, sempre, antes de deixar carregar em enviar:

- **pré-visualização com contactos reais** — a mensagem já com as variáveis
  substituídas, para três pessoas do segmento. É aqui que se apanha o `Olá {{nome}}!`
  que ia sair assim mesmo.
- **envio de teste só para ti**, no canal real.

E uma confirmação que **diz o número**: `Enviar a 1.240 contactos`. Nunca
`Confirmar`. Quem carrega tem de ver o tamanho do que está a fazer.

## 6. Provar

Faz uma campanha a três contactos teus e verifica na base de dados: três linhas em
`campaign_targets`, estados a evoluir, e o intervalo entre envios respeitado. Depois
manda "sair" de um deles e confirma que ficou marcado e **não recebeu o resto**.

Próximo comando: `/chatbot:launch`.

---

## Antes de dares as campanhas por feitas

1. Só se envia a quem tem consentimento registado, com data e origem?
2. O opt-out corta na hora, inclusive campanha a meio?
3. Quem está fora da janela é filtrado antes, com o número mostrado no ecrã?
4. Há intervalo com variação, limites por hora e por dia?
5. Há paragem automática por taxa de falhas e um parar que pára mesmo?
6. Cada contacto tem estado e motivo, incluindo os ignorados?
7. A confirmação diz o número de destinatários?
8. Testei o opt-out a meio de um envio real?

Se alguma resposta for "não", não publiques isto. O custo do erro aqui não é um bug —
é o canal do cliente.
