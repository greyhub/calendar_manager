from datetime import datetime
import json
from typing import List
from ortools.linear_solver import pywraplp
import numpy as np
import pandas as pd
import time
from time import strftime
from time import gmtime
import os

from pandas.core.frame import DataFrame


def read_data(path, year, week):

    timetable = {}
    file_name = os.listdir(path)
    keys = [k[:-4] for k in file_name]
    count = 0
    for k in keys:
        __year = k.split('_')[0]
        __week = k.split('_')[1]
        name = k.split('_')[2]
        if __year == str(year) and __week == str(week):
            __path = path+ k +'.csv'
            timetable[name] = pd.read_csv(__path)
            count += 1

    return timetable, count

def df2list(df: DataFrame) -> list:
    return df.values.tolist()

def solver(M,D,H,L,timetable: dict):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Khoi tao bien
    x = {}
    for m in range(M):
        for d in range(D):
            for h in range(H):
                x[m*D*H + d*H + h] = solver.IntVar(0, 1, 'x[{},{},{}]'.format(m,d,h))
    # print('Number of variables =', solver.NumVariables())

    # Rang buoc 1. Khong trung thoi khoa bieu leader
    for d in range(D):
        for h in range(H):
            if L[0][h][d+1] == 1:
                # print('Day {} hour {}: Busy'.format(d, L[0][h][0]))
                ct = solver.Constraint(0, 0)
                for m in range(M):
                    ct.SetCoefficient(x[m*D*H + d*H + h], 1)

    # Rang buoc 2. So buoi hop cho moi group
    for m in range(M):
        sumT = 2
        T = solver.IntVar(sumT, sumT, 't')
        ct = solver.Constraint(0, 0)
        for d in range(D):
            for h in range(H):
                ct.SetCoefficient(x[m*D*H + d*H + h], 1)
        ct.SetCoefficient(T, -1)

    # Rang buoc 3. Khong trung thoi khoa bieu moi group
    for m in range(M):
        ct = solver.Constraint(0, 0)
        for d in range(D):
            for h in range(H):
                if L[m+1][h][d+1] == 1:
                    # print('Day {} hour {}: Busy'.format(d, L[m+1][h][0]))
                    ct.SetCoefficient(x[m*D*H + d*H + h], 1)

    # Rang buoc 4. Chi co toi da 1 group cho moi buoi hop
    for d in range(D):
        for h in range(H):
            ct = solver.Constraint(0, 1)
            for m in range(M):
                ct.SetCoefficient(x[m*D*H + d*H + h], 1)

    # Rang buoc 5. Thoi gian hop cho moi group la lien tuc
    # for m in range(M):
    #     sumT = 2
    #     for d in range(D):
    #         for h in range(H):
    #             if h > H - sumT + 1:
    #                 pass
    #             else:
    #                 T = solver.IntVar(sumT, sumT, 't')
    #                 ct = solver.Constraint(0, 0)
    #                 for i in range(sumT):
    #                     ct.SetCoefficient(x[m*D*H + d*H + i], 1)
    #                 ct.SetCoefficient(T, -1)

    
    status = solver.Solve()
    timetable_sg = timetable['leader'].copy()
    _meeting = []
    if status == pywraplp.Solver.OPTIMAL:
        # print('\n____Solution____')
        for m in range(M):
            # print('Group', m, ': ', end='')
            for d in range(D):
                for h in range(H):
                    if(x[m*D*H + d*H + h].solution_value() == 1):
                        # print(timetable_sg.columns[d+1],h+9,end=' | ')
                        _meeting.append([timetable_sg.columns[d+1],h+9,str(m)])
                        timetable_sg.iloc[h, d+1] = 'G'+str(m)
            # print()
    return timetable_sg, _meeting

def greedy(M,D,H,L,timetable):
#     res = open(name+'-out.txt', 'w')
#     print('\nSolution:')
#     c4t = []
#     count = 0
#     for j in range(M):
#       c4t.append([-1])
#     idx_c = sorted(range(len(d)), key=lambda k: d[k])
#     val = sorted(d)
#     for i in range(N):
#         teacher = checktc(c4t, i, count)
#         if teacher != None:
#           count += 1
#         else:
#           teacher = -1
#         print(i, teacher)
#         res.write(str(i)+' '+str(teacher))
#         res.write('\n')
#     print(count)
#     res.write(str(count))
#     res.close()
    return

def suggest(year, week, dir):

    timetable, num = read_data(dir+'group/', year, week)
    D = 7
    H = 8
    M = num
    L = []

    # L.append(df2list(timetable['leader']))
    leader_file = 'data/leader/' + str(year) + '_' + str(week) + '_' + 'leader.csv'
    timetable['leader'] = pd.read_csv(leader_file)
    L.append(df2list(timetable['leader']))
    # print('____Leader____\n', timetable['leader'])

    _gr = []
    # print('\nNumber of groups: {}'.format(num))
    for k in timetable.keys():
        if k != 'leader':
            # print('\n____{}____\n{}'.format(k, timetable[k]))
            L.append(df2list(timetable[k]))
            _gr.append(k)

    if M < 200:
        timetable_sg, _meeting = solver(M,D,H,L,timetable)
    else:
        timetable_sg, _meeting = greedy(M,D,H,L,timetable)

    # print(timetable['leader'])
    # print(timetable_sg)
    # print(_meeting)
    timetable_sg.to_csv('data/output/suggestion.csv', index=False)

    _events = []
    for m in _meeting:
        _group_name = _gr[int(m[2])]
        _s = str(year) + '-' + str(week) + '-' + str(m[0]) + ' ' + str(m[1])
        _start = datetime.strptime(_s, '%G-%V-%A %H')
        _s = str(year) + '-' + str(week) + '-' + str(m[0]) + ' ' + str(m[1]+1)
        _end = datetime.strptime(_s, '%G-%V-%A %H')
        _event = {}
        _event['user_id'] = -1
        _event['leader'] = True
        _event['title'] = 'Meeting with ' + _group_name
        _event['start'] = str(_start)
        _event['end'] = str(_end)
        # print(_event)
        _events.append(_event)
    # Serializing json 
    json_object = json.dumps(_events, indent = 4)
    
    # Writing to sample.json
    with open("data/output/suggestion.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':

    start = time.time()

    suggest(2022, 2, 'data/')

    end = time.time()
    run_time = end - start
    if run_time < 20:
        print(round(run_time * 1000), 'ms')
    elif run_time < 30:
        print(round(run_time), 's')
    else:
        print(strftime("%H:%M:%S", gmtime(run_time)))
