# Skryté konfigurační soubory: `.env` a `.gitignore`

## Prostředí v `.env` (Environment variables)

### Co to je?
`.env` je jednoduchý textový soubor obsahující skryté proměnné a tajná hesla pro tvou aplikaci. Slouží k bezpečné konfiguraci bez nutnosti zapisovat hesla přímo do zdrojového kódu (tzv. "hardcoding").

### Jak to funguje?
Najdeš v něm strukturu `KLÍČ=HODNOTA` (např. `OPENAI_API_KEY=sk-xxxx...`). 
Tvá aplikace (v Pythonu) si tyto proměnné umí při zapnutí načíst. Pokud bys dal heslo přímo do `app.py` a ten pak nahrál na veřejný GitHub, každý by ti to heslo mohl zneužít. Tady je to oddělené – samotný `.env` se z tvého počítače většinou nikam nenahrává.

---

## Ignorování souborů s `.gitignore`

### Co to je?
Je to soubor, který říká systému Git, které soubory a složky má **ignorovat** (aby je nahrával pryč do cloudu na GitHub). 

### Jak to funguje?
V souboru jen vyjmenuješ cesty k souborům (např. jméno `.env`, složku `__pycache__/` nebo `venv/`). Git dělá jakoby dané soubory vůbec neexistovaly. Tím se zajišťuje bezpečí (zabráníš nechtěnému nahrání hesel) i čistota v repository (neuploaduješ dočasné nebo obří záložní instalační soubory).
