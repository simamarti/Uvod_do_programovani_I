from pyproj import Transformer
import json
from math import sqrt

def dist(source, finish) -> float:          # Vzdálenost dvou bodů
    return sqrt((finish[0] - source[0])**2 + (finish[1] - source[1])**2)

def only_free(bins : dist) -> None:         # Výběr pouze volně přístupných kontejnerů
    free_bins = []
    for can in bins['features']:
        if can['properties']['PRISTUP'] == "volně":
            free_bins.append(can)
    bins['features'] = free_bins

def change_coord(adresses : dist) -> None:  # Převod souřadnic z WGS84 do jtsk
    wgstojtsk = Transformer.from_crs(4326,5514, always_xy = True)
    for item in adresses['features']:
        item['geometry']['coordinates'] = wgstojtsk.transform(*item['geometry']['coordinates'])

def dist_calc(bins : list, coord_adr : list) -> int:
    min_dist = None
    for can in bins:
        coord_bin = can['geometry']['coordinates']
        distance = dist(coord_adr, coord_bin)
        if min_dist == None:
            min_dist = distance
        elif min_dist > distance:
            min_dist = distance
    return min_dist

def process(adresses : dist, bins : dist) -> tuple:
    average = 0
    min_distance = 0
    adress = None
    counter = 0
    max_dist = 0
    for item in adresses['features']:
        coord_adr = item['geometry']['coordinates']
        counter += 1
        min_distance = dist_calc(bins['features'], coord_adr)
        average += min_distance
        if min_distance > 10000:
            print(">> minimální vzdálenost k některému kontejneru přesáhla 10 km.") 
            exit(1)
        if max_dist < min_distance:
            max_dist = min_distance
            adress = [item['properties']['addr:street'], item['properties']['addr:housenumber']]
        min_distance = 0
    return average/counter, adress, max_dist

try:
    adresses = None         # slovník s adresami
    bins = None             # slovník s kontejnery
    far_adress = None       # Adresa, z které je to ke kontejneru nejdále
    average = 0             # Průměrná minimální vzdálenost

    with open("adresy copy.geojson", "r", encoding = 'utf-8') as adr, \
        open("kontejnery copy.json", "r", encoding = 'utf-8') as cont:
        adresses = json.load(adr)
        bins = json.load(cont)
        print(f"Počet načtených adres: {len(adresses['features'])}")
        print(f"Počet načtených kontejnerů: {len(bins['features'])}")
            # Výběr volně přístupných kontejnerů
        only_free(bins)
            # Převod WGS84 na S-JTSK
        change_coord(adresses)
        change_coord(bins)
        if  not len(bins['features']) or not len(adresses['features']):
            print(">> nebyly načteny žádné adresy nebo žádné veřejné kontejnery.")
        else:
            average, far_adress, max_dist = process(adresses, bins)
            print(f"Prumerna vzdalenost ke kontejneru je {round(average, 0)} m.")
            print(f"Nejdále ke kontejneru je z adresy {far_adress[0]} {far_adress[1]} a to {round(max_dist, 0)} m.")
except FileNotFoundError:
    print(">> Soubor s daným jménem neexistuje.")
except PermissionError:
    print(">> Ke čtení souboru nemáte práva.")
#except KeyError:
    #print(">> Klíč nebyl ve slovníku nalezen.")

