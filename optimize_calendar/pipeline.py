from preprocess import preprocess
from solver.LinearSolver import suggest

def main():
    preprocess(input='data/Demo_data.json', dir='data/')
    suggest(year=2022, week=2, dir='data/')
