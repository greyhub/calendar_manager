from os import path
from re import I
from time import time
import pandas as pd
from datetime import datetime


def convertTime(s):
    date_object = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    full = date_object.isocalendar()
    year = date_object.isocalendar()[0]
    week = date_object.isocalendar()[1]
    dayOfWeek = date_object.strftime('%A')
    hour = date_object.strftime('%H')
    minute = date_object.strftime('%M')
    return year, week, dayOfWeek, hour

# print(convertTime("2022-01-01 15:05:00"))


def read_data(input, dir='data/'):

    _data = pd.read_json(input, orient='records').set_index('user_id')
    for i in _data.index.unique():
        _person = _data.loc[i]
        _leader = _person['leader'].iloc[0]
        if _leader:
            name = "leader"
            __dir = "leader/"
        else:
            name = "group" + str(i)
            __dir = "group/"
        _person = _person.drop(['leader', 'title'], axis=1)
        _person['start'] = _person['start'].apply(convertTime)
        _person['end'] = _person['end'].apply(convertTime)
        _person['year'] = _person['start'].apply(lambda x: x[0])
        _person['week'] = _person['start'].apply(lambda x: x[1])
        _person['dayOfWeek'] = _person['start'].apply(lambda x: x[2])
        _person['hour_start'] = _person['start'].apply(lambda x: x[3])
        _person['hour_end'] = _person['end'].apply(lambda x: x[3])
        _person = _person.drop(['start', 'end'], axis=1)
        _person = _person.reset_index(drop=True)
        _person = _person.set_index(['year', 'week']).sort_index()

        print(i)

        for j in _person.index.unique():
            print(j)
            __person = _person.loc[j]
            __name = '_'.join([str(j[0]), str(j[1]), name])
            __person.to_csv('data/'+'tmp/'+__name+'.csv', index=False)
            std_data(input='data/'+'tmp/'+__name+'.csv', output=__name+'.csv', dir=dir+__dir)
    return

def std_data(input, output, dir='data/'):
    _fmtperson = pd.read_csv("data/data_format.csv")
    _fmtperson = _fmtperson.set_index('Hour')

    _person = pd.read_csv(input)

    for i in _person.index:
        row = _person.loc[i]
        _dayOfWeek = row['dayOfWeek']
        _start = row['hour_start']
        _end = row['hour_end']
        if _start < 9 and _end <= 17:
            _start = 9
        if _start >= 9 and _end > 17:
            _end = 17
        if _start >= 9 and _end <= 17:
            if _start == _end:
                _fmtperson.loc[_start, _dayOfWeek] = 1
            else:
                for j in range(_start, _end):
                    _fmtperson.loc[j, _dayOfWeek] = 1

    _fmtperson.to_csv(dir+output)
    print('Saved to', dir+output)
    return

def preprocess(input, dir='data/'):
    read_data(input=input, dir=dir)
    return

if __name__ == '__main__':
    preprocess(input='data/Demo_data.json', dir='data/')
