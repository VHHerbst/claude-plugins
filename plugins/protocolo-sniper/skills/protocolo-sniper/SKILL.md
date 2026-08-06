---
name: protocolo-sniper
description: Aviso de mudança de nome. O Protocolo Sniper passou a viver no plugin ops, como /ops:sniper. Esta skill existe só para redirecionar quem ainda tem o plugin antigo instalado, e será removida.
---

# O Protocolo Sniper mudou de casa

As regras não mudaram. O sítio mudou.

O protocolo passou a fazer parte do plugin **`ops`**, ao lado do recon, da triage e
da doctrine, e chama-se agora:

```
/ops:sniper
```

## O que fazer, uma vez

```
/plugin marketplace update v2h
```

```
/plugin install ops@v2h
```

```
/plugin uninstall protocolo-sniper@v2h
```

E depois `/reload-plugins`.

## Enquanto não fizeres isso

**Não uses as regras a partir daqui — este ficheiro já não as tem.** Carrega o
`/ops:sniper` e lê as regras de lá, que é a versão que continua a ser atualizada.

Se estiveres a meio de trabalho num sistema em produção e não puderes parar para
reinstalar: o protocolo continua a ser o mesmo, e está em
`plugins/ops/skills/sniper/SKILL.md` no repositório `VHHerbst/claude-plugins`.
