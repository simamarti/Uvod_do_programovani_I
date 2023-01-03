# Domácí úkol 3 - dokumentace
## Uživatelský manuál
Program načte na vstupu soubory *.geojson s uloženými adresami a kontejnery. Program vypočítá průměrnou vzdálenost k nejbližšímu kontejneru, počet načtených adres a kontejner, medián vzdálenotí k nejbližšímu kontejneru a adresu, z které je to k nejbližšímu kontejneru nejdále. Dále se do pracovního adresáře uloží soubor s názvem "adresy_kontejnery.geojson", ve kterém je ke každé adrese přiřazeno ID nejbližšího, obyvatelům domu přístupného, kontejneru.

### Formát vstupního souboru
Vstupní soubory jsou slovníky (formát geojson). 
Vstupní soubory mají klíč "features". Pod tímto klíčet je pole. V každém prvku pole je další slovník, který obsahuje klíče "properties" a "geometry". Pod klíčem "geometry" je další slovník s informacemi o adrese. Pod klíčem "geometry" se nachází další slovník s klíčem "coordinates", v kterém se nachází poles se souřadnicemi.<br/>
### Prametry programu
Pokud není dáno jinak, program hledá a načítá souboru s názvem adresy.geojson a kontejnery.geojson.<br/>
Pokud se do příkazového řádku za příkaz pro spuštění programu "py -u du_3.py" zde zadat volitelné parametry. Parametry lze libovolně kombinovat<br/>
"-a <název souboru>"  program použije jako adresy uložené v zadaném souboru<br/> 
"-k <název souboru>"  program použije jako kontejnery uložené v zadaném souboru<br/> 

Příklad: "py -u "du_3.py" -a adresy2.geojson -k kontejnry2.geojson"

### Chybové hlášky 
Pokud nastane výjimka, uživatel o tom bude informován v terminálu chybovou hláškou.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---:|:---:|
|č. 1|Soubor neexistuje|">> Soubor s názvem <název souboru> neexistuje."|
|č. 2|Uživatel nemá právo číst soubor|">> Ke čtení souboru s názvem <název souboru> nemáte práva."|
|č. 3|Ve slovníku se daný klíč nenachází|">> Klíč nebyl ve slovníku nalezen."|
|č. 4|Souřadnice v souborech nejsou čísla|">> Špatný formát vstupu."|
|č. 5|Minimální vzdálenost pro některou adresu vejde více než 10 000 m|">> Minimální vzdálenost přesáhla stanovený limit (10 km). Program byl ukončen."|

Každý kontejner má pod klíčem "properties" klíč "PRISTUP", v kterém je informace o přístupnosti kontejneru. Tento parametr nabývá dvou stavů "volně", nebo "obyvatelům domu". Hodnotu "obyvatelům domu" mají kontejnery, které jsou přístupné pouze obyvatelům daného domu.<br/>
Pokud se adresa kontejneru rovná adrese domu, je nejbližší vzdálenost ke kontejneru nastave na 0, a tato nula je i započtena po průměru. Pokud adresa nemá vlastní kontejner, nejbližší kontejner je počítán poze z "volných" kontejnerů (klíč "PRISTUP" se rovná "volně").

## Výstupní soubor
Program na konci svého běhu uloží do pracovního adresáře soubor s názvem "adresy_kontejnery.geojson". Tento soubor má stejnou strukturu jako vstupní soubor adres. Pouze je u každé adresy přidaný klíč "kontejner" s uloženým ID nejbližšího kontejneru.

## Komentář ke zdrojovému kódu
### Zpracování dat
### Importované knihovny
pyproj (metoda transformer) - převádí souřadnicové systémy mezi sebou<br/>
json - knihovna ke zpracovnání souborů formátu geojson<br/>
aargparse - knihovna sloužící k nastavení parametrů programu<br/>

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
||adresss - pole s adresou dommu|
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
|Popis|Funkce uloží do souboru "adresy_kontejnery.geojson" slovník s adresama|
|Argumenty|adresses - slovník s adresama s přidanými ID nejbližších kontejnerů|
|Návratová hodnota|None|

|Název|median_calc()|
|:---:|:---|
|Popis|Funkce vrátí medián zadaného pole|
|Argumenty|dist_array - pole se vzdálenostmi k nejbližím kontejnerů u jednotlivých adres|
||counter - počet adres v poli|
|Návratová hodnota|medián - medián pole|

|Název|process()|
|:---:|:---|
|Popis|Hlavní funkce, prochází všechny adresy a počítá nejblišší kontejnery|
|Argumenty|adresses - slovník s adresama|
||bins - slovník s kontejnery|
|Návratová hodnota|průměr minimálních vzdáleností|
||med - medián minimálních vzdáleností|
||adress - adresa, z které je to nejdále ke kontejneru|
||max_dist - vzdálenost k adrese nejvzdálenější od kontejneru|

|Název|file_open()|
|:---:|:---|
|Popis|Funkce otevře soubor s daným jménem a obsah uloží do proměnné|
|Argumenty|file_name - jméno souboru|
|Návratová hodnota|dictionary - slovník s načtenými dat ze souboru|
