# Plugins V2H para Claude Code

Catálogo interno de plugins da equipa. O que está aqui é a **fonte da verdade** —
não copies o conteúdo para outros repositórios, instala a partir daqui.

## Instalar (uma vez por pessoa)

Dentro do Claude Code, em qualquer projeto:

```
/plugin marketplace add VHHerbst/claude-plugins
```

```
/plugin install protocolo-sniper@v2h
```

```
/plugin install engineering@v2h
```

Aparece um ecrã a pedir o âmbito da instalação — confirma com Enter. Depois:

```
/reload-plugins
```

E está. Não é preciso clonar nada nem copiar ficheiros.

## Usar

```
/protocolo-sniper:protocolo-sniper
```

Ou simplesmente escrever **"usa o protocolo sniper"** — o Claude reconhece pela
descrição e carrega as regras sozinho quando o trabalho é num sistema em produção.

```
/engineering:review
```

Aceita um número ou URL de pull request. Sem argumento, revê o PR da branch atual;
se não houver, revê o diff local. Também arranca sozinho com **"revê este PR"** ou
**"vê se isto tem bugs antes de publicar"**.

## Atualizações

**Não é preciso fazer nada.** Quando o protocolo é atualizado neste repositório,
o Claude Code de cada pessoa vai buscar a versão nova em segundo plano.

Para forçar a atualização na hora:

```
/plugin marketplace update v2h
```

---

## Plugins disponíveis

| Plugin | O que faz |
|---|---|
| `protocolo-sniper` | Modo de trabalho para alterações em sistemas com utilizadores reais: ler antes de escrever, verificar na ground truth, commits cirúrgicos, resumo por-pessoa |
| `engineering` | `/engineering:review` — revisão de código multi-agente. Encontra com 8 agentes em paralelo, duvida de cada achado com um score 0–100 e só reporta acima de 80. Inclui eixos nossos: RLS e migrações Supabase, env vars, mock em produção, docs por atualizar |

---

## Notas de manutenção (para o Vitor)

### Porque é que não há campo `version`

O `plugins/protocolo-sniper/.claude-plugin/plugin.json` **não tem** campo
`version`, e isso é intencional. Em marketplaces alojados no git, quando o
`version` é omitido cada commit conta como versão nova — e a atualização chega
sozinha a toda a gente.

> **Se acrescentares `"version": "1.0.0"` e não fizeres bump em cada release,
> os teus pushes deixam de chegar a quem já tem o plugin instalado.** O Claude Code
> vê a mesma versão e mantém a cópia em cache. É a armadilha clássica — não mexas
> neste ponto.

### Porquê repositório público

Na atualização automática em segundo plano, o Claude Code corre o `git pull` com
os credential helpers desativados. Em repositório **privado sobre HTTPS** esse pull
falha, e as pessoas ficam com versões antigas sem darem por isso. Sobre SSH
funciona.

Como o protocolo não tem segredos, público é o caminho seguro.

### Adicionar um plugin novo

1. Cria `plugins/<nome>/` com `.claude-plugin/plugin.json` (sem `version`) e as
   skills em `skills/<nome>/SKILL.md`.
2. Acrescenta a entrada ao array `plugins` em `.claude-plugin/marketplace.json`.
3. Commit e push. Chega a toda a gente sozinho.

### Nunca renomeies um plugin sem `renames`

O `name` de um plugin é o identificador estável — está no `enabledPlugins` de
cada pessoa. Se tiveres de mudar, acrescenta um bloco `renames` no
`marketplace.json` a mapear o nome antigo para o novo, senão toda a gente apanha
`plugin-not-found`.
