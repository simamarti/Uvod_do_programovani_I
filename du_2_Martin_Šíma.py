import csv
import math

def is_leap(year : int) -> bool:
    if (year%4 == 0 and year%400 == 0) or (year%4 == 0 and year%100 != 0):
        return True
    return False

def add_to_year(sum_year : int, year_days : int, row) -> tuple:
    year_days += 1
    sum_year += float(row[5])
    return sum_year, year_days

def add_to_week(Time_min : tuple, Time_max : tuple, sum_week : float, Q_min : float, Q_max : float, week_days : int, row) -> tuple:
    if Q_max < float(row[5]):
        Q_max = float(row[5])
        Time_max = (row[0], row[1], row[2], row[3], row[4])
    if Q_min > float(row[5]):
        Q_min = float(row[5])
        Time_min = (row[0], row[1], row[2], row[3], row[4])
    sum_week += float(row[5])
    week_days += 1
    return Time_min, Time_max, sum_week , Q_min, Q_max, week_days

def print_week(writer_week, row, desc_week : tuple, sum_week : int, week_days : int) -> tuple:
    writer_week.writerow([desc_week[0], desc_week[1], desc_week[2], desc_week[3], desc_week[4], round(sum_week/7, 4)])
    sum_week = 0
    week_days = 0
    desc_week = (row[0], row[1], row[2], row[3], row[4])
    return desc_week, sum_week, week_days

def print_year(writer_year, row, desc_year : tuple, sum_year : int, year_days : int) -> tuple:
    writer_year.writerow([desc_year[0], desc_year[1], desc_year[2], desc_year[3], desc_year[4], round(sum_year/365, 4)])
    desc_year = (row[0], row[1], row[2], row[3], row[4])
    year_days = 0
    sum_year = 0
    return desc_year, sum_year, year_days

def print_rest( writer_week, writer_year, desc_week : tuple, desc_year : tuple, sum_week : int, 
                sum_year : int, week_days : int, year_days : int) -> None:
        
        if week_days:
            writer_week.writerow([desc_week[0], desc_week[1], desc_week[2], desc_week[3], desc_week[4], round(sum_week/week_days, 4)])
        if year_days:
            writer_year.writerow([desc_year[0], desc_year[1], desc_year[2], desc_year[3], desc_year[4], round(sum_year/year_days, 4)])

def print_Extremes(Q_max : float, Q_min : float, Time_max : tuple, Time_min : tuple) -> None:

        print("Maximální průtok: " + str(Time_max[0]) + ", " + str(Time_max[1]) + ", " + str(Time_max[2])
         + ", " + str(Time_max[3]) + ", " + str(Time_max[4]) + ", " + str(Q_max))
        print("Minimální průtok: " + str(Time_min[0]) + ", " + str(Time_min[1]) + ", " + str(Time_min[2])
         + ", " + str(Time_min[3]) + ", " + str(Time_min[4]) + ", " + str(Q_min))

def init_min_max(row, Q_min : float, Q_max : float, Time_min : tuple, Time_max : tuple) -> tuple:
    Q_min = float(row[5])
    Q_max = float(row[5])
    Time_min = (row[0], row[1], row[2], row[3], row[4])
    Time_max = (row[0], row[1], row[2], row[3], row[4])
    return Q_min, Q_max, Time_min, Time_max

def analyze() -> None:
    with open("Test_1.csv", encoding = "utf-8", newline = "") as r, \
    open("vystup_7dni.csv", "w", encoding = "utf-8", newline = "") as w7, \
    open("vystup_rok.csv", "w", encoding = "utf-8", newline = "") as wr:

        reader = csv.reader(r, delimiter = ";")
        writer_week = csv.writer(w7)
        writer_year = csv.writer(wr)

        analyze_by_day(reader, writer_week, writer_year)

def analyze_by_day(reader, writer_week, writer_year) -> None:

    sum_year = 0
    sum_week = 0
    week_days = 0
    year_days = 0
    desc_week = None
    desc_year = None
    current_year = 0
    first_row = True
    Q_min = None
    Q_max = None
    Time_min = None
    Time_max = None

    for row in reader:
        if first_row:
            Q_min, Q_max, Time_min, Time_max = init_min_max(row, Q_min, Q_max, Time_min, Time_max)
            first_row = False
        if row == "":
            continue
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

        Time_min, Time_max, sum_week , Q_min, Q_max, week_days = add_to_week(Time_min, Time_max, sum_week , Q_min, Q_max, row, week_days)
        sum_year, year_days = add_to_year(sum_year, year_days, row)
    
    print_rest(writer_week, writer_year, desc_week, desc_year, sum_week, sum_week, week_days, year_days)
    print_Extremes(Q_max, Q_min, Time_max, Time_min)

analyze()


            


