# Domácí ůkol 2 - dokumentace
## Uživatelský manuál 
Program na vstupu načte soubor *.csv s denními průtoky daného vodního toku. Na výstupu program uloží do dvou souborů průměrné týdenní (vystup_7dni.csv) a roční (vystup_rok.csv) průtoky ve stejném formátu.
### Formát vstupního souboru
139000,QD,1.11.1980,    0.6700<br/>
139000,QD,2.11.1980,    0.5800<br/>
139000,QD,3.11.1980,    0.4500<br/>

První sloupec označuje identifikátor vodoměrné stanice<br/>
Druhý sloupec označuje měřenou veličinu (QD - denní průtok)<br/>
Třetí sloupec označuje datum ve formátu "DD.MM.RRRR"<br/>
Čtvrtý sloupec je kladní reálné číslo označující průtok<br/>

Každý denní záznam průtoku je zapsán na nové řádce.
### Chybové hlášky
Pokud nastane výjimka uživatel o tom bude informován v terminálu chybovou hláškou.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---|:---|
|č. 1|Soubor nebyl nalezen|">> Soubor nebyl nalezen."|
|č. 2|Uživatel nemá právo číst/zapisovat do souboru|">> Nemáte právo číst/zapisovat do souboru."|
|č. 3|Prázdný soubor|">> Soubor je prázdný."|
|č. 4|Chyba při čtení, nebo zápisu|">> Chyba pří čtení/zápisu."|

Po načtení každého řádku, před zpracováním program zkontroluje zda jsou data validní.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---|:---|
|č. 5|Špatný formát dat|">> Špatný formát dat."|
|č. 6|Datum měření neexistuje (např. 29. 2. 2003)|">> Datum označnuje nexecistující den v roce (9. 2. 2003)"|
|č. 7|Průtok má špatný formát|">> Špatný datový typ průtoku, musí se jednat o reálné číslo."|
|č. 8|Datum není v chronologickém pořadí|">> Data musí být v chronologickém pořadí."|
|č. 9|Nulový, nebo zápporný průtok|">> Dne <aktuální datum> byl záporný, nebo nulový průtok."|

Program také detekuje mezery v datech. Pokud Program detekuje mezeru, informuje o tom uživatele přes terminál, např. ">> V záznamu chybí datum: 7. 12. 2022"
Program mezery započítává do sedmidenních průtoků, ale nepoužívá se k výpočtu. Např. program načte 4 dni, poté 2 mezery, nakonec nečte pouze 1 den. Z výsledných 5 dní vypočítá sedmidenní průměr. 
Pokud týden skončí uprostřed mezery v datech, nový týden se začne počítat od prvního validního data. Např. 

139000,QD,1.11.1980,    0.6700<br/>
139000,QD,10.11.1980,   0.5800<br/>
139000,QD,11.11.1980,   0.4500<br/>

První sedmidenní průměr bude začínat 1. 11. 1980, druhý sedmidenní průtok se bude počítat od 10. 11. 1980.

Pokud za koncem výpočtu sedmidenního průtoku začíná mezera, další sedmidení průtok je počítán od prvního dne za mezerou.

### Výstupní soubory
Program vypočítané hodnoty uloží do dvou souborů vystup_7dni.csv, vystup_rok.csv, který budou mít stejný formát dat jako vstupní soubor.

## Komentář ke zdrojovému kódu
### Zpracování dat
Pomocí objektu csv.reader() program nejprve zkontroluje, zda soubor existuje (chyba č. 1), zda k němu má uživatel práva pro čtení/zápis (chyba č. 2), nebo zda není prázdný (chyba č. 3), nebo zda nenastane nějaká jiná neočekávatelná chyba spojená se čtením/zápisem do souboru (chyba č. 4). Pokud nastane některá z předchozích chyb, program skončí.<br/>
Následuje načítání jednotlivých řádků z objektu csv.reader(). U každého řádku program postupně zkontroluje, zda má záznam správný formát (chyba č. 5), zda datum měření existuje (např. 29. 2. 2003 neexistuje) (chyba č. 6), a zda je průtok reálné číslo (chyba č. 7). Pokud nastane některá z chyb číslo 5–7, program daný záznam přeskočí a pokračuje dalším řádkem.<br/>
Pokud není aktuálně načítané datum v chronologickém pořadí, např. když 3. 3. nasleduje po 4. 3., program skončí (chyba č. 8). Pokud je načítán první řádek inicializuje se minimální a maximální průtok na hodnoty prvního záznamu.<br/>
Následně jsou detekovány případné mezery v datech. Mezery jsou zařazené do sedmidenních průtoků, ale nepočítá se s nima. Naposled program kontroluje, zda průtok není záporný (chyba č. 9). Pokud chyba nastane, program záznam přeskočí a pokračuje dalším záznamem.<br/>
Následně program zkontroluje, zda nenastala podmínka (součet dnů a mezer je větší nebo roven 7) pro zapsání sedmidenního průtoku do souboru ("vystup_7dni.csv"), popř. zda se již nezačal počítat další sedmidenní průtok (součet dnů a mezer je roven 0). Stejným způsoben je zkontrolována podmínka (aktuálně načítaný rok se liší od předchozího) pro zápis do souboru s ročními průtoky ("vystup_rok.csv").<br/>
Nakonec je aktualizován maximální a minimální průtok a průtok je připočítán do sedmidenní a roční sumy.<br/>
Po ukočení čtení ze souboru je do obou výstupních souborů zapsány zbylé průměry a na terminál jsou vypsány maximální a minimální průtoky.<br/> 
### Importované knihovny
csv - umožňuje čtení a zápis do souboru formátu csv<br/>
datetime - umožňuje ukládat data, kontroluje zda je datum validní, zde k datu přičítat (např. 1 den).<br/>
### Funkce
|Název|Process_record()|
|:---:|:---|
|Popis|Funkce zpracoje řádek na vstupu|
|Argumenty|time_min - datum minimálního průtoku|
||time_max - datum maximálního průtoku|
||sum_week - součet sedmidenních průměrů|
||Q_min - minimální průtoku|
||Q_max - maximální průtoku|
||week_days - počet validních průtoků za sedm dní|
||row - pole vytvořené z právě zpracovávaného řádku|
||current_date - aktuální datum|
||sum_year - součet průtoků za rok|
||year_days - počet validních dní v roce|
|Návratová hodnota|time_min - datum minimálního průtoku|
||time_max - datum maximálního průtoku|
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
|Návratová hodnota|gap_week - počet načtených mezer v týdnu|

|Název|analyze_by_day()|
|:---:|:---|
|Popis|Funkce postupně pracovává průtoky|
|Argumenty|reader - reader, pomocí kterého se čte ze vstupního souboru|
||writer_year - writer, pomocí kterého se zapisuje do souboru vystup_rok.csv|
||writer_week - writer, pomocí kterého se zapisuje do souboru vystup_7dni.csv|
|Návratová hodnota|None| 
