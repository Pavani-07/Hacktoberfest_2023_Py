import queue
import time
import psutil


# To check condition that Missionaries>=Cannibals
# m1->missionaries on left side of lake
# c1->cannibals on left side of lake
# b-> if b==1 then boat is on left side else on the right side
# m2->missionaries on right side of lake
# c2->cannibals on right side of lake
def valid_state(state):
  m1, c1, b, m2, c2 = state
  return (0 <= m1 <= 3) and (0 <= c1 <= 3) and (0 <= m2 <= 3) and (0 <= c2 <= 3) and ((m1 == 0 or m1 >= c1) and (m2 == 0 or m2 >= c2))


# Generating next states
def generate_states(state):
  cost = 0                                                                  # step cost assumed to be 1 everytime a person moves from one side to other
  m1, c1, b, m2, c2 = state
  new_states = []                                                           # empty list to add valid succesive cases
  moves = [(1, 0),(2, 0),(0, 1),(0, 2),(1, 1)]                              # (1M), (2M), (1C), (2C), (1M,1C) on the boat
  for move in moves:
    if b == 1:                                                              # When the boat is on the left side, move it to right in next state
      new_state = (m1 - move[0], c1 - move[1], 0, m2 + move[0], c2 + move[1])
      cost = cost + move[0] + move[1]
    else:                                                                   # When the boat is on the right side, move it to left in next state
      new_state = (m1 + move[0], c1 + move[1], 1, m2 - move[0], c2 - move[1])
      cost = cost + move[0] + move[1]
    if valid_state(new_state):
      new_states.append((new_state, cost))
  return new_states


# BFS implementation
def bfs(initial_state,goal_state):
  que = queue.Queue()
  cost = 0
  path = [initial_state]
  que.put((initial_state, path, cost))
  while not que.empty():
    current_state, path, cost = que.get()
    if current_state == goal_state:
      return path,cost
    for next_state,step_cost in generate_states(current_state):
      if next_state not in path:
        path = path + [next_state]
        cost = step_cost + cost
        que.put((next_state, path, cost))
  return None,cost


goal_state = (0, 0, 0, 3, 3)
start_state = (3, 3, 1, 0, 0)

start_time = time.time()                                  # start time
solution,cost = bfs(start_state, goal_state)
end_time = time.time()                                    # end time

if solution:
  print("Step cost of solution: ",cost)
  print("CPU time taken (seconds):", end_time - start_time)  # CPU time taken

  memory_info = psutil.Process().memory_info()               # Memory used
  memory_used = memory_info.rss
  print("Memory used:", memory_used, "bytes")

  print("Steps in the solution:")
  for step in solution:
    m1, c1, b, m2, c2 = step
    print(f"{m1} missionaries and {c1} cannibals on the left side \t {'boat on left' if b==1 else 'boat on right'} \t\t {m2} missionaries and {c2} cannibals on the right side")
    print("----------------------------------------------------------------------------------------------------------------------------------")
else:
  print("No solution")
