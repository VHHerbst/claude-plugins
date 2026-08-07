# Mensagem para a equipa

> **Envia só depois de teres instalado e testado tu primeiro.**
> Atualizado a 2026-08-06, para o catálogo com `ops`, `design` e `chatbot`.

---

Pessoal, novidade para quem trabalha com o Claude Code.

Juntei num sítio só a forma como trabalhamos: ler o código antes de mexer, confirmar
o resultado no ecrã final e não num "correu bem", e nunca dar por feito o que não foi
verificado. A partir de agora o Claude passa a seguir isso sozinho.

**O que precisam de fazer (uma vez só):**

Abrem o Claude Code e colam isto, uma linha de cada vez:

```
/plugin marketplace add VHHerbst/claude-plugins
```

```
/plugin install ops@v2h
```

E, se trabalham com ecrãs e desenho:

```
/plugin install design@v2h
```

Depois `/reload-plugins` e está.

**O que ganham com isto**

- Escrevem *"revê este PR"* e ele faz uma revisão a sério — procura por oito ângulos
  diferentes e depois **tenta deitar abaixo cada coisa que encontrou**. Só vos mostra
  o que sobreviveu. Menos ruído, e o que aparece é para levar a sério.
- Escrevem *"isto está em produção"* e ele passa a trabalhar em modo cuidadoso, sem
  ser preciso relembrar as regras de cada vez.
- Quem desenha tem *"o que achas deste ecrã"*, *"faz o handoff para o dev"* e a
  auditoria de acessibilidade.

**O Protocolo Sniper continua lá**, com as mesmas regras — agora chama-se
**`/ops:sniper`** e vem dentro do plugin `ops`, ao lado dos outros três.

**As atualizações chegam sozinhas.** Quando eu melhorar alguma coisa, aparece no
vosso Claude Code sem fazerem nada.

Se alguma coisa não funcionar, digam — é para isso que estamos a testar antes de pôr
isto à frente de mais gente.
