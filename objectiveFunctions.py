def F1(argv):

    # -100 <= x <= 100

    x = argv[0]

    y = x**2 - x - 2

    return y


def F2(argv):

    # -4.5 <= x, y <= 4.5
    x = argv[0]
    y = argv[1]

    z = (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2

    return z


def F3(argv):

    # -5 <= x, y <= 5

    from math import exp, sin, cos, pi, sqrt

    x = argv[0]
    y = argv[1]

    z = -20*exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2*pi*x) + cos(2*pi*y))) + exp(1) + 20

    return z


def F4(argv):

    # -10 <= x, y <= 10

    x = argv[0]
    y = argv[1]

    z = (x + 2*y - 7)**2 + (2*x + y - 5)**2

    return z


def F5(argv):

    # -15 <= x <= -5, -3 <= y <= 3

    from math import sqrt

    x = argv[0]
    y = argv[1]

    z = 100 * sqrt(abs(y - 0.01*x**2)) + 0.01*abs(x + 10)

    return z


def F6(argv):

    # -5 <= x, y <= 5

    x = argv[0]
    y = argv[1]

    z = 2*x**2 - 1.05*x**4 + (x**6)/6 + x*y + y**2

    return z


def F7(argv):

    # -100 <= x, y <= 100

    from math import sin, cos

    x = argv[0]
    y = argv[1]

    z = 0.5 + (((cos(sin(abs(x**2 - y**2))))**2) - 0.5)/(1 + 0.001*(x**2 + y**2))**2

    return z


def F8(argv):

    # -100 <= x, y <= 100

    from math import sin, cos, exp, pi

    x = argv[0]
    y = argv[1]

    z = -cos(x)*cos(y)*exp(-((x - pi)**2 + (y - pi)**2))

    return z


def F9(argv):

    # 0 <= x, y <= 14

    from math import sin, pi

    x = argv[0]
    y = argv[1]

    z = (1 - abs((sin(pi*(x - 2))*sin(pi*(y - 2)))/(pi**2*(x - 2)*(y - 2)))**5)*(2 + (x - 7)**2 + 2*(y - 7)**2)

    return z


def F10(argv):

    # 1 <= x <= 60

    from math import sin, cos, tanh, exp

    x1 = argv[0]
    x2 = argv[1]
    x3 = argv[2]
    x4 = argv[3]
    x5 = argv[4]

    z = 0

    for i in xrange(1, 24):

        t = 0.1*(i - 1)

        y = 53.81*(1.27**t)*tanh(3.012*t + sin(2.13*t))*cos(exp(0.507)*t)

        z = z + ((x1*x2**t)*tanh(x3*t + sin(x4*t))*cos(t*exp(x5)) - y)**2

    return z


def F11(argv):

    # -1.5 <= x <= 1.5
    # -0.5 <= y <= 2.5
    # s.t (x - 1)**3 - y + 1 < 0, x + y - 2 < 0

    x = argv[0]
    y = argv[1]

    z = (1 - x)**2 + 100*(y - x**2)**2

    return z


def F12(argv):

    # -1.25 <= x, y <= 1.25
    # s.t x**2 + y**2 <= (1 + 0.2*cos(8*atan(x/y)))**2

    x = argv[0]
    y = argv[1]

    z = 0.1*x*y

    return z


def F13(argv):

    # 0 <= x, y <= Inf
    # s.t 2*x + y <= 5000, 4*x + 5*y <= 15000

    x = argv[0]
    y = argv[1]

    z = 10*x + 7*y

    return z


def BKF1(argv):

    # 0 <= x <= 5
    # 0 <= y <= 3
    # s.t (x - 5)**2 + y**2 <= 25, (x - 8)**2 + (y + 3)**2 >= 7.7

    x = argv[0]
    y = argv[1]

    z = 4*x**2 + 4*y**2

    return z


def BKF2(argv):

    # 0 <= x <= 5
    # 0 <= y <= 3
    # s.t (x - 5)**2 + y**2 <= 25, (x - 8)**2 + (y + 3)**2 >= 7.7

    x = argv[0]
    y = argv[1]

    z = (x - 5)**2 + (y - 5)**2

    return z


def CEP1(argv):

    # 0.1 <= x <= 1
    # 0 <= y <= 5
    # s.t y + 9*x >= 6, -y + 9*x >= 1

    x = argv[0]

    z = x

    return z


def CEP2(argv):

    # 0.1 <= x <= 1
    # 0 <= y <= 5
    # s.t y + 9*x >= 6, -y + 9*x >= 1

    x = argv[0]
    y = argv[1]

    z = (1 + y)/x

    return z


def ZDT3A(argv):

    # 0 <= x(i) <=1
    # 1 <= i <= 30

    x1 = argv[0]

    z = x1

    return z


def ZDT3B(argv):

    from math import sqrt, sin, pi

    f1 = argv[0]
    x = argv[1:]

    g = (1 + (9/29)*sum(x))
    h = (1 - sqrt(f1/g) - (f1/g)*sin(10*pi*f1))

    z = g*h

    return z


def V1(argv):

    # -3 <= x, y <= 3

    from math import sin

    x = argv[0]
    y = argv[1]

    z = 0.5*(x**2 + y**2) + sin(x**2 + y**2)

    return z


def V2(argv):

    # -3 <= x, y <= 3

    x = argv[0]
    y = argv[1]

    z = ((3*x - 2*y + 4)**2)/8 + ((x - y + 1)**2)/27 + 15

    return z


def V3(argv):

    # -3 <= x, y <= 3

    from math import exp

    x = argv[0]
    y = argv[1]

    z = (1/(x**2 + y**2 + 1)) - 1.1*exp(-(x**2 + y**2))

    return z


def T1(argv):
    x1 = argv[0]
    x2 = argv[1]
    z = ((x1 - 2)**2)/2 + ((x2 + 1)**2)/13 + 3

    return z


def T2(argv):

    x1 = argv[0]
    x2 = argv[1]

    z = ((x1 + x2 - 3)**2)/36 + ((-x1 + x2 + 2)**2)/8 + 17

    return z


def T3(argv):

    x1 = argv[0]
    x2 = argv[1]

    z = ((x1 + 2*x2 - 1)**2)/175 + ((-x1 + 2*x2)**2)/17 - 13

    return z

