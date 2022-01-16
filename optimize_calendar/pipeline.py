from preprocess import preprocess
from solver.LinearSolver import suggest

def main(input, data_dir, year, week):
    preprocess(input=input, dir=data_dir)
    suggest(year=year, week=week, dir=data_dir)

if __name__ == '__main__':
    main(input='data/Demo_data.json', data_dir='data/', year=2022, week=2)
