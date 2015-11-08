# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the warehouse domain.

'''
warehouse STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
from copy import deepcopy
from sys import maxsize

##################################################
# The search space class 'warehouse'             #
# This class is a sub-class of 'StateSpace'      #
##################################################

# defines for robot status
_R_NAME = 0
_R_STATUS = 1
_R_LOC = 2
_R_FINISH = 3

# defines for prodact/ pack_station
_P_NAME = 0
_P_LOC = 1

# define for order status
_ORD_PNAME = 0
_ORD_STATION = 1


class warehouse(StateSpace):  # TODO: Done
    _product_list = []
    _packing_station_list = []

    def __init__(self, action, gval,
                 current_time,
                 open_orders,
                 robot_status,
                 parent=None):
        """Initialize a warehouse search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.current_time = current_time
        self.open_orders = open_orders
        self.robot_status = robot_status

# Auxiliary functions updating the status of the robot.
    def get_prod_loc_by_name(self, p_name):
        for p in self._product_list:
            if p[0] == p_name:
                return p[1]

    def get_pack_loc_by_name(self, ps_name):
        for p in self._packing_station_list:
            if p[0] == ps_name:
                return p[1]

    def update_r(self, ru, otd):
            prod_location = self.get_prod_loc_by_name(otd[_ORD_PNAME])
            pack_location = self.get_pack_loc_by_name(otd[_ORD_STATION])
            ru_loc = ru[_R_LOC]
            dist1 = abs(ru_loc[0] - prod_location[0]) + abs(ru_loc[1] - prod_location[1])
            dist2 = abs(pack_location[0] - prod_location[0]) + abs(pack_location[1] - prod_location[1])
            total_dist = dist1 + dist2
            return self.gval + total_dist

    def successors(self):
        '''Return list of warehouse objects that are the successors of the current object'''
        succ_list = []
        t_robots_list = deepcopy(self.robot_status)
        min_time2deliver = maxsize
        for r in t_robots_list:
            if r[_R_STATUS] == 'idle':

                for order in self.open_orders:
                    tmp_r = deepcopy(r)
                    tmp_o = deepcopy(order)
                    r[_R_STATUS] = 'on_delivery'
                    r.append(self.update_r(tmp_r, tmp_o))
                    new_loc = self.get_pack_loc_by_name(tmp_o[_ORD_STATION])
                    r[_R_LOC] = new_loc
                    new_robot_stat = deepcopy(t_robots_list)
                    r[_R_NAME] = tmp_r[_R_NAME]
                    r[_R_STATUS] = tmp_r[_R_STATUS]
                    r[_R_LOC] = tmp_r[_R_LOC]
                    r.pop(_R_FINISH)
                    tmp_ord_list = deepcopy(self.open_orders)
                    tmp_ord_list.remove(order)
                    new_warehouse_a = warehouse('deliver({},{},{})'.format(r[_R_NAME], order[_ORD_PNAME],
                                                                           order[_ORD_STATION]), self.gval,
                                                self.current_time,
                                                tmp_ord_list, new_robot_stat, self)
                    succ_list.append(new_warehouse_a)
            else:
                if r[_R_FINISH] >= self.current_time and min_time2deliver > r[_R_FINISH]:
                    min_time2deliver = r[_R_FINISH]
        min_time_flag = False
        for r in t_robots_list:
            if r[_R_STATUS] == 'on_delivery' and r[_R_FINISH] == min_time2deliver:
                r[_R_STATUS] = 'idle'
                r.pop(_R_FINISH)
                min_time_flag = True
        if min_time_flag:
            new_gval = self.gval + (min_time2deliver - self.current_time)
            new_warehouse_b = warehouse('move_forward(' + str(min_time2deliver) + ')', new_gval, min_time2deliver,
                                        self.open_orders,
                                        t_robots_list, self)
            succ_list.append(new_warehouse_b)
        return succ_list    # ---------end of successor function---------------- #

    def hashable_state(self):
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        robot_list = deepcopy(self.robot_status)
        robot_list.sort(key=lambda robot: robot[0])
        orders = deepcopy(self.open_orders)
        orders.sort(key=lambda order: (order[0], order[1]))
        hashlist = [self.gval]
        for o in orders:
            for oi in o:
                hashlist.append(oi)
        for r in robot_list:
            for ri in r:
                hashlist.append(ri)
        t = tuple(hashlist)
        return t

    def print_state(self):
        # DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        # and in generating sample trace output.
        # Note that if you implement the "get" routines below properly,
        # This function should work irrespective of how you represent
        # your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval,
                                                                         self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Time = {}".format(self.get_time()))
        print("Unfulfilled Orders")
        for o in self.get_orders():
            print("    {} ==> {}".format(o[0], o[1]))
        print("Robot Status")
        for rs in self.get_robot_status():
            print("    {} is {}".format(rs[0], rs[1]), end="")
            if rs[1] == 'idle':
                print(" at location {}".format(rs[2]))
            elif rs[1] == 'on_delivery':
                print(" will be at location {} at time {}".format(rs[2], rs[3]))


                # Data accessor routines.
                # '''Return list containing status of each robot
                #            This list has to be in the format: [rs_1, rs_2, ..., rs_k]
                #            with one status list for each robot in the state.
                #         Each robot status item rs_i is itself a list in the format [<name>, <status>, <loc>, <ftime>]
                #            Where <name> is the name of the robot (a string)
                #                  <status> is either the string "idle" or the string "on_delivery"
                #                  <loc> is a location (a pair (x,y))
                #                        if <status> == "idle" then loc is the robot's current location
                #                        if <status> == "on_delivery" then loc is the robot's future location
                #                 <ftime>
                #                        if <status> == "idle" this item is missing (i.e., the list is of
                #                                       length 3)
                #                        if <status> == "on_delivery" then this is a number that is the
                #                                       time that the robot will complete its current delivery
                # '''

    def get_robot_status(self):
        return self.robot_status

    # Return the current time of this state (a number)

    def get_time(self):
        return self.current_time

    # Return list of unfulfilled orders of this state
    #        This list is in the format [o1, o2, ..., om]
    #        one item for each unfulfilled order.
    #        Each oi is itself a list [<product_name>, <packing_station_name>]
    #        where <product_name> is the name of the product to be delivered
    #        and  <packing_station_name> is the name of the packing station it is to be delivered to'''

    def get_orders(self):
        return self.open_orders


#############################################
# heuristics                                #
#############################################

# Zero Heuristic use to make A* search perform uniform cost search
def heur_zero(state):
    return 0


def heur_min_completion_time(state):
    '''warehouse heuristic'''
    # We want an admissible heuristic. Since the aim is to delivery all
    # of the products to their packing station in as short as a time as
    # possible.
    # NOTE that we want an estimate of the ADDED time beyond the current
    #     state time.
    # Consider all of the possible delays in moving from this state to
    # a final delivery of all orders.
    # 1. All robots have to finish any current delivery they are on.
    #    So the earliest we could finish is the 
    #    maximum over all robots on delivery of 
    #       (robot's finish time - the current state time)
    #    we subtract the current state time because we want time
    #    beyond the current time required to complete the delivery
    #    Let this maximum be TIME1.
    #    Clearly we cannot finish before TIME1
    max1 = 0
    for r in state.robot_status:
        if r[_R_STATUS] == "on_delivery":
            if r[_R_FINISH] - state.gval > max1:
                max1 = (r[_R_FINISH] - state.gval)

    # 2. For all unfulfilled orders we need to pick up the product of
    #    that order with some robot, and then move it to the right
    #    packing station. However, we could do many of these
    #    deliveries in parallel. So to get an *admissible* heuristic
    #    we take the MAXIMUM of a MINUMUM time any unfulfilled order
    #    can be completed. There are many different minimum times that
    #    could be computed...of varying complexity. For simplicity we
    #    ignore the time required to get a robot to package, and
    #    instead take the time to move the package from its location
    #    to the packing station location as being a suitable minimum.
    #    So we compute these minimums, then take the maximum of these
    #    minimums Call this max TIME2
    #    Clearly we cannot finish before TIME2
    max2 = 0
    for O in state.open_orders:
        prod_location = state.get_prod_loc_by_name(O[0])
        pack_location = state.get_pack_loc_by_name(O[1])
        dist = (abs(prod_location[0] - pack_location[0]))
        dist += (abs(prod_location[1] - pack_location[1]))
        if dist > max2:
            max2 = dist

    # Finally we return as a the heuristic value the MAXIMUM of ITEM1 and ITEM2

    if max1 > max2:
        return max1
    return max2


#   return True only if we reached the goal when all orders have been delivered

def warehouse_goal_fn(state):
    if state.open_orders:
        return False
    for r in state.robot_status:
        if r[_R_STATUS] == 'on_delivery' and r[_R_FINISH] >= state.gval:
            return False
    return True


def make_init_state(product_list, packing_station_list, current_time, open_orders, robot_status):

    warehouse._product_list = product_list
    warehouse._packing_station_list = packing_station_list

    temp_state = warehouse("START()", 0, current_time, open_orders, robot_status, None)

    '''Input the following items which specify a state and return a warehouse object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       product_list = [p1, p2, ..., pk]
          a list of products. Each product pi is itself a list
          pi = [product_name, (x,y)] where 
              product_name is the name of the product (a string) and (x,y) is the
              location of that product.
       packing_station = [ps1, ps2, ..., psn]
          a list of packing stations. Each packing station ps is itself a list
          pi = [packing_station_name, (x,y)] where 
              packing_station_name is the name of the packing station (a string) and (x,y) is the
              location of that station.
       current_time = an integer >= 0
          The state's current time.
       open_orders = [o1, o2, ..., om] 
          a list of unfulfilled (open) orders. Each order is itself a list
          oi = [product_name, packing_station_name] where
               product_name is the name of the product (a string) and
               packing_station_name is the name of the packing station (a string)
               The order is to move the product to the packing station
        robot_status = [rs1, rs2, ..., rsk]
          a list of robot and their status. Each item is itself a list  
          rsi = ['name', 'idle'|'on_delivery', (x, y), <finish_time>]   
            rsi[0] robot name---a string 
            rsi[1] robot status, either the string "idle" or the string
                  "on_delivery"
            rsi[2] robot's location--if "idle" this is the current robot's
                   location, if "on_delivery" this is the robots final future location
                   after it has completed the delivery
            rsi[3] the finish time of the delivery if the "on_delivery" 
                   this element of the list is absent if robot is "idle" 

    NOTE: for simplicity you may assume that
         (a) no name (robot, product, or packing station is repeated)
         (b) all orders contain known products and packing stations
         (c) all locations are integers (x,y) where both x and y are >= 0
         (d) the robot status items are correctly formatted
         (e) the future time for any robot on_delivery is >= to the current time
         (f) the current time is >= 0
    '''
    return temp_state


########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def make_rand_init_state(nprods, npacks, norders, nrobots):
    '''Generate a random initial state containing 
       nprods = number of products
       npacks = number of packing stations
       norders = number of unfulfilled orders
       nrobots = number of robots in domain'''

    prods = []
    for i in range(nprods):
        ii = int(i)
        prods.append(["product{}".format(ii), (randint(0, 50), randint(0, 50))])
    packs = []
    for i in range(npacks):
        ii = int(i)
        packs.append(["packing{}".format(ii), (randint(0, 50), randint(0, 50))])
    orders = []
    for i in range(norders):
        orders.append([prods[randint(0, nprods - 1)][0], packs[randint(0, npacks - 1)][0]])
    robotStatus = []
    for i in range(nrobots):
        ii = int(i)
        robotStatus.append(["robot{}".format(ii), "idle", (randint(0, 50), randint(0, 50))])
    return make_init_state(prods, packs, 0, orders, robotStatus)


