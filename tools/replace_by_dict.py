import sys
import re


def multiple_replace(regex, adict, text):
    # Create a regular expression from all of the dictionary keys


    # For each match, look up the corresponding value in the dictionary
    return regex.sub(lambda match: adict[match.group(0)], text)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        replace = {}
        for x in f:
            x = x.strip()
            if x[-1] != ':':
                s, t = x.split(':')
            else:
                s = x[0]
                t = x[-1]
            replace[s] = t
    regex = re.compile("|".join(map(re.escape, replace.keys())))

    for text in sys.stdin:
        text = text.strip()
        print(multiple_replace(regex, replace, text))
