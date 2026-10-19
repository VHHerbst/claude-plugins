---
name: deploy
description: >-
  Põe o clone no ar no domínio do utilizador: portão de pré-voo (testes
  verdes, must-haves feitos, varredura de rebrand limpa, ficha da loja
  verificada, páginas legais no ar), base de dados e variáveis de produção,
  alojamento, DNS do domínio e do email, Stripe em modo live, redirects de
  OAuth, monitorização e builds móveis para TestFlight e Play. Usa depois da
  /replica:launch, ou quando alguém num projeto com pasta replica/ pedir para
  publicar o clone. Nada vai para o ar sem o avanço explícito do utilizador.
---

# replica:deploy

> **[V2H] Onde estão as ferramentas.** Os scripts desta skill vivem na pasta dela
> (o *Base directory* que o Claude Code mostra ao carregá-la), não no projeto. Nos
> comandos abaixo, `python3 <script>.py` quer dizer `python3 <SKILL_DIR>/<script>.py`,
> com `<SKILL_DIR>` trocado por esse caminho absoluto. As ferramentas das outras skills
> do plugin estão nas pastas irmãs (`<SKILL_DIR>/../diff/parity.py`). Os comandos correm
> na raiz do projeto, por isso os caminhos `replica/...` ficam como estão.

Reads everything in `replica/`. Writes `replica/deploy.md` (the checklist in
`preflight.md` in this folder, filled in).

## The rules

- **Nothing goes live without the user's go.** Show the preflight results and
  ask.
- **The user buys and signs in.** Claude never buys a domain, enters a card,
  types a password or pastes a live key. Claude writes the exact DNS records,
  env var names and commands; the user does the account steps.
- **Not until it is rebranded.** The sweep must be clean. No exceptions.

## Step 1: preflight

Run every check and paste the results into `deploy.md`:

```bash
npx playwright test                                                  # replica:test
python3 <SKILL_DIR>/../diff/parity.py replica/features.csv          # must-haves done
python3 <SKILL_DIR>/../brand/sweep.py . --config replica/brand.json # exit 0: clean
python3 <SKILL_DIR>/../launch/listing.py replica/launch/listing.json # if shipping to stores
npm run build                                                        # production build passes
```

([V2H] `<SKILL_DIR>` é a pasta desta skill; as outras ferramentas estão nas
pastas irmãs, dentro do mesmo plugin.)

Plus by hand: no open S1 or S2 bugs, privacy policy and terms pages live
(listing every processor), cookie banner if you use non-essential cookies in
the EU or UK, account deletion works, the favicon, titles and OG image are
yours.

Any failure stops the deploy. Say which and why.

## Step 2: production services

- A **separate production project** for the database (never the dev one),
  backups on, migrations run by the deploy, not by hand.
- Env vars set in the host for production, matching `.env.example`. Live
  keys only here.
- **Stripe**: switch to live mode, recreate products and prices, add the
  production webhook endpoint and its signing secret, test one real
  purchase and refund it.
- **OAuth**: add the production domain to every provider's redirect URIs and
  authorised origins. Google scopes that need verification must be approved,
  or only test users can sign in.
- **Email**: the sending domain verified with the provider.

## Step 3: host and domain

Default: Vercel for Next.js (Netlify, Cloudflare Pages, Fly or Render
otherwise). Connect the repo so `main` deploys and pull requests get preview
URLs.

The domain, after the user buys it at any registrar:

| record | name | value |
| --- | --- | --- |
| A | @ | the host's apex IP (Vercel: shown in the domain settings) |
| CNAME | www | the host's target (Vercel: `cname.vercel-dns.com`) |
| TXT | @ or a subdomain | the host's verification value, if asked |

Email DNS from the email provider: SPF (TXT), DKIM (CNAME or TXT), and a
DMARC record starting at `v=DMARC1; p=none; rua=mailto:you@yourdomain` then
tightened to `quarantine` once reports are clean. Without these, your
confirmation emails go to spam.

Pick one canonical host (apex or www) and redirect the other. HTTPS is
automatic on the hosts above; check it.

## Step 4: watch it

Error tracking (Sentry or the host's), uptime checks on the home page and the
core flow's API, logs kept, analytics (a privacy-friendly one avoids the
cookie banner), and an alert to the user's email or phone. Then do the core
flow on the live site yourself, and ask the user to do it on their phone.

## Step 5: mobile, if there is an app

Expo: `eas build` then `eas submit` to TestFlight and Play internal testing.
Native: archive in Xcode, upload to App Store Connect; Gradle bundle to Play
Console. The user owns the developer accounts ($99 a year for Apple, $25 once
for Google). Beta first, then review with the listing from replica:launch.

## Output

`replica/deploy.md` with every check and its result, the live URL, the DNS
records set, and what to watch in the first week. The clone is now an app
with your name on it.

---

## Origem e licença

Adaptada de [replica-skill](https://github.com/Jakeschincariol/replica-skill), de
Jake Schincariol, sob licença MIT (ver `LICENSE` na raiz deste plugin), a partir do
commit `77c9436`, auditado a 06/10/2026. O corpo fica em inglês para não criar deriva
em relação ao original. O que está marcado **[V2H]** é acrescento da casa e preserva-se
ao sincronizar com o upstream. Procedimento em `UPSTREAM.md`, na raiz do plugin.
