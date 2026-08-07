# Manutenção do catálogo

Notas para quem mexe neste repositório. Quem só quer usar os plugins, o sítio é o
[README](README.md).

---

## Um plugin por caixa de ferramentas, nunca um plugin para tudo

Instalar é escolher. Se meteres engenharia e design no mesmo plugin, o designer leva
o `sniper` à boleia e o programador leva o `handoff` — e ninguém percebe o que é para
si. **Um plugin serve uma pessoa a fazer um tipo de trabalho.**

Há duas famílias, e a diferença decide onde uma skill nova deve ir:

- **Disciplinas** (`ops`, `design`) — uma forma de trabalhar que serve em qualquer
  projeto e nunca acaba. As skills disparam sozinhas pela descrição.
- **Construções** (`chatbot`) — constroem uma coisa específica, do princípio ao fim, e
  consomem-se quando terminam. São uma sequência, e precisam de saber em que passo vais
  — coisa que uma skill, sozinha, não sabe. Por isso escrevem o estado num ficheiro do
  projeto, e confirmam sempre no sistema real em vez de acreditarem nele.

Quando uma construção repetir a segunda vez o trabalho de outra, **aí** é que se extrai
a disciplina comum. Nunca antes: abstrair no primeiro caso é adivinhar a partir de um
exemplo só. Foi por isso que o `comms` não foi criado quando o `chatbot` nasceu.

## Arquitetura de nomes

A invocação é sempre `/<plugin>:<skill>`, portanto **o nome do plugin aparece em todas
as chamadas, para sempre**. Três regras:

1. **O namespace é uma disciplina, não a marca.** A marca já está no `@v2h` do install.
   `/v2h:isto` e `/v2h:aquilo` não diz a ninguém o que cada comando faz.
2. **A skill nomeia a operação.** No `ops`, em codinome de campo — `recon`, `sniper`,
   `triage`, `doctrine` — porque cada um descreve com precisão uma função real:
   reconhecimento é ir ver antes de avançar, triagem é priorizar sob fogo, doutrina é a
   decisão escrita para quem chega depois. **Onde a metáfora deixar de ser precisa,
   ganha o nome claro** — foi o que aconteceu no `design`. Nome giro que não se entende
   é pior que nome banal.
3. **O namespace nunca se repete na skill.** `/protocolo-sniper:protocolo-sniper` foi o
   erro que deu origem a esta secção: nasce de criar o plugin à volta de uma skill em
   vez de à volta de uma disciplina.

Se o catálogo crescer para outras áreas, cresce na mesma língua onde ela servir: **QG
decide, Intel informa, Ops executa** — `/hq:briefing`, `/intel:sitrep`,
`/ops:debrief`.

## Porque é que não há campo `version`

Os `plugin.json` **não têm** campo `version`, e isso é intencional. Em marketplaces
alojados no git, quando o `version` é omitido cada commit conta como versão nova — e a
atualização chega sozinha a toda a gente.

> **Se acrescentares `"version": "1.0.0"` e não fizeres bump em cada release, os teus
> pushes deixam de chegar a quem já tem o plugin instalado.** O Claude Code vê a mesma
> versão e mantém a cópia em cache. É a armadilha clássica — não mexas neste ponto.

## Porquê repositório público

Na atualização automática em segundo plano, o Claude Code corre o `git pull` com os
credential helpers desativados. Em repositório **privado sobre HTTPS** esse pull falha,
e as pessoas ficam com versões antigas sem darem por isso. Sobre SSH funciona.

Como nada disto tem segredos, público é o caminho seguro.

## Campos do `marketplace.json` e versões do Claude Code

Testado no 2.1.132:

| Campo | Estado |
|---|---|
| `category`, `tags`, `homepage` | funcionam |
| `displayName` | **rejeitado** — exige ≥ 2.1.143 |
| `renames` | **rejeitado** — exige ≥ 2.1.193 |

Isto não é só um aviso de validação: se o carregador em runtime usar o mesmo schema
estrito, publicar um campo desconhecido pode **partir o marketplace inteiro** para quem
não atualizou — não só a funcionalidade nova.

### Renomear um plugin

O bloco top-level `renames` migra automaticamente quem tinha o nome antigo:

```json
"renames": { "nome-antigo": "nome-novo", "plugin-removido": null }
```

Enquanto houver gente abaixo do 2.1.193, **não uses o campo**. Em vez disso, deixa o
nome antigo no catálogo como **plugin de redirecionamento**: um `plugin.json` com o
nome velho e uma única skill que diz para onde ir e como mudar. Funciona em todas as
versões.

Mesmo com `renames` a funcionar, um marketplace com source `github` dá
`plugin-cache-miss` depois do rename — a pessoa corre `/plugin install` uma vez de
qualquer maneira. O `renames` evita o erro feio, não evita o passo manual.

Quando toda a gente estiver acima do 2.1.193, trata o `renames` como **histórico
append-only**: nunca edites uma entrada antiga, acrescenta outra.

## Adicionar um plugin novo

1. Cria `plugins/<nome>/` com `.claude-plugin/plugin.json` (**sem `version`**) e as
   skills em `skills/<skill>/SKILL.md`.
2. Acrescenta a entrada ao array `plugins` em `.claude-plugin/marketplace.json`.
3. Corre a validação:
   ```bash
   claude plugin validate .
   ```
4. **Testa a partir do GitHub, não do disco.** O marketplace é lido do remoto — só
   depois do push é que dá para instalar e ver se carrega mesmo.
5. Commit e push. Chega a toda a gente sozinho.

## Como se escreve uma skill deste catálogo

O que faz estas skills diferentes de uma lista de boas práticas:

- **Abrem com o princípio, não com o processo.** A primeira coisa que se lê é *porque*
  é que este trabalho falha, e só depois *como* se faz.
- **Ordenam por dano a quem usa**, com o gosto pessoal numa secção à parte e sem peso.
- **Exigem evidência.** Um achado sem prova apontada é rebaixado, não reportado.
- **Fecham com uma lista de verificação** em que cada "não" significa que ainda não
  está feito.
- **Ligam-se umas às outras** no fim: o que sai de uma diz para onde vai a seguir.

E a regra que atravessa tudo: **verificar na ground truth, nunca num sinal
intermédio**. Um `200 OK` não é prova; a linha na tabela é.
