# Domácí úkol 3 - dokumentace
## Uživatelský manuál
Program načte na vstupu soubory *.geojson s uloženými adresami a kontejnery. Program vypočítá průměrnou vzdálenost k nejbližšímu kontejneru, počet načtených adres a kontejner, medián vzdálenotí k nejbližšímu kontejneru a adresu, z které je to k nejbližšímu kontejneru nejdále. Dále se do pracovního adresáře uloží soubor s názvem "dresy_kontejnery.geojson", ve kterém je ke každé adrese přiřazeno ID nejbližšího, obyvatelům domu přístupného, kontejneru.
### Formát vstupního souboru
Vstupní soubory jsou slovníky (formát geojson). 
Vstupní soubory mají klíč "features". Pod tímto klíčet je pole. V každém prvku pole je další slovník, který obsahuje klíče "properties" a "geometry". Pod klíčem "geometry" je další slovník s informacemi o adrese. Pod klíčem "geometry" se nachází další slovník s klíčem "coordinates", v kterém se nachází poles se souřadnicemi.<br/>
### Chybové hlášky 
Pokud nastane výjimka, uživatel o tom bude informován v terminálu chybovou hláškou.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---:|:---:|
|č. 1|Ve slovníku se daný klíč nenachází|">> Klíč nebyl ve slovníku nalezen."|
|č. 2|||
