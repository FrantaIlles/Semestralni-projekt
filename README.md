# Doporučování knih

Desktopová aplikace v **Pythonu (PyQt5)**, která doporučí knihy podle vámi zadaných parametrů nebo podle již přečtených titulů. Data načítá z **Google Books API**.

## Funkce
- Vyhledání a doporučení knih podle:
  - názvu (nebo části názvu)
  - autora (nebo části jména)
  - kategorie/žánru
  - minimálního počtu stran
- Uložení a správa seznamu již přečtených knih (JSON soubor `read_books.json`).
- Zobrazení detailu knihy (autor, kategorie, popis, počet stran, náhled obálky, pokud je dostupný).

## Požadavky
- **Windows 10/11**
- **Python 3.10+**
- Připojení k internetu (pro Google Books API)

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
   - **Kategorie** (žánr, např. “Fiction”, “Drama”, “Juvenile Fiction” – záleží na tom, co vrací Google Books)
   - **Min. počet stran**
3. Klikněte na tlačítko pro doporučení.
4. Výsledky se zobrazí v seznamu; z detailu lze uložit knihu mezi přečtené.
5. V okně „Přečtené knihy” můžete uložené tituly prohlížet a mazat.

## Časté dotazy / tipy
- Google Books API vrací max. **40 výsledků** na jeden dotaz; při úzkých dotazech zkuste obecnější klíčová slova.
- Kategorie vracené API mohou mít tvar např. „Juvenile Fiction / Fantasy & Magic“; použijte část žánru, která se obvykle vyskytuje (např. „Fiction“, „Drama“).
- Pokud se ikona okna nezobrazuje, ověřte, že soubor ikony (`ikona.png`) je ve stejné složce jako `ui/main_window.py` nebo upravte cestu k souboru.