These files contain sample code for the Cimpress Tech Challenge,
using PHP, Python, and Ruby. However, you may use any language
that can communicate with the API of our puzzle server.

See the rules for full information:

  http://cimpress.com/techchallenge


CALLING THE API

Note that the Puzzle API has two modes: trial and contest. Trial mode
is for practicing: your solutions (and mistakes) don't count. In
contest mode, everything counts toward your score. Make sure to
practice in trial mode until you are confident that your code will not
submit erroneous solutions to the API.

Each code sample explains how to switch between trial mode and contest
mode.

Don't forget to switch your code into "contest mode" when you are
ready!


USING THE CODE SAMPLES

- Each sample program contacts the puzzle server, downloads a
randomly-generated puzzle, and solves it using a trivial algorithm.
Your job is to create a winning algorithm.

- To run this code successfully, you must insert your Registration Key
into these code files. (Each file explains where to put your
registration key.)  If you don't have a Registration Key, you may
obtain one by registering at http://cimpress.com/techchallenge/register.

- The sample code files use only newline characters at the ends of
lines.  They should display fine in any code editor, but not
necessarily in Notepad or similar Windows programs that expect lines
to end in carriage return + newline.


API DOCUMENTATION

The Puzzle API is located at http://techchallenge.cimpress.com. You
communicate with it through HTTP POST and HTTP GET operations. The API
supports two operations: requesting a puzzle, and submitting a
solution. Both operations require your API key in the URI.

1. Requesting a puzzle

GET: /<key>/<mode>/puzzle

Example: if your registration key is 012345678901234567890123456789ab, and you are working
in trial mode, then you would issue a GET to:

   http://techchallenge.cimpress.com/012345678901234567890123456789ab/trial/puzzle

In "contest" mode, you would use:

   http://techchallenge.cimpress.com/012345678901234567890123456789ab/contest/puzzle

Sample response in JSON:

   {
     "id": "71ec6d9997be4821b2e38e7b5506f96d"
     "width": 25,
     "height": 20,
     "puzzle": [
                 [ true, true, false, ... ],
		 [ true, true, true, ...],
		 ...,
		 [ true, false, false, ... ]
	       ],
   }

The parameters are:

- "id": the unique ID of this puzzle. It is NOT your Registration Key.
The ID that comes with each puzzle is valid only ONCE; you may not
submit a second solution. (But you can request and solve more
puzzles!)

- "width" and "height": the dimensions of the puzzle grid

- "puzzle": a puzzle as an array of Boolean arrays, as explained in
the rules. Each inner array represents one row of the puzzle. The
value true represents a unit square that must be covered, and false
represents an empty grid cell that is a non-coverable obstacle.


2. Solving a puzzle

POST: /<key>/<mode>/solution

Example: if your Registration Key is 012345678901234567890123456789ab, and you are working
in trial mode, then you would post to:

   http://techchallenge.cimpress.com/012345678901234567890123456789ab/trial/solution

In "contest mode" you would use:

   http://techchallenge.cimpress.com/012345678901234567890123456789ab/contest/solution

The body of your HTTP POST must contain two values: the ID of the puzzle you
requested, and your solution. An example in JSON is:

   {
     "id": "71ec6d9997be4821b2e38e7b5506f96d",
     "squares": 
     [
       { "X": 3, "Y": 5, "Size": 2 },
       { "X": 5, "Y": 5, "Size": 1 },
       ...
     ]
   }

The parameters are:

- "id": The ID of the puzzle you're solving. This is NOT your
Registration Key.  It is the ID you received when you requested the
puzzle. The ID is valid only ONCE; you may not submit a second
solution. (But you can request and solve more puzzles!)

- "squares": Your solution as an array of hashes. Each array element
(a hash) represents one square of your solution. Its values are:

  - "X" and "Y": the (x,y) coordinate of the upper left corner of your square.
  - "Size": the side length of your square.

Here is a sample JSON response from the Puzzle API:

   {
     "numberOfSquares": 2,
     "score": 0,
     "timePenalty": 0,
     "errors": 
     [
       "Squares overlapped in position: X = 3, Y = 5",
       "Square outside of boundary" 
     ]
   }

The parameters are:

- "numberOfSquares": The total number of covering squares in the
solution you submitted.

- "score": The score that your solution received from our puzzle
server. In trial mode, this score doesn't count for anything.  In
contest mode, it counts toward the prizes. If a solution has errors,
the score will be zero.

- "timePenalty": If it takes more than 10 seconds for your solution to
reach the puzzle server, counting from when the puzzle was issued to
you, your score will be assessed a penalty. Zero means no penalty.

- "errors": An array of error messages regarding your solution. If
this array is empty (size = 0), then the puzzle server has judged your
solution to be a valid covering of the grid.  If your solution is
incorrect or you do not reply at all, you will be deemed to be doing
worse on this puzzle than anyone who submits a correct solution.  So,
practice in "trial mode" until you are confident that your program
will not submit erroneous solutions.


GOOD LUCK!
