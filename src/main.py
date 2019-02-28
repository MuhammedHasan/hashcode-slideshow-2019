def parse(filename):
    pass


def solve(obj):
    pass


def write(filename):
    pass


if __name__ == "__main__":
    files = [
        'example',
        'small',
        'medium',
        'big'
    ]

    for f in files:
        obj = parse('inputs/%s.in' % f)
        solution = solve(obj)
        write(solution, 'outputs/%s.out' % f)
