# Skript pro výběr náhodného filmu ze seznamu

# Importuji knihovny
from imdb import IMDb
import pandas as pd
import random

# Následující řádek kódu vytváří instanci třídy IMDb a přiřazuje ji proměnné ia.
# Třída IMDb je součástí knihovny Cinemagoer a poskytuje metody pro získávání informací z databáze filmů IMDb.
# Proměnná ia se poté používá k volání metod třídy IMDb a získávání informací o filmech.
ia = IMDb()

# Načtu data, ze kterých budu film vybírat
seznam_filmu = pd.read_csv("/var/www/html/data/filmy.csv")

# Vytvořím prázdné pole, které naplním ID filmů k promítání
k_promitani = []

# Procházím seznam filmu prvek po prvku
for i in seznam_filmu.index:
  # Pokud film nebyl promítnut
  if not seznam_filmu["Promítnuto"][i]:
    # Přidám jej do seznamu k výběru
    nepromitnuty_film = seznam_filmu["IMDb ID"][i]
    k_promitani.append(nepromitnuty_film)

# Vylosuji vítězný film
vitez = k_promitani[random.randint(0, len(k_promitani) - 1)]
# Uložím si ID vybraného filmu do separátní proměnné na později
id_edit = vitez
# A vyberu jej z instance třídy IMDb tak, abych mohl vypsat info o filmu
vitez = ia.get_movie(vitez)

print("Příště promítáme:\n")

print("Název:", vitez["title"])

print("Rok:", vitez["year"])

print("Hodnocení:", vitez["rating"])

print("Délka:", vitez["runtime"][0], "minut")

# Pokud je žánr uveden
if "genres" in vitez.data:
  # Vyberu si žánry a uložím do proměnné
  genres = vitez["genres"]
  # Budu přeformátovávat pole na string, deklaruji proměnnou se separátorem
  separator = "/"
  # Aplikuji separátor
  result = separator.join(genres)
  # A vrátím výsledek
  print("Žánry:", result)

# Pokud jsou země původu uvedeny
if "countries" in vitez.data:
  # Vyberu si země pvůodu a uložím do proměnné
  countries = vitez["countries"]
  # Budu přeformátovávat pole na string, deklaruji proměnnou se separátorem
  separator = ", "
  # Aplikuji separátor
  result = separator.join(countries)
  # A vrátím výsledek
  print("Země původu:", result)

# Pokud jsou herci uvedeni
if "cast" in vitez.data:
  # Deklaruji pole pro herce
  cast = []
  # Procházím režiséry cylkem for
  for actor in vitez["cast"][:5]:
    # A jejich jména ukládám do proměnné
    name = actor["name"]
    # A přidávám do pole se jmény herců
    cast.append(name)
  # Nakonec přidám herce do jednoho textového řetězce    
  actors_names = ", ".join(cast)
  print("Hlavní herci/herečky:", actors_names)

# Pokud je režie uvedena
if "director" in vitez.data:
  # Deklaruji pole pro režiséry
  directors = []
  # Procházím režiséry cylkem for
  for director in vitez["director"]:
    # A jejich jména ukládám do proměnné
    name = director["name"]
    # A přidávám do pole se jmény režiséru
    directors.append(name)
  # Nakonec přidám režiséry do jednoho textového řetězce    
  director_names = ", ".join(directors)
  print("Režie:", director_names)

# Pokud je popisek filmu uveden
if "plot outline" in vitez.data:
  # Vypíšu jej
  print("Popisek filmu:", vitez["plot outline"])

# Nakonec přepíšu hodnotu sloupce "Promítnuto" vybraného filmu na True
seznam_filmu.loc[seznam_filmu["IMDb ID"] == id_edit, "Promítnuto"] = True

# Definuji požadované sloupce a jejich pořadí
new_order = ["Film", "Rok vydání", "Žánr", "Režie", "Hodnocení IMDb", "Promítnuto", "IMDb ID", "IMDb stránka"]

# Vyfiltruji pouze požadované sloupce a seřadím je podle definovaného pořadí
seznam_filmu = seznam_filmu[new_order]

# A exportuji data do csv
seznam_filmu.to_csv("/var/www/html/data/filmy.csv")
