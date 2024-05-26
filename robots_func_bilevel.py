#!/usr/bin/env python3  
import sys
import os
import numpy as np
import pandas as pd

from math import pi, cos

DBL_MAX =  99999999999.9
DBL_MIN = -99999999999.9
DBL_EPS = 1e-12
 
# Leader func
def robot_leader_func(robot_work_time, task_completion_time, t_alpha, t_lambda, t_q_0, M1, c_0, c, M2):
    t_q = {i:t_q_0[i]+t_alpha[i]*task_completion_time[i] for i in range(M1)}
    F1 = sum({i:t_lambda[i]*t_q[i] for i in range(M1)}) # the total amount of damages at all M1 tasks when all tasks are completed
    F2 = sum(c_0) # the state-determined cost of renting (or buying) M2 robots used in the tasks
    F3 = sum({i:c[i]*robot_work_time[i] for i in range(M2)}) # the running cost of all the robots

    return F1 + F2 + F3

# Follower func
def robot_follower_func(M1, X, t_s, Dist, v_task, v_path, M2):
    robot_work_time = np.zeros(M2)
    task_completion_time = np.zeros(M1)

    robot_paths = {}

    for i in range(M2):
        robot_path = [0]
        robot_work_time[i] = 0
        pnt = [(j, X[i][j]) for j in range(M1+1) if X[i][j] > 0]
        pnt = sorted(pnt, key=lambda t: t[1])
        # print("pnt\n", pnt)
        k = 0
        for j in range(len(pnt)):
            t_path = Dist[k][pnt[j][0]]/v_path[i]
            robot_work_time[i] += t_path
            k = pnt[j][0]
            if task_completion_time[k-1] == 0:
                t_task = t_s[pnt[j][0]-1]/v_task[i]
                robot_work_time[i] += t_task
                task_completion_time[k-1] = robot_work_time[i]
            robot_path.append(k)
        robot_paths[i] = robot_path

    return np.max(robot_work_time), robot_work_time, task_completion_time, robot_paths


def parse_tasks(fn):
    df = pd.read_csv(fn)
    t_alpha = df['alpha'].values[1:] # inherent increment rate of task
    t_s = df['s'].values[1:] # path length from depot to task
    t_lambda = df['lambda'].values[1:] # total amount of damage at task
    t_q_0 = df['q'].values[1:] # initial demand of task
    M1 = df.shape[0]-1
    Dist = df.iloc[0:M1+1,0:M1+1].values
    return t_alpha, t_s, t_lambda, t_q_0, Dist, M1


def parse_robots(fn):
    df = pd.read_csv(fn)
    c_0 = df['rent'].values # inherent cost of robot
    c = df['run'].values # running cost of robot
    v_task = df['v_task'].values # task efficiency of the robot
    v_path = df['v_path'].values # speed of the robot
    return c_0, c, v_task, v_path


def main():
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

    if flag == 1:
        print(X)

    check = sum(XX)
    if check < M1:
        print("{},{}".format(DBL_MAX, DBL_MAX))
        return

    follower_res, robot_work_time, task_completion_time, robot_paths  = robot_follower_func(M1, X, t_s, Dist, v_task, v_path, M2)
    leader_res = robot_leader_func(robot_work_time, task_completion_time, t_alpha, t_lambda, t_q_0, M1, c_0, c, M2)

    print("{},{}".format(leader_res, follower_res))

    if flag == 1:
        print(robot_paths)

if __name__ == "__main__":
    main()
