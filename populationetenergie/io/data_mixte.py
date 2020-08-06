import numpy as np
import pandas as pd
datafolder = 'populationetenergie/data/'

### ici çà n'est pas le bon fichier data
data  = pd.read_csv([datafolder+'Russie_2050_Total.csv'],usecols=['Year','Sex','Age','Value'], skipfooter=0)

## Il faut prendre le fichier des données des Nations Unies
data = data[data['Age']!='Unknown']
data = data[data['Age']!='Total']
data = data[data['Sex'] =='Both Sexes']
data = data.drop_duplicates(subset = ['Year','Sex','Age'])


age_groups = [i for i in range(0, 80, 1)]
age_group_names = ['0']+ [f'{i+1}' 
for i in range(0, 79, 1)]+['80 +']

#age_groups = [i for i in range(9, 89, 10)]
#age_group_names = ['0 - 9']+ [f'{i+1} - {i+10}' 
#for i in range(9, 79, 10)]+['80 +']

columns = age_group_names

index = data['Year'].value_counts().index

n = data['Year'].value_counts().shape[0]
m = len(age_group_names)

data_2 = pd.DataFrame(np.zeros((n, m)), 
index=index, columns=columns).sort_index()

def age_group_type(df=data):
    group = pd.DataFrame(np.zeros((n, 4), dtype = np.int8), 
    index=df['Year'].value_counts().index, 
    columns=['age', 'group', 'plus', 'zero']).sort_index()
    for index, row in df.iterrows():
        year = row['Year']
        age = row['Age']
        try :
            age = int(age)
            if age != 0 :
                group.loc[(year),'age'] = 1
            else : 
                group.loc[(year),'zero'] = 1
        except ValueError :
            if age[-1] == '+' :
                group.loc[(year),'plus'] = int(age[:-1])
            else :
                liste = age.split('-')
                inf, sup = int(liste[0]), int(liste[1])
                group.loc[(year),'group'] = max(sup - inf, 
                group.loc[(year),'group'])
    return group

group = age_group_type()

years_to_remove = [1949, 1950]

def data_to_2D_table(df=data):
    data_2 = pd.DataFrame(np.zeros((n, m), dtype = np.int8), 
    index=df['Year'].value_counts().index, 
    columns=columns).sort_index()
    for index, row in df.iterrows():
        year = row['Year']
        pop = row['Value']
        age = row['Age']
        if year not in years_to_remove :
            if group.loc[(year), 'age'] == 1 :
                try :
                    age = int(age)
                    i = 0
                    while i<m-1 and age > age_groups[i] :
                        i+=1
                    age_group = age_group_names[i]
                    data_2.loc[(year),(f'{age_group}')] += pop
                except ValueError :
                    if age[-1] == '+' :
                        age = int(age[:-1])
                        if age >= int(age_group_names[-1][:-1]) :
                            data_2.loc[(year),(age_group_names[-1])] += pop
            else : 
                if age[-1] != '+' :
                    liste = age.split('-')
                    age = int(liste[0])
                    i = 0
                    while i<m-1 and age > age_groups[i] :
                        i+=1
                    age_group = age_group_names[i]
                    data_2.loc[(year),(f'{age_group}')] += pop
                else :
                    age = int(age[:-1])
                    if age >= int(age_group_names[-1][:-1]) :
                        data_2.loc[(year),(age_group_names[-1])] += pop
           

    return data_2

table = data_to_2D_table()
table.index.name = 'year'
def plot(df=table):
    df.reset_index().plot(x='index', y=columns)