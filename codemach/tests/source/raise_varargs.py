
class TestException(Exception): pass

try:
    raise TestException()
except TestException:
    pass
else:
    raise Exception()



