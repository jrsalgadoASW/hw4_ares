
import numpy as np
import pandas as pd
import math
from scipy import stats

import scipy.optimize as op

def minus_gamma_log_likelihood (par,x):
    """
    Que tan probable es que cierta gama con ciertos datos se ajuste a los los datos que tienes
    @input: 
        par: parametros de la gamma (o la gama en si porque los parametros definen a la gamma)
        x: datos
    """
    alpha, lam = par
    n =len(x)
    #minimizar la menos verosimilitud = max la verosimilitud
    like = -(n*alpha*np.log(lam)-lam*np.sum(x)+(alpha-1)*np.sum(np.log(x))-n*np.log(math.gamma(alpha)))
    return like


def gamma_estimator(x: np.array):
    """
    Encontrar la gamma mas probable para los datos
    @input: datos 
    """
    #x = [2,2,1,3,2,...]
    first_guess = [1,0.5]
    sol = op.minimize(minus_gamma_log_likelihood, first_guess , args=(x),method='Powell')
    par_optimos = sol.x
    # print(sol)
    return par_optimos

def get_params(data:pd.DataFrame,chosen_stages:list)->dict:
    params:dict  = {}
    for stage in chosen_stages:
        stage_hours = np.array(data[stage==data["CODIGO_ETAPA"]]['DURACION_HORAS'])
        #Saca un np.array con las horas de stage [2,2,3,1,2,...]
        alpha, lambd = gamma_estimator(stage_hours)
        params[stage] = np.array([alpha, lambd])
    return params
    

def calcular_prob(data: pd.DataFrame, chosen_stages: list, stage:str, x1, x2):
    alpha, lambd = get_params(data, chosen_stages)[stage]
    probability = stats.gamma.cdf(x2,a=alpha,scale=1/lambd)-stats.gamma.cdf(x1,a=alpha,scale=1/lambd)
    #Ok, calcula la probabilidad de que x1<x<x2 en una gama con parametros [4.50616811 1.80051312]
    return probability