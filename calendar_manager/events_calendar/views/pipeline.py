from events_calendar.views.preprocess import preprocess
from events_calendar.views.solver.LinearSolver import suggest

def pipeline(input, data_dir, year, week):
    preprocess(input=input, dir=data_dir)
    suggest(year=year, week=week, dir=data_dir)

if __name__ == '__main__':
    pipeline(input='data/Demo_data_1.json', data_dir='data/', year=2022, week=2)
