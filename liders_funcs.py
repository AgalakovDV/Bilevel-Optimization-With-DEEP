# -*- coding: utf-8 -*-
"""
Created on Mon May 13 04:15:33 2024

@author: Daniil
"""

"""
Структура файла leader_params

[dddd]
size=5
alphas=0.3 0.3 0.5 0.2 0.2
start_damage=0 0 0 0 0
distance=[[0 3 3 4 8 8][3 0 5 2 5 8][3 5 0 5 8 5][4 2 5 0 3 5][8 5 8 3 0 2][8 8 5 5 2 0]]
count_types_robots=1
v_path=1
v_task=2
c_0=5
"""

def create_follower_param_file():
    print("hi!")
    

# find_all_damage() в статье это F1 (3.6)
# t_end - список времен, когда были завершены задачи
# start_damages - список начального ущерба, нанесенного задачами
# alphas - список скоростей приращения ущерба задач
# lambda_1 - параметр ущерба, принимается за 1
def find_all_damage(t_end : list, start_damages : list, v_damage : list, lambda_1 = 1):
    res = 0
    for q, alp, t in zip(start_damages, v_damage, t_end):
        res += (q + alp*t)
    return res*lambda_1
 
   
# cost_renting() в статье это F2 (3.7)
# c_0 - список исходных цен на роботов
def cost_renting(c_0 : list):
    return sum(c_0)
    

# running_cost_robots() в статье это F3 (3.8)
def running_cost_robots(c_r : list, t_end : list):
    return sum(c_r)*max(t_end)


# функция лидера
def f_lead(t_end : list, start_damages : list, v_damage : list, c_0 : list, c_r : list, lambda_1 = 1):
    res1 = find_all_damage(t_end, start_damages, v_damage, lambda_1)
    res2 = cost_renting(c_0)
    res3 = running_cost_robots(c_r, t_end)
    return res1 + res2 + res3


# функция последователя
def f_follow(t_end):
    return max(t_end)


# =============================================================================
# # вычисление удельных затрат c_r
# def find_cr(count_robots, distances, count_task):
#     maxS = 0
#     for i in range(count_task + 1):
#         for j in range(i+1, len(distances)):
#             if distances[i][j] > maxS:
#                 maxS = distances[i][j]     
#     minS = maxS
#     for i in range(count_task + 1):
#         for j in range(i+1, len(distances)):
#             if distances[i][j] < minS and 0 < distances[i][j]:
#                 minS = distances[i][j]
#     cr = 0.5 * (minS + maxS) * count_task / count_robots
#     return cr
#   
# 
# # вычисление всех затрат роботов, в статье это F3 (3.8)  
# def find_c_all(distances, count_task, t_end : list):
#     maxS = 0
#     for i in range(count_task + 1):
#         for j in range(i+1, len(distances)):
#             if distances[i][j] > maxS:
#                 maxS = distances[i][j]    
#     minS = maxS
#     for i in range(count_task + 1):
#         for j in range(i+1, len(distances)):
#             if distances[i][j] < minS and 0 < distances[i][j]:
#                 minS = distances[i][j]
#     c_r_sum = 0.5 * (minS + maxS) * count_task
#     c_all = c_r_sum * max(t_end) 
#     return c_all
# =============================================================================


# rastrigin_func
#!/usr/bin/env python3  
import sys
import os

# Get environment variables
#leader_param_file = os.getenv('LEADER_PARAM_FILE')
#follower_param_file = sys.argv[1]
leader_param_file = "leader_params"
follower_param_file = "follower_params"


count_tasks = 0
v_damage = []
start_damage = []
distances = []
count_types_robots = 0
v_path = []
v_task = []
c_0 = []
c_r = []

with open(leader_param_file, 'r') as fx:
    next(fx)
    
    for line_id, p in enumerate(fx):
        pp = p.split('=')[1]
        if (0 == line_id):  # count tasks
            count_tasks = int(pp)
        elif (1 == line_id):    # v_damage (скорости приращения задач)
            lst_str = pp.split(' ')
            for el in lst_str:
                v_damage.append(float(el))
        elif (2 == line_id):    # start damages of tasks
            lst_str = pp.split(' ')
            for el in lst_str:
                start_damage.append(float(el))
        elif (3 == line_id):    # distances
            lst_str = pp.split(';') # строка расстояний от места
            for el in lst_str:
                lst_str_dist = el.split(' ') # массив строк расстояний
                lst_dist = []
                for el_s in lst_str_dist:
                    lst_dist.append(float(el_s)) # создание списка расстояний от места до других
                distances.append(lst_dist)
        elif (4 == line_id):  # count types of robots
            count_types_robots = int(pp)
        elif (5 == line_id):    # скорости перемещения роботов
            lst_str = pp.split(' ')
            for el in lst_str:
                v_path.append(float(el))
        elif (6 == line_id):    # мощности роботов
            lst_str = pp.split(' ')
            for el in lst_str:
                v_task.append(float(el))
        elif (7 == line_id):    # начальная стоимость роботов
            lst_str = pp.split(' ')
            for el in lst_str:
                c_0.append(float(el))
        elif (8 == line_id):    # удельный расход роботов
            lst_str = pp.split(' ')
            for el in lst_str:
                c_r.append(float(el))

        
print(count_tasks)
print(v_damage)
print(start_damage)
print(distances)
print(count_types_robots)
print(v_path)
print(v_task)
print(c_0)
print(c_r)
        

count_robots = []


# with open(follower_param_file, 'r') as fx:
#     next(fx)
#     for line_id, p in enumerate(fx):
#         pp = p.split('=')[1]
#         if (0 == line_id): # количество роботов каждого типа
#             lst_str = pp.split(' ')
#             for el in lst_str:
#                 count_robots.append(float(el))
#         elif (1 == line_id):    # удельные расходы роботов
#             lst_str = pp.split(' ')
#             for el in lst_str:
#                 c_r.append(float(el))


# 1 узнать максимальную мощность робота и максимальную скорость приращения задачи
# а затем узнать минимальное число роботов, меньше которого задачу точно не решить
max_v_task = max(v_task)
max_alphas = max(v_damage)
min_count_robots = max_alphas // max_v_task
while max_alphas > min_count_robots*max_v_task:
    min_count_robots += 1

print(f"count robos = {min_count_robots}")

# запуск программы последователя для числа роботов
count_robots = min_count_robots
while (count_robots > 0):
    count_robots -= 10
    

