# Aplikace v Pythonu (`app.py` a `requirements.txt`)

## Jádro aplikace: `app.py`

### Co to je?
V tomto souboru se většinou nachází celá backendová logika aplikace psaná v Pythonu, konkrétně s využitím frameworku Flask. Tady sídlí ten "hlavní mozek".

### Jak to funguje?
Najdeš v něm:
- **Routy (Cesty)**: Kód určuje, co se má stát, když uživatel přijde na stránku `/` (hlavní stránka), nebo co se stane při odeslání dat přes `/generate` formulář.
- **Logiku AI Omluvenkáře**: Samotné volání na API modely. Program vezme data z tvého požadavku, pošle je někam (OpenAI nebo tvá školní lokální instance) a zpracuje vrácený text ("Zde je omluvenka...").
- **Napojení na databázi**: Pokud aplikace historii omluvenek někam ukládá, kód odtud komunikuje i s databází (klidně až přes SQL příkazy). Přečte historii nebo zapíše nově vygenerovaný text.

Nakonec script vždycky vezme výsledek a „pošle“ ho HTML šabloně (`render_template`), aby se to člověku pěkně zobrazilo v prohlížeči.

---

## Závislosti: `requirements.txt`

### Co to je?
Soubor `requirements.txt` obsahuje pouhý seznam jmen Python knihoven (např. `Flask==3.0.0`, `requests`, `openai`), které musí být nainstalované pro to, aby `app.py` vůbec mohl běžet.

### Jak to funguje?
Když přijdeš k novému počítači, místo abys tam ručně dohledával a instaloval všechny potřebné pomůcky příkazem po příkazu, zkrátka jen zavoláš:
`pip install -r requirements.txt` (Případně to za tebe zavolá Docker uvnitř tvého kontejneru).
A automaticky se ti stáhnou přesně ty správné verze podpůrných balíčků.
