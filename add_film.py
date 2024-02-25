# Skript pro přidání nového filmu do seznamu

# Načtu knihovny
from imdb import IMDb
import pandas as pd
import re
import os

# Načtu data
nove = pd.read_csv("/var/www/html/data/odkazy.csv", index_col=False)
seznam_filmu = pd.read_csv("/var/www/html/data/filmy.csv", index_col=False)

# Definuji funkci na získání informací o filmu na základě URL z csv s filmy k přidání
def get_movie_info(row):
    # url jsou řádky ve sloupci IMDb odkaz
    url = row["IMDb Odkaz"]

    # Následující řádek kódu vytváří instanci třídy IMDb a přiřazuje ji proměnné ia.
    # Třída IMDb je součástí knihovny Cinemagoer a poskytuje metody pro získávání informací z databáze filmů IMDb.
    # Proměnná ia se poté používá k volání metod třídy IMDb a získávání informací o filmech.
    ia = IMDb()

    # Vyhledám ID filmu z odkazu pomocí regulárního výrazu
    movie_id = re.findall(r'\d+', url)[0]

    # Načtu si film
    movie = ia.get_movie(movie_id)

    # A získám potřebné údaje:
    # Titulek
    title = movie["title"]

    # Rok vydání
    year = movie["year"]

    # Žánry
    genres = movie["genres"]
    # Pokud je žánr uveden
    if "genres" in movie.data:
        # Budu přeformátovávat pole na string, deklaruji proměnnou se separátorem
        separator = "/"
        # Aplikuji separátor
        result = separator.join(genres)
        # A vrátím výsledek
        genres = result
    # V opačném případě vrátím None
    else:
        genres = None

    # Režie
    # Pokud máme informace o režisérech
    if "director" in movie.data:
        # Vytvořím seznam s odkazy na režiséry
        directors = []
        # Procházím režiséry cylkem for
        for director in movie["director"]:
            # A jejich jména ukládám do proměnné
            name = director["name"]
            # A přidávám do pole se jmény režiséru
            directors.append(name)
        # Nakonec přidám režiséry do jednoho textového řetězce    
        director_names = ', '.join(directors)
    # V opačném případě None
    else:
        director_names = None

    # Hodnocení
    rating = movie["rating"]

    # Promítnuto
    promitnuto = False

    # Krátká verze URL
    url_short = ia.get_imdbURL(movie)


    # A nakonec všechna data vrátím: Film, Rok vydání, Žánr, Režie, Hodnocení IMDb, Promítnuto, IMDb ID, IMDb stránka
    return title, year, genres, director_names, rating, promitnuto, movie_id, url_short



# Nyní aplikuji definovanou funkci na načtená data

# Ověřím, jestli seznam s filmy k přidání obsahuje položky k přidání
if not nove.empty:
    # Použiji funkci apply na DataFrame nove a získám informace o filmech
    nove_info = nove.apply(get_movie_info, axis=1, result_type='expand')

    # Přejmenuji sloupce nového DataFrame
    nove_info.columns = ["Film", "Rok vydání", "Žánr", "Režie", "Hodnocení IMDb", "Promítnuto", "IMDb ID", "IMDb stránka"]

    # Připojím nový DataFrame k seznam_filmu
    seznam_filmu = pd.concat([seznam_filmu, nove_info], ignore_index=True)

    # Definuji požadované sloupce a jejich pořadí
    new_order = ["Film", "Rok vydání", "Žánr", "Režie", "Hodnocení IMDb", "Promítnuto", "IMDb ID", "IMDb stránka"]

    # Vyfiltruji pouze požadované sloupce a seřadím je podle definovaného pořadí
    seznam_filmu = seznam_filmu[new_order]

    # Odstraním případné duplicitní řádky
    seznam_filmu = seznam_filmu.drop_duplicates()

    # Exportuji data do csv
    seznam_filmu.to_csv("/var/www/html/data/filmy.csv")

    ## Odstraním soubor s filmy k přidání
    os.system('rm /var/www/html/data/odkazy.csv')

    # Vytvořím nové csv s příslušnou hlavičkou
    os.system('echo "IMDb Odkaz" > /var/www/html/data/odkazy.csv')

    # A upravím u csv práva tak, aby fungoval PHP skript
    os.system('chmod a+rw /var/www/html/data/odkazy.csv')
