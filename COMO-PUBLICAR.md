# Feed RSS "ao vivo" — Comunicação TRE-PE (do zero)

Desta vez, monte tudo **criando cada arquivo manualmente pelo site do
GitHub**, em vez de arrastar pastas. Isso evita o problema anterior
(a pasta `.github`, por começar com ponto, ficou oculta no seu
explorador de arquivos e não foi enviada).

## 0. Repositório novo

1. Apague o repositório antigo (opcional): **Configurações** do repo
   → role até o fim → **Delete this repository**
2. Crie um novo em https://github.com/new
   - Nome: `feed-comunicacao-tre-pe` (ou o que preferir)
   - Marque **Public**
   - Pode marcar "Add a README file" — não atrapalha

## 1. Criar cada arquivo

Em todos os casos: no repositório, clique **Add file → Create new file**,
cole o **nome do arquivo** (com o caminho completo — o GitHub cria as
pastas automaticamente ao digitar `/`), cole o **conteúdo** no editor,
e clique **Commit changes...** no fim da página.

Repita esse processo 5 vezes, um arquivo de cada vez:

---

### Arquivo 1 — `requirements.txt`
Nome exato: `requirements.txt`
Conteúdo: veja o arquivo `requirements.txt` deste pacote.

---

### Arquivo 2 — `scripts/gerar_feed_comunicacao.py`
Nome exato: `scripts/gerar_feed_comunicacao.py`
Conteúdo: veja o arquivo `scripts/gerar_feed_comunicacao.py` deste pacote.

---

### Arquivo 3 — `docs/comunicacao-tre-pe.xml`
Nome exato: `docs/comunicacao-tre-pe.xml`
Conteúdo: veja o arquivo `docs/comunicacao-tre-pe.xml` deste pacote.
(É só a versão inicial — o Action vai sobrescrever automaticamente.)

---

### Arquivo 4 — `docs/.nojekyll`
Nome exato: `docs/.nojekyll`
Conteúdo: deixe vazio (não precisa digitar nada, só criar o arquivo).

---

### Arquivo 5 — `.github/workflows/atualizar-feed.yml`
Nome exato: `.github/workflows/atualizar-feed.yml`

⚠️ Este é o mais importante — foi o que faltou da vez passada.
Digite o caminho completo com o `.github/` no início, exatamente
assim, letra por letra. O GitHub vai criar as duas pastas
(`.github` e `workflows`) sozinho.

Conteúdo: veja o arquivo `.github/workflows/atualizar-feed.yml`
deste pacote.

---

## 2. Conferir que a pasta `.github` existe

Depois de criar o Arquivo 5, volte para a página principal do
repositório (clique no nome dele) e confirme que aparece uma pasta
chamada `.github` na listagem. Se não aparecer, o commit do passo
anterior não foi salvo corretamente — repita.

## 3. Ativar permissão de escrita

**Configurações → Ações → Geral** → em "Permissões de fluxo de
trabalho", selecione **Read and write permissions** → Salvar.

## 4. Ativar o GitHub Pages

**Configurações → Pages** → em "Build and deployment" → Source:
**Deploy from a branch** → Branch: **main**, pasta: **/docs** → Salvar.

A URL pública do feed vai ser:
```
https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/comunicacao-tre-pe.xml
```

## 5. Rodar a primeira vez

Aba **Ações** → clique em "Atualizar feed RSS Comunicação TRE-PE"
(se esse workflow não aparecer na lista, volte ao passo 1/2 — a
pasta `.github` não foi criada direito) → **Run workflow**.

Depois de rodar com sucesso (ícone ✅ verde), ele passa a rodar
sozinho a cada 30 minutos.

## Uso na TV Corporativa

No artifact `rss-tv-corporativa.html`, troque:
```js
const RSS_URL = "https://www.tre-pe.jus.br/rss";
```
pela URL final do seu feed no GitHub Pages.
