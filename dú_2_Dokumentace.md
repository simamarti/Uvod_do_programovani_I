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

Pokud za konce týdne začíná mezera, tato mezera je započítána do následujícího týdne.

### Výstupní soubory
Program vypočítané hodnoty uloží do dvou souborů vystup_7dni.csv, vystup_rok.csv, který budou mít stejný formát dat jako vstupní soubor.

## Komentář ke zdrojovému kódu
### Zpracování dat
Program postupně načítání vstupní hodnoty. Po kontrole validity jsou průtoky přičteny k sedmidenní a roční sumě, zároveň je zvýšen o jedničku počet dní v týdnu.<br/>
Pokud je součet dní v týdnu, mezer větší, nebo roven 7, vypočítá se průměrný sedmidenní průtok a poté je zapsán do souboru "vystup_7dni.csv".<br/>
Dále ji při načítání ukládán letopočet. Pokud se nově načtený letopočet liší od předešlého, vypočítá se průměrný roční průtok a ten je zapsán do souboru "vystup_rok.csv".

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
||sum_week - součet sedmidenních průměrů|
||Q_min - minimální průtoku|
||Q_max - maximální průtoku|
||week_days - počet validních průtoků za sedm dní|
||row - pole vytvořené z právě zpracovávaného řádku|
||current_date - aktuální datum|
||sum_year - součet průtoků za rok|
||year_days - počet validních dní v roce|
|Návratová hodnota|Time_min - datum minimálního průtoku|
||Time_max - datum maximálního průtoku|
||sum_week - součet sedmidenních průměrů|
||Q_min - minimální průtoku|
||Q_max - maximální průtoku|
||week_days - počet validních průtoků za sedm dní|
||row - pole vytvořené z právě zpracovávaného řádku|
||current_date - aktuální datum|
||sum_year - součet průtoků za rok|
||year_days - počet validních dní v roce|

|Název|print_week()|
|:---:|:---|
|Popis|Funkce uloží sedmidenní průtok do souboru|
|Argumenty|writer_week - writer, pomocí kterého se zapisuje do souboru vystup_7dni.csv|
||row - pole vytvořené z právě zpracovávaného řádku|
||desc_week - popis aktuálně zpracovávaného sedmidenního průtoku|
||sum_week - součet denních průtoků v týdnu|
||week_days - počet dní v týdnu|
|Návratová hodnota|desc_week - popis aktuálně zpracovávaného sedmidenního průtoku|

|Název|print_year()|
|:---:|:---|
|Popis|Funkce uloží roční průtok do souboru|
|Argumenty|writer_year - writer, pomocí kterého se zapisuje do souboru vystup_rok.csv|
||row - pole vytvořené z právě zpracovávaného řádku|
||desc_year - popis aktuálně zpracovávaného ročního průtoku|
||sum_year - součet denních průtoků v roce|
||year_days - počet dní v roce|
|Návratová hodnota|desc_year - popis aktuálně zpracovávaného ročního průtoku|

|Název|print_rest()|
|:---:|:---|
|Popis|Funkce zapíše do obou souborů zbylé průměry na konci načítání dat|
|Argumenty|writer_week - writer, pomocí kterého se zapisuje do souboru vystup_7dni.csv|
||writer_year - writer, pomocí kterého se zapisuje do souboru vystup_rok.csv|
||desc_week - popis aktuálně zpracovávaného sedmidenního průtoku|
||desc_year - popis aktuálně zpracovávaného ročního průtoku|
||sum_week - součet sedmidenních průměrů|
||sum_year - součet průtoků za rok|
||week_days - počet validních průtoků za sedm dní|
||year_days - počet validních dní v roce|
|Návratová hodnota|None|

|Název|print_Extremes()|
|:---:|:---|
|Popis|Funkce vypíše maximální a minimální průtoky|
|Argumenty|Q_max - maximální průtoku|
||Q_min - minimální průtoku|
||desc_max - popis nejvyššího denního průtoku|
||desc_min - popis nejnižšího denního průtoku|
|Návratová hodnota|None|

|Název|init_min_max()|
|:---:|:---|
|Popis|Funkce vypíše maximální a minimální průtoky|
|Argumenty|row - pole vytvořené z právě zpracovávaného řádku|
||Q_min - minimální průtoku|
||Q_max - maximální průtoku|
||desc_max - popis nejvyššího denního průtoku|
||desc_min - popis nejnižšího denního průtoku|
|Návratová hodnota||Q_min - minimální průtoku|
||Q_max - maximální průtoku|
||desc_max - popis nejvyššího denního průtoku|
||desc_min - popis nejnižšího denního průtoku|

|Název|gap_detect()|
|:---:|:---|
|Popis|Funkce vypíše maximální a minimální průtoky|
|Argumenty|current_date - aktuální datum|
||Date - následující datum|
||gap_week - počet načtených mezer v týdnu|
||gap_pre - počet načtených mezer, které však patří do následujícího týdne|
||week_days - počet validních průtoků za sedm dní|
|Návratová hodnota|gap_week - počet načtených mezer v týdnu|
||gap_pre - počet načtených mezer, které však patří do následujícího týdne|

|Název|analyze_by_day()|
|:---:|:---|
|Popis|Funkce postupně pracovává průtoky|
|Argumenty|reader - reader, pomocí kterého se čte ze vstupního souboru|
||r - vstupní soubor otevřený pro čtení|
||writer_year - writer, pomocí kterého se zapisuje do souboru vystup_rok.csv|
||writer_week - writer, pomocí kterého se zapisuje do souboru vystup_7dni.csv|
|Návratová hodnota|None|
