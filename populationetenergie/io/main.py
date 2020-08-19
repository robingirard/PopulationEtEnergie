chemin_absolu = 'C:\\Users\\jujug\\OneDrive - mines-paristech.fr\\Documents\\Mines\\1A\\EC\\Mini-projet\\repo_git\\' #à adapter à chaque ordinateur

import sys

sys.path.append(chemin_absolu + 'populationetenergie\\io')


from read_data import age_group_type, data_to_2D_table
from predict_pop import prediction
from compare import compare, compare_total
import pandas as pd

datafolder = chemin_absolu + 'populationetenergie\\data\\'

def predict_pop(pays:str, year_0, year_n, year_i, year_f, pas=1):
    ''' Lit et nettoye les données puis renvoie une prédiction de population entre year_i et year_f
    grâce aux données entre year_0 et year_n. Pour choisir les années, il faut des années consecutives où l'on a  les données pour tous les ages (colonne age de age_group_type). Il ne faut pas hésiter à revenir aux talbeaux csv pour avoir une idée plus précises de la forme des données '''
    # On lit les données fornies par le site : http://data.un.org/Data.aspx?d=POP&f=tableCode%3a22
    print()
    data  = pd.read_csv(datafolder+pays+'.csv',usecols=['Year','Sex','Age','Value'], skipfooter=0)

    # On garde que les lignes intéressantes
    data = data[data['Age']!='Unknown']
    data = data[data['Age']!='Total']
    data = data[data['Sex'] =='Both Sexes']
    # On supprime les données en double
    data = data.drop_duplicates(subset = ['Year','Sex','Age'])

    # On récupère les informations sur les groupes d'âges
    age_group_info = age_group_type(data)
    age_group_info.to_csv(datafolder+pays+'_info_age.csv')
    print(age_group_info)
    population_table = data_to_2D_table(data, age_group_info)
    population_table.index.name = 'year'
    population_table.to_csv(datafolder+pays+'_données_ordonnées.csv')

    pred, theorie, erreur = prediction(population_table, year_0, year_n, year_i, year_f, pas)
    print(erreur)
    pred.to_csv(datafolder+pays+'_pred.csv')
    theorie.to_csv(datafolder+pays+'_theo.csv')
    compare(pred, theorie, pays)

predict_pop('Uzbe', 2010, 2017, 2010, 2050)


