#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 23:36:32 2024

@author: Daniil
"""

import numpy as np
# import pandas as pd
from random import randint


def CreateTasksAndRobots(filename, task_name, robot_name):
    with open(filename, 'r') as myFile:
        for i in range(3):
            next(myFile)
        # size
        p = myFile.readline()
        pp = p.split(':')[1].strip()
        count = int(pp)
        for i in range(3):
            next(myFile)
        #count = 2
        coords = np.zeros((count, 2))
        alphas = np.zeros(count)
        t_s = np.zeros(count)
        lambdas = np.ones(count)
        lambdas[0] = 0
        q_0 = np.zeros(count)
    
        # distance
        for (i,p) in zip(range(count), myFile):
            pp = p.split('\t')
            coords[i][0] = pp[1]
            coords[i][1] = pp[2]
        
        # demand (t_s and alphas)
        next(myFile)
        next(myFile)
        max_t_s = 0
        for (i,p) in zip(range(1,count), myFile):
            pp = p.split('\t')
            t_s[i] = int(pp[1])
            if (max_t_s < t_s[i]):
                max_t_s = t_s[i]
            alphas[i] = round(t_s[i]**0.5 + 5)
        
    left = round(0.2*max_t_s)
    right = 2*left
    
    sizes = np.zeros((count, count))
    v_path = np.zeros(count)
    v_task = np.zeros(count)
    c_0 = np.ones(count) * 100
    c = np.ones(count) * 10
    
    max_d = 0
    min_d = 9999999
    avg = 0
    
    ga = 0
    gb = count//3
    gc = gb*2
    for i in range(count):
        for j in range(i+1, count):
            x_i = coords[i][0]
            x_j = coords[j][0]
            y_i = coords[i][1]
            y_j = coords[j][1]
            d = ((x_i - x_j)**2 + (y_i - y_j)**2)**0.5
            sizes[j][i] = sizes[i][j] = round(d,2)
            if (d < min_d):
                min_d = d
            if (d > max_d):
                max_d = d
            avg += d
        
        v_task[i] = max_t_s * 0.3   # _1
        v_path[i] = 300             # _1
        if (i == ga or i == gb or i == gc):
            v_task[i] = randint(left, right) # _2, _3
            v_path[i] = randint(200, 400)    # _2, _3
            c[i] = 10 - (0.3 * max_t_s - v_task[i])//4 - (300 - v_path[i])//64 #_3
            if (c[i] < 1):   #_3
                c[i] = 1     #_3
            if (c[i] >= 30): #_3
                c[i] = 30    #_3
        else:
            v_task[i] = v_task[i-1] # _2, _3
            v_path[i] = v_path[i-1]    # _2, _3
            c[i] = c[i-1]
        
    print("max_dist = {}, min_dist = {},  avg_dist = {}".format(max_d, min_d, 2*avg / (count) / (count-1)))
    print("max_t_s = {}".format(max_t_s))
          
#    print("\n-----------\ncoords:\n{}\n---------\n".format(coords))          
#    print("\n\n---------\nsizes :\n{}\nalphas:\n{}\nt_s:\n{}\nv_path:\n{}\nv_task:\n{}\n".format(sizes, alphas, t_s, v_path, v_task))    
            
    with open(task_name, 'w') as myFile:
        print("\n-----------------------------------\ntasks write")
        res = ','
        for i in range(count):
            res += str(i)
            res += ','
        res += "q,alpha,lambda,s\n"
#        print(res, end='')
        myFile.write(res)
        for i in range(count):
            res = ''
            res += str(i)
            res += ','
            for j in range(count):
                res += str(sizes[i][j])
                res += ','
            res += str(q_0[i])
            res += ','
            res += str(alphas[i])
            res += ','
            res += str(lambdas[i])
            res += ','
            res += str(t_s[i])
            res += '\n'
            myFile.write(res)
#            print(res, end='')
        print('task file {} is recorded'.format(task_name))
            
    with open(robot_name, 'w') as myFile:
        print("\n-----------------------------------\nrobot write")
        res = ',rent,run,v_task,v_path'
        res2 = '' # доболнительные роботы для оптимизатора
        myFile.write(res)
        for i in range(count-1):
            res = '\n'
            res += str(i)
            res += ','
            res += str(c_0[i])
            res += ','
            res += str(c[i])
            res += ','
            res += str(round(v_task[i],2))
            res += ','
            res += str(v_path[i])
            # res += '\n'
            myFile.write(res)
        for i in range(count-1):
            res2 = '\n'
            res2 += str(i + count - 1)
            res2 += ','
            res2 += str(c_0[i])
            res2 += ','
            res2 += str(c[i])
            res2 += ','
            res2 += str(round(v_task[i],2))
            res2 += ','
            res2 += str(v_path[i])
            myFile.write(res2)
        print('robot file {} is recorded'.format(robot_name))
            

def main():
    print("hi")
    # filename = 'E:/диплом/третий_этап/clients_base/X/X-n101-k25.vrp.txt'
    filename = 'E:/диплом/третий_этап/clients_base/X/X-n11.txt'
    # filename = 'E:/диплом/третий_этап/clients_base/X/X_n15.txt'
    # filename = 'E:/диплом/третий_этап/clients_base/X/X-n3.txt'
    # имена task_name = 'E:/диплом/третий_этап/clients_base/X/11/task_11_2.csv'# имена
    # имена rob_name = 'E:/диплом/третий_этап/clients_base/X/11/rob_11_2.csv'  # имена
    # filename = 'E:/диплом/третий_этап/clients_base/X/X-n4.txt'
    # filename = 'E:/диплом/третий_этап/clients_base/X/X_n41.txt'
    task_name = 'E:/диплом/третий_этап/clients_base/X/11/task_11_3.csv'
    rob_name = 'E:/диплом/третий_этап/clients_base/X/11/rob_11_3.csv'
    CreateTasksAndRobots(filename, task_name, rob_name)
    
    
    
if __name__ == "__main__":
    main()