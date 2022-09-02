# Manuál pro vývojáře
Tento dokument navazuje na [uživatelskou příručku](/docs/User%20Manual%20(cz).md) a popisuje vnitřní fungování programu columnator.

## Základní běh
Columnator běží nepřetržitě, přičemž donekonečna alternuje mezi následujícími činnostmi:

1. přečte soubor Model
2. nahradí tabulátory výplní
3. zapíše do souboru View
4. počká
5. přečte soubor View
6. vyvodí odpovídající podobu souboru Model
7. zapíše do souboru Model
8. počká

Čtení a zápis do souborů jsou optimalizovány tak, aby nedocházelo k záškubům a aby bylo respektování chování souborů při přepisování
(soubory jsou těsně před zápisem zbaveny veškerého obsahu).

Základní běh je možno najít jako top-level kód v modulu `columnator.py`, souborové operace pak v modulu `fileworks.py`.

## Nahrazení tabulátorů
Jedná se o vcelku triviální operaci, kdy je spočten v rámci neporušené posloupnosti tabulátorů daného indexu nejzazší pravý okraj.
K němu jsou pak ve všech zúčastněných řádcích doplněny výplňové znaky. Celá operace probíhá rekurzivně podle hloubky odsazení.

Viz modul `rendering.py`, výchozí funkce je `render(tab_width, tab_fill, model)`.

## Odvození tabulátorů z výplně
Jedná se o značně netriviální operaci, neboť program prakticky nemá jak bezchybně uhodnout,
které výplňové znaky jsou součástí odsazení a které figurují jako běžné znaky (a jsou tedy součástí textu mimo odsazení).
Tento problém je řešen pomocí dvou iterativních heuristik, prováděných v tomto pořadí:

1. Řádky se rozdělí podle dostatečně dlouhých posloupností výplňových znaků.
V tomto kroku jsou pohlceny všechny přebytečné výplňové znaky, které sousedí s odsazením.

2. Vertikálně se překrývající odsazení, z nichž jedno zabírá délku více odsazení v řádcích výše nebo níže, jsou rozdělena tak,
aby hranice všech odsazení lícovaly. V tomto kroku jsou implicitně doplněny výplňové znaky chybějící do perfektního zarovnání.

Kvůli heuristické povaze tohoto kroku a také inherentními omezeními použitého interakčního paradigmatu
(celé View se zpracovává naráz, nikoliv po atomických operacích) je tento krok ztrátový - pokud tento krok označíme `back` a
krok nahrazení tabulátorů výplní označíme `fwd`, potom pro obecný řetězec `A` platí `fwd(back(A)) != A`. Ovšem u většiny běžných
případů použití nastává rovnost, navíc chybám v odvozených tabulátorech lze předejít častým ukládáním souboru View a použitím
větší minimální šířky odsazení nebo výplňového znaku, který je jinak vzácně používaný.

Pro diskuzi dalších limitací viz [technickou analýzu](/docs/Technical%20description%20and%20analysis%20(cz).md).

Viz modul `viewing.py`, výchozí funkce je `desugar(tab_width, tab_fill, view)`.
