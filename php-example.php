<?php

########################################################################
# Cimpress Tech Challenge 2: Covering a grid with squares
# Sample solution by Cimpress (PHP).
# Illustrates how to communicate with the Cimpress API server.
########################################################################

class Solver {
	// CHANGE THIS VALUE
	// Your unique API key obtained when you registered
	// Hard-code this. Use the same key for the entire contest.
	const API_KEY = 'your key here';

	// CHANGE THIS VALUE
	// The environment, either 'trial' for practicing and debugging, or 'contest'
	// for actual submissions that count.
	const ENV = 'trial';

	// URL of contest server
	const BASE_URL = 'http://techchallenge.cimpress.com';

	// Retrieve a puzzle from the server. Returns JSON.
	public function getPuzzle() {
		// The URL for retrieving a puzzle instance
		$url = sprintf('%s/%s/%s/puzzle', self::BASE_URL, self::API_KEY, self::ENV);

		// Do the HTTP GET
		$json = file_get_contents($url);
		if ($json === false) {
			echo "Something went wrong. Check the HTTP response.\n";
			exit(1);
		}
		return $json;
	}

	// Your solution algorithm!
	// Here is a naive solution that just covers each grid cell with a square of size 1.
	// Returns an array of arrays for convenient conversion to JSON.
	public function solve($puzzle) {
		$solution = array();
		for ($row = 0; $row < $puzzle->height; $row++) {
			for ($column = 0; $column < $puzzle->width; $column++) {
				if ($puzzle->puzzle[$row][$column]) {
					$solution[] = array(
							    'X' => $column,
							    'Y' => $row,
							    'Size' => 1,
							    );
				}
			}
		}
		return $solution;
	}

	// Submit the solution. Returns JSON results.
	public function submitSolution($puzzleID, $squares) {
		// URL for submissions
		$url = sprintf('%s/%s/%s/solution', self::BASE_URL, self::API_KEY, self::ENV);

		// The solution as an array. Will get converted into JSON by the code below.
		$solution = array(
				  'id' => $puzzleID,
				  'squares' => $squares,
				  );

		// Do the HTTP POST.
		// There are various ways to do this in PHP.
		// Here we use the PHP cURL functions.
		// Many systems have them installed, but some don't.
		// For example, on Ubuntu Linux, install them with:
		//    sudo apt-get install php5-curl
		// More information:
		//    http://php.net/manual/en/book.curl.php
		$ch = curl_init($url);
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($solution));
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

		$json = curl_exec($ch);
		curl_close($ch);

		return $json;
	}
}


# Main program
echo 'Using API key: ' . Solver::API_KEY . "\n";
$solver = new Solver();

# Get a puzzle, and convert the returned JSON to a PHP object
$json = $solver->getPuzzle();
$puzzle = json_decode($json);

# Demonstrate some of the returned values
printf("You retrieved a puzzle with %d width x %d height and ID=%s\n",
       $puzzle->width,
       $puzzle->height,
       $puzzle->id);

echo "Generating solution\n";
$squares = $solver->solve($puzzle);

echo "Submitting solution\n";
$json = $solver->submitSolution($puzzle->id, $squares);
if ($json === false) {
	echo "Submission failed - server error\n";
	exit(1);
}

# Describe the response
$response = json_decode($json);
if (count($response->errors) > 0) {
	printf("Your solution failed with %d problems and used %d squares.\n",
	       count($response->errors),
	       $response->numberOfSquares);
} else {
	printf("Your solution succeeded with %d squares, for a score of %d, with a time penalty of %d.\n",
	       $response->numberOfSquares,
	       $response->score,
	       $response->timePenalty);
}
