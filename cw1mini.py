from matplotlib.cbook import index_of
import numpy as np
import itertools as it
import time
#Kacper Marchlewicz

#zbiór danych
w = np.array([8, 3, 5, 2]) #waga przedmiotów
#w = np.array([8, 3, 5, 2,5,7,3,5,7,9,4,2,6,8,3,2,4,1,5,7,3,5])
#w=np.random.rand(320000)
W = 9 #maksymalna waga plecaka
p = np.array([16, 8, 9, 6]) #wartość przedmiotów
#p=np.random.rand(320000)
#p = np.array([8, 3, 5, 2,6,3,8,9,4,5,10,6,3,2,12,4,3,5,12,5,7,6])

results = []

#======zad.1=====================================================
def create_options(how_many):
    chosen = it.product(range(2), repeat=how_many)
    return chosen

def get_all_options_result(how_many):
    chosen = create_options(how_many)
    for combination in chosen:
        current_weight=0
        current_value=0
        combination_backup = combination
        for item in combination:
            if item != 0:
                current_weight += w[combination.index(item)]
                current_value += p[combination.index(item)]
                combi_for_taken = list(combination)
                combi_for_taken[combination.index(item)]=0
                combination = tuple(combi_for_taken)
        if current_weight > W:
            continue
        else:
            results.append([current_weight,current_value,combination_backup])
    return results    

def choose_best(weight,value):
    how_many=len(weight)
    start = time.time()
    results = get_all_options_result(how_many)
    option_weight = [ow[0] for ow in results]
    option_value = [ov[1] for ov in results]
    option_combo=[oc[2] for oc in results]
    best_value = max(option_value)
    best_weight = option_weight[option_value.index(best_value)]
    best_combo = option_combo[option_value.index(best_value)]
    end = time.time()
    print("========================================================")
    print("Przeszukanie przez przedgląd wyczerpujący")
    print("Wartość przedmiotów: ",best_value)
    print("Waga przedmiotów: ",best_weight)
    print("Kombinacja: ",best_combo)
    print("Czas obliczeń: ",end - start)
    return best_value,best_weight,best_combo

#===============zad2==============================================================
def calculate_paremeters(weight, value):
    params=np.divide(value,weight)
    return params

def get_from_valuest(weight, value):
    start = time.time()
    combo = [0] * len(weight)
    params = calculate_paremeters(weight, value)
    current_weight=0
    current_value=0
    i=0
    while i < len(params):
        to_get = np.argmax(params)
        if current_weight+w[to_get] > W:
            params[to_get]=0
            i+=1
            continue
        if current_weight+w[to_get] <= W:
            current_weight += w[to_get]
            current_value += p[to_get]
            params[to_get]=0
            combo[to_get]=1
            i+=1
            continue
    end = time.time()
    print("Rozwiązanie heurystyką")
    print("Wartość przedmiotów: ",current_value)
    print("Waga przedmiotów: ",current_weight)
    print("Kombinacja: ",combo)
    print("Czas obliczeń: ",end - start)
    print("========================================================")
    return combo,current_value,current_weight
#===============================================================================

if __name__ == "__main__":
    #choose_best(w,p)
    get_from_valuest(w,p)


