# Doporučování knih

Desktopová aplikace v **Pythonu (PyQt5)**, která doporučí knihy podle vámi zadaných parametrů nebo podle již přečtených titulů. Data načítá z **Google Books API** a **Open Library API** pro širší pokrytí výsledků.

Cílem projektu vytvořit funkční aplikaci, která uživateli doporučuje knihy. Napojená na API s knihami, které doporučuje.

## Funkce
- **Vyhledání a doporučení knih** podle:
  - názvu (nebo části názvu)
  - autora (nebo části jména)
  - kategorie/žánru
  - minimálního počtu stran
- **Inteligentní doporučení** na základě již přečtených knih:
  - Algoritmus hodnotí podobnost podle autorů, kategorií, počtu stran a podobnosti názvů
  - **Progresivní bonus za autora**: Čím více knih od stejného autora máte přečtených, tím vyšší prioritu mají jeho další knihy (50 bodů za první knihu + 20 bodů za každou další)
  - Automaticky vylučuje již přečtené knihy
  - Detekce knih ze série podle společných slov v názvech
  - Hledání podle všech přečtených autorů najednou
- **Kombinované vyhledávání** ze dvou zdrojů:
  - Google Books API
  - Open Library API
  - Automatické odstranění duplicit podle názvu a autorů
  - Inteligentní deduplikace variant (překlady, různá vydání stejné knihy)
  - Stabilní řazení výsledků (abecedně) pro konzistentní zobrazení
- Uložení a správa seznamu již přečtených knih (JSON soubor `read_books.json`)
- Zobrazení detailu knihy (autor, kategorie, popis, počet stran, náhled obálky, pokud je dostupný)
- Okno pro správu přečtených knih s možností mazání

## Požadavky
- **Windows 10/11**
- **Python 3.10+**
- Připojení k internetu (pro Google Books API a Open Library API)

## Instalace závislostí
```powershell
python -m pip install --upgrade pip
python -m pip install PyQt5 requests
```

## Spuštění aplikace
V kořenové složce projektu:
```powershell
python main.py
```

## Použití
1. Spusťte aplikaci.
2. Do políček můžete zadat libovolnou kombinaci:
   - **Název** (nebo jeho část)
   - **Autor** (nebo část jména - stačí příjmení)
   - **Kategorie** (žánr, např. "Fiction", "Fantasy")
   - **Min. počet stran**
3. Klikněte na tlačítko pro doporučení podle parametrů.
4. Výsledky se zobrazí v seznamu s kombinovanými výsledky z obou API.
5. Klikněte na knihu v seznamu pro zobrazení detailů (obálka, popis, počet stran).
6. Z detailu lze uložit knihu mezi přečtené pomocí tlačítka "Přidat do přečtených".
7. Tlačítkem "Zobrazit přečtené knihy" otevřete okno se seznamem uložených knih.
8. Tlačítkem "Doporučit podle přečtených" získáte inteligentní doporučení na základě všech vašich přečtených knih.

## Doporučovací algoritmus
Aplikace hodnotí kandidátní knihy podle následujících kritérií:

### Bodování podobnosti
- **Shoda v kategorii**: 10 bodů za každou shodnou kategorii
- **Shoda v autorovi**: 30 bodů za každého stejného autora
- **Podobný počet stran**: 
  - 15 bodů, pokud se liší max. o 30 stran
  - 8 bodů, pokud se liší o 31-60 stran
- **Podobnost názvů**: 
  - 6 bodů za každé společné smysluplné slovo (delší než 3 znaky)
  - 10 bodů bonus, pokud začínají stejným slovem (detekce série)

### Progresivní bonus za autora
- **1. přečtená kniha** od autora: +50 bodů
- **2. přečtená kniha** od autora: +70 bodů
- **3. přečtená kniha** od autora: +90 bodů
- atd. (+20 bodů za každou další)

### Vyhledávání kandidátů
- Hledá knihy od **všech přečtených autorů** (podle příjmení i celého jména)
- Hledá knihy ve **všech kategoriích** z přečtených knih
- Kombinuje výsledky z obou API pro maximální pokrytí
- Automaticky filtruje již přečtené knihy

## Časté dotazy / tipy
- Aplikace kombinuje výsledky z **Google Books API** a **Open Library API** – získáte až 40 výsledků.
- Kategorie vracené API mohou mít různé formáty; zkuste obecnější klíčová slova jako „Fiction", „Drama".
- **Deduplikace** odstraňuje různá vydání stejné knihy (překlady, ilustrované verze) – zobrazí se jen jedna varianta.
- Při doporučování podle přečtených knih se **automaticky preferují autoři**, od kterých máte více přečtených knih.
