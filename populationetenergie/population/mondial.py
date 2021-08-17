import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from compare import compare, compare_total
from predict_pop import prediction
from read_data import age_group_type, data_to_2D_table
import sys
chemin_absolu = 'C:\\Users\\cotil\\Desktop\\COURS\\Mines\\Energie_et_societe\\Poster\\PopulationEtEnergie\\'


sys.path.append(chemin_absolu + 'populationetenergie\\io')


datafolder = chemin_absolu + 'populationetenergie\\data\\'


def determine_annee(pays: str, information):
    liste_annee = information.index.values[5::]
    annee_valide = []

    for annee in liste_annee[::-1]:
        i = 0
        continu = True

        while continu:
            if annee - i in liste_annee and information.loc[annee - i, "age"] == 1 and len(annee_valide) < 8:
                annee_valide.append(annee - i)
                i += 1
            elif len(annee_valide) > 3:
                return annee_valide[-1], annee_valide[0]
            else:
                annee_valide = []
                continu = False
    print("ERREUR de plage d'annee !!!!!")

# print(determine_annee(pays,age_group_info))


# Pour créer les fichiers en forme csv

def to_fichier_csv(fichier):

    lec = pd.read_csv(datafolder + fichier + '.csv')
    print(lec.columns)
    lec_by_country = lec.groupby('Country or Area')

    for name, subdf in lec_by_country:
        # print(
        # f"La dataframe de clé '{name}' a {subdf.shape[0]} éléments sur les {lec.shape[0]}")
        subdf.to_csv(datafolder + name + '1' + '.csv')


def predict_pop(pays: str, pas=1):
    ''' Lit et nettoye les données puis renvoie une prédiction de population entre 2010 et 2050
    grâce aux données entre des bonnes années. Pour choisir les années, il faut des années consecutives où l'on a  les données pour tous les ages (colonne age de age_group_type). Il ne faut pas hésiter à revenir aux talbeaux csv pour avoir une idée plus précises de la forme des données '''
    # On lit les données fornies par le site : http://data.un.org/Data.aspx?d=POP&f=tableCode%3a22
    arret = False

    data = pd.read_csv(datafolder+pays+'.csv',
                       usecols=['Year', 'Sex', 'Age', 'Value'], skipfooter=0)

    # On garde que les lignes intéressantes
    data = data[data['Age'] != 'Unknown']
    data = data[data['Age'] != 'Total']
    data = data[data['Sex'] == 'Both Sexes']
    # On supprime les données en double
    data = data.drop_duplicates(subset=['Year', 'Sex', 'Age'])
    # print(data)
    # On récupère les informations sur les groupes d'âges
    age_group_info = age_group_type(data)
    age_group_info.to_csv(datafolder+pays+'_info_age.csv')
    print(age_group_info)
    year_0, year_n = determine_annee(pays, age_group_info)

    while year_n - year_0 >= 4 and arret == False:
        try:
            year_i, year_f = year_0, 2070

            print(year_0, year_n)
            population_table = data_to_2D_table(data, age_group_info)
            population_table.index.name = 'year'
            population_table.to_csv(datafolder+pays+'_données_ordonnées.csv')

            pred, theorie, erreur = prediction(
                population_table, year_0, year_n, year_i, year_f, pas)
            # print(erreur)
            pred.to_csv(datafolder+pays+'_pred.csv')
            theorie.to_csv(datafolder+pays+'_theo.csv')
            population = compare(pred, theorie, pays)
            arret = True
            return population
        except RuntimeError:
            year_n -= 1
            print(year_0, year_n)
            population_table = data_to_2D_table(data, age_group_info)
            population_table.index.name = 'year'
            population_table.to_csv(datafolder+pays+'_données_ordonnées.csv')

            pred, theorie, erreur = prediction(
                population_table, year_0, year_n, year_i, year_f, pas)
            # print(erreur)
            pred.to_csv(datafolder+pays+'_pred.csv')
            theorie.to_csv(datafolder+pays+'_theo.csv')
            population = compare(pred, theorie, pays)
            return population


def liste_pays(fichier):
    """
    renvoie la liste des pays inclus dans un fichier csv
    """
    liste_pays = []
    lec = pd.read_csv(datafolder + fichier + '.csv')
    # print(len(lec))
    lec_by_country = lec.groupby('Country or Area')

    for name, subdf in lec_by_country:
        if name.isdigit() or name == "footnoteSeqID":
            continue
        liste_pays.append(name)
    return liste_pays


pays_dev_total = ['Algeria1', 'Argentina1', 'Australia', 'Austria', 'Belarus1', 'Belgium1',
                  'Bulgaria1', 'Canada', 'Chile1', 'China, Hong Kong SAR1', 'China1', 'Croatia1', 'Czechia1', 'Denmark1', 'Estonia1', 'Ecuador1', 'Finland1', 'France1', 'Germany', 'Greece1', 'Georgia1', 'Honduras1', 'Hungary1', 'Iceland1', 'Ireland1', 'Italy1', 'Japan', 'Latvia1', 'Lebanon1', 'Lithuania1', 'Luxembourg1', 'Malta1', 'Mexico1', 'Montenegro1', 'Morocco1', 'Netherlands1', 'New Zealand1', 'Norway', 'Paraguay1', 'Peru1', 'Poland1', 'Portugal1', 'Republic of Korea1', 'Republic of Moldova1', 'Romania1', 'Russie', 'Serbia1', 'Slovakia1', 'Slovenia1', 'South Africa1', 'Spain1', 'Sweden1', 'Switzerland1', 'Tunisia1', 'Turkey1', 'United Kingdom of Great Britain and Northern Ireland1', 'Ukraine1', 'Uruguay1', "US"]
pays_fin_dev_total = ['Armenia1', 'Azerbaijan1', 'Belize1', 'Brazil1', 'Cambodia1', 'Colombia1', 'Costa Rica1', 'Cuba1', 'El Salvador1', 'Greenland1', 'Grenada1', 'Guatemala1', 'Guyana1', 'India1', 'Indonesia1', 'Iran (Islamic Republic of)1', 'Iraq1', 'Libya1', 'Micronesia (Federated States of)1', 'Nicaragua1', 'Pakistan1', 'Panama1', 'Papua New Guinea1', 'Philippines1', 'Saudi Arabia1', 'Senegal1', 'Suriname1', 'Sri Lanka1', 'Tajikistan1', 'Thailand1', 'Turkmenistan1', 'United Arab Emirates1', 'Venezuela (Bolivarian Republic of)1', 'Viet Nam1', 'Yemen1',
                      'Kazakhstan1', 'Mongolia1',  'Qatar1']
pays_en_dev_total = ['Afghanistan1', 'Angola1',
                     'Bangladesh1', 'Bhutan1', 'Botswana1', 'Burkina Faso1', 'Burundi1', 'Cameroon1', 'Central African Republic1', 'Chad1', 'Congo1', 'Côte d\'Ivoire1', 'Djibouti1', 'Dominican Republic1', 'Kyrgyzstan', 'Equatorial Guinea1', 'Ethiopia1', 'Fiji1', 'Gabon1', 'Gambia1', 'Ghana1', 'Guinea1', 'Jordan1', 'Kenya1', 'Kuwait1', 'Lesotho1', 'Liberia1', 'Madagascar1', 'Malawi1', 'Mali1', 'Mauritania1', 'Mozambique1', 'Myanmar1', 'Namibia1', 'Nepal1', 'Niger1', 'Nigeria1', 'Republic of South Sudan1', 'Rwanda1', 'Sierra Leone1', 'Somalia1', 'Sudan1', 'Syrian Arab Republic1', 'Togo1', 'Uganda1', 'Uzbekistan1', 'Zambia1', 'Zimbabwe1']

Pays_fonctionne = ['Albania', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Åland Islands', 'Bahamas', 'Belgium', 'Bermuda', 'Bulgaria', 'Canada', 'China, Macao SAR', 'Croatia', 'Cuba', 'Czechia', 'Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'Greece', 'Guam', 'Guernsey', 'Hungary', 'Iceland', 'Italy', 'Japan', 'Jersey', 'Kazakhstan', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Maldives', 'Malta',
                   'Mauritius', 'Mongolia', 'Montenegro', 'Netherlands', 'New Zealand', 'Norway', 'Pitcairn', 'Poland', 'Portugal', 'Qatar', 'Republic of Korea', 'Republic of Moldova', 'Romania', 'Russian Federation', 'San Marino', 'Serbia', 'Seychelles', 'Slovakia', 'Slovenia', 'Sweden', 'Switzerland', 'United Kingdom of Great Britain and Northern Ireland', 'Uzbekistan']
Pays_dev = ['Australia', 'Austria', 'Belgium1',
            'Bulgaria1', 'Canada', 'Croatia1', 'Czechia1', 'Denmark1', 'Estonia1', 'Finland1', 'Greece1', 'Hungary1', 'Iceland1', 'Italy1', 'Japan', 'Lithuania1', 'Luxembourg1', 'Netherlands1', 'New Zealand1', 'Norway', 'Poland1', 'Portugal1', 'Romania1', 'Serbia1', 'Slovakia1', 'Slovenia1', 'Sweden1', 'United Kingdom of Great Britain and Northern Ireland1', "US"]
Pays_fin_dev = ['Kazakhstan1', 'Mongolia1',  'Qatar1']
Pays_en_dev = ['Kyrgyzstan', 'Uzbekistan1']

# Analyse générale des données sans approximation

annee_finale = 2070


def calc(pays):
    """
    calcul le pourcentage moyen de croissance d'un pays sur des periodes de 5 ans de 2020 a 2050
    il faut d'abord avoir lance predic_pop sur le pays en question pour construire data
    """
    data = pd.read_csv(datafolder+pays+'_pred.csv', index_col="year")
    taux = []
    taux.append(0)
    for i in range(1, annee_finale - 2020 + 1):
        pop1 = data.loc[2020+i-1][-1]
        pop2 = data.loc[2020+i][-1]
        taux.append((pop2-pop1)/pop1 * 100)
    print(f"Calc fait pour {pays}")
    return taux


PD_calc_dev = {}
for pays in Pays_dev:
    PD_calc_dev[pays] = calc(pays)

with open(datafolder + "moyenne_dev.csv", "w") as f:
    f.write("Pays")
    for i in range(20, annee_finale-2000+1):
        f.write(f",{i}")
    f.write('\n')

    for pays in PD_calc_dev:
        f.write(f"{pays}, ")
        for i in range(annee_finale - 2020):
            f.write(f"{PD_calc_dev[pays][i]:.3f}, ")
        f.write(f"{PD_calc_dev[pays][annee_finale - 2020]:.3f}\n")

#  f"{pays}, {PD_calc_dev[pays][0]}, {PD_calc_dev[pays][1]}, {PD_calc_dev[pays][2]}, {PD_calc_dev[pays][3]}, {PD_calc_dev[pays][4]}, {PD_calc_dev[pays][5]}, {PD_calc_dev[pays][6]}, {PD_calc_dev[pays][7]}, {PD_calc_dev[pays][8]}, {PD_calc_dev[pays][9]}, {PD_calc_dev[pays][10]}, {PD_calc_dev[pays][11]}, {PD_calc_dev[pays][12]}, {PD_calc_dev[pays][13]}, {PD_calc_dev[pays][14]}, {PD_calc_dev[pays][15]}, {PD_calc_dev[pays][16]}, {PD_calc_dev[pays][17]}, {PD_calc_dev[pays][18]}, {PD_calc_dev[pays][19]}, {PD_calc_dev[pays][20]}, {PD_calc_dev[pays][21]}, {PD_calc_dev[pays][22]}, {PD_calc_dev[pays][23]}, {PD_calc_dev[pays][24]}, {PD_calc_dev[pays][25]}, {PD_calc_dev[pays][26]}, {PD_calc_dev[pays][27]}, {PD_calc_dev[pays][28]}, {PD_calc_dev[pays][29]}, {PD_calc_dev[pays][30]}\n")

taux_moy_dev = []
taux_moy_fin_dev = calc("Kazakhstan1")
taux_moy_en_dev = calc("Mongolia1")
data = pd.read_csv(datafolder + "moyenne_dev.csv")

for i in range(annee_finale - 2020 + 1):
    taux_moy_dev.append(data[f"{20+i}"].describe().loc["mean"])

annees = np.arange(2020, annee_finale + 1, 1)

population = np.zeros((annee_finale - 2020 + 1, 1))
population2 = np.zeros((annee_finale - 2020 + 1, 1))
population3 = np.zeros((annee_finale - 2020 + 1, 1))

initial_2020_dev = 0
for pays in pays_dev_total:
    data = pd.read_csv(datafolder + pays + ".csv")
    pop_pays = data.iloc[0][-2]
    initial_2020_dev += pop_pays
population[0] = initial_2020_dev + 1e8

initial_2020_fin_dev = 0
for pays in pays_fin_dev_total:
    data = pd.read_csv(datafolder + pays + ".csv")
    pop_pays = data.iloc[0][-2]
    initial_2020_fin_dev += pop_pays
population2[0] = initial_2020_fin_dev + 2e8

initial_2020_en_dev = 0
for pays in pays_en_dev_total:
    data = pd.read_csv(datafolder + pays + ".csv")
    pop_pays = data.iloc[0][-2]
    initial_2020_en_dev += pop_pays
population3[0] = initial_2020_en_dev + 3e8

for i in range(1, annee_finale - 2020 + 1):
    population[i] = population[i-1]*(1+taux_moy_dev[i]/100)

for i in range(1, annee_finale - 2020 + 1):
    population2[i] = population2[i-1]*(1+taux_moy_fin_dev[i]/100)

for i in range(1, annee_finale - 2020 + 1):
    population3[i] = population3[i-1]*(1+taux_moy_en_dev[i]/100)

plt.stackplot(annees, population.T, population2.T, population3.T, labels=(
    "Développé", "Fin de développement", "En développement"))
#plt.plot(annees, population + population2)
#plt.plot(annees, population3 + population2 + population)
plt.xlabel("Année")
plt.ylabel("Population en milliards")
plt.yticks([1e9, 2e9, 3e9, 4e9, 5e9, 6e9, 7e9, 8e9, 9e9, 10e9], [
           '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
print((population3 + population2 + population))
print(population)
print(population2)
print(population3)

plt.show()

# Les données interessantes

# Choix des pays par région et population associée

#Denmark = predict_pop("Denmark1")
#Kazakhstan = predict_pop("Kazakhstan1")
#Mongolie = predict_pop("Mongolia1")

# Taux de croissance par années de 2020 à 2050 bornes incluses

# print(calc("Denmark1"))
# print(taux_moy_dev)
# print(calc("Kazakhstan1"))
# print(calc("Mongolia1"))

# population par region de 2020 à 2050 bornes incluses

population_dev = population  # on prend un taux de croissance moyen global
population_fin_dev = population2  # on prend le taux de croissance du Kazakhstan
population_en_dev = population3  # on prend le taux de croissance du Senegal


# Approximation linéaire avec les données de United Nations

annual_rate = {"Senegal": 2.7}


def add_year(years, pays, annual_rate):
    """
    Ajoute pour une plage d'année l'estimation de la population d'un pays : créé une nouvelle table csv de nom pays+"_grossi.csv".
    Attention: on doit connaitre l'année anterieure ou superieure ! (qui peut avoir été calculé par les fonctions)
    """
    with open(datafolder + pays + "1" + ".csv") as f1:
        with open(datafolder + pays + "1" + "_grossi.txt", "w") as f2:

            year_0 = years[0]
            f2.write(
                f"k,Country or Area,Year,Area,Sex,Age,RecordType,Reliability,SourceYear,Value,ValueFootnotes\n")

            for year in years:
                somme = 0

                if year == year_0:
                    df = pd.read_csv(datafolder + pays + "1" + ".csv")
                else:
                    print(df)
                    df = pd.read_csv(datafolder + pays + "1" + "_grossi.csv")

                for age in range(0, 80):
                    if year == year_0:
                        sous_table1 = df.loc[(df["Year"] == (int(year)+1))]
                    else:
                        sous_table1 = df
                    sous_table = sous_table1.loc[sous_table1["Age"] == str(
                        age)]
                    # if year == "2007":
                    # print(sous_table1, sous_table)
                    # print((df["Year"]))
                    valeur_pop = sous_table.iloc[0, 9] * \
                        (1-annual_rate/100)**(-int(year)+int(year_0)+1)
                    somme += valeur_pop
                    print(valeur_pop, age, year)
                    f2.write(
                        f"100,{pays},{int(year)},Total,Both Sexes,{age},Estimate - de jure,\"Final figure, complete\", {year}.0, {valeur_pop:.1f},\n")
                f2.write(
                    f"100,{pays},{int(year)},Total,Both Sexes,Total,Estimate - de jure,\"Final figure, complete\", {year}.0, {somme:.1f},\n")

            for line in f1:
                f2.write(line)


# with open(datafolder + "Mali" + "1" + "_grossi.txt") as f1:
#     with open(datafolder + "Mali" + "1" + "_grossi.csv", "w") as f2:
#         for line in f1:
#             f2.write(line)

# df = pd.read_csv(datafolder + "Mali" + "1" + "_grossi.csv")
# print(df["Year"])
# add_year(["2008", "2007", "2006",
#   "2005"], "Mali", 2.1)
