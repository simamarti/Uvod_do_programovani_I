# Domácí ůkol 2 - dokumentace
## Uživatelský manuál 
Program na vstupu načte soubor *.csv s denními průtoky daného vodního toku. Na výstupu program uloží do dvou souborů průměrné týdenní (vystup_7dni.csv) a roční (vystup_rok.csv) průtoky ve stejném formátu.
### Formát vstupního souboru
139000,QD,1.11.1980,    0.6700<br/>
139000,QD,2.11.1980,    0.5800<br/>
139000,QD,3.11.1980,    0.4500<br/>

První sloupec označuje identifikátor vodoměrné stanice<br/>
Druhý sloupec označuje měřenou veličinu (QD - denní průtok)<br/>
Třetí sloupec označuje datum ve formátu "DD. MM. RRRR"<br/>
Čtvrtý sloupec je kladní reálné číslo označující průtok<br/>

Každý denní záznam průtoku je zapsán na nové řádce.
### Chybové hlášky
Pokud nastane výjimka uživatel o tom bude informován v terminálu chybovou hláškou.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---|:---|
|č. 1|Soubor nebyl nalezen|">> Soubor nebyl nalezen."|
|č. 2|Prázdný soubor|">> Soubor je prázdný."|


Po načtení každého řádku, před zpracováním program zkontroluje zda jsou data validní.

|Číslo chyby|Chyba|Výpis na terminál|
|:---:|:---|:---|
|č. 3|Špatný formát dat|">> Špatný formát dat."|
|č. 4|Datum měření neexistuje (např. 29. 2. 2003)|">> Datum označnuje nexecistující den v roce (9. 2. 2003)"|
|č. 5|Průtok má špatný formát|">> Špatný datový typ průtoku, musí se jednat o reálné číslo."|
|č. 6|Datum není v chronologickém pořadí|">> Data musí být v chronologickém pořadí."|
|č. 7|Nulový, nebo zápporný průtok|">> Dne <aktuální datum> byl záporný, nebo nulový průtok."|

V případě chyb č. 4 a 8 je zpracování dat ukončeno a do souboru jsou zapsány doposud úspěšně zapsané průměry.

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
Pomocí objektu csv.reader() program nejprve zkontroluje zda soubor existuje (chyba č. 1), nebo zda není prázdný (chyba č. 2). Pokud nastane některá z předchozích chyb, program skončí.<br/>
Následuje načítání jednotlivých řádků z objektu csv.reader(). U každého řádku program postupně zkontroluje zda má záznam správný formát (chyba č. 3), zda datum měření existuje (např. 29. 2. 2003 neexistuje) (chyba č. 4) a zda je průtok reálné číslo (chyba č. 5). Pokud nastane některá z chyb číslo 3–5, program daný záznam přeskočí a pokračuje dalším řádkem.<br/>
Pokud není aktuálně načítané datum v chronologickém pořadí, např. když 3. 3. nasleduje po 4. 3., program skončí (chyba č. 6). Pokud je načítán první řádek inicializuje se minimální a maximální průtok na hodnoty prvního záznamu.<br/>
Následně jsou detekovány případné mezery v datech. Mezery jsou zařazené do sedmidenních průtoků, ale nepočítá se s nima.
Následně program zkontroluje zda nenastala podmínka (součet dnů a mezer je většíí nebo roven 7) pro zapsání sedmidenního průtoku do souboru ("vystup_7dni.csv"), popř. zda se již nezačal počítat další sedmidenní průtok (součet dnů a mezer je roven 0). Stejnejným způsoben je zkontrolována podmínka (aktuálně načítaný rok se liší od předchozího) pro zápis do souboru s ročními průtoky ("vystup_rok.csv").<br/>
Nakonec je aktualizován maximální a minimální průtok a průtok je připočítán do sedmidenní a roční sumy.<br/>
Po ukočení čtení ze souboru je do obou výstupních souborů zapsány zbylé průměry a na terminál jsou vypsány maximální a minimální průtoky.<br/> 
