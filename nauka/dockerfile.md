# Dockerfile

## Co to je?
`Dockerfile` je textový dokument, který obsahuje všechny příkazy (instrukce) potřebné k vytvoření takzvaného "Docker image" (otisk/obraz). Z tohoto obrazu se pak spouští konkrétní kontejner.

## Jak to funguje?
Zatímco `compose.yml` orchestrálně řídí a spouští _už hotové_ nebo připravené kontejnery, `Dockerfile` slouží přímo k výrobě takového kontejneru. 

Představ si ho jako recept na upečení dortu:
1. **Zdroj (např. `FROM python:3.9`)**: Říkáš, z jakého základu vycházíš. Nechceš stavět celý operační systém od nuly, vezmeš si už připravený minimalistický Linux s nainstalovaným Pythonem.
2. **Kopírování souborů (`COPY . /app`)**: Přetáhne tvé zdrojové kódy (jako je `app.py` nebo složka `templates`) dovnitř image.
3. **Příprava (`RUN pip install ...`)**: Nainstaluje všechny knihovny (závislosti), které aplikace potřebuje.
4. **Spuštění (`CMD ["python", "app.py"]`)**: Definuje ten úplně poslední příkaz, který se provede ve chvíli, kdy kontejner z tohoto obrazu někdo spustí (nastartuje se tvá webová aplikace).

Díky Dockerfile ti aplikace poběží na každém počítači nebo serveru stejně, bez ohledu na to, jaké verze tam mají předinstalované. Má to svůj vlastní izolovaný svět.
