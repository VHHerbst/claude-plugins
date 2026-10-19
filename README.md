# Plugins V2H para Claude Code

Comandos que fazem o Claude Code trabalhar como um profissional experiente trabalha:
a duvidar do que encontra, a ordenar pelo que custa de facto, e a dizer o que ficou
por fazer em vez de dar tudo por concluído.

São quatro caixas de ferramentas. Instalas só a tua.

---

## Instalar

Dentro do Claude Code, em qualquer projeto:

```
/plugin marketplace add VHHerbst/claude-plugins
```

Depois **só o que precisas**:

```
/plugin install ops@v2h
```

```
/plugin install design@v2h
```

```
/plugin install chatbot@v2h
```

```
/plugin install replica@v2h
```

Confirma o âmbito com Enter, corre `/reload-plugins`, e está. Não é preciso clonar
nada nem copiar ficheiros. As atualizações chegam sozinhas.

---

## `ops` — para quem constrói e mantém

| Comando | Quando |
|---|---|
| `/ops:recon` | **Antes de avançar.** Revisão de um PR ou do diff local |
| `/ops:sniper` | **Durante.** Alterar um sistema que tem gente a usá-lo agora |
| `/ops:isolate` | **Quando alguma coisa partiu.** Descobrir a camada culpada antes de abrir um ficheiro |
| `/ops:triage` | **Quando o projeto está lento de mexer.** Dívida técnica ordenada |
| `/ops:doctrine` | **Depois de uma decisão grande.** O ADR que evita rediscutir daqui a meses |

**O `recon` não é mais um "revê este código".** Oito agentes procuram em paralelo —
regras do projeto, bugs, histórico do git, comentários de PRs antigos, falhas
silenciosas, RLS e migrações, configuração de produção. Depois, **um agente por
achado tenta deitá-lo abaixo** e dá-lhe uma nota de 0 a 100. Só passa acima de 80.

É o passo que falta na maior parte das revisões automáticas: elas encontram, mas não
duvidam. Vinte observações plausíveis valem menos que três confirmadas — a partir da
terceira falsa, quem lê passa a ignorar todas.

**O `isolate` começa por perguntar se há mesmo avaria.** Ausência de atividade não é
sintoma: "não entraram mensagens hoje" só é problema depois de se saber que devia ter
havido tráfego. Depois corta o percurso ao meio em vez de o seguir por ordem, e obriga
a guardar a prova antes de mexer — porque a primeira alteração apaga-a, e há painéis
onde se escreve a configuração e não se consegue voltar a lê-la.

**O `triage` faz a pergunta que ninguém faz:** *quando é que isto custou tempo a
alguém nos últimos seis meses — commit, incidente ou entrega atrasada?* Sem resposta,
o achado é arrumado como **"fica, não tocar"**. Código feio que funciona e não
bloqueia nada não é dívida, é código feio.

---

## `design` — para quem desenha

| Comando | Quando |
|---|---|
| `/design:research` | Transformar entrevistas e testes em achados com evidência |
| `/design:critique` | Crítica de um ecrã, ordenada por quanto atrapalha quem usa |
| `/design:copy` | O texto: botões, erros, estados vazios, confirmações |
| `/design:accessibility` | Auditoria WCAG feita por tarefa, não por checklist |
| `/design:handoff` | Passar para o dev sem ele ter de adivinhar |
| `/design:taste` | Landing pages, lojas e portfólios que não pareçam template — e que vendam |

**A `critique` separa o dano do gosto.** Três colunas: *bloqueia*, *atrasa* e
*preferência* — e a última fica marcada como tal, **sem peso nenhum**. É essa
honestidade que faz as outras duas serem levadas a sério.

**A `research` nunca mistura três coisas de peso diferente:** o que a pessoa **disse**
(opinião), o que a pessoa **fez** (observação) e o que **tu concluíste**
(interpretação). Quando aparecem no mesmo parágrafo, a interpretação ganha peso de
facto — e alguém constrói uma funcionalidade em cima disso. Um padrão só é padrão com
três sessões independentes.

**O `handoff` lê o design system antes de especificar.** Um handoff que ignora o que
já existe cria o sétimo botão do produto. E traz a secção que falta em quase todos —
*o que acontece quando a lista está vazia, quando o pedido falha a meio, quando a
pessoa não tem permissão*.

**A `taste` lê o brief antes de tocar em código.** Primeiro declara a leitura — *que
tipo de página, para que audiência, com que linguagem visual* — e só depois gera. É o
antídoto para o default de IA: gradiente roxo, herói centrado sobre mesh escuro, três
cartões iguais. Adaptada de [taste-skill](https://github.com/Leonxlnx/taste-skill)
(Leonxlnx, MIT), a skill de frontend mais instalada do skills.sh.

**Em páginas de venda, a `taste` muda de juiz.** A camada V2H fixa o piso de conversão
que os 19.000+ testes do Baymard confirmaram — proposta de valor acima da dobra, envio
visível na página do produto, checkout em ≤ 3 passos, LCP < 2,5s — e a regra de
arbitragem: *quando gosto e conversão conflituam, conversão ganha*. As referências
estão separadas pela intenção: quem converte (Allbirds, Brooklinen), quem tem o melhor
UX medido (Nike, Zalando, Glossier) e quem ganha prémios (Apple, Scout Motors) — e a
skill sabe que a terceira lista nunca justifica quebrar as duas primeiras.

---

## `chatbot` — construir a tua própria plataforma de conversas

O que o ManyChat faz, mas teu: a tua base de dados, os teus fluxos, sem mensalidade
por contacto.

Este é diferente dos outros — **é uma sequência**, não uma caixa de ferramentas.

| Comando | O que constrói |
|---|---|
| `/chatbot:start` | O plano, e o corte de âmbito que decide se o projeto acaba |
| `/chatbot:schema` | O modelo de dados: identidade do contacto e isolamento, à primeira |
| `/chatbot:channel` | O canal a sério — alguém escreve do telemóvel, aparece na tua tabela |
| `/chatbot:engine` | O motor: condições, esperas, respostas guardadas, passar a humano |
| `/chatbot:builder` | O ecrã onde uma pessoa sem código monta fluxos, e a caixa de entrada |
| `/chatbot:dispatch` | Campanhas, com opt-out e travões contra banimento |
| `/chatbot:launch` | Pôr no ar, e saber que partiu antes do cliente ligar |

**A ordem é a parte importante.** Quem desiste destes projetos desiste sempre no mesmo
sítio: a construir o editor visual de fluxos na primeira semana, antes de uma única
mensagem real ter entrado no sistema. Por isso o construtor é o quinto passo.

E os travões do `dispatch` não são zelo a mais. Um envio mal feito não dá erro — dá um
número banido e um cliente sem canal de vendas na segunda-feira de manhã.

---

## `replica` — clonar um app e torná-lo teu

Reconstrói o que um app **faz**, nunca o que é **dele**: as funcionalidades e os
fluxos, escritos de raiz. Nem o código, nem o logótipo, nem o texto, nem o conteúdo.

Tal como o `chatbot`, **é uma sequência**. Cada passo escreve numa pasta `replica/` do
projeto, e o seguinte lê dali.

| Comando | O que faz |
|---|---|
| `/replica:recon` | Mapeia o original: ecrãs, fluxos, componentes, modelo de dados, matriz de funcionalidades |
| `/replica:architect` | Stack, schema e API do clone, e a ordem de construção |
| `/replica:design` | O sistema de design em tokens, com assets teus e contraste verificado |
| `/replica:build` | O clone, ecrã a ecrã, com todos os estados |
| `/replica:backend` | Auth, base de dados, pagamentos e integrações por APIs oficiais |
| `/replica:test` | Plano de testes, Playwright e bugs com severidade |
| `/replica:diff` | Quão perto está do original, em número, e o que falta |
| `/replica:entrepreneur` | O que os utilizadores do original detestam, cada citação com o link da fonte |
| `/replica:brand` | Nome, paleta e voz próprios, e a varredura que apanha restos do original |
| `/replica:launch` | Landing page, preços e ficha das lojas |
| `/replica:deploy` | No ar, no teu domínio, só depois do pré-voo passar |

**Uma cópia direta não tem razão para existir.** O passo que faz o clone valer dinheiro
é o `entrepreneur`: lê as reviews reais do original e transforma as queixas em
correções e num ângulo de venda. E o `deploy` não avança enquanto a varredura do
`brand` encontrar o nome, o domínio ou as cores do original no código.

**Lê a internet sem lhe obedecer.** O `recon` e o `entrepreneur` põem dentro da sessão
texto escrito por desconhecidos — páginas, reviews, comentários do Reddit. A camada V2H
trata esse texto como dado, nunca como instrução, e pede para correr sem conectores de
email ou Drive ligados.

Adaptado de [replica-skill](https://github.com/Jakeschincariol/replica-skill) (Jake
Schincariol, MIT) e **fixado num commit auditado**: as mudanças do original só chegam
cá depois de alguém ler o diff. Ver [UPSTREAM.md](plugins/replica/UPSTREAM.md).

---

## Como isto funciona

Não é preciso decorar comandos. Cada skill carrega-se sozinha quando o pedido bate com
a descrição: escreves *"revê este PR"* e vem o `recon`; *"isto está em produção"* e vem
o `sniper`; *"o que achas deste ecrã"* e vem a `critique`; *"ligar o WhatsApp"* e vem o
`channel`.

Escrever o comando é só a forma explícita de o chamar.

Todas as skills terminam da mesma maneira: uma lista de verificação em que **cada
resposta "não" significa que ainda não está feito**. É o que impede uma entrega
confiante de uma coisa que ninguém confirmou.

---

## Atualizações

Chegam sozinhas, em segundo plano. Para forçar na hora:

```
/plugin marketplace update v2h
```

---

## Contribuir e manter

Regras de nomes, arquitetura do catálogo e o que nunca mexer estão em
[MANUTENCAO.md](MANUTENCAO.md). O histórico de mudanças está em
[CHANGELOG.md](CHANGELOG.md).

Apanhaste um erro que uma regra nova teria evitado? Abre uma issue. As melhores regras
nascem sempre de algo que correu mal a sério — não de teoria.

---

## Licença

**Podes usar. Não podes redistribuir.**

Instala, usa no teu trabalho e no dos teus clientes — incluindo trabalho pago — e
adapta a tua cópia à vontade. O que não podes é republicar isto noutro repositório ou
marketplace, partilhar versões alteradas, vender, ou incluir em algo vendido.

Queres distribuir? Pede: **vitor@v2h.com.br**

Detalhe completo em [LICENSE](LICENSE).

A exceção é o conteúdo adaptado de projetos MIT, que mantém a licença de origem:
o plugin `replica` ([LICENSE](plugins/replica/LICENSE)) e a base da `design:taste`.

**Autor:** Vitor Hugo Herbst — [V2H](https://v2h.com.br)
