from fontTools.ttLib import TTFont
import sys
import os
import argparse

parser = argparse.ArgumentParser(description="check if all char is valid in the font")
parser.add_argument('-d', '--dict')
parser.add_argument('-f', '--font')
args = parser.parse_args()


def check(char_set: set, font: TTFont):
    cmap_chars = set()
    glyph_chars = set()
    for table in font['cmap'].tables:
        for k in table.cmap.keys():
            cmap_chars.add(chr(k))
            if table.cmap.get(k) is not None:
                glyph_chars.add(chr(k))

    return char_set - cmap_chars, char_set - glyph_chars


if __name__ == '__main__':
    char_dict = set()
    with open(args.dict) as f:
        for c in f:
            if c.strip() != '':
                char_dict.add(c.strip())

    font = TTFont(args.font)
    print(check(char_dict, font))
