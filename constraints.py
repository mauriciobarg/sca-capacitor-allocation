def F11C1(argv):

    x = argv[0]
    y = argv[1]

    z = (x - 1)**3 - y + 1

    if z < 0:

        return True

    else:

        return False


def F11C2(argv):

    x = argv[0]
    y = argv[1]

    z = x + y - 2

    if z < 0:

        return True

    else:

        return False


def F12C1(argv):

    from math import atan, cos

    x = argv[0]
    y = argv[1]

    z = x**2 + y**2

    if z <= (1 + 0.2*cos(8*atan(x/y)))**2:

        return True

    else:

        return False


def F13C1(argv):

    x = argv[0]
    y = argv[1]

    z = 2*x + y

    if z <= 5000:

        return True

    else:

        return False


def F13C2(argv):

    x = argv[0]
    y = argv[1]

    z = 4*x + 5*y

    if z <= 15000:

        return True

    else:

        return False


def BKC1(argv):

    x = argv[0]
    y = argv[1]

    z = (x - 5)**2 + y**2

    if z <= 25:

        return True

    else:

        return False


def BKC2(argv):

    x = argv[0]
    y = argv[1]

    z = (x - 8)**2 + (y + 3)**2

    if z >= 7.7:

        return True

    else:

        return False


def CEPC1(argv):

    x = argv[0]
    y = argv[1]

    z = y + 9*x

    if z >= 6:

        return True

    else:

        return False


def CEPC2(argv):

    x = argv[0]
    y = argv[1]

    z = -y + 9*x

    if z >= 1:

        return True

    else:

        return False
