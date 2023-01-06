import quadtree
import json

def load():
    adresses = None
    try:
        with open("input.geojson", 'r', encoding = "utf-8") as file:
            adresses = json.load(file)
        return adresses
    except FileNotFoundError:
        SystemError(">> Soubor daného jména nebyl nalezen.")
    except PermissionError:
        SystemError(">> Uživatel nemá přístupová práva k souboru.")

def save(adresses):
    with open("output.geojson", 'w', encoding = "utf-8") as file:
        json.dump(adresses, file, ensure_ascii = False, indent = 2)

try:
    adresses = load()
    quadtree.quadtree(adresses)
    save(adresses)
except SystemError as sysError:
    print(sysError)