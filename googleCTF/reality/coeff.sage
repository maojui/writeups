with open('data', 'r') as f:
    A = []
    for _ in range(3):
        A.append([Integer(f.readline()) for _ in range(5)])
    A = Matrix(A)
    y = vector([Integer(f.readline()) for _ in range(3)])
Ay = Matrix([r.list() + [v] + [1 if i == j else 0 for j in range(len(y))] for i, (r, v) in enumerate(zip(A, y))])
B = Ay.right_kernel_matrix()
print(-B.LLL()[0])
