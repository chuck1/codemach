
def func():
    print(locals())
    l = locals()
    l['a']=1
    print(locals())

func()

