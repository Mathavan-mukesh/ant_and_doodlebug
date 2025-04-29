import random
import time


size = 20
ant_breed = 3
bug_breed = 8
bug_death = 3

grid = [[None for _ in range(size)] for _ in range(size)]

def create_ant(x, y, moved=False, steps=0):
    return {"x": x, "y": y, "type": "ant", "moved": moved, "steps": steps}

def create_bug(x, y, moved=False, steps=0, step_eat=0):
    return {"x": x, "y": y, "type": "bugs", "moved": moved, "steps": steps, "step_eat": step_eat}

def start_world():
    ant_count = 0
    while ant_count < 100:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if grid[x][y] is None:
            grid[x][y] = create_ant(x, y)
            ant_count += 1

    bugs_count = 0
    while bugs_count < 5:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if grid[x][y] is None:
            grid[x][y] = create_bug(x, y)
            bugs_count += 1

def first_print():
    for i in grid:
        for j in i:
            if j is None:
                print(".", end="")
            elif j["type"] == "ant":
                print("0", end="")
            elif j["type"] == "bugs":
                print("X", end="")
        print()

def move_bug():
    for i in range(size):
        for j in range(size):
            if grid[i][j] is not None and grid[i][j]["type"] == "bugs" and not grid[i][j]["moved"]:
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(directions)
                for dx, dy in directions:
                    new_x, new_y = i + dx, j + dy
                    if 0 <= new_x < size and 0 <= new_y < size:
                        target = grid[new_x][new_y]
                        if target is not None and target["type"] == "ant":
                            grid[new_x][new_y] = create_bug(
                                new_x, new_y, moved=True,
                                steps=grid[i][j]["steps"] + 1,
                                step_eat=0
                            )
                            grid[i][j] = None
                            break
                        elif target is None:
                            grid[new_x][new_y] = create_bug(
                                new_x, new_y, moved=True,
                                steps=grid[i][j]["steps"] + 1,
                                step_eat=grid[i][j]["step_eat"] + 1
                            )
                            grid[i][j] = None
                            break

def move_ant():
    for i in range(size):
        for j in range(size):
            if grid[i][j] is not None and grid[i][j]["type"] == "ant" and not grid[i][j]["moved"]:
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(directions)
                for dx, dy in directions:
                    new_x, new_y = i + dx, j + dy
                    if 0 <= new_x < size and 0 <= new_y < size and grid[new_x][new_y] is None:
                        grid[new_x][new_y] = create_ant(
                            new_x, new_y, moved=True,
                            steps=grid[i][j]["steps"] + 1
                        )
                        grid[i][j] = None
                        break

def move_reset():
    for i in range(size):
        for j in range(size):
            if grid[i][j] is not None:
                grid[i][j]["moved"] = False

def breed_ant():
    for i in range(size):
        for j in range(size):
            if grid[i][j] is not None and grid[i][j]["type"] == "ant" and grid[i][j]["steps"] >= ant_breed:
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(directions)
                for dx, dy in directions:
                    new_x, new_y = i + dx, j + dy
                    if 0 <= new_x < size and 0 <= new_y < size and grid[new_x][new_y] is None:
                        grid[new_x][new_y] = create_ant(new_x, new_y)
                        grid[i][j]["steps"] = 0
                        break

def breed_bug():
    for i in range(size):
        for j in range(size):
            if grid[i][j] is not None and grid[i][j]["type"] == "bugs" and grid[i][j]["steps"] >= bug_breed:
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(directions)
                for dx, dy in directions:
                    new_x, new_y = i + dx, j + dy
                    if 0 <= new_x < size and 0 <= new_y < size and grid[new_x][new_y] is None:
                        grid[new_x][new_y] = create_bug(new_x, new_y)
                        grid[i][j]["steps"] = 0
                        break

def death_bug():
    for i in range(size):
        for j in range(size):
            if grid[i][j] is not None and grid[i][j]["type"] == "bugs":
                if grid[i][j]["step_eat"] >= bug_death:
                    grid[i][j] = None
def death_ant():
    for i in range(size):
        for j in range(size):
            if grid[i][j] is not None and grid[i][j]["type"] == "ant":
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                surrounded = True

                for dx, dy in directions:
                    new_x, new_y = i + dx, j + dy

                    if not (0 <= new_x < size and 0 <= new_y < size):
                        surrounded = False
                        break
                    if grid[new_x][new_y] is None or grid[new_x][new_y]["type"] != "ant":
                        surrounded = False
                        break

                if surrounded:
                    grid[i][j] = create_bug(i, j)  

def last_step():
    ant = 0
    bug = 0
    empty = 0
    for i in grid:
        for j in i:
            if j is None:
                print(".", end="")
                empty += 1
            elif j["type"] == "ant":
                print("0", end="")
                ant += 1
            elif j["type"] == "bugs":
                print("X", end="")
                bug += 1
        print()
    print(f"number of ant alive : {ant}, number of bug alive : {bug}, number of empty spaces {empty}")

def main():
    start_world()
    first_print()

    while True:
        move_ant()
        move_bug()
        move_reset()
        breed_ant()
        breed_bug()
        death_bug()
        death_ant()
        last_step()
        time.sleep(3)

main()
