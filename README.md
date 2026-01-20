# Doporučování knih

Desktopová aplikace v **Pythonu (PyQt5)**, která doporučí knihy podle vámi zadaných parametrů nebo podle již přečtených titulů. Data načítá z **Google Books API** a **Open Library API** pro širší pokrytí výsledků.

Cíle projektu vytvořit funkční aplikaci, která uživateli doporučuje knihy. Napojená na API s knihami, které doporučuje.

## Funkce
- **Vyhledání a doporučení knih** podle:
  - názvu (nebo části názvu)
  - autora (nebo části jména)
  - kategorie/žánru
  - minimálního počtu stran
- **Inteligentní doporučení** na základě již přečtených knih:
  - Algoritmus hodnotí podobnost podle autorů, kategorií, počtu stran a podobnosti názvů
  - Automaticky vylučuje již přečtené knihy
  - Detekce knih ze série podle společných slov v názvech
- **Kombinované vyhledávání** ze dvou zdrojů:
  - Google Books API
  - Open Library API
  - Automatické odstranění duplicit
- Uložení a správa seznamu již přečtených knih (JSON soubor `read_books.json`).
- Zobrazení detailu knihy (autor, kategorie, popis, počet stran, náhled obálky, pokud je dostupný).

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
   - **Autor** (nebo část jména)
   - **Kategorie** (žánr, např. "Fiction", "Drama")
   - **Min. počet stran**
3. Klikněte na tlačítko pro doporučení.
4. Výsledky se zobrazí v seznamu s kombinovanými výsledky z Google Books a Open Library.
5. Klikněte na knihu v seznamu pro zobrazení detailů.
6. Z detailu lze uložit knihu mezi přečtené.
7. V okně „Přečtené knihy" můžete uložené tituly prohlížet a mazat.
8. Aplikace může doporučit knihy podobné vašim již přečteným knihám pomocí inteligentního algoritmu.

## Časté dotazy / tipy
- Aplikace kombinuje výsledky z **Google Books API** a **Open Library API** – získáte až 40 výsledků (20 z každého zdroje).
- Kategorie vracené API mohou mít různé formáty; zkuste obecnější klíčová slova jako „Fiction", „Drama".
- **Doporučovací algoritmus** hodnotí knihy podle:
  - Shody v kategorii (5 bodů za každou shodnou kategorii)
  - Shody v autorovi (20 bodů za každého stejného autora)
  - Podobného počtu stran (3 body, pokud se liší max. o 30 stran)
  - Podobnosti názvů (15 bodů za každé společné smysluplné slovo – detekce série)
  - Aplikace automaticky testuje dostupnost obou API při spuštění.
