from heapq import heappush, heappop
from Planning.ClosedList import ClosedList

class BestFirstSearch:

    @staticmethod
    def plan(start_state):
        open = []
        closed = ClosedList()
        heappush(open, start_state)
        closed.insert(start_state)
        node_counter = 0
        while open:
            u = heappop(open)
            if u.is_goal():
                ans = []
                u.get_plan(ans)
                print(node_counter)
                node_counter = 0
                # return plan
                return ans
            else:
                successors = u.expand()
                node_counter += 1
                for v in successors:
                    #  if v is in closed
                    if v in closed:
                        # if v.f >= closed(v).f
                        if v >= closed.get(v):
                            # continue
                            continue
                        else:
                            closed.remove(v)
                    # insert v to open and closed
                    heappush(open, v)
                    closed.insert(v)
        raise ValueError('No valid path exist from %s' % start_state)
