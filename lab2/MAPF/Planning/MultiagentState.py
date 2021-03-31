from Utils.constants import Action, NAV_ACTIONS
import Utils.constants as C


class MultiagentState:
    def mapf_heuristic(self, actions):
        # Getting the robots current position
        x1_0 = self.robots[0].position_x
        y1_0 = self.robots[0].position_y
        # Getting the Goals coordinates
        x2_0 = self.robots[0].goal_x
        y2_0 = self.robots[0].goal_y
        dist_0 = (abs(x1_0 - x2_0) + abs(y1_0-y2_0))

        x1_1 = self.robots[1].position_x
        y1_1 = self.robots[1].position_y
        # Getting the Goals coordinates
        x2_1 = self.robots[1].goal_x
        y2_1 = self.robots[1].goal_y
        dist_1 = (abs(x1_1 - x2_1) + abs(y1_1-y2_1))

        dist = dist_0 + dist_1
        print("OG Dist: ")
        print(dist)
        if actions:
            for action in actions:
                if action in  [Action.turn_north, Action.turn_south, Action.turn_east, Action.turn_west]:

                    dist+= 3  # Adding a value of 3 to the distance for each turn.

        print("Updated distance")
        print(dist)
        return (dist) #Modified Manhattan distance heuristic

    def __init__(self, p, robots, g, actions):
        self.robots = robots
        self.p = p
        self.g = g
        self.h = self.mapf_heuristic(actions) # TODO: Your job. Set a better heuristic value
        self.actions = actions


    def expand_r(self, robot_index, successors, current_assignment, actions, g_child, occupied_cells, occupied_edges):
        if robot_index == len(self.robots):
            successors.append(MultiagentState(self, current_assignment, g_child, actions))
        else:
            r = self.robots[robot_index]
            for action in Action:
                if action.value not in NAV_ACTIONS:
                    continue  # Lift, drop, and process are not part of the path planning
                child_robot = self.robots[robot_index].copy()
                child_robot.plan = [action, action]
                try:
                    occupies = child_robot.step()
                except ValueError:
                    continue  # Ignore illegal actions
                if child_robot.warehouse.are_open_cells(occupies[0], child_robot.carry):
                    occupies = self.norm_occupation(occupies)
                    if self.is_valid_assignment(occupied_cells,occupied_edges, occupies):
                        g_next = g_child
                        new_assignment = current_assignment + [child_robot]
                        new_occupied_cells = occupied_cells + occupies[0]
                        new_occupied_edges = occupied_edges + occupies[1]
                        new_actions = actions + [action]
                        if not child_robot.at_goal():
                            g_next += 1
                        self.expand_r(robot_index + 1, successors, new_assignment, new_actions, g_next, new_occupied_cells, new_occupied_edges)

    def expand(self):
        successors = []
        self.expand_r(0, successors, [], [], self.g, [], [])
        return successors

    def is_valid_assignment(self, occupied_cells, occupied_edges, occupies):
        for c in occupies[0]:
            if c in occupied_cells:
                return False
        for e in occupies[1]:
            if e in occupied_edges:
                return False
        return True

    def norm_occupation(self,occupies):
        ans = [[],[]]
        height = self.robots[0].warehouse.map.height
        width = self.robots[0].warehouse.map.width
        for c in occupies[0]:
            ans[0].append(C.cell_to_index(c[0],c[1],width))
        for e in occupies[1]:
            ans[1].append(C.edge_to_index(e[0],e[1],e[2],width,height))
        return ans

    def get_plan(self, plans):
        for x in range(len(self.robots)):
            plans.append([])
        self.get_plan_r(plans)

    def get_plan_r(self, plans):
        if self.p is not None:
            for x in range(len(self.actions)):
                plans[x].append(self.actions[x])
            self.p.get_plan_r(plans)
        return

    def is_goal(self):
        for r in self.robots:
            if not r.at_goal():
                return False
        return True

    def __eq__(self, other):
        for x in range(len(self.robots)):
            if self.robots[x] != other.robots[x]:
                return False
        return True

    def __hash__(self):
        ans = 0
        for r in self.robots:
            ans += hash(r)
        return ans

    def __lt__(self, other):
         return self.g + self.h < other.g + other.h

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        ans = ''
        for r in self.robots:
            ans += "Robot[%d]-(%d,%d,%s,%d) " %(r.index,r.position_x, r.position_y, r.heading, r.velocity)
        return ans
