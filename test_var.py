class TestVar():

    x = '1'

    def __init__(self):
        pass

    def fun(self):
        x = '2'
        self.x = '3'

        print('x = '+ x)
        print('self.x = ' + self.x)
        print('TestVer.x = ' + TestVar.x)


c = TestVar()
c.fun()


print(dir())

print('-----------------------------------------------')

print(dir(TestVar.__dict__))

print('-----------------------------------------------')


print(dir(c.__dict__))