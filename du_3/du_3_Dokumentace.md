# Domácí úkol 3 - dokumentace
## Uživatelský manuál
Program načte na vstupu soubory *.geojson s uloženými adresami a kontejnery. Program vypočítá průměrnou vzdálenost k nejbližšímu kontejneru, počet načtených adres a kontejner, medián vzdálenotí k nejbližšímu kontejneru a adresu, z které je to k nejbližšímu kontejneru nejdále. Dále se do pracovního adresáře uloží soubor s názvem "adresy_kontejnery.geojson", ve kterém je ke každé adrese přiřazeno ID nejbližšího, obyvatelům domu přístupného, kontejneru.

### Formát vstupního souboru
Vstupní soubory jsou slovníky (formát geojson). 
Vstupní soubory mají klíč "features". Pod tímto klíčet je pole. V každém prvku pole je další slovník, který obsahuje klíče "properties" a "geometry". Pod klíčem "geometry" je další slovník s informacemi o adrese. Pod klíčem "geometry" se nachází další slovník s klíčem "coordinates", ve kterém se nachází pole se souřadnicemi.<br/>
### Parametry programu
Pokud není dáno jinak, program hledá a načítá souboru s názvem adresy.geojson a kontejnery.geojson.<br/>
Pokud se do příkazového řádku za příkaz pro spuštění programu "py -u du_3.py" lze zadat volitelné parametry. Parametry lze libovolně kombinovat<br/>
"-a <název souboru>"  program použije jako adresy uložené v zadaném souboru<br/> 
"-k <název souboru>"  program použije jako kontejnery uložené v zadaném souboru<br/> 

Příklad: "py -u "du_3.py" -a adresy2.geojson -k kontejnry2.geojson"

### Chybové hlášky 
Pokud nastane výjimka, uživatel o tom bude informován v terminálu chybovou hláškou.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---:|:---:|
|č. 1|Soubor neexistuje|">> Soubor s názvem <název souboru> neexistuje."|
|č. 2|Uživatel nemá právo číst soubor|">> Ke čtení souboru s názvem <název souboru> nemáte práva."|
|č. 3|Nebyly načteny žádné adresy ani kontejnery|">> nebyly načteny žádné adresy nebo žádné veřejné kontejnery, program byl ukončen."|
|č. 4|Ve slovníku se daný klíč nenachází|">> Klíč nebyl ve slovníku nalezen."|
|č. 5|Souřadnice v souborech nejsou čísla|">> Špatný formát vstupu."|
|č. 6|Minimální vzdálenost pro některou adresu vyjde více než 10 000 m|">> Minimální vzdálenost přesáhla stanovený limit (10 km). Program byl ukončen."|

Každý kontejner má pod klíčem "properties" klíč "PRISTUP", ve kterém je informace o přístupnosti kontejneru. Tento parametr nabývá dvou stavů "volně", nebo "obyvatelům domu". Hodnotu "obyvatelům domu" mají kontejnery, které jsou přístupné pouze obyvatelům daného domu.<br/>
Pokud se adresa kontejneru rovná adrese domu, je nejbližší vzdálenost ke kontejneru nastavena na 0 a tato 0 je i započtena do průměru. Pokud adresa nemá vlastní kontejner, nejbližší kontejner je počítán pouze z "volných" kontejnerů (klíč "PRISTUP" se rovná "volně").

## Výstupní soubor
Program na konci svého běhu uloží do pracovního adresáře soubor s názvem "adresy_kontejnery.geojson". Tento soubor má stejnou strukturu jako vstupní soubor adres. Pouze je u každé adresy přidaný klíč "kontejner" s uloženým ID nejbližšího kontejneru.

## Komentář ke zdrojovému kódu
### Zpracování dat
Po spuštění programu se pomocí funkce file_open() načtou pomocí knihovny "json" soubory s názvem "adresy.geojson" a "kontejnery.geojson", popř. soubory s názvy zadanými v parametrech programu.<br/>
Poté se souřadnicový systém adresních bodů převede z WGS do S-JTSK, aby bylo možné počítat vzdálenosti pomocí pythagorovy věty. Po kontrole počtu adres a kontejnerů se pro každou adresu vypočítá vzdálenost k nejbližšímu kontejneru a jeho ID. Při tomto výpočtu se postupně u každého kontejneru zkontroluje, zda má stejnou adresu. Pokud to tak je minimální vzdálenost ke kontejneru je automaticky nastavena na 0. Pokud na adrese žádný privátní kontejner není, jsou pro výpočet minimální vzdálenosti brány v potaz pouze kontejnery s hodnotou "volně" v klíči 'PRISTUP'. Pokud je některá minimální vzdálenost větší než 10 km, program je automaticky ukončen.<br/>
Do proměnné s adresami je ke každé přidán klíč 'kontejner' s hodnotou ID nejbližšího kontejneru. Vzdálenost k nejbližšímu kontejneru je také přidána do pole s minimálními vzdálenostmi všech kontejnerů.<br/>
Po zpracování každé adresy je aktualizována suma vzdáleností, ze které je poté počítán průměr a adresní bod, z kterého je to ke kontejneru nejdále a je také uložena vzdálenost k tomuto adresnímu bodu.<br/>
Nakonec je proměnná s adresními aktualizovanými o ID nejbližšího kontejneru uložena do souboru "adresy_kontejnery.geojson". Pole minimálních vzdáleností je seřazeno a je z něj vypočten medián.<br/>
Jako výstup na termínál je vypsán počet načtených adresních bodů a kontejnerů, průměrná minimální vzdálenost ke kontejnerům, medián minimálních vzdáleností, a ze které adresy je to nejdále ke kontejneru a vzdálenost k němu.<br/>

### Importované knihovny
pyproj (metoda transformer) - převádí souřadnicové systémy mezi sebou<br/>
json - knihovna ke zpracovnání souborů formátu geojson<br/>
argparse - knihovna sloužící k nastavení parametrů programu<br/>

### Funkce
|Název|dist()|
|:---:|:---|
|Popis|Funkce počítá vzdálenost mezi dvěma body|
|Argumenty|source - počáteční bod (pole se souřadnicemi x, y)|
||finish - koncový bod (pole se souřadnicemi x, y)|
|Návratová hodnota| vzdálenost mezi body|

|Název|is_private()|
|:---:|:---|
|Popis|Funkce určí zda má daná adresa vlastní kontejner|
|Argumenty|can - slovník s informacemi o kontejneru|
||house_adr - řetezec s adresou domu|
|Návratová hodnota| bool - True/False|

|Název|change_coord()|
|:---:|:---|
|Popis|Funkce souřařadnice z WGS do S-JTSK|
|Argumenty|adresses - slovník se všemi adresami|
|Návratová hodnota|None|

|Název|dist_calc()|
|:---:|:---|
|Popis|Funkce určí nejbližší kontejner a jeho vzdálenost|
|Argumenty|bins - slovník se všemi kontejnery|
||coord_adr - pole se souřadnicemi adresy|
||adresss - pole s adresou domu|
|Návratová hodnota|min_dist - vzdálenost k nejbližšímu kontejneru|
||id_number - ID nejbližšího kontejneru|

|Název|upload_stat()|
|:---:|:---|
|Popis|Funkce aktualizuje adresu s nejvzdálenějším kontejnerem a součet vzdáleností|
|Argumenty|adresss - pole s adresou domu|
||item - slovník s adresou|
||max_dist - minimální vzdálenost ke kontejneru u adresy s nejvzdálenějším kontejnerem|
|Návratová hodnota|adresss - pole s adresou domu|
||item - slovník s adresou|
||max_dist - minimální vzdálenost ke kontejneru u adresy s nejvzdálenějším kontejnerem|

|Název|file_ID()|
|:---:|:---|
|Popis|Funkce uloží do souboru "adresy_kontejnery.geojson" slovník s adresami|
|Argumenty|adresses - slovník s adresama s přidanými ID nejbližších kontejnerů|
|Návratová hodnota|None|

|Název|median_calc()|
|:---:|:---|
|Popis|Funkce vrátí medián zadaného pole|
|Argumenty|dist_array - pole se vzdálenostmi k nejbližím kontejnerům u jednotlivých adres|
||counter - počet adres v poli|
|Návratová hodnota|medián - medián pole|

|Název|process()|
|:---:|:---|
|Popis|Hlavní funkce, prochází všechny adresy a počítá nejblišší kontejnery|
|Argumenty|adresses - slovník s adresami|
||bins - slovník s kontejnery|
|Návratová hodnota|průměr minimálních vzdáleností|
||med - medián minimálních vzdáleností|
||adress - adresa, z které je to nejdále ke kontejneru|
||max_dist - vzdálenost k adrese nejvzdálenější od kontejneru|

|Název|file_open()|
|:---:|:---|
|Popis|Funkce otevře soubor s daným jménem a obsah uloží do proměnné|
|Argumenty|file_name - jméno souboru|
|Návratová hodnota|dictionary - slovník s načtenými daty ze souboru|
