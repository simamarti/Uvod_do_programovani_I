import csv
import math
import datetime

def add_zeros(number):  # Přidání nul na konec čísla, pokud nemá 4 desetinná místa
    number_list = list(number)
    dot = 0
    for index, item in enumerate(number_list):
        if item == '.':
            dot = (len(number_list) - index - 1)
            break
    while dot < 4:
        number += "0"
        dot += 1
    return number

def process_record(Time_min : tuple, Time_max : tuple, sum_week : float, Q_min : float, Q_max : float, week_days : int, row, current_date : tuple, sum_year : int, year_days : int) -> tuple:
        # Zpracování záznamu

    current_date = datetime.date(int(row[2]), int(row[3]), int(row[4]))
    if Q_max < row[5]:                                              # aktualizace minima a maxima
        Q_max = row[5]
        Time_max = (row[0], row[1], row[2], row[3], row[4])
    if Q_min > row[5]:
        Q_min = row[5]
        Time_min = (row[0], row[1], row[2], row[3], row[4])
    sum_week += float(row[5])
    week_days += 1

    year_days += 1
    sum_year += float(row[5])
    return Time_min, Time_max, sum_week , Q_min, Q_max, week_days, current_date, sum_year, year_days

def print_week(writer_week, row, desc_week : tuple, sum_week : int, week_days : int) -> tuple:          # zápis týdne do souboru  
    writer_week.writerow([desc_week[0], desc_week[1], str(desc_week[4]).zfill(2) + "." + str(desc_week[3]).zfill(2) + "." + str(desc_week[2]), "\t" + add_zeros(str(round(sum_week/(week_days), 4)))])
    desc_week = (row[0], row[1], row[2], row[3], row[4])
    return desc_week

def print_year(writer_year, row, desc_year : tuple, sum_year : int, year_days : int) -> tuple:      # zápis roku do souboru
    writer_year.writerow([desc_year[0], desc_year[1], str(desc_year[4]).zfill(2) + "." + str(desc_year[3]).zfill(2) + "." + str(desc_year[2]), "\t" + add_zeros(str(round(sum_year/(year_days), 4)))])
    desc_year = (row[0], row[1], row[2], row[3], row[4])
    return desc_year

def print_rest( writer_week, writer_year, desc_week : tuple, desc_year : tuple, sum_week : int, 
                sum_year : int, week_days : int, year_days : int) -> None:                          # Výpis zbývajících dní a let

        if week_days:
            writer_week.writerow([desc_week[0], desc_week[1], str(desc_week[4]).zfill(2) + "." + str(desc_week[3]).zfill(2) + "." + str(desc_week[2]), "\t" + add_zeros(str(round(sum_week/(week_days), 4)))])
        if year_days:
            writer_year.writerow([desc_year[0], desc_year[1], str(desc_year[4]).zfill(2) + "." + str(desc_year[3]).zfill(2) + "." + str(desc_year[2]), "\t" + add_zeros(str(round(sum_year/(year_days), 4)))])

def print_Extremes(Q_max : float, Q_min : float, Desc_max : tuple, Desc_min : tuple) -> None:       # Výpis maxilálního a minimálního průtoku
        print("Maximální průtok: " + str(Desc_max[0]) + ", " + str(Desc_max[1]) + ", " + str(Desc_max[4])
         + ". " + str(Desc_max[3]) + ". " + str(Desc_max[2]) + ", " + str(Q_max))
        print("Minimální průtok: " + str(Desc_min[0]) + ", " + str(Desc_min[1]) + ", " + str(Desc_min[4])
         + ". " + str(Desc_min[3]) + ". " + str(Desc_min[2]) + ", " + str(Q_min))

def init_min_max(row, Q_min : int, Q_max : int, Desc_min, Desc_max) -> tuple:       # inicializace minimálního a maximálního průtoku pří načtení prvného řádku
    Q_min = row[5]
    Q_max = row[5]
    Desc_min = (row[0], row[1], row[2], row[3], row[4])
    Desc_max = (row[0], row[1], row[2], row[3], row[4])
    return Q_min, Q_max, Desc_min, Desc_max

def gap_detect(current_date, Date, gap_week : int, week_days : int) -> int:    # Detekce a výpis chybějících dní
    tmp = gap_week
    if current_date == None:
        current_date = Date
    else:
        if current_date + datetime.timedelta(days=1) != Date:
            for i in range(1, int((Date - current_date).days)):
                current = current_date + datetime.timedelta(i)
                print(">> V záznamu chybí datum: " + str(current.day) + ". " + str(current.month) + ". " + str(current.year))
                gap_week += 1
        current_date = Date
    
    return gap_week

def analyze_by_day(reader, r, writer_week, writer_year) -> None:    # Načtení jednoho záznamu, kontrola validity
    
    sum_year = 0            # Součet dnů v roce
    sum_week = 0            # Součet dnů v týdnu
    week_days = 0           # Počet dnů v týdnu
    year_days = 0           # Počet dnů v roce
    desc_week = None        # Popisek týdne (např. [139000,QD,1980,11,1]), to, co se vypíše do csv
    desc_year = None        # Popisek roku (např. [139000,QD,1980,11,1]), to, co se vypíše do csv
    current_year = 0        # Momentálně zpracovávnaný letopočet
    current_date = None     # Poslední úspěšně zpracovávané datum
    first_row = True        # Detekování, zda byl načten první řádek, bool
    Q_min = None            # Minimální průtok
    Q_max = None            # Maximální průtok
    Time_min = None         # datum minimálního průtoku
    Time_max = None         # datum maximálního průtoku
    Date = None             # Nově načtené datum
    gap_week = 0            # Počet chybějících dní v týdnu
    items = 0               # Počet načtených položek
    row = None              # Pole hodnot načtených z každého řádku   
    number = 0              # Hodnota průtoku 

    if len(list(reader)) == 0:
        print(">> Soubor je prázdný.")
        return 1
    r.seek(0)
    
    for line in reader:                  # iterace přes všechny řádky souboru
        try:
            row = [line[0], line[1], line[2].split(".")[2], line[2].split(".")[1], line[2].split(".")[0], line[3]]
        except IndexError:
            print(">> Špatný formát dat.")
            current_date = Date
            continue
            
        try:
            Date = datetime.date(int(row[2]), int(row[3]), int(row[4]))
        except ValueError:
            print(">> Datum označnuje neexistující den v roce (" + row[4] + ". " + row[3] + ". " + row[2] + ")")
            current_date = Date
            continue

        try:
            number = float(row[5])
        except ValueError:
            print(">> Špatný datový typ průtoku, musí se jednat o reálné číslo.")
            current_date = Date
            continue
        
        if first_row == False and current_date >= Date:
            print(">> Data musí být v chronologickém pořadí.")
            print_rest(writer_week, writer_year, desc_week, desc_year, sum_week, sum_year, week_days, year_days)
            return 1
        if first_row:           # inicializace maximálního a minimálního průtoku
            Q_min, Q_max, Time_min, Time_max = init_min_max(row, Q_min, Q_max, Time_min, Time_max)
            first_row = False
        gap_week = gap_detect(current_date, Date, gap_week, week_days)
        
        if number <=  0:
            print(">> Dne " + str(row[4]) + ". " + str(row[3]) + ". " + str(row[2]) + " byl záporný, nebo nulový průtok.")
            current_date = Date
            gap_week += 1
            continue
        current_date = Date
                                            # Zápis do souboru týden
        if week_days + gap_week == 0:
            desc_week = (row[0], row[1], row[2], row[3], row[4])
        elif week_days + gap_week >= 7:
            desc_week = print_week(writer_week, row, desc_week, sum_week, week_days)
            gap_week = 0
            sum_week = 0
            week_days = 0
                                            # Zápis do souboru rok
        if sum_year == 0:
            desc_year = (row[0], row[1], row[2], row[3], row[4])
            current_year = row[2]
        elif current_year != row[2]:
            current_year = row[2]
            desc_year = print_year(writer_year, row, desc_year, sum_year, year_days) 
            year_days = 0
            sum_year = 0
                                            # Započítání do průměrů týdne a roku
        Time_min, Time_max, sum_week , Q_min, Q_max, week_days, current_date, sum_year, year_days = process_record(Time_min, Time_max, sum_week , Q_min, Q_max, week_days, row, current_date, sum_year, year_days)
        items += 1
                                            # Výpis zbylých dnů/roku
    print_rest(writer_week, writer_year, desc_week, desc_year, sum_week, sum_year, week_days, year_days) 
    
    if items:                               # Výpis minima a maxima
        print_Extremes(Q_max, Q_min, Time_max, Time_min)
    else:
        print(">> Nebyly načteny žádné validní hodnoty.")

try:                                                                            # Otevření a zavření souboru
    with open("Tests/Test_12.csv", encoding = "utf-8", newline = "") as r, \
    open("vystup_7dni.csv", "w", encoding = "utf-8", newline = "") as w7, \
    open("vystup_rok.csv", "w", encoding = "utf-8", newline = "") as wr:

        reader = csv.reader(r, delimiter = ",")
        writer_week = csv.writer(w7, delimiter = ",")
        writer_year = csv.writer(wr, delimiter = ",")

        analyze_by_day(reader, r, writer_week, writer_year)

except FileNotFoundError:
    print(">> Soubor nebyl nalezen.")
