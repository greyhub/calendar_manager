from typing import List
from ortools.linear_solver import pywraplp
import numpy as np
import pandas as pd
import time
from time import strftime
from time import gmtime
import os

from pandas.core.frame import DataFrame


def read_data(path='data/'):

    timetable = {}
    file_name = os.listdir(path)
    keys = [k[:-4] for k in file_name]
    for k in keys:
        timetable[k] = pd.read_csv(path+k+'.csv')

    return timetable, len(keys)-1

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
    print('Number of variables =', solver.NumVariables())

    # Rang buoc 1. Khong trung thoi khoa bieu leader
    for d in range(D):
        for h in range(H):
            if L[0][h][d+1] == 1:
                print('Day {} hour {}: Busy'.format(d, L[0][h][0]))
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
                    print('Day {} hour {}: Busy'.format(d, L[m+1][h][0]))
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
    if status == pywraplp.Solver.OPTIMAL:
        print('\n____Solution____')
        for m in range(M):
            print('Group', m, ': ', end='')
            for d in range(D):
                for h in range(H):
                    # print(x[m*D*H + d*H + h].solution_value())
                    if(x[m*D*H + d*H + h].solution_value() == 1):
                        print(d,h+9,end=' | ')
                        timetable['leader'].iloc[h, d+1] = 'G'+str(m)
            print()
    return timetable


if __name__ == '__main__':
    timetable, num = read_data('data/')
    D = 7
    H = 8
    M = num
    L = []

    print('____Leader____\n', timetable['leader'])
    L.append(df2list(timetable['leader']))

    print('\nNumber of groups: {}'.format(num))
    for k in timetable.keys():
        if k != 'leader':
            print('\n____{}____\n{}'.format(k, timetable[k]))
            L.append(df2list(timetable[k]))

    timetable_sg = solver(M,D,H,L,timetable)
    print(timetable['leader'])
