VERSION = (0, 1, 1, 'beta')

def get_version():
    number = VERSION[0:2]
    main = '.'.join(str(x) for x in number)

    sub = ''
    if VERSION[3] != 'final':
        sub = VERSION[3][0]

    return main + sub