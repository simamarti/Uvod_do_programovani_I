import csv
import math

def is_leap(year : int) -> bool:
    if (year%4 == 0 and year%400 == 0) or (year%4 == 0 and year%100 != 0):
        return True
    return False

def is_valid(time : tuple) -> bool:     # time[0] = rok; time[1] = měsíc; time[2] = den

    if time[1] > 12 or time[1] < 0:
        return False
    if time[2] > 31 or time[2] < 0:
        return False
    if time[1] == 2:
        if is_leap(time[0]):
            if time[2] > 29:
                return False
        else:
            if time[2] > 28:
                return False
    elif (time[1] < 7 and time[1]%2 == 0) or (time[1] > 8 and time[1]%2 == 1):    # 30
        if time[2] > 30:
            return False
    return True

def is_next(current, next):
    if current == None:
        return True
    if current[0] != next[0]:
        if current[0] + 1 != next[0]:
            return False
        if current[1] != 12 or next[1] != 1:
            return False
        if current[2] != 31 or next[2] != 1:
            return False  
    if current[1] != next[1]:
        if current[1] + 1 != next[1]:
            return False
        if next[2] != 1:
            return False
        if current[1] == 2:
            if is_leap(current[0]):
                if current[2] != 29:
                    return False
            else:
                if current[2] != 28:
                    return False
        elif (current[1] < 7 and current[1]%2 == 0) or (current[1] > 8 and current[1]%2 == 1):    # 30
            if current[2] != 30:
                return False
        else:
            if current[2] != 31:
                return False
    return True

def process_record(Time_min : tuple, Time_max : tuple, sum_week : float, Q_min : float, Q_max : float, week_days : int, row, current_date : tuple, sum_year : int, year_days : int) -> tuple:
    print("Zapsáno: " + str(row))
    current_date = (row[2], row[3], row[4])
    if Q_max < row[5]:
        Q_max = row[5]
        Time_max = (row[0], row[1], row[2], row[3], row[4])
    if Q_min > row[5]:
        Q_min = row[5]
        Time_min = (row[0], row[1], row[2], row[3], row[4])
    sum_week += row[5]
    week_days += 1

    year_days += 1
    sum_year += row[5]
    return Time_min, Time_max, sum_week , Q_min, Q_max, week_days, current_date, sum_year, year_days

def print_week(writer_week, row, desc_week : tuple, sum_week : int, week_days : int) -> tuple:
    writer_week.writerow([desc_week[0], desc_week[1], desc_week[2], desc_week[3], desc_week[4], round(sum_week/(week_days), 4)])
    print("Suma: " + str(sum_week) + "; Počet dní v týdnu: " + str(week_days))
    sum_week = 0
    week_days = 0
    desc_week = (row[0], row[1], row[2], row[3], row[4])
    return desc_week, sum_week, week_days

def print_year(writer_year, row, desc_year : tuple, sum_year : int, year_days : int) -> tuple:
    writer_year.writerow([desc_year[0], desc_year[1], desc_year[2], desc_year[3], desc_year[4], round(sum_year/(year_days), 4)])
    desc_year = (row[0], row[1], row[2], row[3], row[4])
    print("Suma: " + str(sum_year) + "Počet dní v roce: " + str(year_days))
    year_days = 0
    sum_year = 0
    return desc_year, sum_year, year_days

def print_rest( writer_week, writer_year, desc_week : tuple, desc_year : tuple, sum_week : int, 
                sum_year : int, week_days : int, year_days : int) -> None:
        print("_-------------------------------_")
        if week_days:
            writer_week.writerow([desc_week[0], desc_week[1], desc_week[2], desc_week[3], desc_week[4], round(sum_week/(week_days), 4)])
            print("Suma: " + str(sum_week) + "; Počet dní v týdnu: " + str(week_days))
        if year_days:
            writer_year.writerow([desc_year[0], desc_year[1], desc_year[2], desc_year[3], desc_year[4], round(sum_year/(year_days), 4)])
            print("Suma: " + str(sum_year) + "Počet dní v roce: " + str(year_days))

def print_Extremes(Q_max : float, Q_min : float, Desc_max : tuple, Desc_min : tuple) -> None:

        print("Maximální průtok: " + str(Desc_max[0]) + ", " + str(Desc_max[1]) + ", " + str(Desc_max[2])
         + ", " + str(Desc_max[3]) + ", " + str(Desc_max[4]) + ", " + str(Q_max))
        print("Minimální průtok: " + str(Desc_min[0]) + ", " + str(Desc_min[1]) + ", " + str(Desc_min[2])
         + ", " + str(Desc_min[3]) + ", " + str(Desc_min[4]) + ", " + str(Q_min))

def process_gap(current_date, next_date):
    counter = 0
    

    
    return counter
def init_min_max(row, Q_min, Q_max, Desc_min, Desc_max) -> tuple:
    Q_min = row[5]
    Q_max = row[5]
    Desc_min = (row[0], row[1], row[2], row[3], row[4])
    Desc_max = (row[0], row[1], row[2], row[3], row[4])
    return Q_min, Q_max, Desc_min, Desc_max

def analyze_by_day(reader, writer_week, writer_year) -> None:
    
    sum_year = 0
    sum_week = 0
    week_days = 0
    year_days = 0
    desc_week = None
    desc_year = None
    current_year = 0
    current_date = None
    first_row = True
    Q_min = None
    Q_max = None
    Time_min = None
    Time_max = None
    counter = 0


    for row in reader:
        if len(row) == 0 and first_row:
            print(">> Soubor je prázdný.")
            return 1
        try:
            row[2] = int(row[2])
            row[3] = int(row[3])
            row[4] = int(row[4])
            row[5] = float(row[5])

        except ValueError:
            print(">> Hodnota průtoku, nebo datum není reálné číslo.")
            return 1
        except IndexError:
            print(">> Vstupní data nemají správný formát.")
            return 1
        if row[5] <= 0:
            print(">> Dne " + str(row[4]) + ". " + str(row[3]) + ". " + str(row[2]) + " byl záporný, nebo nulový průtok.")
            continue
        if not is_valid((row[2], row[3], row[4])):
            print("datum špatný formát, nebo označnuje nexecistující den v roce (např. 29. 2. 2003).") 
            continue
        if first_row:
            Q_min, Q_max, Time_min, Time_max = init_min_max(row, Q_min, Q_max, Time_min, Time_max)
            first_row = False
        if not is_next(current_date, row[2:-1]):          # KOntrola, zda se v datech neobjevila mezera/chyba
            print(">> Mezera v datech. >>" + str(row) + "<<")
            counter = process_gap(current_date, row[2:-1])
        if week_days == 0:
            desc_week = (row[0], row[1], row[2], row[3], row[4])
        elif week_days == 7:
            desc_week, sum_week, week_days = print_week(writer_week, row, desc_week, sum_week, week_days)

        if sum_year == 0:
            desc_year = (row[0], row[1], row[2], row[3], row[4])
            current_year = row[2]
        elif current_year != row[2]:
            current_year = row[2]
            desc_year, sum_year, year_days = print_year(writer_year, row, desc_year, sum_year, year_days) 
        Time_min, Time_max, sum_week , Q_min, Q_max, week_days, current_date, sum_year, year_days = process_record(Time_min, Time_max, sum_week , Q_min, Q_max, week_days, row, current_date, sum_year, year_days)

    print_rest(writer_week, writer_year, desc_week, desc_year, sum_week, sum_year, week_days, year_days)
    print_Extremes(Q_max, Q_min, Time_max, Time_min)

try:
    with open("Tests/Test_4.csv", encoding = "utf-8", newline = "") as r, \
    open("vystup_7dni.csv", "w", encoding = "utf-8", newline = "") as w7, \
    open("vystup_rok.csv", "w", encoding = "utf-8", newline = "") as wr:

        reader = csv.reader(r, delimiter = ",")
        writer_week = csv.writer(w7, delimiter = ",")
        writer_year = csv.writer(wr, delimiter = ",")

        analyze_by_day(reader, writer_week, writer_year)

except FileNotFoundError:
    print(">> Soubor nebyl nalezen.")
except IOError:
    print(">> Chyba při čtení/zápisu.")
