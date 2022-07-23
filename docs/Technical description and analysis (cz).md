# Úvod
Columnator je program na dynamické zarovnávání tabulátorů. Operuje na dvou souborech, z nichž jeden *(Model)* obsahuje tabulátory a slouží jako vzor pro renderování do druhého *(View)*. Uživatel pracuje s View a Columnator podle jeho úprav udržuje Model v podobě konzistentní[^konzistentní] s View.

[^konzistentní]: To jest, po uživatelově úpravě má View podobu A, Model je upraven na podobu B, jejíž vyrenderování je v ideálním případě totožné s A.

Tento dokument slouží jako výstup z vývoje nástroje Columnator. Obsahuje stručný výčet funkcí tohoto nástroje a analýzu limitací a možných rozšíření.

# Funkce
Columnator lze spustit s následujícím nastavením:
- jméno souboru Model **(povinné, soubor nemusí existovat)**
- jméno souboru View **(povinné, soubor nemusí existovat)**
- minimální šířka tabulátoru **(volitelné, výchozí hodnota = 4)**
- výplňový znak tabulátoru **(volitelné, výchozí hodnota = ' ')**

Za prvé, Columnator zarovnává odpovídající tabulátory v po sobě jdoucích řádcích v souboru Model do sloupců v souboru View. Tabulátory v po sobě následujících řádcích jsou odpovídající, právě když jejich pořadí je stejné *(tedy např. druhý tabulátor ve 3. a 4. je odpovídající dvojice tabulátorů)*. Zarovnání do sloupců je nahrazení odpovídajících tabulátorů výplňovými znaky tak, že počet výplňových znaků na všech zasažených řádcích je větší nebo roven minimální šířce tabulátoru a že konce posloupností výplňových znaků, které odpovídají odpovídajícím tabulátorům, mají stejný index jakožto znaky na řádcích.

Za druhé, Columnator sleduje uživatelovy úpravy v souboru View a převádí je na úpravy souboru Model. Typické úpravy jsou:
- úprava textu, který nezasahuje do výplně tabulátorů
- úprava výplně tabulátorů:
	- smazání
	- rozšíření
	- rozdělení *(= vepsání znaku dovnitř výplně)*

# Analýza
Skutečná implementace Columnatoru obsahuje jisté limitace, které omezují rozsah jeho funkcí. Tato analýza vyjmenovává problematické případy a diskutuje o rozdílech mezi ideální implementací a skutečnou implementací. Nakonec jsou zde nastíněny konkrétní směry, v nichž lze implementaci Columnatoru rozšířit a zlepšit.

Limitace Columnatoru se téměř výhradně týkají převádění úprav souboru View na odpovídající úpravy souboru Model. Toto totiž nebylo předem úplně jasně definováno a ukázalo se, že je to problém velmi citlivý na konkrétní "kybernetizaci" Columnatoru.[^kybernetizace]

[^kybernetizace]: Jestli bude operovat na hromadných změnách jednorázově, na rozdílech kontinuálně, zda bude reaktivní nebo proaktivní, …

## Hraniční případy
1. Mazání a přidávání výplňových znaků v množství, které přesahuje zarovnání zbytku odpovídajícího sloupce, avšak nedosahuje zarovnání sloupce následujícího.
2. Synchronizace dvou souborů za stálého sledování úprav v obou.

## Idealizovaná podoba
1. Nadbytečné výplňové znaky jsou ponechány jako samostatné v souboru Model *(nejsou "pohlceny" znakem tabulátoru)*.
2. V případě změny souboru Model se přizpůsobí View. V případě změny souboru View při neměnném souboru Model se přizpůsobí Model.

## Implementovaná podoba
1. Nadbytečné výplňové znaky jsou pohlceny tabulátorem a při dalším renderu jsou tedy smazány. Pokud má posloupnost výplňových znaků délku kratší než bezchybné zarovnání, avšak delší než je minimální šířka tabulátoru, je chybějící výplň doplněna.
2. Zde by implementace měla odpovídat ideálu, avšak kvůli povaze úprav souborů a nutnosti zavádět časové prodlevy je možné, že spolehlivost není stoprocentní.

## Limitace
Hlavní limitací současné implementace je, že operuje na celých souborech naráz - nedokáže úpravy provádět pouze na základě rozdílů mezi původní a novou podobou. "Diffová" implementace by zaručila větší spolehlivost jak po stránce přístupu k souborům Model a View, tak po stránce zachování nadbytečných výplňových znaků.

Hromadné zpracování bylo zvoleno pro jednoduchost implementace a názornost a ergonomii pro uživatele. Díky tomu lze Columnator vyzkoušet jako samostatný program. Pokud by měl skutečně sloužit pouze jako modul do textového editoru, převážily by výhody "diffové" implementace.

## Rozšíření a zlepšení
Jak bylo nastíněno výše, Columnator lze upravit do podoby, která operuje pouze s rozdíly mezi verzemi souborů. Tato podoba umožňuje výraznou časovou i prostorovou optimalizaci, jakož i zavedení některých ergonomických funkcí.

Potom se naskýtá otázka, jaké rozhraní má Columnator mít. Je totiž potřeba brát v potaz interakci s externím editorem a otvírají se možnosti pro rozdělení Columnatoru do více nástrojů *(samotné zarovnávání a zpětná úprava, diffování souborů, sledování změn souborů, potenciálně práce přímo s textovými strukturami jako rope atp.)*.
