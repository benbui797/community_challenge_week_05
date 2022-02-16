import pandas as pd
# import requests
import os

def clear():
    os.system('cls')

# url = "https://community-challenge.netlify.app/data/sudoku2Solve.json"
# r2 = requests.get(url)
# json_file2 = r2.json()
# sudoku_solve = json_file2["sudokuSolve"]

df_medium = pd.read_csv("sudoku_medium.csv", header=None)
df_hard = pd.read_csv("sudoku_hard.csv", header=None)
df_evil = pd.read_csv("sudoku_evil.csv", header=None)
df_evil2 = pd.read_csv("sudoku_evil2.csv", header=None)

sudoku_medium = df_medium.to_numpy().tolist()
sudoku_hard = df_hard.to_numpy().tolist()
sudoku_evil = df_evil.to_numpy().tolist()
sudoku_evil2 = df_evil2.to_numpy().tolist()

def find_missing(numbers_list):
    missing_list = []
    for i in range(1,10):
        if i not in numbers_list:
            missing_list.append(i)
    return missing_list

def find_easy_row(grid):
    frow = None
    frow_count = 9
    frow_values = None

    for r in range(9):
        if grid[r].count(0) != 0 and grid[r].count(0) < frow_count:
            frow = r
            frow_count = grid[frow].count(0)
            frow_values = grid[frow]
    return frow, frow_count, frow_values

def find_easy_column(grid):
    fcol = None
    fcol_count = 9
    fcol_values = None

    for c in range(9):
        col_values = [grid[i][c] for i in range(9)]
        if col_values.count(0) != 0 and col_values.count(0) < fcol_count:
            fcol = c
            fcol_count = col_values.count(0)
            fcol_values = col_values
    return fcol, fcol_count, fcol_values

def find_easy_block(grid):
    fblockrows = None
    fblockcols = None
    fblock_count = 9
    fblock_values = None
    
    for block_r_start in range(0, 9, 3):
        for block_c_start in range(0, 9 ,3):
            block_values = [grid[r][c] for r in range(block_r_start, block_r_start + 3) for c in range(block_c_start, block_c_start +3)]
            block_rows = [r for r in range(block_r_start, block_r_start + 3)]
            block_cols = [c for c in range(block_c_start, block_c_start + 3)]
            if block_values.count(0) != 0 and block_values.count(0) < fblock_count:
                fblock_count = block_values.count(0)
                fblockrows = block_rows
                fblockcols = block_cols
                fblock_values = block_values
    return fblockrows, fblockcols, fblock_count, fblock_values

def get_block_values(grid, row, col):
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    block_values = [grid[r][c] for r in range(row_start, row_start + 3) for c in range(col_start, col_start +3)]
    return block_values

def find_easy_cell(grid):
    frow, frow_count, frow_values = find_easy_row(grid)
    fcol, fcol_count, fcol_values = find_easy_column(grid)
    fblockrows, fblockcols, fblock_count, fblock_values = find_easy_block(grid)
    
    # if all rows are full, return None
    if frow == None:
        return None, None, None
    
    # if block is most filled, get missing values from block. 
    # Get first empty cell in block and get missing values for that row and column.
    #
    # elif column is most filled, get missing values for column, row and empty cell block.
    #
    # elif row is most filled, get missing values for column, row and empty cell block.

    if fblock_count < fcol_count and fblock_count < frow_count:
        for r in fblockrows:
            for c in fblockcols:
                if grid[r][c] == 0:
                    col_values = [grid[i][c] for i in range(9)]
                    row_values = grid[r]
                    guesslist = find_missing(fblock_values + col_values + row_values)
                    return r, c, guesslist
    elif fcol_count < frow_count:
        for r in range(9):
            if grid[r][fcol] == 0:
                row_values = grid[r]
                block_values = get_block_values(grid, r, fcol)
                guesslist = find_missing(fcol_values + row_values + block_values)
                return r, fcol, guesslist
    elif frow_count <= fcol_count:
        for c in range(9):
            if grid[frow][c] == 0:
                block_values = get_block_values(grid, frow, c)
                col_values = [grid[i][c] for i in range(9)]
                guesslist = find_missing(frow_values + block_values + col_values)
                return frow, c, guesslist
    return None, None, None

def find_empty_cell(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None, None

def check_guess(grid, guess, row, col, x_sudoku=False):
    
    # Check if guess is in the same row
    row_values = grid[row]
    if guess in row_values:
        return False

    # Check if guess is in the same column    
    
    col_values = [grid[i][col] for i in range(9)]
    if guess in col_values:
        return False

    # Check if guess is in the same 'block'
    
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start +3):
            if grid[r][c] == guess:
                return False
    
    # Check if guess is on diagonal axis
    if x_sudoku is True:
        for i in range(9):
            if grid[i][i] == guess:
                return False
        for j in range(9):           
            if grid[0+j][8-j] == guess:
                return False
    return True

def solve_sudoku(grid):
    # row, col = find_empty_cell(grid)
    row, col, guesslist = find_easy_cell(grid)
    if row is None:
        return True

    # for guess in range(1, 10):
    for guess in guesslist:
        global counter
        counter += 1
        if check_guess(grid, guess, row, col):
            grid[row][col] = guess
            # clear()
            # grid_print(grid)
            if solve_sudoku(grid):
                return True
        grid[row][col] = 0
    return False

def grid_print(grid):
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("-" * 23)
        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")

counter = 0

def solve_start(sudoku):
    print("\nSudoku to solve:")
    grid_print(sudoku)
    solve_sudoku(sudoku)
    print("\nSudoku solved:")
    grid_print(sudoku)

    if solve_sudoku(sudoku):
        print(f"Solved after {counter} attempts")
    else:
        print("Could not find a solution")

# solve_start(sudoku_solve)

solve_start(sudoku_evil2)
