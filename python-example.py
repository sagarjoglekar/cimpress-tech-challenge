#!/usr/bin/python

########################################################################
# Cimpress Tech Challenge 2: Covering a grid with squares
# Sample solution by Cimpress (Python).
# Illustrates how to communicate with the Cimpress API server.
########################################################################

import json
import requests

class Solver:
    # CHANGE THIS VALUE
    # Your unique API key obtained when you registered
    # Hard-code this. Use the same key for the entire contest.
    API_KEY = 'your key here'

    # CHANGE THIS VALUE
    # The environment, either 'trial' for practicing and debugging, or 'contest'
    # for actual submissions that count.
    ENV = 'trial'

    # URL of contest server
    BASE_URL = 'http://techchallenge.cimpress.com'

    # Retrieve a puzzle from the server. Returns JSON.
    def getPuzzle(self):
        url = '{0}/{1}/{2}/puzzle'.format(self.BASE_URL, self.API_KEY, self.ENV)
        return requests.get(url).text

    # Your solution algorithm!
    # Here is a naive solution that just covers each grid cell with a square of size 1.
    # Returns an array of arrays for convenient conversion to JSON.
    def solve(self, puzzle):
        solution = []
        for row in range(0, puzzle['height']):
            for col in range(0, puzzle['width']):
                if puzzle['puzzle'][row][col]:
                    solution.append({'X': col, 'Y': row, 'Size': 1})
        return solution

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
