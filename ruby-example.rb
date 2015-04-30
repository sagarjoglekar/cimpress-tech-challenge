#!/usr/bin/ruby

########################################################################
# Cimpress Tech Challenge 2: Covering a grid with squares
# Sample solution by Cimpress (Ruby).
# Illustrates how to communicate with the Cimpress API server.
########################################################################

require 'rubygems'
require 'json'
require 'net/http'

class Solver

  # CHANGE THIS VALUE
  # Your unique API key obtained when you registered
  # Hard-code this. Use the same key for the entire contest.
  @@api_key = 'your key here'

  # CHANGE THIS VALUE
  # The environment, either 'trial' for practicing and debugging, or 'contest'
  # for actual submissions that count.
  @@env = 'trial'

  # URL of contest server
  @@base_url = 'http://techchallenge.cimpress.com'

  # Retrieve a puzzle from the server. Returns JSON.
  def getPuzzle()
    url = sprintf('%s/%s/%s/puzzle', @@base_url, @@api_key, @@env)
    return Net::HTTP.get(URI(url))
  end

  # Your solution algorithm!
  # Here is a naive solution that just covers each grid cell with a square of size 1.
  # Returns an array of hashes for convenient conversion to JSON.
  def solve(puzzle)
    result = Array.new
    puzzle['puzzle'].each_with_index do |row, rowindex|
      row.each_with_index do |column, colindex|
        if puzzle['puzzle'][rowindex][colindex] == true
          result.push({'X' => colindex, 'Y' => rowindex, 'Size' => 1})
        end
      end
    end
    return result
  end

  # Submit the solution. Returns JSON results.
  def submitSolution(puzzleID, squares)
    # URL for submissions
    url = sprintf('%s/%s/%s/solution', @@base_url, @@api_key, @@env);
    uri = URI(url)

    # The solution as a hash.
    solution = {'id' => puzzleID, 'squares' => squares}

    # Do the post and return the JSON
    http = Net::HTTP.new(uri.host, uri.port)
    response = http.post(uri.path, solution.to_json)
    return response.body
  end

end


# Main program
if __FILE__ == $0 
  solver = Solver.new
  json = solver.getPuzzle()
  puzzle = JSON.parse(json)

  printf("You retrieved a puzzle with %d width x %d height and ID=%s\n",
         puzzle['width'],
         puzzle['height'],
         puzzle['id'])

  puts "Generating solution"
  squares = solver.solve(puzzle)

  puts "Submitting solution"
  json = solver.submitSolution(puzzle['id'], squares)
  result = JSON.parse(json)

  if result['errors'].length > 0
    printf("Your solution failed with %d problems and used %d squares.\n",
           result['errors'].length,
           result['numberOfSquares'])
  else
    printf("Your solution succeeded with %d squares, for a score of %d, with a time penalty of %d.\n",
           result['numberOfSquares'],
           result['score'],
           result['timePenalty'])
  end
end
