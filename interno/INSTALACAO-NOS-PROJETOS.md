# Instalação automática nos projetos

Em vez de pedires a cada pessoa para correr os dois comandos, podes deixar o
convite dentro de cada projeto. Quem abrir o projeto e confiar na pasta é
convidado a instalar — carrega em sim e acabou.

## O que colar

No ficheiro `.claude/settings.json` de **cada projeto** (`bigone-ops-hub`,
`klc-bigone`, `nexxorhub`, `cr-clinic`, `febracised`, `galp-galen`…):

```json
{
  "extraKnownMarketplaces": {
    "v2h": {
      "source": {
        "source": "github",
        "repo": "VHHerbst/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "ops@v2h": true
  }
}
```

> Se o projeto **já tiver** um `.claude/settings.json`, não substituas o ficheiro —
> junta só estas duas chaves ao objeto que já lá está.

> Se o projeto ainda tiver `"protocolo-sniper@v2h": true`, **substitui essa linha
> por `"ops@v2h": true`**. O plugin antigo já não existe no catálogo, e deixado ali
> dá `plugin-not-found` a quem abrir o projeto.

Commita o ficheiro. Uma vez por projeto, para sempre.

## Ordem recomendada

1. Faz push deste repositório.
2. **Testa primeiro na tua máquina** — instala e confirma que a skill carrega.
3. Só depois commita o `settings.json` nos projetos da equipa.

Nunca distribuas antes do passo 2. É o próprio protocolo a aplicar-se a si mesmo:
verificar na ground truth antes de dar por feito.
