import sys

class Matrix:

    def __init__(self, a, unknowns):
        self.a = a
        self.unknowns = unknowns
        self.rowsize = len(a)
        self.colsize = len(a[0])
        self.swap_list = []
        self.result = ""

    def add_row(self, c, i, k):
        for j in range(self.colsize):
            self.a[k][j] += c * self.a[i][j]

    def swap_row(self, i, k):
        self.a[i], self.a[k] = self.a[k], self.a[i]

    def scaler_row(self, c, i):
        for j in range(self.colsize):
            self.a[i][j] *= c

    def add_col(self, c, j, k):
        for i in range(self.rowsize):
            self.a[i][k] += c * self.a[i][j]

    def swap_col(self, j, k):
        for i in range(self.rowsize):
            self.a[i][j], self.a[i][k] = self.a[i][k], self.a[i][j]

    def scaler_col(self, c, j):
        for i in range(self.rowsize):
            self.a[i][j] *= c

    def rank_row(self, colsize):
        rank = 0
        for i in range(self.rowsize):
            for j in range(colsize):
                if self.a[i][j] != 0:
                    rank += 1
                    break
        return rank

    def rank_col(self, colsize):
        rank = 0
        for j in range(colsize):
            for i in range(self.rowsize):
                if self.a[i][j] != 0:
                    rank += 1
                    break
        return rank

    def reduced_echelonize_row(self):
        for j in range(1, self.rowsize):
            for i in range(self.rowsize):
                if self.a[i][j] != 0:
                    zero_column_flag =False
                    break
            else:
                self.swap_col(j, 0)
                self.swap_list.append(j)

        if self.rank_row(self.rowsize) != self.rank_row(self.colsize):
            return "No solutions"

        for j in range(self.rowsize):
            for i in range(self.rowsize):
                if self.a[i][j] != 0:
                    break
            else:
                continue
            break

        nonzero_j =j 
        k = 0
        for j in range(nonzero_j, self.rowsize):
            pivot_row = -1
            for i in range(k, self.rowsize):
                if self.a[i][j] != 0:
                    if  pivot_row == -1:
                        pivot_row = i
                        pivot = self.a[i][j]
                        self.scaler_row(1 / pivot, i)
                        if i > k:
                            self.swap_row(i, k)
                    else:
                        c = self.a[i][j]
                        if c:
                            self.add_row(-c, k, i)
            k += 1
    
        k = 0
        for j in range(nonzero_j, self.rowsize):
            for i in range(k):
                c = self.a[i][j]
                if c:
                    self.add_row(-c, k, i) 
            k += 1

        if self.rank_row(self.unknowns) != self.rank_row(self.unknowns + 1):
            self.result = "No solutions"
        elif self.rank_col(self.colsize - 1 ) > self.rank_row(self.colsize - 1):
            self.result = "Infinitely many solutions"

    def get_solution(self):
        solution = [[row[-1]] for row in self.a[:self.unknowns]]
        return solution

def load_matrix(filename):
    with open(filename) as f:
        lines = f.readlines()
    input_list = [int(x) for x in lines[0].split()]
    unknowns, equations = input_list

    try:
        matrix = [[float(x) for x in line.split()] for line in lines[1:equations + 1]]
    except ValueError:
        matrix = [[complex(x) for x in line.split()] for line in lines[1:equations + 1]]

    return matrix, unknowns

def save_matrix(filename, matrix):
    text = ""
    for row in matrix:
        row_list = [str(elm) for elm in row]
        text += " ".join(row_list) + "\n"

    with open(filename, "w") as f:
        f.write(text)

def save_text(filename, text):
    with open(filename, "w") as f:
        f.write(text)

def get_args():
    infile_flag = False
    outfile_flag = False
    infile = None
    outfile = None
    for arg in sys.argv:
        if arg == "--infile":
            infile_flag = True
        elif arg == "--outfile":
            outfile_flag = True
        elif infile_flag:
            infile = arg
            infile_flag = False
        elif outfile_flag:
            outfile = arg
            outfile_flag = False
    return infile, outfile

def print_contents(filename):
    with open(filename) as f:
        text = f.read()
    print(text)

infile, outfile = get_args()
# infile = "in1i.txt"
# outfile = "out.txt"
print_contents(infile)
a, unknowns = load_matrix(infile)
m = Matrix(a, unknowns)
# m.swap_row(0, 1)
# m.swap_col(0, 1)
# m.scaler_row(2, 1)
# m.scaler_col(2, 1)
# m.add_row(2, 1, 2)
# m.add_col(2, 1, 2)
m.reduced_echelonize_row()
if m.result:
    save_text(outfile, m.result)
else:     
    save_matrix(outfile, m.get_solution())