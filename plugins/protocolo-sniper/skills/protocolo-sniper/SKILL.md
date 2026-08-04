---
name: protocolo-sniper
description: Modo de trabalho obrigatório para alterações em sistemas que já estão em produção com utilizadores reais. Usa quando o pedido envolver alterar código, RPCs, migrações SQL, fluxos ou ecrãs de um projeto em uso (bigone-ops-hub, klc-bigone, nexxorhub, cr-clinic, febracised, galp-galen…), ou quando alguém disser "protocolo sniper", "modo sniper", "sem erros" ou "isto está em produção".
---

# Protocolo Sniper

Trabalhamos em sistemas que a equipa está a usar **neste momento**. Um erro publicado
não é um bug — é uma venda atrasada, uma reunião perdida, um cliente à espera.
Não temos o luxo de tentar duas vezes.

Aplica as dez regras abaixo, todas, sem exceção.

---

## 1. Ler antes de escrever

Lê o corpo atual da RPC, do componente ou da policy **antes** de a alterares.
Nunca reproduzas de memória.

Confirma qual é a versão **mais recente** de uma função: pode haver hardening
posterior noutra migração que ainda não viste. A última migração que menciona a
função ganha — não a primeira que encontraste.

## 2. Migrações não são corridas por ti

Escreves o SQL **idempotente** e entregas. Quem tem acesso corre-o no Supabase
SQL Editor.

- Migrações de **enum** ficam num ficheiro isolado e correm **antes** das que as usam.
- Ficheiros de migração empurrados para o git **não correm sozinhos**. A Lovable
  não os aplica. Se ninguém correu o SQL à mão, a base de dados não mudou.

## 3. Commits cirúrgicos

`git add` **apenas** dos ficheiros que tocaste. **Nunca `git add -A`.**

Costuma haver outra sessão de Claude Code a trabalhar em paralelo no mesmo
working tree. Um `add -A` leva o trabalho de outra pessoa à boleia e ninguém
percebe até rebentar.

## 4. Trio verde antes de dar por feito

O CI corre em Node 20. Corre o mesmo localmente:

```bash
nvm use 20 && npx tsc --noEmit && TZ=UTC npx vitest run && npx vite build
```

O `TZ=UTC` dá paridade com o CI — sem ele, testes com datas passam na tua
máquina e falham lá.

## 5. Verificar na ground truth, nunca num sinal intermédio

Um `200 OK` não é prova. `ok: true` não é prova. Testes a passar não são prova.
`tsc` sem erros não é prova.

**Prova** é: o registo apareceu na tabela, o card mudou de coluna no ecrã, o
bundle servido em produção contém o código novo. Vai ver no sítio final.

Se não conseguires ver o resultado final, di-lo em vez de assumir.

## 6. Ordem de rollout pensada

- Estado/campo novo que ficaria **invisível ou partido** se chegasse antes do
  ecrã → **frontend primeiro, migração depois**.
- Mudança sem risco de invisibilidade → **migração primeiro, frontend depois**.

Decide a ordem *antes* de entregar, e escreve-a na entrega.

## 7. Código no GitHub não está live

Nos projetos Lovable, o deploy é o **Publish**. Enquanto ninguém carregar em
Publish, o que está no GitHub não existe para os utilizadores.

Diz isto explicitamente em cada entrega. Nunca deixes ninguém assumir que "está
no main" significa "está no ar".

## 8. Fechar cada bloco com resumo por-pessoa

Quem pediu tem de conseguir ler só a sua linha. Organiza por pessoa
(Diana / Nathalia / Wesley / Rita / Hélder…), e para cada pedido diz o estado:

- **feito e publicado**
- **feito, falta publicar**
- **feito, falta correr a migração**
- **em falta** — e porquê

Sem jargão técnico. A pessoa quer saber se já pode usar.

## 9. Superfície nova = checklist transversal

Sempre que acrescentas um passo ou estado a um fluxo, verifica **na mesma
entrega**:

- observações / notas
- histórico e auditoria
- labels e badges
- filtros e pesquisas
- permissões por papel
- documentação (`AGENTS.md`, `docs/features/`)

Um estado novo que não aparece nos filtros é um estado que ninguém encontra.

## 10. Não prometas o que não verificaste

Se ficou a meio, diz o que ficou e porquê. Se não conseguiste testar, diz que
não testaste.

Uma entrega honesta e incompleta custa uma hora. Uma entrega falsamente completa
custa um dia e a confiança da equipa.

---

## Antes de dizer "está feito", responde a isto

1. Li o código atual antes de o mudar?
2. O `git add` levou só os meus ficheiros?
3. O trio verde passou em Node 20?
4. Vi o resultado no sítio final, ou só num `200 OK`?
5. Disse claramente o que falta — publicar, migração, ou ambos?
6. O resumo está por pessoa, em linguagem que ela entende?

Se alguma resposta for "não", ainda não está feito.
