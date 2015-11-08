from sudoku_csp import *
from propagators import *
import test_sudoku_solution

b1 = [[0,0,2,0,9,0,0,6,0],
     [0,4,0,0,0,1,0,0,8],
     [0,7,0,4,2,0,0,0,3],
     [5,0,0,0,0,0,3,0,0],
     [0,0,1,0,6,0,5,0,0],
     [0,0,3,0,0,0,0,0,6],
     [1,0,0,0,5,7,0,4,0],
     [6,0,0,9,0,0,0,2,0],
     [0,2,0,0,8,0,1,0,0]]


b2 = [[1,0,6,0,8,0,3,0,0],
      [0,9,7,4,0,1,0,0,0],
      [0,5,0,3,0,0,7,0,0],
      [4,0,0,0,0,7,0,6,0],
      [2,0,0,0,0,0,0,0,8],
      [0,7,0,5,0,0,0,0,9],
      [0,0,3,0,0,9,0,1,0],
      [0,0,0,2,0,3,8,5,0],
      [0,0,8,0,6,0,9,0,4]]


b3 = [[0,7,0,8,5,0,0,0,0],
      [0,9,0,0,0,1,5,0,6],
      [0,0,0,3,0,0,4,0,0],
      [0,3,0,0,0,0,0,0,8],
      [1,0,5,0,0,0,7,0,3],
      [7,0,0,0,0,0,0,2,0],
      [0,0,1,0,0,6,0,0,0],
      [2,0,3,7,0,0,0,6,0],
      [0,0,0,0,3,2,0,1,0]]


b4 = [[0, 0, 0, 0, 0, 6, 0, 0, 0],
      [0, 0, 0, 4, 0, 0, 2, 0, 8],
      [6, 3, 7, 0, 0, 8, 0, 0, 0],
      [2, 4, 0, 0, 0, 0, 0, 9, 0],
      [0, 0, 0, 9, 1, 7, 0, 0, 0],
      [0, 7, 0, 0, 0, 0, 0, 1, 3],
      [0, 0, 0, 3, 0, 0, 6, 8, 1],
      [1, 0, 4, 0, 0, 9, 0, 0, 0],
      [0, 0, 0, 8, 0, 0, 0, 0, 0]]

b5 = [[0, 6, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 7, 0, 0, 0, 0, 0, 4],
      [0, 9, 3, 0, 7, 0, 0, 0, 2],
      [0, 0, 1, 6, 0, 0, 0, 0, 5],
      [0, 0, 0, 8, 4, 2, 0, 0, 0],
      [3, 0, 0, 0, 0, 7, 8, 0, 0],
      [6, 0, 0, 0, 9, 0, 3, 1, 0],
      [7, 0, 0, 0, 0, 0, 5, 0, 0],
      [0, 0, 0, 0, 0, 5, 0, 9, 0]]

b6 = [[7, 0, 0, 1, 6, 0, 0, 0, 0],
      [3, 0, 0, 9, 0, 0, 0, 6, 0],
      [0, 0, 0, 8, 0, 0, 9, 2, 0],
      [0, 0, 6, 0, 1, 0, 0, 5, 0],
      [9, 0, 0, 0, 0, 0, 0, 0, 6],
      [0, 2, 0, 0, 3, 0, 7, 0, 0],
      [0, 1, 3, 0, 0, 2, 0, 0, 0],
      [0, 6, 0, 0, 0, 4, 0, 0, 8],
      [0, 0, 0, 0, 9, 1, 0, 0, 5]]

b7 = [[0, 9, 4, 3, 0, 0, 0, 0, 0],
      [0, 0, 7, 5, 0, 0, 0, 0, 0],
      [0, 0, 1, 4, 0, 0, 0, 2, 0],
      [4, 6, 0, 8, 0, 0, 0, 0, 3],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [2, 0, 0, 0, 0, 3, 0, 6, 9],
      [0, 5, 0, 0, 0, 6, 2, 0, 0],
      [0, 0, 0, 0, 0, 5, 1, 0, 0],
      [0, 0, 0, 0, 0, 1, 6, 4, 0]]

g1_test_board_0=[[2, 0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 7, 5, 0, 3, 0], [0, 4, 8, 0, 9, 0, 1, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0], [3, 0, 0, 0, 1, 0, 0, 0, 9], [0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 1, 0, 2, 0, 5, 7, 0], [0, 8, 0, 7, 3, 0, 0, 0, 0], [0, 9, 0, 0, 0, 0, 0, 0, 4]]


def print_sudo_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":
    flag = True
    listofboards = []
    #for i,b in enumerate([b1, b2, b3, b4, b5, b6, b7]):
    for i,b in enumerate([b1]):
        print("Solving board: {}".format(i))
        # for row in b:
        #     print(row)
        print("Using Model 1")
        csp, var_array = sudoku_csp_model_1(b)
        solver = BT(csp)
        #solver.trace = True
        print("=======================================================")
        print("GAC")

        solver.bt_search(prop_GAC)
        if test_sudoku_solution.check_solution(var_array):
            print("Solution:{} is ok".format(i))
        else:
            print("Solution:{} failed".format(i))
        #print_sudo_soln(var_array)

        print("Using Model 2")
        csp, var_array = sudoku_csp_model_2(b)
        print("finish creating csp")
        solver = BT(csp)
        print("=======================================================")
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_sudo_soln(var_array)
        print("=======================================================")
        if test_sudoku_solution.check_solution(var_array):
            print("Solution:{} is ok".format(i))
        else:
            flag=False
            listofboards.append(i)
            print("Solution:{} failed".format(i))

    if not flag:
        print ("fail at:")
        print(listofboards)
    else:
        print("OooooooooooooKKKK")