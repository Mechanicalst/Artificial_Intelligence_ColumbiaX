
import Queue


class ConstraintSatProblem(object):
    

    def __init__(self, csp_type=None, generator=None):

        self.csp_type = csp_type
        self.variables = generator["variables"]()
        self.domains = generator["domains"](self.variables)
        self.constraints = generator["constraints"](self.variables)
        self.assignments = {}
        self.unassigned = {var: True for var in self.variables}

    def backtrack_solve(self):

        return self.backtrack(self.deep_copy_flat_dict(self.assignments),
                              self.deep_copy_flat_dict(self.unassigned),
                              self.deep_copy_domains(self.domains))

    def backtrack(self, assignments, unassigned, domains):

        if self.check_solved(assignments):
            return assignments

        var = self.select_var_to_assign(unassigned, domains, "mrv")

        possible_values = self.deep_copy_flat_dict(domains[var])
        for val in possible_values:

            if not self.is_allowed(var, val, assignments):
                continue

            assignments[var] = val
            del unassigned[var]
            domains_before_assignment = self.deep_copy_domains(domains)
            domains[var] = {val: True}

            inferences = self.inference_arc_3(domains)
            if inferences[0]:
                for inference_var in inferences[1]:
                    for key in domains[inference_var]:
                        assignments[inference_var] = key
                        del unassigned[inference_var]

                result = self.backtrack(self.deep_copy_flat_dict(assignments),
                                        self.deep_copy_flat_dict(unassigned),
                                        self.deep_copy_domains(domains))

                if result != -1:
                    return result

            domains = domains_before_assignment
            domains[var] = {val: True}
            del assignments[var]
            unassigned[var] = True
            domains = domains_before_assignment
            if inferences[0]:
                for inference_var in inferences[1]:
                    del assignments[inference_var]
                    unassigned[inference_var] = True

        return -1

    def is_allowed(self, var, val, assignments):

        for var_two in self.constraints[var]["arcs"]:
            if var_two in assignments and assignments[var_two] == val:
                return False
        return True

    def deep_copy_flat_dict(self, dict):

        copy = {}
        for key in dict.keys():
            val = dict[key]
            copy[key] = val
        return copy

    def deep_copy_domains(self, domains):

        copy = {}

        for var in domains.keys():
            copy[var] = {}
            for val in domains[var].keys():
                copy[var][val] = True
        return copy

    def select_var_to_assign(self, unassigned, domains, strategy="mrv"):

        if strategy == "mrv":
            min = 0
            min_var = None
            for var in unassigned:

                if not min_var:
                    min = len(domains[var])
                    min_var = var
                vals = len(domains[var])
                if vals < min:
                    min = vals
                    min_var = var
            return min_var

    def inference_arc_3(self, domains):

        q = Queue.Queue()
        for var in self.constraints:
            for arc in self.constraints[var]["arcs"]:
                q.put((var,arc))

        inference_assignments = []
        while not q.empty():
            (x_left, x_right) = q.get()
            revised = self.revise_arc(x_left, x_right, domains)
            if revised:

                if len(domains[x_left]) < 1:
                    return False, inference_assignments

                if len(domains[x_left]) == 1:
                    inference_assignments.append(x_left)

                for x_other in self.constraints[x_left]["arcs"]:
                    if x_other == x_right:
                        continue
                    q.put((x_other, x_left))

        return True, inference_assignments

    def revise_arc(self, x_left, x_right, domains):

        revised = False

        val_deletion_list = []

        for val_x_left in domains[x_left]:
            can_satisfy = False

            for val_x_right in domains[x_right]:
                if val_x_right != val_x_left:
                    can_satisfy = True
                    break
            if not can_satisfy:
                val_deletion_list.append(val_x_left)
                revised = True
        for val in val_deletion_list:
            del domains[x_left][val]

        return revised

    def check_solved(self, assignments):

        if len(assignments) == len(self.variables):
            return True
        return False
