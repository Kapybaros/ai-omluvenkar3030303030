# Docker Compose (`compose.yml`)

## Co to je?
Díky nástroji Docker Compose a jeho konfiguračnímu souboru `compose.yml` (případně `docker-compose.yml`) můžeš snadno spravovat projekty, které potřebují více propojených částí (např. aplikaci samotnou a k ní databázi, nebo lokální AI model).

## Jak to funguje?
Normálně bys musel pro každou část tvého systému (třeba Flask aplikaci, databázi PostgreSQL atd.) volat složité příkazy v terminálu, nastavovat jim sítě a ručně je propojovat.

V `compose.yml` si všechno přehledně "naklikáš" jako do nějakého receptu:
1. **Služby (services)**: Vyjmenuješ, jaké programy chceš zapnout (např. Webový server, Databáze).
2. **Porty**: Řekneš, jak se k nim z venku dostaneš (např. port `5000` u tebe na PC odkáže na port `5000` uvnitř kontejneru).
3. **Environment proměnné**: Předáš službám tajná hesla a nastavení.
4. **Volumes (svazky)**: Zabezpečíš, že se data z databáze nesmažou, když se kontejner vypne.

Pak už jen stačí zadat do terminálu `docker compose up` a celá tahle orchestrace naběhne automaticky.
