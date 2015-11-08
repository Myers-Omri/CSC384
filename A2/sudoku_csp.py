# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the warehouse domain.

# Omri Myers: 1001902177

'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools


def create_var(csp_obj, board, N=9):  # TESTED
    csp_soduko_vars = []
    for r, row in enumerate(board):
        new_row = []
        for c, val in enumerate(row):
            name = "v{}{}".format(r, c)
            if val == 0:
                newVar = Variable(name, range(1, N + 1))
            else:
                newVar = Variable(name, [val])
                newVar.assign(val)
            new_row.append(newVar)
            csp_obj.add_var(newVar)
        csp_soduko_vars.append(new_row)
    return csp_soduko_vars


def create_sat_tuples(var1, var2):
    satisfying_tuples = []
    for v1 in var1.dom:
        for v2 in var2.dom:
            if v1 != v2:
                t = (v1, v2)
                satisfying_tuples.append(t)
    return tuple(satisfying_tuples)


def create_rols_constrains(csp_obj, vars_arr, trace=False, N=9):
    csp_rows_constrains = []
    csp_cols_constrains = []
    for r in range(0, N):
        for i in range(0, N):
            for j in range(i + 1, N):
                new_scope = [(vars_arr[r][i]), (vars_arr[r][j])]
                new_name = "cr{}_{}{}".format(r, i, j)
                new_const = Constraint(new_name, new_scope)
                sat_tupless = create_sat_tuples((vars_arr[r][i]), (vars_arr[r][j]))
                new_const.add_satisfying_tuples(sat_tupless)
                csp_rows_constrains.append(new_const)
                csp_obj.add_constraint(new_const)
                new_scopec = [(vars_arr[i][r]), (vars_arr[j][r])]
                new_namec = "cc{}_{}{}".format(r, i, j)
                new_constc = Constraint(new_namec, new_scopec)
                sat_tuplessc = create_sat_tuples((vars_arr[i][r]), (vars_arr[j][r]))
                new_constc.add_satisfying_tuples(sat_tuplessc)
                csp_cols_constrains.append(new_constc)
                csp_obj.add_constraint(new_constc)

    return csp_rows_constrains, csp_cols_constrains


# def create_cols_constrains(csp_obj, vars_arr, N=9, trace=False):
#     csp_cols_constrains = []
#     for c in range(0, N):
#         for i in range(0, N):
#             for j in range(i + 1, N):
#                 new_scopec = [(vars_arr[i][c]), (vars_arr[j][c])]
#                 new_namec = "cc{}_{}{}".format(c, i, j)
#                 new_constc = Constraint(new_namec, new_scopec)
#                 sat_tuplessc = create_sat_tuples((vars_arr[i][c]), (vars_arr[j][c]))
#                 new_constc.add_satisfying_tuples(sat_tuplessc)
#                 csp_cols_constrains.append(new_constc)
#                 csp_obj.add_constraint(new_constc)
#
#     return csp_cols_constrains


def create_subsquares_constrains(csp_obj, vars_arr, trace=False, N=9):
    csp_subsuares_constrains = []
    for rs in range(0, 9, 3):
        for cs in range(0, 9, 3):
            for k in range(rs, rs + 3):
                for h in range(cs, cs + 3):
                    for i in range(rs, rs + 3):
                        for j in range(cs, cs + 3):
                            if k > i and h != j:
                                new_scope = [(vars_arr[k][h]), (vars_arr[i][j])]
                                new_name = "cs{}x{}_{}{}_{}{}".format(rs, cs, k, h, i, j)
                                new_const = Constraint(new_name, new_scope)
                                sat_tupless = create_sat_tuples((vars_arr[k][h]), (vars_arr[i][j]))
                                new_const.add_satisfying_tuples(sat_tupless)
                                csp_subsuares_constrains.append(new_const)
                                csp_obj.add_constraint(new_const)
                                if trace:
                                    print("var {}: \n scop:".format(new_name))
                                    print(new_scope)
                                    print("list of tuple_is_valid: ")
                                    print(sat_tupless)
    return csp_subsuares_constrains


def sudoku_csp_model_1(initial_sudoku_board):
    new_sudoku_csp = CSP('sud_mod1')
    var_array = create_var(new_sudoku_csp, initial_sudoku_board)
    tcr, tcc = create_rols_constrains(new_sudoku_csp, var_array)
    tcs = create_subsquares_constrains(new_sudoku_csp, var_array)
    return new_sudoku_csp, var_array


# board = [[0, 0, 8, 7, 0, 0, 0, 5, 0],
#          [0, 3, 0, 0, 1, 0, 0, 9, 0],
#          [0, 0, 0, 5, 0, 0, 1, 0, 0],
#          [4, 0, 3, 0, 0, 7, 0, 0, 0],
#          [9, 7, 0, 0, 0, 0, 0, 1, 8],
#          [0, 0, 0, 8, 0, 0, 3, 0, 9],
#          [0, 0, 6, 0, 0, 4, 0, 0, 0],
#          [0, 9, 0, 0, 8, 0, 0, 2, 0],
#          [0, 5, 0, 0, 0, 1, 8, 0, 0]]
#
#
# def test_row_cons():
#     new_sudoku_csp = CSP('sud_mod1')
#     var_array = create_var(new_sudoku_csp, board)
#     # tcr = create_cols_constrains(new_sudoku_csp, var_array, 9, True)
#     tcs = create_subsquares_constrains(new_sudoku_csp, var_array, True, 9)
#

# test_row_cons()



# '''Return a CSP object representing a sudoku CSP problem along
#    with an array of variables for the problem. That is return
#
#    sudoku_csp, variable_array
#
#    where sudoku_csp is a csp representing sudoku using model_1
#    and variable_array is a list of lists
#
#    [ [  ]
#      [  ]
#      .
#      .
#      .
#      [  ] ]
#
#    such that variable_array[i][j] is the Variable (object) that
#    you built to represent the value to be placed in cell i,j of
#    the sudokup board (indexed from (0,0) to (8,8))
#
#
#
#    The input board is specified as a list of 9 lists. Each of the
#    9 lists represents a row of the board. If a 0 is in the list it
#    represents an empty cell. Otherwise if a number between 1--9 is
#    in the list then this represents a pre-set board
#    position. E.g., the board
#
#    -------------------
#    | | |2| |9| | |6| |
#    | |4| | | |1| | |8|
#    | |7| |4|2| | | |3|
#    |5| | | | | |3| | |
#    | | |1| |6| |5| | |
#    | | |3| | | | | |6|
#    |1| | | |5|7| |4| |
#    |6| | |9| | | |2| |
#    | |2| | |8| |1| | |
#    -------------------
#    would be represented by the list of lists
#
#    [[0,0,2,0,9,0,0,6,0],
#    [0,4,0,0,0,1,0,0,8],
#    [0,7,0,4,2,0,0,0,3],
#    [5,0,0,0,0,0,3,0,0],
#    [0,0,1,0,6,0,5,0,0],
#    [0,0,3,0,0,0,0,0,6],
#    [1,0,0,0,5,7,0,4,0],
#    [6,0,0,9,0,0,0,2,0],
#    [0,2,0,0,8,0,1,0,0]]
#
#
#    This routine returns Model_1 which consists of a variable for
#    each cell of the board, with domain equal to {1-9} if the board
#    has a 0 at that position, and domain equal {i} if the board has
#    a fixed number i at that cell.
#
#    Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
#    all relevant variables (e.g., all pairs of variables in the
#    same row, etc.), then invoke enforce_gac on those
#    constraints. All of the constraints of Model_1 MUST BE binary
#    constraints (i.e., constraints whose scope includes two and
#    only two variables).
# '''
#
# IMPLEMENT
##############################


def get9permutes():
    return list(itertools.permutations(range(1, 10)))


def is_legale(p, varscope):
    i = 0
    for v in varscope:
        if v.domain_size() == 1:
            if v.domain()[0] != p[i]:
                return False
        i += 1
    return True


def create_9_sat_tuples(var_scope, all_9_permuts):
    valid_tup = []
    for p in all_9_permuts:
        if is_legale(p, var_scope):
            valid_tup.append(p)

    return tuple(valid_tup)


# try, was slower
# def create_f_9_tuples(var_scope):
#     valid_tup = []
#     ttup = []
#     domLeft = []
#     for i, v in enumerate(var_scope):
#         if v.domain_size == 1:
#             ttup.append(v.get_assigned_value())
#         else:
#             ttup.append(0)
#             domLeft.append(v.get_assigned_value())
#
#     get_part_permutes = get9permutes(domLeft)
#
#     for p in get_part_permutes:
#         legal_per = []
#         l = 0
#         for j, val in enumerate(ttup):
#             if val==0:
#                 legal_per.append(p[l])
#                 l+=1
#             else:
#                 legal_per.append(val)
#         valid_tup.append(legal_per)
#     return tuple(valid_tup)



# def create_rows_constrains2(csp_obj, vars_arr, all_9_permuts, N=9):
#     csp_rows_constrains = []
#     for r in range(0, N):
#         new_scope = vars_arr[r]
#         new_name = "cr{}".format(r)
#         new_const = Constraint(new_name, new_scope)
#         sat_tuples = create_9_sat_tuples(new_scope, all_9_permuts)
#         new_const.add_satisfying_tuples(sat_tuples)
#         csp_rows_constrains.append(new_const)
#         csp_obj.add_constraint(new_const)
#     print("rows")
#     return csp_rows_constrains


def get_col_scope(col, varsArr):
    tscope = []
    for r in range(0, 9):
        tscope.append(varsArr[r][col])
    return tscope


def create_rols_constrains2(csp_obj, vars_arr, all_9_permuts, N=9):
    csp_cols_constrains = []
    csp_rows_constrains = []
    for c in range(0, N):
        r = c
        new_scope = get_col_scope(c, vars_arr)

        new_name = "cl{}".format(c)
        new_const = Constraint(new_name, new_scope)
        sat_tuples = create_9_sat_tuples(new_scope, all_9_permuts)
        new_const.add_satisfying_tuples(sat_tuples)
        csp_cols_constrains.append(new_const)
        csp_obj.add_constraint(new_const)

        new_scope = vars_arr[r]
        new_name = "cr{}".format(r)
        new_const = Constraint(new_name, new_scope)
        sat_tuples = create_9_sat_tuples(new_scope, all_9_permuts)
        new_const.add_satisfying_tuples(sat_tuples)
        csp_rows_constrains.append(new_const)
        csp_obj.add_constraint(new_const)
    return csp_rows_constrains, csp_cols_constrains


def create_subsquares_constrains2(csp_obj, vars_arr, all_9_permuts, N=9):
    csp_subsqares_constrains = []

    for rs in range(0, 9, 3):
        for cs in range(0, 9, 3):
            new_scope = []
            for i in range(rs, rs + 3):
                for j in range(cs, cs + 3):
                    new_scope.append(vars_arr[i][j])

            new_name = "cs{}{}".format(rs, cs)
            new_const = Constraint(new_name, new_scope)
            sat_tuples = create_9_sat_tuples(new_scope, all_9_permuts)
            new_const.add_satisfying_tuples(sat_tuples)
            csp_subsqares_constrains.append(new_const)
            csp_obj.add_constraint(new_const)
    return csp_subsqares_constrains


def sudoku_csp_model_2(initial_sudoku_board):
    new_sudoku_csp = CSP('sud_mod2')
    var_array = create_var(new_sudoku_csp, initial_sudoku_board)
    all_9_permuts = get9permutes()
    tcr, tcc = create_rols_constrains2(new_sudoku_csp, var_array, all_9_permuts)
    tcs = create_subsquares_constrains2(new_sudoku_csp, var_array, all_9_permuts)
    return new_sudoku_csp, var_array


'''Return a CSP object representing a sudoku CSP problem along
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''


# IMPLEMENT
