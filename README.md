# Plugins V2H para Claude Code

Catálogo interno de plugins da equipa. O que está aqui é a **fonte da verdade** —
não copies o conteúdo para outros repositórios, instala a partir daqui.

## Instalar (uma vez por pessoa)

Dentro do Claude Code, em qualquer projeto:

```
/plugin marketplace add VHHerbst/claude-plugins
```

Depois instala **só o que precisas**:

```
/plugin install ops@v2h
```

```
/plugin install design@v2h
```

```
/plugin install chatbot@v2h
```

Aparece um ecrã a pedir o âmbito da instalação — confirma com Enter. Depois:

```
/reload-plugins
```

E está. Não é preciso clonar nada nem copiar ficheiros.

## Os comandos

### `ops` — engenharia

Cada comando é um momento diferente do trabalho.

| Comando | Quando |
|---|---|
| `/ops:recon` | **Antes de avançar.** Revisão de um PR ou do diff local. Diz o que está mal e se bloqueia publicação |
| `/ops:sniper` | **Durante.** Modo de trabalho para alterar um sistema que tem utilizadores a usá-lo agora |
| `/ops:triage` | **Quando o projeto está lento de mexer.** Audita a base de código e ordena a dívida técnica por quanto custa de facto |
| `/ops:doctrine` | **Depois de uma decisão grande.** Escreve o ADR, com as alternativas rejeitadas e o gatilho que reabre a discussão |

### `design` — design e UX

| Comando | Quando |
|---|---|
| `/design:research` | **Antes de desenhar.** Transforma entrevistas e testes em achados, separando o que foi dito do que foi observado |
| `/design:critique` | **Com o desenho feito.** Crítica ordenada por quanto atrapalha quem usa — e as preferências marcadas como tal |
| `/design:copy` | **O texto do ecrã.** Botões, erros, estados vazios, confirmações |
| `/design:accessibility` | **Antes de entregar.** Auditoria WCAG feita por tarefa, não por checklist |
| `/design:handoff` | **Para o dev.** Estados, casos limite e o que reutilizar do design system |

### `chatbot` — construir a tua plataforma de conversas

Este é diferente dos outros: **é uma sequência**, não uma caixa de ferramentas. Corre
pela ordem, do princípio ao fim.

| Comando | O que constrói |
|---|---|
| `/chatbot:start` | O plano. Corta o âmbito antes de haver código — é o que decide se o projeto acaba |
| `/chatbot:schema` | O modelo de dados. Identidade do contacto e isolamento entre clientes, à primeira |
| `/chatbot:channel` | O canal a sério. Uma pessoa escreve do telemóvel e aparece na tua tabela |
| `/chatbot:engine` | O motor de fluxos: condições, esperas, recolha de respostas, passar para humano |
| `/chatbot:builder` | O ecrã onde uma pessoa sem código monta os fluxos, e a caixa de entrada |
| `/chatbot:dispatch` | Campanhas — com opt-out, ritmo e travões contra banimento |
| `/chatbot:launch` | Pôr no ar e saber que partiu **antes** do cliente ligar |

Não é preciso decorar nada. Cada skill carrega-se sozinha quando o pedido bate com a
descrição — "revê este PR" chama o `recon`, "isto está em produção" chama o
`sniper`, "o que achas deste ecrã" chama a `critique`, "ligar o WhatsApp" chama o
`channel`.

## Atualizações

**Não é preciso fazer nada.** Quando algo é atualizado neste repositório, o Claude
Code de cada pessoa vai buscar a versão nova em segundo plano.

Para forçar a atualização na hora:

```
/plugin marketplace update v2h
```

---

## Plugins disponíveis

Cada plugin é uma caixa de ferramentas própria. **Instala só os que fazem sentido
para o teu trabalho** — o designer não precisa do `sniper`, o programador não precisa
do `handoff`.

| Plugin | Para quem | O que traz |
|---|---|---|
| `ops` | quem constrói e mantém sites e apps | `recon`, `sniper`, `triage`, `doctrine` |
| `design` | quem desenha ecrãs e fluxos | `research`, `critique`, `copy`, `accessibility`, `handoff` |
| `chatbot` | quem quer a sua própria plataforma de automação de conversas | `start`, `schema`, `channel`, `engine`, `builder`, `dispatch`, `launch` |
| `protocolo-sniper` | — | **Descontinuado.** Redireciona para `ops@v2h`. Será removido |

### Vieste do `protocolo-sniper`?

As regras não mudaram, mudou o sítio: agora é `/ops:sniper`. Uma vez só:

```
/plugin install ops@v2h
```

```
/plugin uninstall protocolo-sniper@v2h
```

---

## Notas de manutenção (para o Vitor)

### Um plugin por caixa de ferramentas, nunca um plugin para tudo

Instalar é escolher. Se meteres engenharia e design no mesmo plugin, o designer leva
o `sniper` à boleia e o programador leva o `handoff` — e ninguém percebe o que é
para si. **Um plugin serve uma pessoa a fazer um tipo de trabalho.**

Há duas famílias, e a diferença entre elas decide onde uma skill nova deve ir:

- **Disciplinas** (`ops`, `design`) — uma forma de trabalhar que serve em qualquer
  projeto e nunca acaba. As skills disparam sozinhas pela descrição.
- **Construções** (produtos guiados) — constroem uma coisa específica, do princípio
  ao fim, e consomem-se quando terminam. São uma sequência, e precisam de saber em
  que passo vais — coisa que uma skill, sozinha, não sabe.

Quando uma construção repetir a segunda vez o mesmo trabalho de outra, **aí** é que
se extrai a disciplina comum. Nunca antes: abstrair no primeiro caso é adivinhar a
partir de um exemplo só.

### Arquitetura de nomes

A invocação é sempre `/<plugin>:<skill>`, portanto **o nome do plugin aparece em
todas as chamadas, para sempre**. Três regras:

1. **O namespace é uma disciplina, não a marca.** A marca já está no `@v2h` do
   install. `/v2h:isto` e `/v2h:aquilo` não diz a ninguém o que cada comando faz.
2. **A skill nomeia a operação**, em codinome de campo: `recon`, `sniper`,
   `triage`, `doctrine`. A metáfora só funciona se for um mundo inteiro — se um dia
   um comando não couber na linguagem militar, é sinal de que pertence a outro
   namespace.
3. **O namespace nunca se repete na skill.** `/protocolo-sniper:protocolo-sniper`
   foi o erro que deu origem a esta secção: nasce de criar o plugin à volta de uma
   skill em vez de à volta de uma disciplina.

Quando o catálogo crescer, cresce na mesma língua: **QG decide, Intel informa, Ops
executa** — `/hq:briefing` para especificação, `/intel:sitrep` para estado do
projeto, `/ops:debrief` para o comunicado à equipa.

### Porque é que não há campo `version`

Os `plugin.json` **não têm** campo `version`, e isso é intencional. Em marketplaces
alojados no git, quando o `version` é omitido cada commit conta como versão nova — e
a atualização chega sozinha a toda a gente.

> **Se acrescentares `"version": "1.0.0"` e não fizeres bump em cada release,
> os teus pushes deixam de chegar a quem já tem o plugin instalado.** O Claude Code
> vê a mesma versão e mantém a cópia em cache. É a armadilha clássica — não mexas
> neste ponto.

### Porquê repositório público

Na atualização automática em segundo plano, o Claude Code corre o `git pull` com
os credential helpers desativados. Em repositório **privado sobre HTTPS** esse pull
falha, e as pessoas ficam com versões antigas sem darem por isso. Sobre SSH
funciona.

Como nada disto tem segredos, público é o caminho seguro.

### Renomear plugins: `renames` só a partir do 2.1.193

O `marketplace.json` suporta um bloco top-level `renames` que migra automaticamente
quem tinha o nome antigo:

```json
"renames": { "nome-antigo": "nome-novo", "plugin-removido": null }
```

**Mas exige Claude Code ≥ 2.1.193**, e o `claude plugin validate` de versões
anteriores rejeita o campo com `Unrecognized key`. Enquanto houver gente em versões
antigas, um plugin renomeado fica no catálogo como **redirecionamento** — um
`plugin.json` com o nome antigo e uma skill que só diz para onde ir. Foi o que se
fez com o `protocolo-sniper`.

Mesmo com `renames` a funcionar, um marketplace com source `github` dá
`plugin-cache-miss` depois do rename: a pessoa tem de correr `/plugin install` uma
vez de qualquer maneira. O `renames` evita o erro feio, não evita o passo manual.

O campo `displayName` (nome bonito na UI sem afetar o namespace) tem o mesmo
problema — exige ≥ 2.1.143.

Quando toda a gente estiver acima do 2.1.193, adota os dois e trata o `renames` como
**histórico append-only**: nunca edites uma entrada antiga, acrescenta outra.

### Adicionar um plugin novo

1. Cria `plugins/<nome>/` com `.claude-plugin/plugin.json` (sem `version`) e as
   skills em `skills/<skill>/SKILL.md`.
2. Acrescenta a entrada ao array `plugins` em `.claude-plugin/marketplace.json`.
3. Corre `claude plugin validate .`
4. Commit e push. Chega a toda a gente sozinho.
