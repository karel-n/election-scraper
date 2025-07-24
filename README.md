## Popis projektu

Tento Python skript slouží ke scrapování volebních výsledků z webu [volby.cz](https://www.volby.cz) pro volby do PSP ČR 2017. 
Na základě zadané URL (např. okresu) stáhne výsledky za jednotlivé obce a uloží je do CSV souboru.

## Požadavky

- Python 3.x  
- Knihovny: `requests`, `beautifulsoup4`  
(nainstalujte pomocí `pip install -r requirements.txt`)

## Spuštění

Spusťte skript v terminálu následovně:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4205" "vysledky_most.csv"
```

Kde:
- první argument je URL pro výběr obcí v okrese (např. Most)
- druhý argument je název výstupního CSV souboru


## Autor

Karel Nodes  
k.nodes00@gmail.com
