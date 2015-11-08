from warehouse import *

if __name__ == '__main__':
    s = make_init_state([['prod1', (0,0)], ['prod2', (0,10)], ['prod3', (0, 20)]], 
                        [['pack1', (20,0)], ['pack2', (20,10)], ['pack3', (20,20)]],
                        7,
                        [['prod1', 'pack1']],
                        [['r1', 'on_delivery', (0,0), 14]])

    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    se.search(s, warehouse_goal_fn, heur_min_completion_time)
    se.set_strategy('breadth_first')
    se.search(s, warehouse_goal_fn)
