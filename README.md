# Plugins V2H para Claude Code

Catálogo interno de plugins da equipa. O que está aqui é a **fonte da verdade** —
não copies o conteúdo para outros repositórios, instala a partir daqui.

## Instalar (uma vez por pessoa)

Dentro do Claude Code, em qualquer projeto:

```
/plugin marketplace add VHHerbst/claude-plugins
```

```
/plugin install ops@v2h
```

Aparece um ecrã a pedir o âmbito da instalação — confirma com Enter. Depois:

```
/reload-plugins
```

E está. Não é preciso clonar nada nem copiar ficheiros.

## Os comandos

O plugin `ops` são **operações**: cada comando é um momento diferente do trabalho.

| Comando | Quando |
|---|---|
| `/ops:recon` | **Antes de avançar.** Revisão de um PR ou do diff local. Diz o que está mal e se bloqueia publicação |
| `/ops:sniper` | **Durante.** Modo de trabalho para alterar um sistema que tem utilizadores a usá-lo agora |
| `/ops:triage` | **Quando o projeto está lento de mexer.** Audita a base de código e ordena a dívida técnica por quanto custa de facto |
| `/ops:doctrine` | **Depois de uma decisão grande.** Escreve o ADR, com as alternativas rejeitadas e o gatilho que reabre a discussão |

Não é preciso decorar. Cada skill carrega-se sozinha quando o pedido bate com a
descrição — "revê este PR" chama o `recon`, "isto está em produção" chama o
`sniper`, "o que devíamos refatorar" chama a `triage`, "documenta esta decisão"
chama a `doctrine`.

## Atualizações

**Não é preciso fazer nada.** Quando algo é atualizado neste repositório, o Claude
Code de cada pessoa vai buscar a versão nova em segundo plano.

Para forçar a atualização na hora:

```
/plugin marketplace update v2h
```

---

## Plugins disponíveis

| Plugin | O que faz |
|---|---|
| `ops` | Operações de engenharia: `recon`, `sniper`, `triage`, `doctrine` |
| `protocolo-sniper` | **Descontinuado.** Redireciona para `ops@v2h`. Será removido |

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
