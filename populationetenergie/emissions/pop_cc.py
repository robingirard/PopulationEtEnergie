import numpy as np

'''
L'argument fichier de la première fonction est trouvé à l'adresse suivante : https://www.theshiftdataportal.org/energy/final-energy?chart-type=stacked&chart-types=stacked&chart-types=stacked-percent&chart-types=pie&chart-types=line&chart-types=ranking&disable-en=false&energy-families=Oil%20products&energy-families=Gas&energy-families=Electricity&energy-families=Coal&energy-families=Heat&energy-families=Geothermal&energy-families=Biofuels%20and%20waste&energy-families=Crude%20oil&energy-families=Others&energy-unit=KWh&group-names=Albania&is-range=true&gdp-unit=GDP%20(constant%202010%20US%24)&sectors=Transport&dimension=byEnergyFamily&end=2015&start=2014&multi=false
'''

def conso_par_vect(fichier):        
    fic=open(fichier)               # Selon l'endroit où le fichier est rangé, on mettra la lettre r devant le chemin d'accès, sinon open() n'aime pas
    ch=fic.readline()
    while ch!="":                   #dans le fichier dont nous disposons, on ne s'interesse qu'à la dernière ligne, qui est la donnée la plus récente
        L=ch.split(",")
        ch=fic.readline()           #L est la liste [date, biofuels, charbon, pétrole brut, électricité, gaz, géothermique, thermique, produits pétroliers] en kWh (ou en l'unité qu'on choisit sur le site)
    for i in range(1,len(L)-1):
        L[i]=float(L[i])            #On convertit les valeurs de notre liste en flottants : attention, le premier élement est undate (donc pas un float) et le dernier a un vilain '\n' au bout
    L[-1]=float(L[-1][:-1])         #On n'oiublie pas de supprimmer le \n
    return L

'''
Le coût en CO2 équivalent de l'électricité dans chaque pays est disponible à l'adresse :
https://www.bilans-ges.ademe.fr/documentation/UPLOAD_DOC_FR/index.htm?moyenne_par_pays.htm

Le mix électrique précis est disponible ici :
https://www.theshiftdataportal.org/energy/electricity?chart-type=stacked&chart-types=stacked&chart-types=stacked-percent&chart-types=pie&chart-types=line&chart-types=ranking&disable-en=false&ef-generation=Oil&ef-generation=Coal&ef-generation=Gas&ef-generation=Nuclear&ef-generation=Hydro&ef-generation=Wind&ef-generation=Biomass&ef-generation=Waste&ef-generation=Solar%20PV&ef-generation=Geothermal&ef-generation=Solar%20Thermal&ef-generation=Tide&ef-capacity=Fossil%20Fuels&ef-capacity=Hydroelectricity&ef-capacity=Nuclear&ef-capacity=Hydroelectric%20Pumped%20Storage&ef-capacity=Wind&ef-capacity=Solar%2C%20Tide%2C%20Wave%2C%20Fuel%20Cell&ef-capacity=Biomass%20and%20Waste&ef-capacity=Geothermal&energy-unit=TWh&group-names=World&is-range=true&gdp-unit=GDP%20(constant%202010%20US%24)&type=Generation&dimension=byEnergyFamily&end=2015&start=1990&multi=false
'''


'''
Remarque sur la suite : je n'ai pas trouvéde base de donnée qui donne pour chaque pays les émissions de CO2 par kWh par source d'énergie, donc je n'écris pas encore la fonction associée (attention aux unités, c'est en cCO2eq/kWh)
'''

def calcul(consvect,elec,CO2vect):                              #En gCO2eq
    L1=conso_par_vect(consvect)
    L2=CO2_par_vect(CO2vect)
    L3=L2[:3]+[elec]+L2[4:]                                     #On propose bien le mix électrique de chaque pays.
    conso_totale=np.sum([L1[i+1]*L3[i] for i in range(8)])      #On procède à une habile multiplication : conso_CO2_totale_dun_vecteur = conso_énergétique_par_vecteur * conso_en_CO2_du_vecteur, puis on somme pour chaque vecteur
    return conso_totale



'''
Pour que l'algorithme tourne quand même, je vais utiliser les moyennes mondiales : https://fr.wikipedia.org/wiki/Empreinte_carbone#%C3%89missions_directes_en_CO2_des_combustibles pour le charbon et le gaz ou https://fr.wikipedia.org/wiki/Empreinte_carbone#%C3%89missions_directes_en_CO2_des_combustibles pour la géothermie et la thermique, https://www.ademe.fr/mediatheque/recherche?query=BIOCARBURANT%20%C3%A9mission&items_per_page=10&sort_by=field_resource_edition_date&sort_order=DESC pour les biocarburants (attention c'est en kg equivalent CO2 par MJ) ou https://convertlive.com/fr/u/convert/kilowatt-heures/a/gigajoules#73.6 pour les pétroles.
'''

CO2vect=[90,377,264,0,243,50,850,300]

def calcul2(consvect,elec,CO2vect):
    L1=conso_par_vect(consvect)
    L2=CO2vect
    L3=L2[:3]+[elec]+L2[4:]
    conso_totale=np.sum([L1[i+1]*L3[i] for i in range(8)])
    return conso_totale