import requests
import folium
import webbrowser


def obtenir_villes_par_departement(departement, population_minimale):
    url = f"https://geo.api.gouv.fr/departements/{departement}/communes"

    params = {
        'fields': 'nom,population,centre,codeDepartement',
        'format': 'json',
        'geometry': 'centre',
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Erreur lors de la récupération des données pour le département {departement}")
        return []

    villes = response.json()

    villes_filtrees = [ville for ville in villes if
                       'population' in ville and ville['population'] >= population_minimale]

    return villes_filtrees


def afficher_carte(villes_total):
    if villes_total:
        centre_carte = [villes_total[0]['centre']['coordinates'][1], villes_total[0]['centre']['coordinates'][0]]
    else:
        centre_carte = [48.8566, 2.3522]

    carte = folium.Map(location=centre_carte, zoom_start=6)

    for ville in villes_total:
        nom_ville = ville['nom']
        population = ville['population']
        lat = ville['centre']['coordinates'][1]
        lon = ville['centre']['coordinates'][0]

        folium.Marker(
            location=[lat, lon],
            popup=f"{nom_ville} (Population: {population})",
            tooltip=nom_ville
        ).add_to(carte)

    fichier_html = f"carte_villes_multi_departements.html"
    carte.save(fichier_html)
    print(f"Carte enregistrée sous le nom: {fichier_html}")

    webbrowser.open(fichier_html)


def interface_utilisateur():
    villes_total = []

    while True:
        departement = input("Entrez le code du département (ou tapez 'fin' pour terminer) : ")

        if departement.lower() == 'fin':
            break

        try:
            population_minimale = int(
                input(f"Entrez le nombre minimum d'habitants pour le département {departement} : "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        villes = obtenir_villes_par_departement(departement, population_minimale)

        if villes:
            print(f"\nVilles du département {departement} avec plus de {population_minimale} habitants :")
            for ville in villes:
                print(f"- {ville['nom']} (Population: {ville['population']})")

            villes_total.extend(villes)
        else:
            print(
                f"Aucune ville trouvée dans le département {departement} avec plus de {population_minimale} habitants.")

    if villes_total:
        afficher_carte(villes_total)
    else:
        print("Aucune ville trouvée au total.")


if __name__ == "__main__":
    interface_utilisateur()
