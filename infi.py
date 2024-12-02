import itertools

DIM = 30
DIRS = ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1))

class Program:
    def __init__(self):
        self.instructions = []
    def add(self, instr):
        self.instructions.append(instr)
    def run(self, env):
        while env.pc < len(self.instructions):
            self.instructions[env.pc].execute(env)
            env.pc += 1
        return env.value()

class Environment:
    def __init__(self, x, y, z):
        self.pc = 0
        self.block = {'X': x, 'Y': y, 'Z': z}
        self.stack = []
    def __getitem__(self, key):
        return self.block[key]
    def value(self):
        return self.stack[-1]

class Push:
    def __init__(self, val):
        if val[0] not in ('X', 'Y', 'Z'):
            self.val = int(val)
        else:
            self.val = val
    def execute(self, env):
        if isinstance(self.val, str):
            env.stack.append(env[self.val])
        else:
            env.stack.append(self.val)

class Add:
    def execute(self, env):
        env.stack.append(env.stack.pop() + env.stack.pop())

class Jmpos:
    def __init__(self, val):
        self.val = int(val)
    def execute(self, env):
        if env.stack.pop() >= 0:
            env.pc += self.val

class Ret:
    def execute(self, env):
        env.pc = 10**9

def load(fname):
    program = Program()
    lines = []
    with open(fname, 'r') as f:
        lines = f.readlines()
    for line in lines:
        tmp = line.split()
        match tmp:
            case ['push', val]:
                program.add(Push(val))
            case ['add']:
                program.add(Add())
            case ['jmpos', val]:
                program.add(Jmpos(val))
            case ['ret']:
                program.add(Ret())
    return program

def walk(x, y, z, grid, vis):
    vis[x][y][z] = True
    for dx, dy, dz in DIRS:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < DIM and 0 <= ny < DIM and 0 <= nz < DIM and grid[nx][ny][nz] == 1 and not vis[nx][ny][nz]:
            walk(nx, ny, nz, grid, vis)

def components(grid):
    res = 0
    vis = [[[False for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for x, y, z in itertools.product(range(DIM), repeat=3):
        if grid[x][y][z] == 1 and not vis[x][y][z]:
            walk(x, y, z, grid, vis)
            res += 1
    return res

if __name__ == '__main__':
    program = load('infi.txt')
    grid = [[[0 for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    total = 0
    for x, y, z in itertools.product(range(DIM), repeat=3):
        env = Environment(x, y, z)
        cnt = program.run(env)
        if cnt > 0:
            grid[x][y][z] = 1
        total += cnt
    print(f'Total sum: {total}')
    print(f'Number of components: {components(grid)}')
