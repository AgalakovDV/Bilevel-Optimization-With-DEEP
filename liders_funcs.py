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
def find_all_damage(t_end : list, start_damages : list, alphas : list, lambda_1 = 1):
    res = 0
    for q, alp, t in zip(start_damages, alphas, t_end):
        res += (q + alp*t)
    return res*lambda_1
 
   
# cost_renting() в статье это F2 (3.7)
# c_0 - список исходных цен на роботов
def cost_renting(c_0 : list):
    return sum(c_0)
    

# running_cost_robots() в статье это F3 (3.8)
def running_cost_robots():
    print("running_cost_robots() надо доделать")
    return 0
    

# rastrigin_func
#!/usr/bin/env python3  
import sys
import os

# Get environment variables
#leader_param_file = os.getenv('LEADER_PARAM_FILE')
#follower_param_file = sys.argv[1]
leader_param_file = "leader_params"



size = 0
alphas = []
start_damage = []
distance = []
count_types_robots = 0
v_path = []
v_task = []
c_0 = []

with open(leader_param_file, 'r') as fx:
    next(fx)
    
    for line_id, p in enumerate(fx):
        pp = p.split('=')[1]
        if (0 == line_id):  # count tasks
            size = int(pp)
        elif (1 == line_id):    # alphas (скорости приращения задач)
            lst_str = pp.split(' ')
            for el in lst_str:
                alphas.append(float(el))
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
                distance.append(lst_dist)
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
        elif (7 == line_id):    # начальная стаимость роботов
            lst_str = pp.split(' ')
            for el in lst_str:
                c_0.append(float(el))
        
print(size)
print(alphas)
print(start_damage)
print(distance)
print(count_types_robots)
print(v_path)
print(v_task)
print(c_0)
        

#yy = list()

#with open(follower_param_file, 'r') as fy:
#    next(fy)
#    next(fy)
#    for p in fy:
#        pp = p.split('=')[1]
#        yy.append(float(pp))

#res = rastrign_func(xx, yy)

#print("{},{}".format(res[0], res[1]))



