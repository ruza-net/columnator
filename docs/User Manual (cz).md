# Uživatelská příručka
Toto je příručka popisující funkce programu columnator.

## Účel programu
Columnator operuje na dvou souborech označovaných jako Model a View.
Má dvě funkce: převod tabulátorů na zarovnané mezery a převod zarovnávacích mezer na tabulátory.

### Tabulátory → Mezery
Jeho funkcí je převádět obsah souboru Model do souboru View tak, aby byly tabulátory nahrazeny výplňovými znaky, jako např. mezerami.
Toto je prováděno tak, aby byly sobě odpovídající tabulátory zarovnány pod sebou (pokud se vyskytují v po sobě jdoucích řádcích).
Jinými slovy, tabulátory se pak chovají jako oddělovače sloupců.

Příklad zarovnání tabulátorů (výplňový znak je mezera, min. šířka je 4):

Soubor Model (zde mezery jsou tabulátory, hvězdička označuje konec řádku, na němž je pouze jeden tabulátor):
```
asdf
as	dsa
	jwie	3u1	i2
sdreq3fasdfdsa	i3n	92j1i0ij30	jf
ai	93
	*
asd0	02	kso9

asdhfiwuho
as	ieu
```

Soubor View (zde mezery jsou mezery, hvězdička označuje konec řádku, na němž jsou pouze mezery):
```
asdf
as                dsa
                  jwie    3u1           i2
sdreq3fasdfdsa    i3n     92j1i0ij30    jf
ai                93
                  *
asd0              02    kso9

asdhfiwuho
as    ieu
```

Všimněte si, že 3. a 4. řádek mají 2. sloupec zarovnaný, ovšem 7. řádek jej má odsazený nezávisle.
Je to proto, že je 7. řádek od 3. a 4. oddělen řádky, které 2. postrádají.
Naopak mezi 2. až 7. řádkem bylo zarovnání v 1. sloupci díky tabulátoru v jinak prázdném 6. řádku přeneseno, a proto se zarovnávají společně.

Dále poslední řádek se zarovnává nezávisle na předposledním, protože předposlední neobsahuje jediný tabulátor.
Takto by situace vypadala, kdyby předposlední řádek obsahoval na konci tabulátor:

Model (hvězdička má stejný účel jako výše):
```
asdhfiwuho	*
as	ieu
```

View (hvězdička má stejný účel jako výše):
```
asdhfiwuho    *
as            ieu
```

### Mezery → Tabulátory
Pokud v průběhu spuštění provedete úpravy souboru View, columnator dané úpravy převede do souboru Model.
Úpravy obyčejného textu se převedou triviálně, avšak columnator se bude také snažit převést mezery,
které jsou použity k zarovnání textu do sloupců, na tabulátoru.
Jedná se o operaci opačnou k té, která byla popsána v předchozí podsekci.

## Spuštění programu
Columnator se spouští z příkazové řádky následujícím způsobem: `python columnator.py (model) (view) [(šířka tab) [(výplň tab)]]`.
Kulaté závorky označují název parametru. Je potřeba za ně dosadit nějakou hodnotu, a to následovně:

- `(model)` - název souboru, který bude použit jako Model; soubor nemusí existovat
- `(view)` - název souboru, který bude použit jako View; soubor nemusí existovat
- `(šířka tab)` - číslo určující minimální počet znaků `(výplň tab)`, na nějž se budou tabulátory v souboru `(model)` převádět do souboru `(view)`
- `(výplň tab)` - jediný znak použitý jako výplň tabulátoru

Hranaté závorky označují část příkazu, kterou lze vynechat. Příklady validních spuštění:

- `python columnator.py model.txt view.txt`
- `python columnator.py model.txt view.txt 4`
- `python columnator.py model.txt view.txt 10 +`

Příklady **ne**validních spuštění:

- `python columnator.py model.txt` (chybí `(view)`)
- `python columnator.py model.txt view.txt +` (namísto `+` má být číslo)
- `python columnator.py model.txt view.txt 3 'abc'` (`(výplň tab)` má být jediný znak)

Při spuštění columnatoru bude na standardní výstup terminálu vypsán ukázkový text v originální podobě
a v podobě vygenerované na základě použitého nastavení.

Columnator vytvoří soubory Model a View, pokud neexistují, a pak na nich začne operovat.
Zatímco columnator běží, můžete oba soubory libovolně upravovat ve svém oblíbeném editoru.
Po uložení změn do toho kterého souboru provede columnator odpovídající změny v souboru druhém.
Po vypnutí columnatoru (standardně zkratka `ctrl-C` v terminálu) zůstanou oba soubory ve své poslední podobě.

Pokud columnator spustíte na existujících souborech Model a View, přičemž View svou podobou neodpovídá souboru Model a nastavení columnatoru,
columnator soubor View přepíše - tj. **podoba souboru Model má v případě konfliktu přednost před podobou souboru View**.
