from Utils.constants import Action, NAV_ACTIONS


class SingleAgentState:

    def heuristic_Astar(self, action):
        # Getting th robots current position
        x1 = self.robot.position_x
        y1 = self.robot.position_y
        # Getting the Goals coordinates
        x2 = self.robot.goal_x
        y2 = self.robot.goal_y
        dist = (abs(x1 - x2) + abs(y1-y2))
        #print(action)
        if action in  [Action.turn_north, Action.turn_south, Action.turn_east, Action.turn_west]:
            #print("THE ROBOT IS TURNING")
            dist+= 3  # Adding a value of 3 to the distance for each turn.
        return (dist) #Modified Manhattan distance heuristic

    def __init__(self, p, robot, g, action):
        self.robot = robot
        self.p = p
        self.g = g
        self.h = self.heuristic_Astar(action) # TODO: Your job - Set a better heuristic value
        self.action = action
        #print(self.robot.heading)
        # if self.action in [Action.turn_north, Action.turn_south, Action.turn_east, Action.turn_west]:
        #     print("this is big")
        #print(g)
        #print(p)
        #print(robot.position_x)
        #print(robot.goal_x)

    def expand(self):
        successors = []
        for action in Action:
            if action.value not in NAV_ACTIONS:
                continue  # Lift, drop, and process are not part of the path planning
            child_robot = self.robot.copy()
            child_robot.plan = [action, action]
            try:
                occupies = child_robot.step()
            except ValueError:
                continue  # Ignore illegal actions
            if child_robot.warehouse.are_open_cells(occupies[0], self.robot.carry):
                successors.append(SingleAgentState(self, child_robot, self.g + 1, action))
        return successors

    def get_plan(self, plan):
        if self.p is not None:
            plan.append(self.action)
            self.p.get_plan(plan)
            #print(plan)
        return

    def is_goal(self):
        return self.robot.at_goal()

    def __eq__(self, other):
        return self.robot == other.robot

    def __hash__(self):
        return hash(self.robot)

    def __lt__(self, other):
         return self.g + self.h < other.g + other.h

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return self.g + self.h <= other.g + other.h

    def __str__(self):
        return "%d,%d" %(self.robot.position_x, self.robot.position_y)
