import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

test  = pd.read_csv('data/Uzbe_test_1.csv', index_col = 'year')
theory = pd.read_csv('data/Uzbe_theory_1.csv', index_col = 'year')
pays = 'Ouzbékistan'

### Les fichiers ici sont model et theory de lewis_birth_gauss
age_groups = [i for i in range(9, 109, 10)]
age_group_names = ['0 - 9']+ [f'{i+1} - {i+10}'
for i in range(9, 99, 10)]+['100 +']

columns = age_group_names


n = test.shape[0]
m = len(age_group_names)


def convert_age(df):
    n = df.shape[0]
    data_2 = pd.DataFrame(np.zeros((n, m), dtype = np.int8), 
    index=df.index, 
    columns=columns).sort_index()
    for index, row in df.iterrows():
        year = index
        for column in df.columns :
            pop = df.loc[index, column]
            if column[-1] == '+' :
                age = int(column[:-1])
            elif column != 'Total' :
                age = int(column.split('-')[0])
            if column != 'Total' :
                i = 0
                while i<m-1 and age > age_groups[i] :
                    i+=1
                age_group = age_group_names[i]
                data_2.loc[year,age_group] += pop
    return data_2

def compare():
    df1=convert_age(test)/10**6
    df2=convert_age(theory)/10**6
    test_year = test.index
    the_year = theory.index
    prec1 = np.zeros(len(test_year))
    prec2 = np.zeros(len(the_year))
    for column in df1.columns :
        prec1 += df1.loc[test_year, column]
        prec2 += df2.loc[the_year, column]
        plt.plot(test_year, prec1, label = column)
        plt.plot(the_year, prec2, '--', label = column)
    plt.title(f'Population en {pays}')
    plt.xlabel('Année')
    plt.ylabel('Population en millions')

def compare_total(min=0, max=None):
    test_year = test.index
    the_year = theory.index
    plt.plot(test_year, test.sum(1)/10**6, label = 'Modélisation')
    plt.plot(the_year, theory.sum(1)/10**6, '--', label = 'Theorie')
    plt.title(pays)
    plt.ylim( bottom = min, top = max)
    plt.xlabel('Année')
    plt.ylabel('Population totale en millions')