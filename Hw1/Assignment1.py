import math
import pathlib

#1
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []

    for line in path.read_text().splitlines():
        left, right = line.split("=")
        B.append(float(right))

        x=0.0
        y=0.0
        z=0.0
        sign =1

        for term in left.split():
            if term == "+":
                sign = 1
            elif term == "-":
                sign = -1
            else:
                letter = term[-1]
                nr = term[:-1]

                if nr == "":
                    coef = 1.0
                else:
                    coef = float(nr)
                coef = coef * sign

                if letter == "x":
                    x = coef
                elif letter == "y":
                    y = coef
                else:
                    z = coef
        A.append([x,y,z])
    return A,B

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} {B=}")

#2.1
def determinant(matrix: list[list[float]]) -> float:
    a= matrix
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])- a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])+ a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))

print(f"{determinant(A)=}")

#2.2
def trace(matrix: list[list[float]]) -> float:
    a=matrix
    return a[0][0] + a[1][1] + a[2][2]

print(f"{trace(A)=}")

#2.3
def norm(vector: list[float]) -> float:
    return math.sqrt(sum(x**2 for x in vector))

print(f"{norm(B)=}")

#2.4
def transpose(matrix: list[list[float]]) -> list[list[float]]:
    rows = len(matrix)
    cols = len(matrix[0])

    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

print(f"{transpose(A)=}")

#2.5
def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    rows = len(matrix)
    cols = len(matrix[0])

    result = [0.0] * rows

    for i in range(rows):
        for j in range(cols):
            result[i] += matrix[i][j] * vector[j]

    return result

print(f"{multiply(A, B)=}")

#3
def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("The system has no unique solution (determinant is zero)")

    sol = []
    num_vars = len(vector)

    for col_index in range(num_vars):
        matrix_replaced =[]
        for row_index in range(len(matrix)):
            row_copy = list(matrix[row_index])
            row_copy[col_index] = vector[row_index]

            matrix_replaced.append(row_copy)

        det_ai = determinant(matrix_replaced)
        sol.append(det_ai / det_a)
    return sol

print(f"{solve_cramer(A, B)=}")


#4
def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    return [[matrix[r][c] for c in range(len(matrix)) if c != j] for r in range(len(matrix)) if r != i]

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    rows = len(matrix)
    cols = len(matrix[0])
    cof_matrix = []

    for i in range(rows):
        cof_row = []
        for j in range(cols):
            sub = minor(matrix, i, j)
            det_sub = sub[0][0] * sub[1][1] - sub[0][1] * sub[1][0]
            sign = (-1) ** (i + j)
            cof_row.append(sign * det_sub)
        cof_matrix.append(cof_row)

    return cof_matrix

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("The system has no unique solution (determinant is zero)")

    adj = adjoint(matrix)
    rows = len(adj)
    cols = len(adj[0])

    inverse =[[adj[i][j] / det_a for j in range(cols)] for i in range(rows)]

    return multiply(inverse, vector)

print(f"{solve(A, B)=}")