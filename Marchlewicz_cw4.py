import math
import numpy as np
import random


def get_breast_cancer_data_in_ratio():
    cancer_data = []
    cancer_data_learning = []
    cancer_data_testing = []
    index = 1
    file = open('breast-cancer.data', 'r')
    lines = file.readlines()
    for line in lines:
        data_line = line.split(',')
        new_instance = Instance()
        new_instance.atr_dec = data_line[0]
        new_instance.atr1 = data_line[1]
        new_instance.atr2 = data_line[2]
        new_instance.atr3 = data_line[3]
        new_instance.atr4 = data_line[4]
        new_instance.atr5 = data_line[5]
        new_instance.atr6 = data_line[6]
        new_instance.atr7 = data_line[7]
        new_instance.atr8 = data_line[8]
        new_instance.atr9 = data_line[9]
        cancer_data.append(new_instance)
    random.shuffle(cancer_data)
    for instance in cancer_data:
        if index == 1 or index == 3 or index == 5:
            cancer_data_learning.append(instance)
        elif index == 2 or index == 4:
            cancer_data_testing.append(instance)
        index += 1
        if index > 5:
            index = 1
    return cancer_data_learning, cancer_data_testing


def get_shroom_data_in_ratio():
    shroom_data = []
    shroom_data_learning = []
    shroom_data_testing = []
    index = 1
    file = open('agaricus-lepiota.data', 'r')
    lines = file.readlines()
    for line in lines:
        data_line = line.split(',')
        new_instance = Instance()
        new_instance.atr_dec = data_line[0]
        new_instance.atr1 = data_line[1]
        new_instance.atr2 = data_line[2]
        new_instance.atr3 = data_line[3]
        new_instance.atr4 = data_line[4]
        new_instance.atr5 = data_line[5]
        new_instance.atr6 = data_line[6]
        new_instance.atr7 = data_line[7]
        new_instance.atr8 = data_line[8]
        new_instance.atr9 = data_line[9]
        new_instance.atr10 = data_line[10]
        new_instance.atr11 = data_line[11]
        new_instance.atr12 = data_line[12]
        new_instance.atr13 = data_line[13]
        new_instance.atr14 = data_line[14]
        new_instance.atr15 = data_line[15]
        new_instance.atr16 = data_line[16]
        new_instance.atr17 = data_line[17]
        new_instance.atr18 = data_line[18]
        new_instance.atr19 = data_line[19]
        new_instance.atr20 = data_line[20]
        new_instance.atr21 = data_line[21]
        new_instance.atr22 = data_line[22]
        shroom_data.append(new_instance)
    random.shuffle(shroom_data)
    for instance in shroom_data:
        if index == 1 or index == 3 or index == 5:
            shroom_data_learning.append(instance)
        elif index == 2 or index == 4:
            shroom_data_testing.append(instance)
        index += 1
        if index > 5:
            index = 1
    return shroom_data_learning, shroom_data_testing


class Instance:
    def __init__(self):
        self.atr_dec = None
        self.atr1 = None
        self.atr2 = None
        self.atr3 = None
        self.atr4 = None
        self.atr5 = None
        self.atr6 = None
        self.atr7 = None
        self.atr8 = None
        self.atr9 = None

    def get_atribute_from_order(self, number):
        if number == 0:
            return self.atr_dec
        if number == 1:
            return self.atr1
        if number == 2:
            return self.atr2
        if number == 3:
            return self.atr3
        if number == 4:
            return self.atr4
        if number == 5:
            return self.atr5
        if number == 6:
            return self.atr6
        if number == 7:
            return self.atr7
        if number == 8:
            return self.atr8
        if number == 9:
            return self.atr9


class Shroom:
    def __init__(self):
        self.atr_dec = None
        self.atr1 = None
        self.atr2 = None
        self.atr3 = None
        self.atr4 = None
        self.atr5 = None
        self.atr6 = None
        self.atr7 = None
        self.atr8 = None
        self.atr9 = None
        self.atr10 = None
        self.atr11 = None
        self.atr12 = None
        self.atr13 = None
        self.atr14 = None
        self.atr15 = None
        self.atr16 = None
        self.atr17 = None
        self.atr18 = None
        self.atr19 = None
        self.atr20 = None
        self.atr21 = None
        self.atr22 = None

    def get_atribute_from_order(self, number):
        if number == 0:
            return self.atr_dec
        if number == 1:
            return self.atr1
        if number == 2:
            return self.atr2
        if number == 3:
            return self.atr3
        if number == 4:
            return self.atr4
        if number == 5:
            return self.atr5
        if number == 6:
            return self.atr6
        if number == 7:
            return self.atr7
        if number == 8:
            return self.atr8
        if number == 9:
            return self.atr9
        if number == 10:
            return self.atr10
        if number == 11:
            return self.atr11
        if number == 12:
            return self.atr12
        if number == 13:
            return self.atr13
        if number == 14:
            return self.atr14
        if number == 15:
            return self.atr15
        if number == 16:
            return self.atr16
        if number == 17:
            return self.atr17
        if number == 18:
            return self.atr18
        if number == 19:
            return self.atr19
        if number == 20:
            return self.atr20
        if number == 21:
            return self.atr21
        if number == 22:
            return self.atr22


class Node:
    def __init__(self):
        self.value = None
        self.next_node = None
        self.branches = None
        self.height = None


class Tree:
    def __init__(self, data, class_id, params_id):
        self.data = data
        self.entropy = self.get_inf_entropy(self.data)
        self.node = Node()
        self.node.height = 1
        self.best = []
        self.class_id = class_id
        self.params_id = params_id

    def get_inf_entropy(self, data):
        all_decisions = []
        for instance in data:
            all_decisions.append(instance.get_atribute_from_order(0))
        length = len(all_decisions)
        decisions_stat = [(x, all_decisions.count(x)) for x in set(all_decisions)]
        params = []
        for stat in decisions_stat:
            s = stat[1] / length
            params.append(s)
        entropy = 0
        for param in params:
            entropy = entropy + ((-param) * math.log(param))
        return entropy

    def get_param_entropy(self, data, param_nr):
        all_decisions = []
        for instance in data:
            all_decisions.append(instance.get_atribute_from_order(param_nr))
        length = len(all_decisions)
        decisions_stat = [(x, all_decisions.count(x)) for x in set(all_decisions)]
        for x in range(len(decisions_stat)):
            supp_list = []
            for instance in data:
                if instance.get_atribute_from_order(param_nr) == decisions_stat[x][0]:
                    supp_list.append(instance.get_atribute_from_order(0))
                    supp_decisions_stat = [(x, supp_list.count(x)) for x in set(supp_list)]
            for supp_stat in supp_decisions_stat:
                decisions_stat[x] = decisions_stat[x] + (supp_stat[1] / decisions_stat[x][1],)
        list_of_e = []
        for stat in decisions_stat:
            val = 0
            s = stat[1] / length
            stat_i = 0
            for x in range(2, len(stat)):
                stat_i = stat_i + ((-stat[x]) * math.log(stat[x]))
            val = s * stat_i
            list_of_e.append(val)
        entropy = sum(list_of_e)
        return entropy

    def get_param_gain(self, data, param_nr):
        inf_entropy = self.get_inf_entropy(data)
        param_entropy = self.get_param_entropy(data, param_nr)
        param_gain = inf_entropy - param_entropy
        return param_gain

    def find_max_gain_and_param_nr(self, data, nrs_of_params_can_use):
        current_max_gain = -1
        current_max_param_nr = None
        for param in nrs_of_params_can_use:
            max_gain = self.get_param_gain(data, param)
            if max_gain > current_max_gain:
                current_max_gain = max_gain
                current_max_param_nr = param
        return current_max_gain, current_max_param_nr

    def start_id3(self):
        self.node = self.id3_recur(self.data, self.params_id, self.class_id, self.node, 1)

    def id3_recur(self, data, params_ids, dec_id, node, height):
        # is there a node
        if not node:
            node = Node()
        # if all instances have same decision
        check_decs = []
        for instance in data:
            check_decs.append(instance.get_atribute_from_order(0))
        decisions_stat = [(x, check_decs.count(x)) for x in set(check_decs)]
        if len(decisions_stat) == 1:
            node.value = decisions_stat[0][0]
            return node
        # if there are not more to compute, return node with the most probable decision
        if len(params_ids) == 0:
            for instance in data:
                check_decs.append(instance.get_atribute_from_order(0))
            decisions_stat = [(x, check_decs.count(x)) for x in set(check_decs)]
            m = -1
            l = None
            for stat in decisions_stat:
                if stat[1] > m:
                    m = stat[1]
                    l = stat[0]
            node.value = l
            return node
        # then choose best from rest and send then further
        best_value, best_id = self.find_max_gain_and_param_nr(data, params_ids)
        node.value = best_id
        node.branches = []
        # get values of the chosen feature for each instance and give to branch
        best_data = []
        for instance in data:
            best_data.append(instance.get_atribute_from_order(best_id))
        best_params_stats = [(x, best_data.count(x)) for x in set(best_data)]
        # loop through all the values
        for param in best_params_stats:
            child = Node()
            child.value = param[0]
            child.height = height + 1
            node.branches.append(child)
            branch_data = []
            for instance in data:
                if instance.get_atribute_from_order(best_id) == child.value:
                    branch_data.append(instance)
            # if nothing give most numerous output
            if not branch_data:
                num_data = []
                for instance in data:
                    num_data.append(instance.get_atribute_from_order(0))
                decisions_stat = [(x, num_data.count(x)) for x in set(num_data)]
                val = -1
                lab = None
                for stat in decisions_stat:
                    if stat[1] > val:
                        lab = stat[0]
                child.next_node = lab
            # send rest to next node
            else:
                if best_id in params_ids:
                    params_ids.remove(best_id)
                child.next_node = self.id3_recur(branch_data, params_ids, dec_id, child.next_node, child.height)
        return node


def get_value_from_node(tree, node, instance, height):
    if node.branches is not None:
        for branch in node.branches:
            par_id = node.value
            if instance.get_atribute_from_order(par_id) == branch.value:
                return get_value_from_node(tree, branch, instance, height + 1)
    elif node.branches is None:
        if node.next_node is not None:
            if node.next_node.branches is not None:
                return get_value_from_node(tree, node.next_node, instance, height + 1)
            else:
                return node.next_node.value
        elif node.next_node is None:
            return None


def main_cancer():
    # create tree - cancer
    c = 0
    p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    learn, test = get_breast_cancer_data_in_ratio()
    tree = Tree(learn, c, p)
    tree.start_id3()
    # start evaluating - cancer
    had_r_but_given_nr = 0
    had_nr_but_given_r = 0
    had_r_given_r = 0
    had_nr_given_nr = 0
    how_many_correct = 0
    how_many_bad = 0
    for tester in test:
        prediction = get_value_from_node(tree, tree.node, tester, tree.node.height)
        if prediction == tester.get_atribute_from_order(c):
            how_many_correct += 1
            if tester.get_atribute_from_order(c) == "no-recurrence-events":
                had_nr_given_nr += 1
            else:
                had_r_given_r += 1
        elif prediction != tester.get_atribute_from_order(c):
            how_many_bad += 1
            if tester.get_atribute_from_order(c) == "no-recurrence-events":
                had_nr_but_given_r += 1
            else:
                had_r_but_given_nr += 1
    #print(how_many_correct, how_many_bad)
    print("Correct prediction: ", (how_many_correct / (how_many_correct + how_many_bad)) * 100,
          "% Incorrect prediction: ",
          (how_many_bad / (how_many_correct + how_many_bad)) * 100, "%")
    print("TN: ", had_nr_given_nr, "TP: ", had_r_given_r, "FP: ", had_nr_but_given_r, "FN: ", had_r_but_given_nr)
    return (how_many_correct / (how_many_correct + how_many_bad)) * 100


def main_shroom():
    # create tree - shroom
    c = 0
    p = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    learn, test = get_shroom_data_in_ratio()
    tree = Tree(learn, c, p)
    tree.start_id3()
    # start evaluating - shroom
    had_e_but_given_p = 0
    had_p_but_given_e = 0
    had_e_given_e = 0
    had_p_given_p = 0
    how_many_correct = 0
    how_many_bad = 0
    for tester in test:
        prediction = get_value_from_node(tree, tree.node, tester, tree.node.height)
        if prediction == tester.get_atribute_from_order(c):
            how_many_correct += 1
            if tester.get_atribute_from_order(c) == "p":
                had_p_given_p += 1
            else:
                had_e_given_e += 1
        elif prediction != tester.get_atribute_from_order(c):
            how_many_bad += 1
            if tester.get_atribute_from_order(c) == "p":
                had_e_but_given_p += 1
            else:
                had_p_but_given_e += 1
    #print(how_many_correct, how_many_bad)
    print("Correct prediction: ", (how_many_correct / (how_many_correct + how_many_bad)) * 100,
          "% Incorrect prediction: ",
          (how_many_bad / (how_many_correct + how_many_bad)) * 100, "%")
    print("TN: ", had_p_given_p, "TP: ", had_e_given_e, "FP: ", had_p_but_given_e, "FN: ", had_e_but_given_p)
    return (how_many_correct / (how_many_correct + how_many_bad)) * 100


if __name__ == "__main__":
    p = 0
    i = 1
    while i < 26:
        x = main_cancer()
        p += x
        i += 1
    #print(p/25)
    #print("breast:")
    #main_cancer()
    #print("shroom:")
    #main_shroom()

