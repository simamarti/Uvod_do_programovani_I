# Domácí ůkol 2 - dokumentace
## Uživatelský manuál 
Program na vstupu načte soubor *.csv s denními průtoky daného vodního toku. Na výstupu program uloží do dvou souborů průměrné týdenní (vystup_7dni.csv) a roční (vystup_rok.csv) průtoky ve stejném formátu.
### Formát vstupního souboru
139000,QD,1.11.1980,    0.6700<br/>
139000,QD,2.11.1980,    0.5800<br/>
139000,QD,3.11.1980,    0.4500<br/>

První sloupec označuje identifikátor vodoměrné stanice
Drhý sloupec označuje měřenou veličinu (QD - denní průtok)
Třetí sloupec označuje datum ve formátu "DD. MM. RRRR"
Čtvrtý sloupec je kladní reálné číslo označující průtok
### Chybové hlášky
Pokud nastane výjimka uživatel o tom bude informován v terminálu chybovou hláškou.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---|:---|
|č. 1|Zadaný soubor neexistuje|">> Soubor nebyl nalezen."|
|č. 2|Chyba při čtení/zápisu|">> Chyba při čtení/zápisu."|
|č. 3|Prázdný soubor|">> Soubor je prázdný."|


Po načtení každého řádku, před zpracováním program zkontroluje zda jsou data validní.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---|:---|
|č. 4|Špatný formát dat|">> Špatný formát dat."|
|č. 5|Datum měření neexistuje (např. 29. 2. 2003)|">> Datum označnuje nexecistující den v roce (9. 2. 2003)"|
|č. 6|Průtok má špatný formát|">> Špatný datový typ průtoku, musí se jednat o reálné číslo."|
|č. 7|Na vstupu je den, který v minulost vzhledem k minulému|">> Do minulosti lízt nemůžeme, zatím."|
|č. 8|Nulový, nebo zápporný průtok|">> Dne <aktuální datum> byl záporný, nebo nulový průtok."|

V případě chyb č. 3 a 8 je zpracování dat ukončeno a do souboru jsou zapsány doposud úspěšně zapsané průměry.

Program také detekuje mezery v datech. Pokud Program detekuje mezeru, informuje o tom uživatele přes terminál, např. ">> V záznamu chybí datum: 7. 12. 2022"
Program mezery započítává do sedmidenních průtoků, ale nepoužívá se k výpočtu. Např. program načte 4 dni, poté 2 mezery, nakonec nečte pouze 1 den. Z výsledných 5 dní vypočítá sedmidenní průměr. 
Pokud týden skončí uprostřed mezery v datech, nový týden se začne počítat od prvního validního data. Např. 

139000,QD,1.11.1980,    0.6700<br/>
139000,QD,10.11.1980,   0.5800<br/>
139000,QD,11.11.1980,   0.4500<br/>

První sedmidenní průměr bude začínat 1. 11. 1980, druhý sedmidenní průtok se bude počítat od 10. 11. 1980.

### Výstupní soubory
Program vypočítané hodnoty uloží do dvou souborů vystup_7dni.csv, vystup_rok.csv, který budou mít stejný formát dat jako vstupní soubor.

## Komentář ke zdrojovému kódu
### Funkce
|Název|add_zeros()|
|:---:|:---|
|Popis|Funkce doplní spočítaný průtok na 4 desetinná místa|
|Argumenty|number - číslo ve formě řetězce|
|Návratová hodnota|číslo doplněné na 4 desetinná místa ve formě řetězce|

|Název|Process_record()|
|:---:|:---|
|Popis|Funkce zpracoje řádek na vstupu|
|Argumenty|Time_min - datum minimálního průtoku|
||Time_max - datum maximálního průtoku|
|Návratová hodnota|číslo doplněné na 4 desetinná místa ve formě řetězce|
