import module_1

print("module2 is starting.....")
print(dir())
print("__annotations__ : ",__annotations__)
print("__builtins__ : ",__builtins__)
print("__cached__ : ",__cached__)
print("__doc__ : ",__doc__)
print("__file__ : ",__file__)
print("__loader__ : ",__loader__)
print("__name__ : ",__name__)
print("__package__ : ",__package__)
print("__spec__ : ",__spec__)
print("module_1 : ",module_1)
print()

for dirItem in dir():
    print("dirItem({0}):", dirItem , type(dirItem))

varA = 'a'

def defA(a=None,b=None):
    varDefA = 'b'
    varA = 'b'
    print("===========================================> defA() local namespace")
    print(locals())
    return varDefA + varA
defA()
print(defA)
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(locals())
print(globals())
print(globals()['defA'])

class classA():
    varClassA = 'c'
    def defClassA(self):
        varDefClassA = 'd'
        pass

class_classA = classA()

print("====================== dir() ")
print(dir())

print("====================== dir(object) ")
print("dir(classA)",dir(classA))
print("dir(defA)",dir(defA))
print("dir(varA)",dir(varA))
print("dir(dirItem)",dir(dirItem))

print("===================== __class__")
print("classA.__class__ : ", classA.__class__)
print("defA.__class__ :", defA.__class__)
print("varA.__class__ :", varA.__class__)
print("dirItem.__class__ :", dirItem.__class__)

print("===================== __dict__")
print("classA.__dict__ : ", classA.__dict__)
print("class_classA.__dict__ : ", class_classA.__dict__)

print("defA.__dict__ :", defA.__dict__)
print("varA.__dict__ : '__dict__ 단 일부 built-in 객체(int,float,tuple,str 등)'")

print("===================== __dir__")
print("defA.__dir__ :", defA.__dir__)

print("===================== ")
print(type(module_1))
print(module_1.__dict__)

print("======================= fucntion")
print(defA.__dict__)
print(defA.__class__)
# print(defA.__code__.__dict__)

# print(dirItem)

# print(__doc__)
# print(__loader__)
# print(__name__)
# print(__package__)
# print(__spec__)