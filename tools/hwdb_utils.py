import struct
import numpy as np
import cv2
from PIL import Image
import sys
import os


def load_gnt(file):
    char_dict = {}
    f = open(file, 'rb')
    while f.read(4):
        tag_code = f.read(2).decode('gbk')[0]
        width = struct.unpack('<h', bytes(f.read(2)))
        height = struct.unpack('<h', bytes(f.read(2)))
        data = f.read(width[0] * height[0])
        tmp = np.array(Image.frombytes('L', (width[0], height[0]), data))
        if tag_code in {'a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 't', 'u', 'v', 'w', 'x', 'z'}:
            tmp = cv2.resize(tmp, (tmp.shape[1] * 24 // tmp.shape[0], 24))
            tmp = np.concatenate([(np.ones((8, tmp.shape[1])) * 255).astype(np.uint8), tmp], 0)
        else:
            tmp = cv2.resize(tmp, (tmp.shape[1] * 32 // tmp.shape[0], 32))
        char_dict[tag_code] = tmp
    f.close()
    return char_dict


def create_words(text: str, char_dict: dict, space_width=0):
    if space_width > 0:
        space = (np.ones((32, space_width)) * 255).astype(np.uint8)

    result = []
    for c in text:
        result.append(char_dict[c])
        if space_width > 0:
            result.append(space)

    result = np.concatenate(result, 1)
    return result


if __name__ == '__main__':
    gnt = sys.argv[1]
    word_file = sys.argv[2]
    save_path = sys.argv[3]

    gnt_dict = load_gnt(gnt)
    words = []
    with open(word_file) as f:
        for x in f:
            words.append(x.strip())

    with open(save_path + '.txt', 'w') as f:
        for i, word in enumerate(words):
            try:
                word_img = create_words(word, gnt_dict, np.random.randint(1, 4))
                cv2.imwrite(os.path.join(save_path, '{}.jpg'.format(i)), word_img)
                f.write('{}\t{}\n'.format(os.path.join(save_path, '{}.jpg'.format(i)), word))
            except:
                print(word)

