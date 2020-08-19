import numpy as np
import pandas as  pd
import numpy.linalg as lin
import scipy.optimize

def prediction(data, year_0, year_n, year_i, year_f, pas=1):
    ''' Renvoie une prédiction de population entre year_i et year_f
    grâce aux données entre year_0 et year_n '''

    calcul = data.loc[[i for i in range(year_0, year_n + pas,  pas)]]
    print(calcul)
    n, m = calcul.shape[0], calcul.shape[1]

    pred = pd.DataFrame(np.zeros(((year_f-year_i)+1, m), dtype = np.int8),
    index=np.arange(year_i, year_f+1), columns=calcul.columns).sort_index()
    pred.index.name = 'year'
    pred.loc[year_i] = calcul.loc[year_i]

    pred = pred.loc[[i for i in range(year_i, year_f + pas,  pas)]]
    theory = data.loc[[i for i in range(year_i, year_n + pas,  pas)]]

    for j in range(m-1) :
        calcul['s '+calcul.columns[j+1]] = 0
        for i, year in enumerate(calcul.index):
            if year- pas in calcul.index :
                calcul.loc[year, 's '+calcul.columns[j+1]] = calcul.loc[year, calcul.columns[j+1]]/calcul.loc[year- pas, calcul.columns[j]]

    matrix = calcul.loc[:year_n-pas,calcul.columns[1:m]].to_numpy()
    birth = calcul.loc[year_0+pas:,calcul.columns[0]].to_numpy()

    def gauss(x, alpha, beta, mean_age) :
        def fecondity(age):
            return np.exp(-(age-mean_age)**2/beta)/alpha
        nb_birth = 0
        for i, age in enumerate(calcul.columns[1:m-1]):
            nb_birth += x[i]*np.sum([fecondity(t) for t in range(pas*i, pas*(i+1))])
        return nb_birth

    def err(x):
        return (matrix.dot(x)-birth)/birth*100

    alpha, beta, mean_age = scipy.optimize.curve_fit(gauss, np.transpose(matrix), birth, p0 = [5, 7, 45])[0]
    def fecondity(age):
            return np.exp(-(age-mean_age)**2/beta)/alpha

    f = pd.DataFrame([0] + [np.sum([fecondity(t) for t in range(pas*i, pas*(i+1))]) for i in range(1, m)], index =  ['f '+calcul.drop([year_0]).columns[i] for i in range(m)])


    s = pd.DataFrame([calcul.drop([year_0])['s '+calcul.columns[i+1]].mean() for i in range(m-1)],
        index = ['s '+calcul.drop([year_0]).columns[i+1] for i in range(m-1)])

    for i, year in enumerate(pred.index):
        if i!=0 :
            for j, column in enumerate(pred.columns) :
                if j!=0 :
                    pred.iloc[i, j] = s.iloc[j-1, 0]*pred.iloc[i-1, j-1]
                    pred.iloc[i, 0] += pred.iloc[i-1, j]*f.iloc[j, 0]

    pred['Total'] = pred.sum(1)
    theory['Total'] = theory.sum(1)

    erreur = (pred.loc[[i for i in range(year_i, year_n+pas, pas)]]-theory)/theory*100

    return pred, theory, erreur