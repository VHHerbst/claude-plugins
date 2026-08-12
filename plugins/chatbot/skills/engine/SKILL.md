---
name: engine
description: O motor que corre os fluxos de conversa — nós, condições, esperas, recolha de respostas e passagem para atendimento humano. Usa depois do /chatbot:channel, ou quando alguém pedir "motor de fluxos", "automação da conversa", "o bot tem de responder conforme a resposta", "esperar 2 horas e mandar outra mensagem", "passar para um humano".
---

# Engine

O motor é a parte que as pessoas acham que é a mais difícil e não é. A parte difícil
é o que acontece **entre** as mensagens: a conversa fica parada horas, o servidor
reinicia, a pessoa responde três coisas seguidas, ou responde ontem a uma pergunta
que já não interessa.

Um motor de fluxos é, no fundo, **uma máquina de estados guardada na base de dados**.
Se o estado viver na memória do processo, funciona nos testes e perde conversas em
produção.

---

## 1. O fluxo é dados, não código

O fluxo guarda-se em `jsonb` — uma lista de nós, cada um com o seu tipo e a ligação
para o seguinte:

```json
{
  "inicio": "n1",
  "nos": {
    "n1": { "tipo": "mensagem", "texto": "Olá {{nome}}! Em que posso ajudar?",
            "seguinte": "n2" },
    "n2": { "tipo": "pergunta", "guardar_em": "assunto", "seguinte": "n3" },
    "n3": { "tipo": "condicao", "se": "assunto contém preço",
            "entao": "n4", "senao": "n5" }
  }
}
```

Guardar como dados é o que permite, mais tarde, ter um construtor visual sem
reescrever o motor — o construtor passa a ser só um editor deste objeto. É por isso
que este passo vem antes do `/chatbot:builder`, e não ao contrário.

**Versiona.** Um fluxo publicado nunca é editado no sítio: cria-se uma versão nova.
As conversas a meio continuam na versão em que entraram — senão uma pessoa fica presa
num nó que deixou de existir.

## 2. Os tipos de nó, e chega

Resiste a inventar vinte. Estes fazem 90% do que qualquer plataforma destas faz:

- **mensagem** — envia texto, imagem ou botões
- **pergunta** — envia e **espera** resposta, guardando-a num atributo do contacto
- **condicao** — ramifica por atributo, por texto recebido ou por hora
- **espera** — pausa até um momento
- **acao** — marca etiqueta, chama um webhook teu, escreve noutra tabela
- **humano** — pára a automação e passa a conversa para uma pessoa

## 3. As quatro coisas que partem um motor

**A espera.** Nunca com `setTimeout` nem processo a dormir. Guarda `retomar_em` no
`flow_runs` e tem uma tarefa periódica a acordar quem já passou da hora. Foi para
isto que a coluna existe.

**A resposta fora de tempo.** A pessoa responde 6 horas depois, quando o fluxo já
seguiu. Decide **antes de programar**: a resposta tardia retoma o fluxo, ignora-se, ou
começa de novo? Não há resposta certa — há a resposta escrita, ou o comportamento
aleatório.

**Duas mensagens seguidas.** A pessoa manda "olá" e logo "quero saber o preço". Se
processas as duas em paralelo, o fluxo avança dois nós e a conversa fica sem sentido.
**Processa por conversa, em série** — uma fila por `conversation_id`, ou um lock.

**O ciclo infinito.** Um fluxo mal desenhado que volta ao mesmo nó envia mensagens
até o número ser banido. Põe um **limite de nós por execução** (por exemplo 50) e
pára com erro registado. Isto não é defensivo de mais: é a diferença entre um bug e
um número bloqueado.

## 4. O humano manda sempre

Quando uma conversa passa para atendimento humano, **a automação cala-se**. Nada de
"o bot responde se o humano demorar". Uma pessoa a falar com um cliente e a plataforma
a mandar mensagens automáticas por cima é a pior experiência que este produto pode
dar.

E dá sempre saída: uma palavra que a pessoa escreve para falar com alguém. Um chatbot
sem saída para humano é uma armadilha, e é assim que se perde o cliente que estava
mesmo a querer comprar.

**Calar por horário não é calar por handoff.** A regra de cima aplica-se a uma
conversa que alguém assumiu de facto. Calar a automação porque *são horas de
expediente* não tem ninguém do outro lado — tem a suposição de que alguém está a
olhar para a caixa de entrada. Numa clínica em produção essa guarda durou um dia:
um cliente pediu preços a meio da tarde e ficou uma hora à espera. Se quiseres dar
prioridade à equipa, dá-lha com um atraso — N minutos, e depois o bot entra.

## 5. Provar que funciona

Corre uma conversa inteira do telemóvel, e depois **olha para a base de dados**:

- o `flow_runs` avançou nó a nó, e ficou `em_espera` no sítio certo?
- a resposta ficou guardada no atributo do contacto?
- a espera de 2 minutos acordou sozinha?
- duas mensagens rápidas seguidas não fizeram saltar um nó?
- pediste humano e a automação calou-se?

Próximo comando: `/chatbot:builder`.

---

## Antes de dares o motor por feito

1. O estado da execução está na base de dados, e não na memória?
2. As esperas usam `retomar_em` + tarefa periódica?
3. Está decidido e escrito o que acontece com resposta fora de tempo?
4. Mensagens seguidas na mesma conversa são processadas em série?
5. Há limite de nós por execução?
6. Passar para humano cala a automação, e há saída para humano em qualquer momento?
7. Vi tudo isto na base de dados, não só nos logs?

Se alguma resposta for "não", o motor vai portar-se bem nos testes e mal em produção.
