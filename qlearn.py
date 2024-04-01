import gym
import random
import numpy as np

# =================                params                  =========================================
# 0: LEFT
# 1: DOWN
# 2: RIGHT
# 3: UP
# =================                program               ===========================================
env = gym.make('FrozenLake-v1', render_mode="rgb_array", desc=None, map_name="8x8", is_slippery=True)
env.reset()
env.render()


def test(q_table, beta, gamma, e):
    t = 0
    succ = 0
    while t < 10000:
        finish = False
        action_count = 0
        current_state_sth = env.reset()
        current_state = current_state_sth[0]
        while not finish:
            if action_count > 200:
                break
            # epsilon strategy
            number = random.uniform(0, 1)
            if number <= e:
                action = env.action_space.sample()
            # choose action from q table
            else:
                temp_q = np.array(q_table[current_state])
                max_vad_ids = np.where(temp_q == max(q_table[current_state]))
                action = np.random.choice(max_vad_ids[0].tolist(), 1)
                action = action[0]
            next_state, reward, finish, truncated, info = env.step(action)
            # my addon
            if finish and reward == 0:
                reward = -10
            if finish and reward == 1:
                reward = 10
            #  calculate q table values
            delta = reward + gamma * np.max(q_table[next_state]) - q_table[current_state, action]
            q_table[current_state, action] = q_table[current_state, action] + beta * delta
            if reward == 1:
                succ += 1
            current_state = next_state
            action_count += 1
        t += 1
    per = succ / 10000
    return q_table, per * 100


def run(q_table):
    t = 0
    succ = 0
    while t < 1000:
        finish = False
        action_count = 0
        current_state_sth = env.reset()
        current_state = current_state_sth[0]
        while not finish:
            if action_count > 200:
                break
            # choose action from q table
            temp_q = np.array(q_table[current_state])
            max_vad_ids = np.where(temp_q == max(q_table[current_state]))
            action = np.random.choice(max_vad_ids[0].tolist(), 1)
            action = action[0]
            next_state, reward, finish, truncated, info = env.step(action)
            if reward == 1:
                succ += 1
            current_state = next_state
            action_count += 1
        t += 1
    per = succ / 1000
    return per * 100


# =================                params testing                 =========================================


def give_values_25_times(q_table, beta, gamma, e):
    i = 0
    score = 0
    score_list = []
    while i < 25:
        calculated_table, rate = test(q_table, beta, gamma, e)
        val = run(calculated_table)
        score_list.append(val)
        i += 1
        print(i)
    ef = score / 25
    best_eff_value = np.max(score_list)
    worst_eff_value = np.min(score_list)
    mean_eff = np.mean(score_list)
    std_eff = np.std(score_list)
    print("mean: ", mean_eff, "max: ", best_eff_value, "min: ", worst_eff_value, "std: ", std_eff)
    return ef


def calculate_best_params():
    q_table = np.zeros((64, 4))
    e = 0.1
    beta = 0.0  # learning rate (jak bardzo zmienić oryginalną ocenę)
    gamma = 0.0  # discount factor (im więcej tym bardziej w przyszłość patrzy)
    values = [0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 1]
    effects = []
    eff_vals = []
    for val1 in values:
        beta = val1
        for val2 in values:
            gamma = val2
            rune = []
            score = give_values_25_times(q_table, beta, gamma, e)
            rune.append(score)
            rune.append(beta)
            rune.append(gamma)
            effects.append(rune)
            print(val1, val2)
    print("getting params")
    for eff in effects:
        eff_vals.append(eff[0])
    action_eff = np.argmax(eff_vals)
    print("=====all results=======")
    print(effects)
    print("======best result=======")
    print(effects[action_eff])


def calculate_best_param():
    q_table = np.zeros((64, 4))
    e = 0
    beta = 0.1  # learning rate (jak bardzo zmienić oryginalną ocenę)
    gamma = 0.5  # discount factor (im więcej tym bardziej w przyszłość patrzy)
    values = [0.1]
    effects = []
    eff_vals = []
    for val1 in values:
        e = val1
        rune = []
        score = give_values_25_times(q_table, beta, gamma, e)
        rune.append(score)
        rune.append(e)
        effects.append(rune)
        print(e)
    print("getting params")
    for eff in effects:
        eff_vals.append(eff[0])
    action_eff = np.argmax(eff_vals)
    print("=====all results=======")
    print(effects)
    print("======best result=======")
    print(effects[action_eff])


calculate_best_param()
