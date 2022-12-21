from pyproj import Transformer
import json
from math import sqrt

def dist(source, finish):       ## Vzdálenost dvou bodů
    return sqrt((finish[0] - source[0])**2 + (finish[1] - source[1])**2)

def process(adresses, bins):
    max_adr = {'dist' : 0}
    adr = {'dist' : 10000}
    suma = 0
    counter = 0
    max_min_dist = 0
    for place in adresses['features']:
        counter += 1
        for can in bins['features']:
            if can['properties']['PRISTUP'] != "volně":
                continue
            coord = can['geometry']['coordinates']
            distance = dist(place['geometry']['coordinates'], can['geometry']['coordinates'])
            if adr['dist'] > distance:
                adr['street'] = place['properties']['addr:street']
                adr['streetnumber'] = place['properties']['addr:streetnumber']
                adr['dist'] = distance
        if adr['dist'] > max_adr['dist']:
            max_adr['street'] = adr['street']
            max_adr['streetnumber'] = adr['streetnumber']
            max_adr['dist'] = adr['dist']
        suma += adr['dist']
    mean = suma/counter
    print(mean)
    print(max_adr)

def only_free(bins):
    for idx, can in enumerate(bins['features']):
        if can['properties']['PRISTUP'] != "volně":
            bins['features'].remove(idx)

def change_coord(adresses):
    wgstojtsk = Transformer.from_crs(4326,5514, always_xy = True)
    for item in range(len(adresses['features'])):
        item['geometry']['coordinates'] = wgstojtsk.transform(*item['geometry']['coordinates'])

try:
    adresses = None
    bins = None
    with open("du_3/adresy.geojson", "r", encoding = 'utf-8') as adr, \
        open("du_3/kontejnery.json", "r", encoding = 'utf-8') as cont:
        adresses = json.load(adr)
        bins = json.load(cont)
            # Výběr volně přístupných kontejnerů
        only_free(bins)
            # Převod WGS84 na JTSK
        change_coord(adresses)
        
        process(adresses, bins)
except FileNotFoundError:
    print(">> Soubor s daným jménem neexistuje.")
except PermissionError:
    print(">> Ke čtení souboru nemáte práva.")
#except KeyError:
 #   print(">> Klíč nebyl ve slovníku nalezen.")

