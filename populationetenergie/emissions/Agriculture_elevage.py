'''
Les données que nous utilisons sont celles de la FAO (food and agriculture organization of the united nations) en 2020.
Il y a aussi des projections jusqu'en 2029 dans ces données de consommation de viande.
La distinction est faite entre pays dévoloppés et pays en développement, nous conserverons cette distinction.
Les habitants de pays en dévoleppement, d'après ces projections, vont voir stagner à 27.4 kg/hab leur consommation annuelle de viande,
Nous serons un peu plus laxistes et considérerons que leur consommation passera à 30 kg/hab en 2050.
Quant aux pays développés, leur consommation de viande risque d'augmenter ! Mais nous ne le laisserons pas faire, et notre modèle 
leur demandera de faire quelques efforts, c'est à dire de ne pas augmenter leur consommation de cochons et de poules.

Mais que vais-je faire dans ce modèle ?
Tout simplement demander aux habitants de la planète Terre d'arrêter progressivement de manger des taurreaux et des moutons.
Pour ce faire, on garde la distinction entre les pays développés et en développement :
==> Pour les pays développés, qui consomment beaucoup (trop) de viande déjà, la consommation de cochons et de poules ne varie
    pas, mais on remplace les calories du boeuf et du mouton par des légumes/céréales, dont l'empreinte carbone est plus faible.
==> Pour les pays en développement, on remplace ces viandes par d'autres viandes, dont les proportions seront les mêmes qu'aujourd'hui,
    On fera aussi augmenter linéairement leur consommation annuelle de 25.6 kg/hab en 2020 à 30 en 2050.

Le remplacement sera exponentiel : on baisse la consommation de boeuf de 5% par an.
On remplacera 1 kg de boeuf/mouton par 2 kg de produit végétal moyen, car 100g de boeuf/mouton ~ 200 kcal et 100g de produit vétégal (légume, légumineuses, céréales, pommes de terre) ~ 100 kcal
'''

'''
On commence par initialiser : ce qui commence par D concerne les pays développés,
ce qui commence par ED concerne les pays en développement

On calcule en kg la consommation totale de chaque type de viande, puis on calcule la proportion de viande que chacune représente
'''


'''
D_vege = 0
D_boeuf_tot = 29513000000    #38336921000 pour le K, 15991959000 pour le D
D_cochon_tot = 41239000000   #17025771000 pour le K, 13973861000 pour le D
D_mouton_tot = 2716000000    #15712000000 pour le K, 516100000 pour le D
D_coq_tot = 50313000000      #30218300000 pour le K, 15029700000 pour le D
D_par_hab = 69.5              #63.7 pour le K, 80.1 pour le D
D_prop_boeuf = D_boeuf_tot/(D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_prop_cochon = D_cochon_tot/(D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_prop_mouton = D_mouton_tot/(D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_prop_coq = D_coq_tot/(D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_tot = D_boeuf_tot + D_mouton_tot + D_cochon_tot + D_coq_tot
'''

import csv
import numpy as np
K_vege = 0
K_boeuf_tot = 38336921000
K_cochon_tot = 17025771000
K_mouton_tot = 15712000000
K_coq_tot = 30218300000
K_par_hab = 63.7
K_prop_boeuf = K_boeuf_tot / \
    (K_boeuf_tot + K_cochon_tot + K_coq_tot + K_mouton_tot)
K_prop_cochon = K_cochon_tot / \
    (K_boeuf_tot + K_cochon_tot + K_coq_tot + K_mouton_tot)
K_prop_mouton = K_mouton_tot / \
    (K_boeuf_tot + K_cochon_tot + K_coq_tot + K_mouton_tot)
K_prop_coq = K_coq_tot/(K_boeuf_tot + K_cochon_tot + K_coq_tot + K_mouton_tot)
K_tot = K_boeuf_tot + K_mouton_tot + K_cochon_tot + K_coq_tot

D_vege = 0
D_boeuf_tot = 15991959000
D_cochon_tot = 13973861000
D_mouton_tot = 516100000
D_coq_tot = 15029700000
D_par_hab = 80.1
D_prop_boeuf = D_boeuf_tot / \
    (D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_prop_cochon = D_cochon_tot / \
    (D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_prop_mouton = D_mouton_tot / \
    (D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_prop_coq = D_coq_tot/(D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
D_tot = D_boeuf_tot + D_mouton_tot + D_cochon_tot + D_coq_tot

ED_boeuf_tot = 41369000000
ED_cochon_tot = 65040000000
ED_mouton_tot = 12804000000
ED_coq_tot = 80917000000
ED_par_hab = 25.6
ED_prop_boeuf = ED_boeuf_tot / \
    (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
ED_prop_cochon = ED_cochon_tot / \
    (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
ED_prop_mouton = ED_mouton_tot / \
    (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
ED_prop_coq = ED_coq_tot / \
    (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
ED_tot = ED_mouton_tot + ED_cochon_tot + ED_coq_tot + ED_boeuf_tot


K_conso = [[K_par_hab*K_prop_boeuf, K_par_hab*K_prop_mouton,
            K_par_hab*K_prop_cochon, K_par_hab*K_prop_coq, 0, 22]]
# le dernier chiffre est une moyenne pour le poisson qui vient aussi de la FAO, et l'avant dernier c'est les végétaux
D_conso = [[D_par_hab*D_prop_boeuf, D_par_hab*D_prop_mouton,
            D_par_hab*D_prop_cochon, D_par_hab*D_prop_coq, 0, 22]]
ED_conso = [[ED_par_hab*ED_prop_boeuf, ED_par_hab*ED_prop_mouton,
             ED_par_hab*ED_prop_cochon, ED_par_hab*ED_prop_coq, 0, 12]]

ED_par_hab2 = ED_par_hab

for n in range(50):  # On applique ntre modèle sur 30 ans
    # On remplace le boeuf et le mouton par des légumes
    D_vege = D_vege + 0.1*D_par_hab*(D_prop_boeuf + D_prop_mouton)
    D_boeuf_tot = D_boeuf_tot * 0.95  # On diminue le boeuf
    D_mouton_tot = D_mouton_tot * 0.95  # On diminue le mouton
    # On calcule la nouvelle proportion de boeuf
    D_prop_boeuf = D_boeuf_tot / \
        (D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
    D_prop_mouton = D_mouton_tot / \
        (D_boeuf_tot + D_cochon_tot + D_coq_tot + D_mouton_tot)
    # On multiplie la consommation par habitant totale, qui n'a pas varié, par les nouvelles proportions de chaque viande
    D_conso.append([D_par_hab*D_prop_boeuf, D_par_hab*D_prop_mouton,
                    D_par_hab*D_prop_cochon, D_par_hab*D_prop_coq, D_vege, 22])
    # On remplace le boeuf et le mouton par Kes légumes
    K_vege = K_vege + 0.1*K_par_hab*(K_prop_boeuf + K_prop_mouton)
    K_boeuf_tot = K_boeuf_tot * 0.95  # On Kiminue le boeuf
    K_mouton_tot = K_mouton_tot * 0.95  # On Kiminue le mouton
    # On calcule la nouvelle proportion Ke boeuf
    K_prop_boeuf = K_boeuf_tot / \
        (K_boeuf_tot + K_cochon_tot + K_coq_tot + K_mouton_tot)
    K_prop_mouton = K_mouton_tot / \
        (K_boeuf_tot + K_cochon_tot + K_coq_tot + K_mouton_tot)
    K_conso.append([K_par_hab*K_prop_boeuf, K_par_hab*K_prop_mouton,
                    K_par_hab*K_prop_cochon, K_par_hab*K_prop_coq, K_vege, 22])
    ED_par_hab = ED_par_hab + 4.6/30
    # C'est la quantité de boeuf et mouton qu'on supprime qu'il faudra redistribuer chez les cochons et les coqs
    ED_remplacement = 0.05*ED_par_hab * (ED_prop_boeuf + ED_prop_mouton)
    prop_coq = ED_coq_tot/(ED_coq_tot + ED_cochon_tot)
    ED_boeuf_tot = ED_boeuf_tot * 0.95
    ED_mouton_tot = ED_mouton_tot * 0.95
    ED_cochon_tot = ED_cochon_tot + ED_remplacement * (1 - prop_coq)
    ED_coq_tot = ED_coq_tot + ED_remplacement * prop_coq
    ED_prop_boeuf = ED_boeuf_tot / \
        (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
    ED_prop_mouton = ED_mouton_tot / \
        (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
    ED_prop_coq = ED_coq_tot / \
        (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
    ED_prop_cochon = ED_cochon_tot / \
        (ED_boeuf_tot + ED_cochon_tot + ED_coq_tot + ED_mouton_tot)
    ED_conso.append([ED_par_hab*ED_prop_boeuf, ED_par_hab*ED_prop_mouton,
                     ED_par_hab*ED_prop_cochon, ED_par_hab*ED_prop_coq, 0, 12])


# Les émissions de CO2 par kilo de chaque aliment : [boeuf, mouton, cochon, coq, végétaux en moyenne, poisson]
emission = [67.6, 23.4, 6.1, 5.4, 0.3, 6.0]
K_emission = []
D_emission = []
ED_emission = []

# On calcule les émissions due à chaque viande de 2020 à 2050 (liste de liste : chaque sous-liste est une année)
for i in range(len(D_conso)):
    K = []
    D = []
    E = []
    for j in range(6):
        K.append(K_conso[i][j] * emission[j])
        D.append(D_conso[i][j] * emission[j])
        E.append(ED_conso[i][j] * emission[j])
    K_emission.append(K)
    D_emission.append(D)
    ED_emission.append(E)


D_viande_début = np.sum(D_emission[0])
D_viande_fin = np.sum(D_emission[-1])

ED_viande_début = np.sum(ED_emission[0])
ED_viande_fin = np.sum(ED_emission[-1])

'''
Avec les données du shiftdataportal et de solagro, on trouve les émissons totales de CO2 de l'agriculture : 163 Mt eqCO2 en France par exemple, alors que notre calcul donne 105 Mt eqCO2 pour la viande. En prenant les ratios du Shiftdataportal, on trouve que les émissions dues à la viande dans les pays développés sont 2 tiers des émissons totales de l'agriculture., et la moitié pour les pays en développement.
'''

K_vege_toutletemps = 851
D_vege_toutletemps = 851
ED_vege_toutletemps = 608

for i in range(len(D_emission)):  # On ajoute les émissions due aux végétaux
    K_emission[i].append(K_vege_toutletemps)
    D_emission[i].append(D_vege_toutletemps)
    ED_emission[i].append(ED_vege_toutletemps)

K_emission_début = np.sum(K_emission[0])
K_emission_fin = np.sum(K_emission[-1])

D_emission_début = np.sum(D_emission[0])
D_emission_fin = np.sum(D_emission[-1])

ED_emission_début = np.sum(ED_emission[0])
ED_emission_fin = np.sum(ED_emission[-1])

K_emission_par_an = []
D_emission_par_an = []
ED_emission_par_an = []
for i in range(len(D_emission)):  # On somme pour avoir les émissions totales par an
    # La multiplication par 0.7 vient du fait que 30% des émissions de CO2 liées à l'agriculture vient du transport, et Guillaume a déjà compté les émissions dues au transport.
    D_emission_par_an.append(np.sum(D_emission[i])*0.7)
    ED_emission_par_an.append(np.sum(ED_emission[i])*0.7)
    K_emission_par_an.append(np.sum(K_emission[i])*0.7)

'''
Après avoir exécuté ce programme, les listes D_emission_par_an et ED_emission_par_an sont celles qui nous intéresse,
En effet, il s'agit des listes qui recensent les émissions de CO2 de chaque habitant d'un pays développé ou en développement
chaque année, en kg eqCO2 par personne.
'''


myFile = open(r"C:\Users\Max\Documents\Mines\Ecologie\Agri2070.csv",
              'w', newline='')  # à changer en fonction de l'ordi !
with myFile:
    writer = csv.writer(myFile)
    writer.writerow(['Kazhakstan'])
    writer.writerows([[x] for x in K_emission_par_an])
    writer.writerow(['Danemark'])
    writer.writerows([[x] for x in D_emission_par_an])
    writer.writerow(['Pays en dev'])
    writer.writerows([[x] for x in ED_emission_par_an])
print('Cest fait!')
