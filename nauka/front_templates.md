# HTML Šablony (Složka `templates/`)

## Co to je?
V této složce obyčejně leží kostry grafického frontend (to, co pak uživatel reálně vidí v internetovém prohlížeči) psaného pomocí HTML a přídavků. Flask má jako standardní místo právě složku, která se jmenuje přesně `templates`.

## Jak to funguje?
Najdeš tam soubory typu `index.html`. Nejsou to ale jen hloupé prázdné dokumenty; fungují jako **šablony (Jinja2)**.
Znamená to, že umí reagovat na věci z Pythonu. Například v HTML souboru uvidíš divné závorky, něco jako `{{ vygenerovana_omluvenka }}`. 
Když `app.py` udělá svou práci a zavolá tuhle šablonu, "vycucne" tato místa v závorkách za reálný text. Pokud generování omluvenky skončí úspěšně, HTML v prohlížeči se dynamicky překreslí a naservíruje uživateli ten správný výsledek přesně tam, kde to designér zrovna navrhnul.

Díky složce `templates` je zkrátka přísně oddělený backendový kód robota (Python) od designových barviček, čudlítek a rozvržení stránky (HTML).
