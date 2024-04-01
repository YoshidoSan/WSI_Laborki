import matplotlib.pyplot as plt
import cec2017
import numpy as np
from cec2017.functions import f4,f5
import math
from autograd import grad
from random import randint
import statistics as stat
from statistics import mean
np.set_printoptions(precision=2)
#===================================zmienne==============================================================
#liczba osobników
pops_size=100
#budżet
bu=10000
#liczba iteracji
tmax=bu/pops_size
#siła mutacji
ms=1
#rozmiar elity
elite_size=1
#ograniczenia kostkowe
UPPER_BOUND = 100
#wymiary
DIMENSIONALITY = 10
#funkcja
function=f5
#===================================funkcje==============================================================
def generate_pops(pops_size,UPPER_BOUND,DIMENSIONALITY,function):
    pops=[]
    scores=[]
    for i in range(pops_size):
        x = np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY)
        pops.append(x)
    for pop in pops:
        scores.append(function(pop))
    return pops, scores
def get_from_valuest(pops, scores):
    leng = len(scores)
    sorted_pops=[]
    sorted_scores=[]
    i=0
    while i < leng:
        to_get = np.argmin(scores)
        sorted_pops.append(pops[to_get])
        sorted_scores.append(scores[to_get])
        pops.pop(to_get)
        scores.pop(to_get)
        i+=1
    return sorted_pops,sorted_scores
def tournament(s_pops,s_values, k=2):
    t_pops=[]
    t_scores = []
    i=0
    while i < len(s_pops):
        arand = randint(0, len(s_pops)-1)
        brand = randint(0, len(s_pops)-1)
        if s_values[arand]>s_values[brand]:
            t_pops.append(s_pops[brand])
            t_scores.append(s_values[brand])
        else:
            t_pops.append(s_pops[arand])
            t_scores.append(s_values[arand])
        i+=1
    return t_pops, t_scores
def mutation(pops , ms):
    i = 0
    while i < len(pops):
        n = np.random.normal(0, 1, size=DIMENSIONALITY)
        pops[i] = pops[i] + ms * n
        i += 1
    return pops
def elite_succession(older_pop,younger_pop,elite_size):
    i=0
    while i < elite_size:
        younger_pop[-1-i] = older_pop[i]
        i+=1
    return younger_pop
#====================algorytm========================================
def algoritm():
    t=0
    parent_pops, parent_scores = generate_pops(pops_size,UPPER_BOUND,DIMENSIONALITY,function)
    to_get = np.argmin(parent_scores)
    best_parent = parent_pops[to_get]
    best_parent_score = parent_scores[to_get]
    #print('start: ',"%.2f" % best_parent_score)
    while t < tmax:
        s_parent_pops, s_parent_scores = get_from_valuest(parent_pops, parent_scores)
        after_tournament_parent_pops , after_tournament_parent_scores = tournament(s_parent_pops, s_parent_scores)
        mutated_pops = mutation(after_tournament_parent_pops, ms)
        mutated_scores=[]
        for m_pop in mutated_pops:
            mutated_scores.append(function(m_pop))
        m_to_get = min(mutated_scores)
        index = mutated_scores.index(m_to_get)
        best_mutated_pop = mutated_pops[index]
        best_mutated_score = mutated_scores[index]
        if best_mutated_score<=best_parent_score:
            best_parent = best_mutated_pop
            best_parent_score = best_mutated_score
        s_mutated_pops, s_mutated_scores = get_from_valuest(mutated_pops, mutated_scores)
        new_pops = elite_succession(s_parent_pops,s_mutated_pops,elite_size)
        new_pops_scores = []
        for n_pop in new_pops:
            new_pops_scores.append(function(n_pop))
        parent_pops = new_pops
        parent_scores = new_pops_scores
        t+=1
    best = min(parent_scores)
    return best
#==================symulacja=========================================================
a=0
wyniki=[]
while a <50:
    wynik = algoritm()
    wyniki.append(wynik)
    a+=1
print("maximum: ","%.2f" % max(wyniki))
print("minimum: ","%.2f" % min(wyniki))
print("średnia: ","%.2f" % mean(wyniki))
print("odchylenie: ","%.2f" % np.std(wyniki))

