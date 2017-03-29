# Project Euclid: Problem 96 Sudoku solver
"""
Su Doku (Japanese meaning number place) is the name given to a popular puzzle
concept. Its origin is unclear, but credit must be attributed to Leonhard Euler
who invented a similar, and much more difficult, puzzle idea called 
Latin Squares. The objective of Su Doku puzzles, however, is to replace the
blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3
box contains each of the digits 1 to 9. Below is an example of a typical
starting puzzle grid and its solution grid.

003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300

483921657
967345821
251876493
548132976
729564138
136798245
372689514
814253769
695417382

A well constructed Su Doku puzzle has a unique solution and can be solved by 
logic, although it may be necessary to employ "guess and test" methods in order
to eliminate options (there is much contested opinion over this). The 
complexity of the search determines the difficulty of the puzzle; the 
example above is considered easy because it can be solved by straight 
forward direct deduction.

The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'),
contains fifty different Su Doku puzzles ranging in difficulty, but all
with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in 
the top left corner of each solution grid; for example, 483 is the 3-digit 
number found in the top left corner of the solution grid above.

"""
import copy
from sudoku_solve import  *

   
current_puzzle = [[0]*9 for _ in range(9)]

f = open("sudoku.txt", 'r')
sudokus = f.read()
f.close()
puzzles = sudokus.split("Grid")

puzzle_number = 0
total_solved = 0
total_tried = 0


#--------------------------------------------------------------------

import time
start_time = time.time()
for puzzle in puzzles[1:]:
    title = puzzle.split('\n')[0:1]
    current_puzzle_txt = puzzle.split('\n')[1:10]
    i = 0
    for line in current_puzzle_txt:
        j = 0
        for chr in line:
            current_puzzle[i][j] = ord(chr)-ord('0')
            j += 1
        i += 1
    puzzle_number+=1
     
    #print("Grid",title[0])
 
    possibles = [[[1,2,3,4,5,6,7,8,9] for _ in range(9)] for _ in range(9)]
    possibles = init_possibles(current_puzzle, possibles)
    #sudoku_print("",possibles)
    current_solution, cells_solved = solve(possibles)
   
    if cells_solved == 81: 
        total_solved += 1
    else:
        pass
        #print("Cells_solved = ", cells_solved)

        
    #sudoku_print("Solution\n", current_solution)
    if cells_solved < 81:
        poss_print(possibles)
    
    total_tried += 1
    summ = summ + (100*current_solution[0][0][0] +  \
                   10*current_solution[0][1][0] + \
                    current_solution[0][2][0])
#----------------------------------------------------------
    
print("--- %4.2f seconds ---" % (time.time() - start_time))
print("Answer is ", summ, ". Expect 24702")
print("Total solved ", total_solved, " out of ",total_tried)
print("Brute force count = ", brute_force_count)
