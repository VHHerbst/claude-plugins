# Anexo — plataformas

Lê isto quando a mudança for **N3** (infraestrutura, integrações, deploys) ou quando
precisares de saber qual é o botão que põe uma coisa no ar.

---

## Qual é o passo de ativação

Push, save e merge não ativam nada em lado nenhum. Antes de dares por feito, descobre
qual é o passo desta plataforma e diz na entrega **quem o carrega**.

- **Lovable** — o **Publish**. Enquanto ninguém carregar, o que está no GitHub não
  existe para os utilizadores.
- **n8n** — **Publicar**. Guardar cria um rascunho e a versão antiga continua a
  atender. Confirma que a versão ativa é a nova.
- **Edge Functions self-hosted** — não há deploy automático nenhum. O ficheiro tem de
  ir parar ao contentor.
- **Migrações SQL** — alguém corre o SQL à mão. Ver a camada C do protocolo.

## O que está no ar pode sair do ar sem ninguém tocar no código

O que vive só na camada de escrita de um contentor — ficheiros copiados à mão,
credenciais escritas com `sed` — não é um deploy. É uma configuração à espera de
desaparecer: basta a infraestrutura recriar o serviço.

Num painel gerido (Easypanel e parecidos), **"Reiniciar" é seguro, "Implantar" recria e
apaga.** Antes de carregar no segundo, confirma que tudo o que o serviço precisa vem de
uma fonte que sobrevive à recriação — imagem, variáveis de ambiente, volume — e não da
tua última sessão de terminal.

## Nunca escrevas direto no destino

Um `>` ou um `sed -i` sobre um ficheiro que está bom destrói-o quando o passo anterior
falha. Basta um download falhado para a mensagem de erro ficar por cima de um webhook
em produção.

Escreve num sítio temporário e move só em caso de sucesso.

## Painéis mentem

"Está configurado no painel" não é prova: há plataformas onde o que defines na
interface nunca chega ao processo. A prova é um caminho que **usa** a definição e
devolve resposta observável — ver o núcleo, regra 4.
