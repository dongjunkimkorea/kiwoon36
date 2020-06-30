import analyze2 as ref

class R():
    def __init__(self):
        r = ref.A()
        r.ref()

        #print('r.__t', r.__t)
        print('r_t', r._t )

        r.sta()

        r.clsMethod()


if __name__ == "__main__":
    ref.A.clsMethod()