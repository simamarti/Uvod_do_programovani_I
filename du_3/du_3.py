from pyproj import Transformer
import json
from math import sqrt
import argparse

def dist(source, finish) -> float:          # Vzdálenost dvou bodů
    return sqrt((finish[0] - source[0])**2 + (finish[1] - source[1])**2)

def is_private(can : dict, house_adr : list) -> int:
    if can['properties']['PRISTUP'] != "volně":
        if can['properties']['STATIONNAME'] == house_adr:
            return True
    return False

def change_coord(adresses : dist) -> None:  # Převod souřadnic z WGS84 do jtsk
    wgstojtsk = Transformer.from_crs(4326,5514, always_xy = True)
    for item in adresses['features']:
        item['geometry']['coordinates'] = wgstojtsk.transform(*item['geometry']['coordinates'])

def dist_calc(bins : list, coord_adr : list, adress : list) -> tuple:   # Kontejnery, souřadnice, číslo
    min_dist = 10000
    id_number = None
    for can in bins: 
        if is_private(can, adress):
            min_dist = 0
            id_number = can['properties']['ID'] 
            break
        if can['properties']['PRISTUP'] == "volně":
            coord_bin = can['geometry']['coordinates']
            distance = dist(coord_adr, coord_bin)
            if min_dist > distance:
                min_dist = distance
                id_number = can['properties']['ID'] 
    if min_dist >= 10000:
        print(">> Minimální vzdálenost přesáhla stanovený limit (10 km).")
        exit(0)
    return min_dist, id_number

def process(adresses : dist, bins : dist) -> tuple:
    average = 0
    min_distance = 0
    dist_array = []
    adress = None
    counter = 0
    max_dist = 0
    median = 0
    id_number = 0
    for item in adresses['features']:
        coord_adr = item['geometry']['coordinates']
        house_adr = f"{item['properties']['addr:street']} {item['properties']['addr:housenumber']}"

        counter += 1

        min_distance, id_number = dist_calc(bins['features'], coord_adr, house_adr)
        item['kontejner'] = id_number
        dist_array.append(min_distance)
        average += min_distance
        if min_distance > 10000:
            print(">> minimální vzdálenost k některému kontejneru přesáhla 10 km.") 
            exit(1)
        if max_dist <= min_distance:
            print(f"{adress},{max_dist}")
            max_dist = min_distance
            adress = [item['properties']['addr:street'], item['properties']['addr:housenumber']]
        # Zápis do souboru adresy_kontejnery.geojson
    with open("adresy_kontejnery.geojson", "w", encoding = 'utf-8') as write_json:
        json.dump(adresses, write_json, ensure_ascii = False, indent = 2)
        # Výpočet mediánu
    dist_array.sort()
    if counter%2 == 1:
        median = dist_array[counter//2]
    else:
        median = (dist_array[counter//2 - 1] + dist_array[counter//2])/2
    return average/counter, median, adress, max_dist

try:
    adresses = None         # slovník s adresami
    bins = None             # slovník s kontejnery
    far_adress = None       # Adresa, z které je to ke kontejneru nejdále
    average = 0             # Průměrná minimální vzdálenost
        # Parametry programu
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--adress", action = "store", dest = "adr", default = "adresy copy.geojson")
    parser.add_argument("-k","--container", action = "store", dest = "cont", default = "kontejnery copy.json")
    arguments = parser.parse_args()

    with open(arguments.adr, "r", encoding = 'utf-8') as adr, \
        open(arguments.cont, "r", encoding = 'utf-8') as cont:
        adresses = json.load(adr)
        bins = json.load(cont)
        print(f"Počet načtených adres: {len(adresses['features'])}")
        print(f"Počet načtených kontejnerů: {len(bins['features'])}")
            # Převod WGS84 na S-JTSK
        change_coord(adresses)
        #change_coord(bins)
        if  not len(bins['features']) or not len(adresses['features']):
            print(">> nebyly načteny žádné adresy nebo žádné veřejné kontejnery.")
        else:
            average, median, far_adress, max_dist = process(adresses, bins)
            print(f"Prumerná minimální vzdalenost ke kontejneru je {round(average, 0)} m.")
            print(f"Medián minimálních vzdáleností ke kontejnerům je {round(median, 0)} m.")
            print(f"Nejdále ke kontejneru je z adresy {far_adress[0]} {far_adress[1]} a to {round(max_dist, 0)} m.")
except FileNotFoundError:
    print(">> Soubor s daným jménem neexistuje.")
except PermissionError:
    print(">> Ke čtení souboru nemáte práva.")
except KeyError:
    print(">> Klíč nebyl ve slovníku nalezen.")