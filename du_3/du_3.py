from pyproj import Transformer
import json
import argparse

def dist(source :list, finish : list) -> float:          # Vzdálenost dvou bodů
    return ((finish[0] - source[0])**2 + (finish[1] - source[1])**2)**0.5

def is_private_for_adress(can : dict, house_adr : str) -> bool:
    if can['properties']['PRISTUP'] != "volně":
        if can['properties']['STATIONNAME'] == house_adr:
            return True
    return False

def change_coord(adresses : dist) -> None:  # Převod souřadnic z WGS84 do jtsk
    wgstojtsk = Transformer.from_crs(4326,5514, always_xy = True)
    for item in adresses['features']:
        item['geometry']['coordinates'] = wgstojtsk.transform(*item['geometry']['coordinates'])

def dist_calc(bins : list, coord_adr : list, adress : list) -> tuple:   # Kontejnery, souřadnice, číslo
    min_dist = None
    id_number = None
    for can in bins: 
        if is_private_for_adress(can, adress):
            min_dist = 0
            id_number = can['properties']['ID'] 
            break
        if can['properties']['PRISTUP'] == "volně":
            coord_bin = can['geometry']['coordinates']
            distance = dist(coord_adr, coord_bin)
            if min_dist == None or min_dist > distance:
                min_dist = distance
                id_number = can['properties']['ID'] 
    return min_dist, id_number
    
def update_stat(adress : list, item : dict, max_dist : float, sum : float, distance : float) -> tuple:
    sum += distance
    if max_dist <= distance:
        max_dist = distance
        adress = [item['properties']['addr:street'], item['properties']['addr:housenumber']]
    return adress, max_dist, sum, distance

def write_file_with_ID(adresses : dict) -> None:
    with open("adresy_kontejnery.geojson", "w", encoding = 'utf-8') as write_json:
        json.dump(adresses, write_json, ensure_ascii = False, indent = 2)

def median_calc(dist_array : list, counter : int) -> int:
    dist_array.sort()
    median = 0
    if counter%2 == 1:
        median = dist_array[counter//2]
    else:
        median = (dist_array[counter//2 - 1] + dist_array[counter//2])/2
    return median

def process(adresses : dist, bins : dist) -> tuple:
    suma = 0
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
        if min_distance >= 10000:
            raise SystemExit(">> Minimální vzdálenost přesáhla stanovený limit (10 km). Program byl ukončen.")
        item['kontejner'] = id_number
        dist_array.append(min_distance)
        adress, max_dist, suma, min_distance = update_stat(adress, item, max_dist, suma, min_distance)
    # Zápis do souboru adresy_kontejnery.geojson
    write_file_with_ID(adresses)
    # Výpočet mediánu
    median = median_calc(dist_array, counter)
    return suma/counter, median, adress, max_dist

def file_open(file_name : str) -> dict:
    try:
        with open(file_name, "r", encoding = 'utf-8') as file:
            dictionary = json.load(file)
        return dictionary
    except FileNotFoundError:
        raise SystemExit(f">> Soubor s názvem <{file_name}> neexistuje.")
    except PermissionError:
        raise SystemExit(f">> Ke čtení souboru s názvem <{file_name}> nemáte práva.")

try:
    adresses = None         # slovník s adresami
    bins = None             # slovník s kontejnery
    far_adress = None       # Adresa, z které je to ke kontejneru nejdále
    average = 0             # Průměrná minimální vzdálenost
        # Parametry programu
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--adress", action = "store", dest = "adr", default = "adresy.geojson")
    parser.add_argument("-k","--container", action = "store", dest = "cont", default = 'kontejnery.geojson')
    arguments = parser.parse_args()

    adresses = file_open(arguments.adr)
    bins = file_open(arguments.cont)   

    print(f"Počet načtených adres: {len(adresses['features']):.0f}")
    print(f"Počet načtených kontejnerů: {len(bins['features']):.0f}")
            # Převod WGS84 na S-JTSK
    change_coord(adresses)
    
    if  not len(bins['features']) or not len(adresses['features']):
        print(">> nebyly načteny žádné adresy nebo žádné veřejné kontejnery, program byl ukončen.")
    else:
        average, median, far_adress, max_dist = process(adresses, bins)
        print(f"Prumerná minimální vzdalenost ke kontejneru je {round(average, 0):.0f} m.")
        print(f"Medián minimálních vzdáleností ke kontejnerům je {round(median, 0):.0f} m.")
        print(f"Nejdále ke kontejneru je z adresy {far_adress[0]} {far_adress[1]} a to {round(max_dist, 0):.0f} m.")
except KeyError:
    print(">> Klíč nebyl ve slovníku nalezen.")
except ValueError:
    print(">> Špatný formát vstupu.")
except SystemExit as sysErr:
    print(sysErr)
