# 📝 AI Omluvenkář

Tento projekt je webová aplikace pro studenty a rodiče, která automaticky přepisuje neformální, obyčejné omluvy za absenci ("Zaspal jsem") do profesionálně formulovaných školních omluvenek ("Vážený pane učiteli / Vážená paní učitelko...").

Aplikace funguje jako kompletní full-stack projekt využívající **Flask (Python)** na backendu, **PostgreSQL** databázi pro ukládání dynamických uživatelských šablon a externí **LLM API** (na bázi modelu rodiny GPT/Gemma) pro samotné generování inteligentního textu. Celé řešení je efektivně kontejnerizováno pomocí infrastruktury **Docker**.

---

## 📂 Struktura projektu (Co kde najít)

Tento repozitář je pečlivě uspořádán podle moderních standardů pro softwarový vývoj. Zde je podrobný rozbor všech důležitých adresářů a souborů napříč projektem:

### `app.py`
**Hlavní mozek aplikace (Backend / Webový Server)**
- Jádro aplikace. Skript je napsán v **Pythonu** s využitím rozšířeného frameworku **Flask**.
- **Klíčové procesy, které tento soubor řeší:**
  1. **Správa Databáze:** Funkce pro nativní bezpečné komunikování s PostgreSQL databází pro získávání výchozích důvodů absence. Aplikace sama pozná, pokud je tabulka prázdná, a automaticky ji nasadí.
  2. **Routování (Endopointy):** Zajišťuje logiku pro komunikaci mezi frontendem a backendem (obsluhuje příchozí kliknutí uživatele na tlačítka posílající síťové relace `GET` a `POST`). 
  3. **Integrace s LLM/AI:** Obsahuje hlavní endpoint `/generate`. Uživatelský text je tu bezpečně transformován a vložen do pečlivě zkonstruovaného *systémového promptu* (instrukce udržující AI ve stručném a naprosto formálním chování). Následně `app.py` vykonává autentizovaný rest-API dotaz rovnou na server s jazykovým modelem a předává výsledek přímočíře zpět do klientského prohlížeče.

### `compose.yml`
**Konfigurace architektury pro nasazení (Docker Compose)**
- Klíčový infrastrukturalní manifest definující prostředí pro nahození projektu. Automatizuje vytvoření a souběžný chod dvou synchronizovaných aplikačních kontejnerů na interní Dockerovské sítí:
  - **`web`**: Flask backend. Právě zde jsou v produkčním nasazení (environment rules) bezpečně obsažena skrytá přístupová hesla a **API tokeny** tak, aby program věděl, ke které inteligenci a pod jakou identitou se hlásí.
  - **`db`**: Oficiální robustní databáze PostgreSQL konfigurovaná s odlehčeným jádrem *alpine* pro svižnost a úspornost paměťových prostředků.

### `Dockerfile`
**Izolované prostředí celého serveru**
- Textový recept na sestavení "krabicové" repliky serveru definující pro Docker engine návod z jakého OS má vycházet. Specifikuje se v něm Python 3.11, kopírují se v něm zdrojové kódy softwaru, provádí se přes něj příkaz na instalaci knihoven z `requirements.txt` a spouští se zde proces.

### `templates/index.html` (v podsložce `templates`)
**Uživatelské rozhraní (Frontend Client)**
- Ve složce `templates/` jsou uschovány responzivní HTML šablony vykreslované frameworkem.
- Frontend není jen obyčejná statická stránka — obsahuje skriptování v asynchronním **JavaScriptu**, který přes API metodu `fetch()` posílá aplikační data neviditelně z okna přímo do Flask serveru a dynamicky po odpovědi upravuje stránku. To zajišťuje perfektní a hladký uživatelský UX zážitek bez neustálého obnovování ("refreshování") karty prohlížeče.

### `.env` a `.gitignore`
**Důvěrnost a bezpečnost systému**
- **`.gitignore`** obsahuje kritický seznam zakázaných souborů. Předchází tak situaci, kdy by vývojář omylem zapsal tajné systémy do veřejného indexu Gitu (systému správy verzí).
- Důležitým maskovaným souborem, který je tímto spravován, je domovský **`.env`** soubor obsahující lokální kritická přístupová hesla, API Klíče, tokens atd. Díky striktním pravidlům je znemožněn jakýkoliv únik těchto pověření.

### `requirements.txt`
**Seznam závislostí**
- Soubor obsahuje explicitní deklaraci jmen balíků třetích stran určených pro překladač jazyka Python (`Flask`, `requests` k posílání payloadů, obslužné protokoly spojení pro SQL `psycopg2`). V produkci garantují plnohodnotné spuštění nezávisle na výchozí kvalitě klientského počítače.

---

## ⚙️ Tok dat pod kapotou (Stručné schéma chodu)

1. **Start:** Nastartování containerů s propojením služeb přes oddělený bezpečný `bridge` router.
2. **Klientský Přístup:** Prohlížeč naváže spojení a aplikace naservíruje uživatelskou plochu `index.html`.
3. **Postup naplnění uživatelského panelu (DB část):** JavaScript vyšle na server skrytý signál, Flask odchytí parametr, promluví uvnitř Docker sítě na databázi a vytáhne šablony (`templates`). Server to převede do JSONU a vrátí - čímž se v prohlížeči vyrenderují nabídky omluv v Select Boxu.
4. **Vlastní inference a LLM Call:** Při odeslání důvodu z javascriptu, Flask přečte data, obalí je do promptující syntaxe, podstrčí mu *SECRET KEY* Bearer token zajištěný z orchestrátoru `compose.yml` a pošle instrukce datovému centru modelu umělé inteligence. 
5. **Návrat s hotovým plagiátem:** AI odpovídající server naparsuje vracející se vygenerovaný objekt. Surovou zprávu vytáhne a zažene přes Flask zpět z cloudu k lokálnímu klientovi do okýnka prohlížeče k pohodlnému okopírování do reálné pošty vyučujícího!
