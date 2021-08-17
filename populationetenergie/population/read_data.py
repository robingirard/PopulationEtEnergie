import numpy as np
import pandas as pd


def age_group_type(df):
    ''' Retourne une dataframe qui donne des informations sur
    les types de groupe d'âge utilisés. Pour chaque année, on
    peut savoir si la population était donnée pour tous les
    ages (colonne age), si elle était donnée par tranche d'age
    et quelle est l'étendue de la tranche d'age (colonne groupe),
    s'il y avait une catégorie x ans et plus (on peut trouver x
    dans la colonne plus) et enfin si on connaissait le nombre
    de naissances (colonne zéro) '''
    n = df['Year'].value_counts().shape[0]
    index = [int(year) for year in df['Year'].value_counts().index]
    group = pd.DataFrame(np.zeros((n, 4), dtype=np.int8),
                         index=index,
                         columns=['age', 'group', 'plus', 'zero']).sort_index()
    for index, row in df.iterrows():
        year = int(row['Year'])
        age = row['Age']
        try:
            age = int(age)
            if age != 0:
                group.loc[(year), 'age'] = 1
            else:
                group.loc[(year), 'zero'] = 1
        except ValueError:
            if age[-1] == '+':
                group.loc[(year), 'plus'] = int(age[:-1])
            else:
                liste = age.split('-')
                inf, sup = int(liste[0]), int(liste[1])
                # print(group.loc[(year),'group'])
                group.loc[(year), 'group'] = max(
                    sup - inf, group.loc[(year), 'group'])
    return group


def data_to_2D_table(df, age_groups):
    ''' Utilise les données dans df pour renvoyer une nouvelle dataframe
    qui va renseigner pour chaque année (qui est dans df) le nombre de
    personnes pour tous les âges entre 0 et 80 ans avec un pas d'un an'''
    group = age_group_type(df)
    age_groups = [i for i in range(0, 80, 1)]
    age_group_names = ['0'] + [f'{i+1}'
                               for i in range(0, 79, 1)]+['80 +']
    columns = age_group_names
    index = [int(year) for year in df['Year'].value_counts().index]
    n = df['Year'].value_counts().shape[0]
    m = len(age_group_names)
    data_2 = pd.DataFrame(np.zeros((n, m), dtype=np.int8),
                          index=index, columns=columns).sort_index()

    for i, row in df.iterrows():
        year = int(row['Year'])
        pop = row['Value']
        age = row['Age']
        if group.loc[(year), 'age'] == 1:
            try:
                age = int(age)
                i = 0
                while i < m-1 and age > age_groups[i]:
                    i += 1
                age_group = age_group_names[i]
                # print(data_2.loc[(year), (f'{age_group}')], type(
                # data_2.loc[(year), (f'{age_group}')]), pop, int(float(pop)))
                data_2.loc[(year), (f'{age_group}')] = float(
                    data_2.loc[(year), (f'{age_group}')]) + int(float(pop))

            except ValueError:
                if age[-1] == '+':
                    age = int(age[:-1])
                    if age >= int(age_group_names[-1][:-1]):
                        data_2.loc[(year), (age_group_names[-1])
                                   ] += int(float(pop))
        else:
            if age[-1] != '+':
                liste = age.split('-')
                age = int(liste[0])
                i = 0
                while i < m-1 and age > age_groups[i]:
                    i += 1
                age_group = age_group_names[i]
                data_2.loc[(year), (f'{age_group}')] = float(
                    data_2.loc[(year), (f'{age_group}')]) + int(float(pop))
            else:
                age = int(age[:-1])
                if age >= int(age_group_names[-1][:-1]):
                    data_2.loc[(year), (age_group_names[-1])
                               ] += int(float(pop))

    return data_2
