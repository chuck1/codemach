

class Wrapper:
    def __init__(self, *args):
        print("Wrapper __init__", args)

    def __call__(self, *args):
        print("Wrapper __call__", args)


@Wrapper
def f():
    print("f")

print(f)

f(1)


