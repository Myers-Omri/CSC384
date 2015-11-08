# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the warehouse domain.

# Omri Myers: 1001902177

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
         
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


DWO = False
OK = True


def fcCheckOne(consToCheck, unAsVar):
    pruned = []
    for uval in unAsVar.cur_domain():
        sati = consToCheck.has_support(unAsVar, uval)
        if not sati:
            pruned.append(uval)

    for uv in pruned:
        unAsVar.prune_value(uv)
    if unAsVar.cur_domain == []:
        return DWO, pruned
    return OK, pruned


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    cons_list = []
    if not newVar:
        for i, cn in enumerate(csp.get_all_cons()):
            if cn.get_n_unasgn() == 1:
                cons_list.append(cn)
    else:
        for cc in csp.get_cons_with_var(newVar):
            if cc.get_n_unasgn() == 1:
                cons_list.append(cc)
    DWOoccured = False
    pruns = []
    for cons in cons_list:
        unass_vars = cons.get_unasgn_vars()
        res, tpruns = fcCheckOne(cons, unass_vars[0])  # FcCheck returns true if not DWO and false otherwise
        for tp in tpruns:
            pruns.append((unass_vars[0], tp))
        if res == DWO:
            DWOoccured = True
            break
    if DWOoccured == False:
        return OK, pruns
    return DWO, pruns


# IMPLEMENT



def GAC_Enforce(csp, GAC_queue):
    cons_queue = []
    for c in GAC_queue:
        cons_queue.append(c)

    pruns = []
    while cons_queue:
        c = cons_queue.pop(0)

        for v in (c.get_unasgn_vars()):

            for d in v.cur_domain():
                if not c.has_support(v, d):
                    if (v, d) not in pruns:
                        v.prune_value(d)
                        pruns.append((v, d))

                    if v.cur_domain_size() == 0:
                        cons_queue.clear()
                        return DWO, pruns
                    else:
                        tcons = csp.get_cons_with_var(v)
                        for tc in tcons:
                            if tc not in cons_queue:
                                cons_queue.append(tc)
    return OK, pruns


def prop_GAC(csp, newVar=None):  # checked V
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    if not newVar:
        res, tpruns = GAC_Enforce(csp, csp.get_all_cons())
    else:
        GAC_queue = csp.get_cons_with_var(newVar)
        res, tpruns = GAC_Enforce(csp, GAC_queue)
    return res, tpruns
