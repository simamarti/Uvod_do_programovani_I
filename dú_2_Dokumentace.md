# Domácí ůkol 2 - dokumentace
Program na vstupu načte soubor *.csv s denními průtoky daného vodního toku. Na výstupu program uloží do dvou souborů průměrné týdenní (vystup_7dni.csv) a roční (vystup_rok.csv) průtoky ve stejném formátu.
## Formát vstupního souboru
139000,QD,1.11.1980,    0.6700<br/>
139000,QD,2.11.1980,    0.6700<br/>
139000,QD,3.11.1980,    0.6700<br/>

První sloupec označuje identifikátor vodoměrné stanice
Drhý sloupec označuje měřenou veličinu (QD - denní průtok)
Třetí sloupec označuje datum ve formátu "DD. MM. RRRR"
Čtvrtý sloupec je kladní reálné číslo označující průtok
## Chybové hlášky
Pokud nastane výjimka uživatel o tom bude informován v terminálu chybovou hláškou.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---:|:---:|
|č. 1|Zadaný soubor neexistuje|">> Soubor nebyl nalezen."|
|č. 2|Chyba při čtení/zápisu|">> Chyba při čtení/zápisu."|
|č. 3|Prázdný soubor|">> Soubor je prázdný."|


Po načtení každého řádku, před zpracováním program zkontroluje zda jsou data validní.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---:|:---:|
|č. 4|Špatný formát dat|">> Špatný formát dat."|
|č. 5|Datum měření neexistuje (např. 29. 2. 2003)|">> Datum označnuje nexecistující den v roce (9. 2. 2003)"|
|č. 6|Průtok má špatný formát|">> Špatný datový typ průtoku, musí se jednat o reálné číslo."|
|č. 7|Na vstupu je den, který v minulost vzhledem k minulému|">> Do minulosti lízt nemůžeme, zatím."|
|č. 8|Nulový, nebo zápporný průtok|">> Dne <aktuální datum> byl záporný, nebo nulový průtok."|

V případě chyb č. 3 a 8 je zpracování dat ukončeno a do souboru jsou zapsány úspěšně zapsané průměry.

Program také detekuje mezery v datech. Pokud Program detekuje mezery, vypíše do terminálu každé chybějící datum ve formátu 
