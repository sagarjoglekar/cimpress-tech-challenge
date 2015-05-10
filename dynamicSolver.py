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

    matrixCache = numpy.zeros((2,2));

    solution = [];

    # Retrieve a puzzle from the server. Returns JSON.
    def getPuzzle(self):
        url = '{0}/{1}/{2}/puzzle'.format(self.BASE_URL, self.API_KEY, self.ENV)
        return requests.get(url).text

    # Solution by Sagar J to solve the cimplress grid solver

    def nullifySquare(self, col, row, neigh):
         print "nullifying Square at {0} , {1} in {2} neighborhood".format(col , row , neigh)
         for p in range(col, col+neigh):
            for q in range(row, row+neigh):
                if(p < puzzle['width'] and q < puzzle['height']):
                    self.matrixCache[p][q] = 0


    def solver(self):
        subsolverMat = numpy.zeros((numpy.size(self.matrixCache[0:,0]),numpy.size(self.matrixCache[0,0:])), numpy.dtype('int64'))
        subsolverMat[0,0:] = self.matrixCache[0,0:]
        subsolverMat[0:,0] = self.matrixCache[0:,0]
        maxSize = 1
        subsquareRow = 0
        subsquareCol = 0
        for col in range (1, numpy.size(subsolverMat[0:,0])):
            for row in range (1, numpy.size(subsolverMat[0,0:])):
                if self.matrixCache[col][row] == 0:
                    subsolverMat[col][row] = 0
                else:
                    interim = min(subsolverMat[col-1][row-1],subsolverMat[col-1][row],subsolverMat[col][row-1])
                    subsolverMat[col][row] = interim +1
                    if(subsolverMat[col][row] > maxSize):
                        maxSize = subsolverMat[col][row]
                        subsquareRow = row - maxSize+1
                        subsquareCol = col - maxSize+1
        print subsolverMat

        if maxSize > 1:
            self.nullifySquare(subsquareCol, subsquareRow, maxSize)
            print "found A Square at: {0},{1} of size {2}".format(subsquareCol,subsquareRow,maxSize)

            self.solution.append({ 'X': subsquareCol, 'Y': subsquareRow, 'Size': maxSize })
            return 1
        else:
            return 0

    def findOneSquares(self):
        for col in range (0, numpy.size(self.matrixCache[0:,0])):
            for row in range (1, numpy.size(self.matrixCache[0,0:])):
                if self.matrixCache[col][row] == 1 :
                    self.solution.append({'X': col, 'Y': row, 'Size': 1})



    def solve(self, puzzle):
        xSize = puzzle['width'];
        ySize = puzzle['height'];
        self.matrixCache = numpy.zeros((xSize,ySize), numpy.dtype('int64'))

        print "size of the puzzle is : {0} x {1} ".format(xSize, ySize)

        for col in range(0, puzzle['width']):
            for row in range(0, puzzle['height']):
                if puzzle['puzzle'][row][col]:
                    self.matrixCache[col][row] = 1

        while self.solver():
            print "finding next one"
        self.findOneSquares()

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
    print 'Your solution failed with {0} problems and used {1} squares. score:{2} time Penalty: {3}'.format(
           len(response['errors']),
           response['numberOfSquares'],
           response['score'],
           response['timePenalty'])
    for i in range(0 , len(response['errors'])):
        print response['errors'][i]
else:
    print 'Your solution succeeded with {0} squares, for a score of {1}, with a time penalty of {2}.'.format(
           response['numberOfSquares'],
           response['score'],
           response['timePenalty'])
