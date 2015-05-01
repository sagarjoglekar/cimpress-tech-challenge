#!/usr/bin/python

########################################################################
# Cimpress Tech Challenge 2: Covering a grid with squares
# Sample solution by Cimpress (Python).
# Illustrates how to communicate with the Cimpress API server.
########################################################################

import json
import requests
import numpy

class Solver:
    # CHANGE THIS VALUE
    # Your unique API key obtained when you registered
    # Hard-code this. Use the same key for the entire contest.
    API_KEY = '1e4f3080545a444f9687ccb2751f07a9'

    # CHANGE THIS VALUE
    # The environment, either 'trial' for practicing and debugging, or 'contest'
    # for actual submissions that count.
    ENV = 'trial'

    # URL of contest server
    BASE_URL = 'http://techchallenge.cimpress.com'

    matrixCache = [];

    solution = [];

    # Retrieve a puzzle from the server. Returns JSON.
    def getPuzzle(self):
        url = '{0}/{1}/{2}/puzzle'.format(self.BASE_URL, self.API_KEY, self.ENV)
        return requests.get(url).text

    # Solution by Sagar J to solve the cimplress grid solver

    def check(self, col , row , neigh):
        print 'Checking for neighborhood ' + str(neigh)
        for i in range(col, col+neigh):
            for j in range(row, row+neigh):

                if(self.matrixCache[i][j] == 0):
                    for p in range(col, col+neigh-1):
                        for q in range(row, row+neigh-1):
                            self.matrixCache[p][q] = 0


                return (neigh-1)

        self.check(col, row, neigh+1)

    def solver(self,i,j):
        for col in range(i , puzzle['width']):
            for row in range(i, puzzle['height']):
                if(self.matrixCache[col][row] == 1):
                    size = self.check(col, row, 2)
                    self.solution.append({'X': col, 'Y': row, 'Size': size})
                    row = row + size
                    col = col + size

    def solve(self, puzzle):

        self.matrixCache = numpy.zeros((puzzle['width'],puzzle['height']))

        for col in range(0, puzzle['width']):
            for row in range(0, puzzle['height']):
                if puzzle['puzzle'][col][row]:
                    self.matrixCache[col][row] = 1

        self.solver(0, 0)

        return self.solution

    # Submit the solution. Returns JSON results.
    def submitSolution(self, id, squares):
        url = '{0}/{1}/{2}/solution'.format(self.BASE_URL, self.API_KEY, self.ENV)
        solution = {'id': id, 'squares': squares}
        return requests.post(url, data=json.dumps(solution)).text

# Main program
print 'Using API key: {0}'.format(Solver.API_KEY)
s = Solver()

# Get a puzzle, and convert the returned JSON to a Python dictionary
jsonResult = s.getPuzzle()
puzzle = json.loads(jsonResult)

# Demonstrate some of the returned values
print 'You retrieved a puzzle with {0} width x {1} height and ID={2}'.format(
    puzzle['width'],
    puzzle['height'],
    puzzle['id'])

print 'Generating solution'
squares = s.solve(puzzle)

print 'Submitting solution'
jsonResult = s.submitSolution(puzzle['id'], squares)

# Describe the response
response = json.loads(jsonResult);
if len(response['errors']) > 0:
    print 'Your solution failed with {0} problems and used {1} squares.'.format(
           len(response['errors']),
           response['numberOfSquares'])
else:
    print 'Your solution succeeded with {0} squares, for a score of {1}, with a time penalty of {2}.'.format(
           response['numberOfSquares'],
           response['score'],
           response['timePenalty'])
