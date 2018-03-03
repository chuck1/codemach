class Matrix:
    def __matmul__(self, b): pass
    def __rmatmul__(self, b): pass
    def __imatmul__(self, b): pass
a, b = Matrix(), Matrix()
a @ b
1 @ a
#a @= b
