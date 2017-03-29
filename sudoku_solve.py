#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys   # for flush
import copy


def sudoku_txt_print(txt,sud):
    print(txt)
    print(sud, flush=True)


summ = 0
brute_force_count = 0

def sudoku_txt(sud):
    if sud == None:
        return ""
    txt = ""
    for i in range(0,9):
        for j in range(0,9):
            if len(sud[i][j]) == 1:
                txt += chr(ord('0') + sud[i][j][0])
            else:
                txt += "0"
            if (j == 2) or (j == 5) :
                txt += "|"
        if (i == 2) or (i == 5):
            txt += "\n---+---+---\n"
        else:
            txt += "\n"
    return txt
   
    

def sudoku_print(txt,sud):
    print(txt, end="")
    txt2 = sudoku_txt(sud)
    print(txt2, flush=True)
            
 #--------------------------------------------------------------------
 
def count_solved(possibles):
    solved = 0
    for i in possibles:
        #print("i=", i)
        for j in i:
            #print("j=", j)
            if len(j) == 1:
                solved += 1
             
    #print("solved_count=",solved)
    #poss_print(possibles)
    return solved

 #--------------------------------------------------------------------
            
def poss_print(possibles):
    for r in range(0,9):
        for c in range(0,9):
            print("[", end="")
            for p in possibles[r][c]:
                print("{0:1d} ".format(p), end="")
            print("]", end="")
            if (c == 2) or (c == 5) :
                print(" | ", end="")
        if (r == 2) or (r == 5):
            print("\n---+---+---")
        else:
            print("")

#--------------------------------------------------------------------
            
def init_possibles(puzzle, possibles):
    for r in range(0,9):
        for c in range(0,9):
            if puzzle[r][c] != 0:
                possibles[r][c] = [puzzle[r][c]]
    return possibles
        
def edit_possibles(possibles,row,col):
    
    val = possibles[row][col]
    if len(val) > 1:
        return possibles
    if len(val) == 0:
        #print("Warning: No possible values left, row, col = ",row,col)
        return possibles
    val = val[0]
    
    new_possibles = copy.deepcopy(possibles)
    # edit column
    for rrow in range(0,9):
        if rrow != row:
            if val in new_possibles[rrow][col]:
                new_possibles[rrow][col].remove(val)
    # edit row
    for rcol in range(0,9):
        if rcol != col:
            if val in new_possibles[row][rcol]:
                new_possibles[row][rcol].remove(val)    
    # edit square
    row_lb = (row//3)*3
    col_lb = (col//3)*3
    for sqrow in range(row_lb,row_lb+3):
        for sqcol in range(col_lb, col_lb+3): 
            if (sqrow != row) and (sqcol != col):
                if val in new_possibles[sqrow][sqcol]:
                    new_possibles[sqrow][sqcol].remove(val)

    return new_possibles

def possibles_valid(possibles):
    # Gone too far and removed all possibilities from a cell
    # follows a call to edit_possibles
    for r in range(0,9):
        for c in range(0,9):
            if len(possibles[r][c]) == 0:
                return False
    return True

def is_valid(possibles):
    # In force_solve. Looking for invalid solutions.
    # first - removed all possibilities
    if not possibles_valid(possibles): return False
    # next, look through unique possibles and see if any dups 

    for r in possibles:
        row = []
        for c in r:
            if len(c) == 1:
                row.append(c[0])       
        setr = set(row)     
        if len(setr) < len(row):
            #print("Invalid row", row, setr)
            # Got a dup
            return False
    for r in range(0,9):
        col = []
        for c in range(0,9):
            if len(possibles[r][c]) == 1:
                col.append(possibles[r][c][0])
        setc=set(col)

        if len(setc) < len(col):
            #print("Invalid col ",col, setc)
            # Got a dup in column
            return False
 
    for sqr in range(0,9,3):
        for sqc in range(0,9,3):
            sq=[]
            for r in range(sqr,sqr+3):
                for c in range(sqc,sqc+3):
                    if len(possibles[r][c]) == 1:
                        sq.append(possibles[r][c][0])
      
            setsq = set(sq)
            if len(setsq) < len(sq):
                #print("Invalid square at ", sqr, sqc, sq, setsq)
                return False
    
    return True
        

#--------------------------------------------------------------------

def force_solve(possibles, rr, cc, depth):
    global brute_force_count 
    if depth == 1:
        brute_force_count+=1
    worked = False
    #print("force_solve, depth = ", depth, rr, cc)
    solved = count_solved(possibles)
    if solved == 81: return possibles, True

    leave = False
    for r in range(rr,9):
        for c in range(cc,9):
            if len(possibles[r][c]) > 1:
                #print("Row=", r,"Col=", c)
               
                for poss in possibles[r][c]:
                    #print("Try ", poss)
                    possibles[r][c] =  [poss]
                    new_possibles = edit_possibles(possibles,r,c)
                    new_possibles, solved = solve(new_possibles)
                    #poss_print(new_possibles)
                    if is_valid(new_possibles):
                        new_count = count_solved(new_possibles)
                        if new_count == 81: return new_possibles, True
                        if new_count > solved:
                            pass
                            #print("New solved count = ", new_count)
                        cc = c+1
                        if cc > 8:
                            rr = r+1
                            cc = 0
                        else: 
                            rr = r
                        new_possibles,worked = force_solve(new_possibles, rr,cc, depth+1)
                        if is_valid(new_possibles):
                            return new_possibles, True
                        else:
                            #print("Not valid")
                            return possibles, False
                            
                    else:
                        #print("Possibles invalid, next poss")
                        leave = True
                        
                        
                        
 
        if leave:
            break
    if worked:
        return new_possibles, True
    else:
        return possibles, True


#--------------------------------------------------------------------                    
    
def solve(possibles):
    #poss_print(possibles)
    cells_solved = 0
        
    cells_solved = count_solved(possibles)
       

    iters = 0
    while True:

        row = col = 0
        iters += 1
        #print("Iteration ", iters)
     
        for i in possibles:
            #print("i=",i)
            for j in i:
                #print("j=", j)
                if len(j) == 1:
                    possibles = edit_possibles(possibles,row,col)
                else:
                    #print(row, col, j)
                    # 1.  Go round col/row/squares editing dups until no change
                    #     Go through row
                    for rcol in range(0,9):
                        if rcol != col:
                            rcval = possibles[row][rcol]
                            if len(rcval) == 1:
                                rcval = rcval[0]
                                if possibles[row][col].count(rcval) != 0:
                                    #print("row removing ", rcval)
                                    possibles[row][col].remove(rcval)
                    # Go through col
                    for rrow in range(0,9):
                        if rrow != row:
                            rcval = possibles[rrow][col]
                            if len(rcval) == 1:
                                rcval = rcval[0]
                                if possibles[row][col].count(rcval) != 0:
                                    #print("col removing ", rcval)
                                    possibles[row][col].remove(rcval)
                    # Go through square
                    row_lb = (row//3)*3
                    col_lb = (col//3)*3
                    for sqrow in range(row_lb,row_lb+3):
                        for sqcol in range(col_lb, col_lb+3): 
                            if sqcol != col and sqrow != row:
                                rcval = possibles[sqrow][sqcol]
                                if len(rcval) == 1:
                                    rcval = rcval[0]
                                    if possibles[row][col].count(rcval) != 0:
                                        #print("square removing ", rcval)
                                        possibles[row][col].remove(rcval)
                    new_solved = count_solved(possibles)
                    if cells_solved == 81:
                        return possibles, cells_solved                                      

                    # 2. Look in row/col/square for any unique possibilities
                    #print("Look for uniques in row")
                    for poss in range(1,10):
                        poss_count = 0
                        which_rcol = 0
                        for rcol in range(0,9):
                             #if len(possibles[row][rcol]) > 1:
                            if poss in possibles[row][rcol]:
                                #print("163: row, rcol, poss -",row, rcol, poss)
                                poss_count += 1
                                which_rcol = rcol
                                which_poss = poss
                                #print(poss_count, rcol, poss)
                        if poss_count == 1:
                            if len(possibles[row][which_rcol]) > 1:
                                #print("Got one in row, ",row,which_rcol,"gets", which_poss)
                                possibles[row][which_rcol] = [which_poss]
                                break
                    #-----look in col for any unique possibilities
                    #print("Look for uniques in col")
                    for poss in range(1,10):
                        poss_count = 0
                        which_rrow = 0
                        for rrow in range(0,9):
                             #if len(possibles[rrow][col]) > 1:
                            if poss in possibles[rrow][col]:
                                #print("163: row, rcol, poss -",rrow, col, poss)
                                poss_count += 1
                                which_rrow = rrow
                                which_poss = poss
                                #print(poss_count, rrow, poss)
                        if poss_count == 1:                               
                            if len(possibles[which_rrow][col]) > 1:
                                #print("Got one in col, ",which_rrow, col,"gets", which_poss)
                                possibles[which_rrow][col] = [which_poss]
                                break
                    
                    #-----look in square for any unique possibilities
                    #print("Look for uniques in square")
                    row_lb = (row//3)*3
                    col_lb = (col//3)*3
                    for poss in range(1,10):
                        poss_count = 0
                        which_rrow = 0                        
                        for sqrow in range(row_lb,row_lb+3):
                            for sqcol in range(col_lb, col_lb+3):
                                if poss in possibles[sqrow][sqcol]:
                                    #print("163: row, rcol, poss -",rrow, col, poss)
                                    poss_count += 1
                                    which_rrow = sqrow
                                    which_rcol = sqcol
                                    which_poss = poss
                        if poss_count == 1:
                            if len(possibles[which_rrow][which_rcol]) > 1:
                                #print("Got one in square, ",which_rrow, which_rcol,"gets", which_poss)
                                possibles[which_rrow][which_rcol] = [which_poss]
                                break 
                            
                    new_solved = count_solved(possibles)
                    if cells_solved == 81:
                        return possibles, cells_solved        
 
                col += 1
                if col > 8:
                    col = 0;
                    row += 1
     
        #poss_print(possibles)
      
        new_solved = count_solved(possibles)

        if new_solved == cells_solved:
            break   # not getting anywhere
        else:
            cells_solved = new_solved
            #print("Solved in simple loop=", new_solved)
        if cells_solved == 81:
            return possibles, cells_solved 

        row = col = 0
        for i in possibles:
            #print("i=",i)
            for j in i:
                #print("j=", j)
                if len(j) == 1:
                    possibles = edit_possibles(possibles,row,col)
                else:        
                    # look for saturated pairs in cols, rows, squares. eg. if you find 47 and 47 in
                    # possibles, remove 4 and 7 from same structure's possibles
                    # go through row
                    for rcol in range(0,9):
                        if len(possibles[row][rcol]) == 2:
                            val1 = possibles[row][rcol][0]
                            val2 = possibles[row][rcol][1]
                            #print("1 Row ",row,"col ", rcol, "val1, val2 = ",val1,val2)
                            for rcol2 in range(rcol+1,9):
                                if len(possibles[row][rcol2]) == 2: 
                                    if (val1 in possibles[row][rcol2]) and (
                                        val2 in possibles[row][rcol2]):
                                        #print("2 Row ",row, "col ", rcol2, "val1, val2 = ",val1,val2)
                                        # got a saturated pair
                                        #print("Saturated pair (row)", val1, val2," in ", row,rcol," and ",row,rcol2)
                                        for rcol3 in range(0,9):
                                            if len(possibles[row][rcol3]) > 2:
                                                if rcol3 != rcol and rcol3 != rcol2:
                                                    if val1 in possibles[row][rcol3]:
                                                        possibles[row][rcol3].remove(val1)
                                                    if val2 in possibles[row][rcol3]:
                                                        possibles[row][rcol3].remove(val2) 
                                                
                    # go through col
                    for rrow in range(0,9):
                        if len(possibles[rrow][col]) == 2:
                            val1 = possibles[rrow][col][0]
                            val2 = possibles[rrow][col][1]
                            for rrow2 in range(rrow+1,9):
                                if len(possibles[rrow2][col]) == 2: 
                                    if (val1 in possibles[rrow2][col]) and (
                                        val2 in possibles[rrow2][col]):
                                        # got a saturated pair
                                        #print("Saturated pair (col)", val1, val2," in ", rrow,col," and ",rrow2,col)
                                        for rrow3 in range(0,9):
                                            if len(possibles[rrow3][col]) > 2:
                                                if rrow3 != rrow and rrow3 != rrow2:
                                                    if val1 in possibles[rrow3][col]:
                                                        possibles[rrow3][col].remove(val1)
                                                    if val2 in possibles[rrow3][col]:
                                                        possibles[rrow3][col].remove(val2) 
                                            
                    # go through square
                    row_lb = (row//3)*3
                    col_lb = (col//3)*3 
                    sq=[]
                    for sqrow in range(row_lb,row_lb+3):
                        for sqcol in range(col_lb, col_lb+3): 
                            sq.append([sqrow, sqcol])
                    
                    idx = 0
                    for sqr in sq:
                        sqrow = sqr[0]
                        sqcol = sqr[1]
                        if len(possibles[sqrow][sqcol]) == 2:
                            val1 = possibles[sqrow][sqcol][0]
                            val2 = possibles[sqrow][sqcol][1]
                            for sq2 in sq[idx+1:9]:
                                sqrow2 = sq2[0]
                                sqcol2 = sq2[1]
                                if len(possibles[sqrow2][sqcol2]) == 2: 
                                    if (val1 in possibles[sqrow2][sqcol2]) and (
                                        val2 in possibles[sqrow2][sqcol2]):
                                        # got a saturated pair
                                        #print("Saturated pair (sq)", val1, val2," in ", sqrow,sqcol," and ", sqrow2,sqcol2)
                                        for sq3 in sq:
                                            sqrow3 = sq3[0]
                                            sqcol3 = sq3[1]
                                            if len(possibles[sqrow3][sqcol3]) > 2:
                                                if sqrow3 != sqrow and sqrow3 != sqrow2:
                                                    if val1 in possibles[sqrow3][sqcol3]:
                                                        possibles[sqrow3][sqcol3].remove(val1)
                                                    if val2 in possibles[sqrow3][sqcol3]:
                                                        possibles[sqrow3][sqcol3].remove(val2)
                        idx+=1
                        
                # In a square, if a number is only found in a specific row or a 
                # specific column, then
                # you can edit out that number from the same row or column 
                # outside the square.
                # go through square
                row_lb = (row//3)*3
                col_lb = (col//3)*3 
                sq=[]
                for sqrow in range(row_lb,row_lb+3):
                    for sqcol in range(col_lb, col_lb+3): 
                        sq.append([sqrow, sqcol])                
                for poss in range(1,10):
                    # do it for the rows
                    for sqrow in range(row_lb,row_lb+3):
                        if ((poss in possibles[sqrow][col_lb]) or 
                            (poss in possibles[sqrow][col_lb+1]) or
                            (poss in possibles[sqrow][col_lb+2])):
                            found = False
                            for sq1 in sq:
                                if sq1[0] != sqrow:
                                    if poss in possibles[sq1[0]][sq1[1]]:
                                        found = True
                            if not found:
                                #print(poss, "found in", row_lb, col_lb, " only in row", sqrow)
                                # we have a row
                                for rcol in range(0,9):
                                    if poss in possibles[sqrow][rcol]:
                                        if (rcol < col_lb) or (rcol > col_lb+2):
                                            #print("removing ", poss, "from ", sqrow, rcol)
                                            possibles[sqrow][rcol].remove(poss)
                    # do it for the cols
                    for sqcol in range(col_lb,col_lb+3): 
                        if (poss in possibles[row_lb][sqcol] or 
                            poss in possibles[row_lb+1][sqcol] or
                            poss in possibles[row_lb+2][sqcol]):
                            found = False
                            for sq1 in sq:
                                if sq1[1] != sqcol:
                                    if poss in possibles[sq1[0]][sq1[1]]:
                                        found = True
                            if not found:
                                #print(poss, "found in", row_lb, col_lb, " only in col", sqcol)
                                # we have a col
                                for rrow in range(0,9):
                                    if poss in possibles[rrow][sqcol]:
                                        if (rrow < row_lb) or (rrow > row_lb+2):
                                            #print("Removing ", poss, "from", rrow, sqcol)
                                            possibles[rrow][sqcol].remove(poss)                    
 
                     
                # Similar to search for saturated pairs. If we find any pair in 
                # row col, square which are the only ones with 2 possibles, edit out 
                # their other possibilities
                # eg. 476 and 478 in a row and no other 4 or 7 - edit out 6 and 8
                # Search r/c/sq for each possibility. If only 2, try each of the 
                # other cells for a match. But note 478 and 478 is no good (unless
                # in 3 unique cells)
                #TBD 43/50 solved so far.
                # go through column
                """ 
                for rcol in range(0,9):
                    lposs = len(possibles[row][rcol]) 
                    if lposs > 2:
                        for i in range(0,lposs):
                            print(possibles[row][rcol])
                            print("i=", i)
                            iposs = possibles[row][rcol][i]
                            for j in range(i+1,lposs):
                                print("j=", j, "lposs=", lposs)
                                print(row, col, possibles[row][rcol])
                                jposs = possibles[row][rcol][j]
                                count_pair = 1
                                for rc1 in range(0,9):
                                    if rc1 != rcol:
                                        if len(possibles[row][rc1]) >= 2:
                                            if (iposs in possibles[row][rc1]) and (
                                                jposs in possibles[row][rc1]):
                                                count_pair += 1
                                                which_rc1 = rc1
                                if count_pair == 2:    
                                    sudoku_print("Temp\n",res)
                                    poss_print(possibles)
                                    print(row, col,possibles[row][rcol], 
                                          row, which_rc1,possibles[row][which_rc1])
                                    possibles[row][rcol] = [iposs,jposs]
                                    possibles[row][which_rc1] = [iposs,jposs]
                                    print("Reducing to saturated pairs, Got one ",
                                          row,rcol,row, which_rc1, "get ",iposs,jposs)
                                    lposs = len(possibles[row][rcol]) 
                                    break
                 
                                    
                """
             
                col += 1
                if col > 8:
                    col = 0;
                    row += 1

        #poss_print(possibles)
 
        new_solved = count_solved(possibles)

        if new_solved == cells_solved:
            break   # not getting anywhere
        else:
            cells_solved = new_solved
            #print("Solved in more complex loop=", new_solved)
        if cells_solved == 81:
            return possibles, cells_solved
       
        
    #print("Iterations = ",iters)
      
    if cells_solved < 81:
        #print("Brute force")
        #sudoku_print("",possibles)
        possibles, worked  = force_solve(possibles,0,0,1)
        if not worked:
            print("Force solve failed")
        cells_solved = count_solved(possibles)

     
    return possibles, cells_solved

    

#--------------------------------------------------------------------
    
def sudoku_solve(txt):

    current_puzzle = [[0]*9 for _ in range(9)]
    puzzle_txt = txt.split('\n')
    i = 0
    for line in puzzle_txt:
        j = 0
        for chr in line:
            current_puzzle[i][j] = int(chr)
            j += 1
        i += 1

 
    possibles = [[[1,2,3,4,5,6,7,8,9] for _ in range(9)] for _ in range(9)]
    possibles = init_possibles(current_puzzle, possibles)
    #sudoku_print("",possibles)
    current_solution, cells_solved = solve(possibles)
   
    #sudoku_print("Solution\n", current_solution)
    if cells_solved < 81:
        poss_print(possibles)
    
    #----------------------------------------------------------
    global brute_force_count    
    if brute_force_count != 0:
        print("Brute force count = ", brute_force_count, flush=True)
        brute_force_count = 0
    return current_solution

#----------------------------------------------------------
