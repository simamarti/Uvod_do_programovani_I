import csv
import datetime

def process_record(time_min : tuple, time_max : tuple, sum_week : float, Q_min : float, Q_max : float, week_days : int, row, current_date : tuple, sum_year : int, year_days : int) -> tuple:
        # Zpracování záznamu

    current_date = datetime.date(int(row[2]), int(row[3]), int(row[4]))
    if Q_max < row[5]:                                              # aktualizace minima a maxima
        Q_max = row[5]
        time_max = (row[0], row[1], row[2], row[3], row[4])
    if Q_min > row[5]:
        Q_min = row[5]
        time_min = (row[0], row[1], row[2], row[3], row[4])
    sum_week += float(row[5])
    week_days += 1

    year_days += 1
    sum_year += float(row[5])
    return time_min, time_max, sum_week , Q_min, Q_max, week_days, current_date, sum_year, year_days

def print_week(writer_week, row, desc_week : tuple, sum_week : int, week_days : int) -> tuple:          # zápis týdne do souboru  
    writer_week.writerow([desc_week[0], desc_week[1], f"{str(desc_week[4]).zfill(2)}.{str(desc_week[3]).zfill(2)}.{str(desc_week[2]).zfill(2)}",f"\t{round(sum_week/(week_days), 4):.04f}"])
    desc_week = (row[0], row[1], row[2], row[3], row[4])
    return desc_week

def print_year(writer_year, row, desc_year : tuple, sum_year : int, year_days : int) -> tuple:      # zápis roku do souboru
    writer_year.writerow([desc_year[0], desc_year[1], f"{str(desc_year[4]).zfill(2)}.{str(desc_year[3]).zfill(2)}.{str(desc_year[2])}", f"\t{round(sum_year/(year_days), 4):.04f}"])
    desc_year = (row[0], row[1], row[2], row[3], row[4])
    return desc_year

def print_rest( writer_week, writer_year, desc_week : tuple, desc_year : tuple, sum_week : int, 
                sum_year : int, week_days : int, year_days : int) -> None:                          # Výpis zbývajících dní a let

        if week_days:
            writer_week.writerow([desc_week[0], desc_week[1], f"{str(desc_week[4]).zfill(2)}.{str(desc_week[3]).zfill(2)}.{str(desc_week[2])}", f"\t{round(sum_week/(week_days), 4):.04f}"])
        if year_days:
            writer_year.writerow([desc_year[0], desc_year[1], f"{str(desc_year[4]).zfill(2)}.{str(desc_year[3]).zfill(2)}.{str(desc_year[2])}", f"\t{round(sum_year/(year_days), 4):.04f}"])

def print_Extremes(Q_max : float, Q_min : float, desc_max : tuple, desc_min : tuple) -> None:       # Výpis maxilálního a minimálního průtoku
        print(f"Maximální průtok: {desc_max[0]}, {str(desc_max[1])}, {str(desc_max[4]).zfill(2)}.{str(desc_max[3]).zfill(2)}.{str(desc_max[2]).zfill(2)},{str(Q_max)}")
        print(f"Minimální průtok: {desc_min[0]}, {str(desc_min[1])}, {str(desc_min[4]).zfill(2)}.{str(desc_min[3]).zfill(2)}.{str(desc_min[2]).zfill(2)},{str(Q_min)}")

def init_min_max(row) -> tuple:       # inicializace minimálního a maximálního průtoku pří načtení prvného řádku
    return row[5], row[5], (row[0], row[1], row[2], row[3], row[4]), (row[0], row[1], row[2], row[3], row[4])

def gap_detect(current_date, Date, gap_week : int) -> int:    # Detekce a výpis chybějících dní
    if current_date != None and current_date + datetime.timedelta(days=1) != Date:
        for i in range(1, int((Date - current_date).days)):
            current = current_date + datetime.timedelta(i)
            print(f">> V záznamu chybí datum: {str(current.day).zfill(2)}.{str(current.month).zfill(2)}.{str(current.year).zfill(2)}")
            gap_week += 1
    return gap_week

def analyze_by_day(reader, writer_week, writer_year) -> None:    # Načtení jednoho záznamu, kontrola validity
    
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
    time_min = None         # datum minimálního průtoku
    time_max = None         # datum maximálního průtoku
    Date = None             # Nově načtené datum
    gap_week = 0            # Počet chybějících dní v týdnu
    items = 0               # Počet načtených položek
    row = None              # Pole hodnot načtených z každého řádku   
    number = 0              # Hodnota průtoku
    is_empty = False        # Pokud bude soubor prázdny, proměnná bude nastavena na True

    for line in reader:                  # iterace přes všechny řádky souboru
        current_date = Date
        try:
            row = [line[0], line[1], line[2].split(".")[2], line[2].split(".")[1], line[2].split(".")[0], line[3]]
        except IndexError:
            print(">> Špatný formát dat.")
            is_empty = True
            continue
            
        try:
            Date = datetime.date(int(row[2]), int(row[3]), int(row[4]))
        except ValueError:
            print(f">> Datum označnuje neexistující den v roce ({str(row[4]).zfill(2)}.{str(row[3]).zfill(2)}.{str(row[2]).zfill(2)})")
            is_empty = True
            continue

        try:
            number = float(row[5])
        except ValueError:
            print(">> Špatný datový typ průtoku, musí se jednat o reálné číslo.")
            is_empty = True
            continue
        
        if first_row == False and current_date >= Date:
            print(">> Data musí být v chronologickém pořadí.")
            print_rest(writer_week, writer_year, desc_week, desc_year, sum_week, sum_year, week_days, year_days)
            is_empty = True
            return 1
        if first_row:           # inicializace maximálního a minimálního průtoku
            Q_min, Q_max, time_min, time_max = init_min_max(row)
            first_row = False
        gap_week = gap_detect(current_date, Date, gap_week)
        
        if number <=  0:
            print(f">> Dne {str(row[4]).zfill(2)}.{str(row[3]).zfill(2)}.{str(row[2]).zfill(2)} byl záporný, nebo nulový průtok.")
            gap_week += 1
            is_empty = True
            continue
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
        time_min, time_max, sum_week , Q_min, Q_max, week_days, current_date, sum_year, year_days = process_record(time_min, time_max, sum_week , Q_min, Q_max, week_days, row, current_date, sum_year, year_days)
        items += 1
        is_empty = True
    print_rest(writer_week, writer_year, desc_week, desc_year, sum_week, sum_year, week_days, year_days) 
    if not is_empty:
        print(">> Soubor je prázdný.")
    elif not items:
        print(">> Nebyly načteny žádné validní hodnoty.")
    else:                               # Výpis minima a maxima
        print_Extremes(Q_max, Q_min, time_max, time_min)

try:                                                                            # Otevření a zavření souboru
    with open("Tests/Test_14.csv", encoding = "utf-8", newline = "") as r, \
    open("vystup_7dni.csv", "w", encoding = "utf-8", newline = "") as w7, \
    open("vystup_rok.csv", "w", encoding = "utf-8", newline = "") as wr:

        reader = csv.reader(r, delimiter = ",")
        writer_week = csv.writer(w7, delimiter = ",")
        writer_year = csv.writer(wr, delimiter = ",")

        analyze_by_day(reader, writer_week, writer_year)

except FileNotFoundError:
    print(">> Soubor nebyl nalezen.")
except PermissionError:
    print(">> Nemáte právo číst/zapisovat do souboru.")
except IOError:
    print(">> Chyba pří čtení/zápisu.")