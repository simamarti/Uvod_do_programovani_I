import csv

def is_leap(year : int) -> bool:
    if (year%4 == 0 and year%400 == 0) or (year%4 == 0 and year%100 != 0):
        return True
    return False

def input():
    with open("", encoding = "utf-8", newline = "") as r, \
    open("vystup_7dni.csv", "w", encoding = "utf-8", newline = "") as w7, \
    open("vystup_rok.csv", "w", encoding = "utf-8", newline = "") as wr:

        year = None
        day = 0
        month = 0
        day_counter = 0
        sum_week = 0
        counter_week = 0
        sum_year = 0
        start_day = None
        start_year = None

        reader = csv.reader(r, delimiter = ",")
        writer_7 = csv.writer(w7)
        writer_year = csv.writer(wr)

        for row in reader:
            if counter_week == 7:
                writer_7.writerow([row[0], row[1], start_day, round(sum_week/7, 4)])
                start_day = (row[2], row[3], row[4])
                counter_week = 0
                sum_week = 0
            counter_week += 1
            sum_week += row[5]

            if year != row[2]:
                writer_year.writerow([row[0], row[1], start_year, round(sum_year/365, 4)])
                start_year = (row[2], row[3], row[4])
                sum_week = 0
                year = row[2]
            sum_year += row[5]



            


