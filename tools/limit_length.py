import sys

if __name__ == '__main__':
    for x in sys.stdin:
        x = x.strip()
        while len(x)>25:
            sys.stdout.write(x[:25]+'\n')
            x = x[25:]
        sys.stdout.write(x[:25] + '\n')
