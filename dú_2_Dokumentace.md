# Domácí ůkol 2 - dokumentace
Program na vstupu načte soubor *.csv s denními průtoky daného vodního toku. Na výstupu program uloží do dvou souborů průměrné týdenní (vystup_7dni.csv) a roční (vystup_rok.csv) průtoky ve stejném formátu.
## Formát vstupního souboru
139000,QD,1.11.1980,    0.6700
139000,QD,2.11.1980,    0.6700
139000,QD,3.11.1980,    0.6700

První sloupec označuje identifikátor vodoměrné stanice
Drhý sloupec označuje měřenou veličinu (QD - denní průtok)
Třetí sloupec označuje datum ve formátu "DD. MM. RRRR"
Čtvrtý sloupec je kladní reálné číslo označující průtok
## Chybové hlášky
Pokud nastane výjimka uživatel o tom bude informován v terminálu chybovou hláškou.

Zadaný soubor neexistuje:             ">> Soubor nebyl nalezen."
Chyba při čtení/zápisu:               ">> Chyba při čtení/zápisu." 
Prázdný soubor:                       ">> Soubor je prázdný."

Po načtení každého řádku, před zpracováním program zkontroluje zda jsou data validní.
