#!/usr/bin/env python3  
import sys
import os
import numpy as np
import pandas as pd
import datetime

from math import pi, cos

DBL_MAX =  99999999999.9
DBL_MIN = -99999999999.9
DBL_EPS = 1e-12
 
# Leader func
def robot_leader_func(robot_work_time, task_completion_time, t_alpha, t_lambda, t_q_0, M1, c_0, c, M2):
    if (M2 == 1):
        with open("AAexp_2_2.txt", 'a+') as my_file:
            my_file.write("c_0: {}\n".format(c_0))
    t_q = {i:t_q_0[i]+t_alpha[i]*task_completion_time[i] for i in range(M1)}
    F1 = sum({i:t_lambda[i]*t_q[i] for i in range(M1)}.values()) # the total amount of damages at all M1 tasks when all tasks are completed
    F2 = c_0[0]*M2 # the state-determined cost of renting (or buying) M2 robots used in the tasks
    F3 = sum({i:c[i]*robot_work_time[i] for i in range(M2)}.values()) # the running cost of all the robots

    with open("AAexp_2_2.txt", 'a+') as my_file:
        my_file.write("t_q: {}\n".format(t_q))
        my_file.write("F1: {}\n".format(F1))
        my_file.write("F2: {}\n".format(F2))
        my_file.write("F3: {}\n".format(F3))
        my_file.write("F: {}\n".format(F1 + F2 + F3))

    return F1 + F2 + F3


# Follower func
def robot_follower_func(M1, X, t_s, Dist, v_task, v_path, M2):
    f = open('AAexp_2_2.txt','a+')
    f.write('\n robot_follower_func :\n')
    M1 = len(X[0]) - 1
    M2 = len(X)
    # print("M1: {}, M2: {}".format(M1, M2))
    f.write("X: {}\n".format(X))
    f.write("M1: {}, M2: {}\n".format(M1, M2))
    f.write('matr_Dist :{}\n'.format(Dist))
    robot_work_time = np.zeros(M2)
    task_completion_time = np.zeros(M1)

    robot_paths = {}
    for i in range(M2):
        robot_path = [0]
        robot_work_time[i] = 0
        pnt = [(j, X[i][j]) for j in range(1,M1+1) if X[i][j] > 0]
        pnt = sorted(pnt, key=lambda t: t[1], reverse=True)
        # print("{}) pnt: {}".format(i,pnt))
        f.write("{}) pnt: {}\n".format(i+1,pnt))
        k = 0
        for j in range(len(pnt)):
            # print("Dist[{}][{}]: {}".format(k,pnt[j][0],Dist[k][pnt[j][0]]))
            f.write("Dist[{}][{}]: {}\n".format(k,pnt[j][0],Dist[k][pnt[j][0]]))
            t_path = Dist[k][pnt[j][0]]/v_path[i]
            robot_work_time[i] += t_path
            k = pnt[j][0]
            # print("k: {}".format(k))
            f.write("k: {}\n".format(k))
            if task_completion_time[k-1] == 0:
                t_task = t_s[k-1]/v_task[i]
                robot_work_time[i] += t_task
                task_completion_time[k-1] = robot_work_time[i]
                # print("task_completion_time[{}]: {}".format(k-1,robot_work_time[i]))
                f.write("task_completion_time[{}]: {}\n".format(k-1,robot_work_time[i]))
            robot_path.append(k)
        robot_paths[i] = robot_path
    #     print("robot path: {}".format(robot_path))
        f.write("robot path: {}\n".format(robot_path))
    # print("robot work time: {}".format(robot_work_time))
    # print("task_completion_time: {}".format(task_completion_time))
    # print("robot paths: {}".format(robot_paths))
    f.write("robot work time: {}\n".format(robot_work_time))
    f.write("task_completion_time: {}\n".format(task_completion_time))
    f.write("robot paths: {}\n".format(robot_paths))
    
    f.close()

    return np.max(robot_work_time), robot_work_time, task_completion_time, robot_paths


def parse_tasks(fn):
    df = pd.read_csv(fn)
    t_alpha = df['alpha'].values[1:] # inherent increment rate of task
    t_s = df['s'].values[1:] # path length from depot to task
    t_lambda = df['lambda'].values[1:] # total amount of damage at task
    t_q_0 = df['q'].values[1:] # initial demand of task
    M1 = df.shape[0]-1
    Dist = df.iloc[0:M1+1,1:M1+2].values
    return t_alpha, t_s, t_lambda, t_q_0, Dist, M1


def parse_robots(fn):
    df = pd.read_csv(fn)
    c_0 = df['rent'].values # inherent cost of robot
    c = df['run'].values # running cost of robot
    v_task = df['v_task'].values # task efficiency of the robot
    v_path = df['v_path'].values # speed of the robot
    return c_0, c, v_task, v_path


def main():
    with open("AAexp_2_2.txt", 'a+') as my_file:
        my_file.write("\n------------------------------------\n")
        my_file.write("robot_func_bielevel.py:\ntime: {}\n".format(datetime.datetime.now()))
        
        
    # Get environment variables
    leader_param_file = os.getenv('LEADER_PARAM_FILE')
    if leader_param_file == '' or leader_param_file == None:
        leader_param_file = sys.argv[-2]
    follower_param_file = sys.argv[-1]
    tasks_table_file = sys.argv[1]
    robots_table_file = sys.argv[2]
    flag = int(sys.argv[3])

    t_alpha, t_s, t_lambda, t_q_0, Dist, M1 = parse_tasks(tasks_table_file)
    c_0, c, v_task, v_path = parse_robots(robots_table_file)
    
    # with open("AAexp_2_2.txt", 'a+') as my_file:
    #     my_file.write("M1: {}\n".format(M1))
    #     my_file.write("t_alpha: {}\n".format(t_alpha))
    #     my_file.write("t_s: {}\n".format(t_s))
    #     my_file.write("t_lambda: {}\n".format(t_lambda))
    #     my_file.write("t_q_0: {}\n".format(t_q_0))
    #     my_file.write("Dist: {}\n".format(Dist))
    #     my_file.write("c_0: {}\n".format(c_0))
    #     my_file.write("c: {}\n".format(c))
    #     my_file.write("v_task: {}\n".format(v_task))
    #     my_file.write("v_path: {}\n".format(v_path))
        

    leader_xx = list()

    with open(leader_param_file, 'r') as fx:
        next(fx)
        next(fx)
        for p in fx:
            pp = p.split('=')[1]
            leader_xx.append(float(pp))

    follower_yy = list()

    with open(follower_param_file, 'r') as fy:
        next(fy)
        next(fy)
        for p in fy:
#            print(p)
            pp = p.split('=')
            if len(pp) > 1:
                pp = pp[1]
#                print(pp)
                follower_yy.append(float(pp))

    M2 = int(leader_xx[0])
    X = np.zeros((M2, M1+1))
    XX = np.zeros(M1)
    k = 0
    for i in range(M2):
        for j in range(1, M1+1):
            X[i][j] = follower_yy[k]
            k += 1
            if X[i][j] > 0:
                XX[j-1] += 1
        X[i][0] = 0
        
    with open("AAexp_2_2.txt", 'a+') as my_file:
        my_file.write("M1: {}, M2: {}\n".format(M1, M2))
        my_file.write("X: {}\n".format(X))

    # check = sum(XX)
    for el in XX:
        if el <= 0:
            print("{},{}".format(DBL_MAX, DBL_MAX))
            return

    if flag == 1:
        print(X)

    follower_res, robot_work_time, task_completion_time, robot_paths  = robot_follower_func(M1, X, t_s, Dist, v_task, v_path, M2)
    with open("AAexp_2_2.txt", 'a+') as my_file:
        my_file.write("follower_res: {}\n".format(follower_res))
        my_file.write("robot_work_time: {}\n".format(robot_work_time))
        my_file.write("task_completion_time: {}\n".format(task_completion_time))
        my_file.write("robot_paths: {}\n".format(robot_paths))
        
    leader_res = robot_leader_func(robot_work_time, task_completion_time, t_alpha, t_lambda, t_q_0, M1, c_0, c, M2)
    with open("AAexp_2_2.txt", 'a+') as my_file:
        my_file.write("leader_res: {}\n---------------------------------------\n".format(leader_res))

    print("{},{}".format(leader_res, follower_res))

    if flag == 1:
        print(robot_paths)

if __name__ == "__main__":
    main()