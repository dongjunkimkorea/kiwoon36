x = 10

def fun():
    # fun()의 지역변수
    x = 20
    print(x)

    global x
    print(x )


print("실행")
fun()
print(x)
