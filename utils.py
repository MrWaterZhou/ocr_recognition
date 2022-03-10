import numpy as np
import cv2
import sys
import glob
import os


def get_rotate_crop_image(img, points):
    '''

    :param img: np.array
    :param points: list of points
    :return:
    '''
    points = sorted(points, key=lambda x: x[0])

    index_1, index_2, index_3, index_4 = 0, 1, 2, 3
    if points[1][1] > points[0][1]:
        index_1 = 0
        index_4 = 1
    else:
        index_1 = 1
        index_4 = 0
    if points[3][1] > points[2][1]:
        index_2 = 2
        index_3 = 3
    else:
        index_2 = 3
        index_3 = 2

    box = [points[index_1], points[index_2], points[index_3], points[index_4]]
    points = np.array(box)

    img_crop_width = max(
        np.linalg.norm(points[0] - points[1]),
        np.linalg.norm(points[2] - points[3]))
    img_crop_height = max(
        np.linalg.norm(points[0] - points[3]),
        np.linalg.norm(points[1] - points[2]))

    if img_crop_height * 1.0 / img_crop_width >= 1.5:
        rota = 32. / img_crop_width
        img_crop_height = rota * img_crop_height
        img_crop_width = 32

    else:
        rota = 32. / img_crop_height
        img_crop_width = rota * img_crop_width
        img_crop_height = 32

    int_height, int_width = int(img_crop_height), int(img_crop_width)
    pts_std = np.float32([[0, 0], [int_width, 0],
                          [int_width, int_height],
                          [0, int_height]])

    # pict channel 3 -> 1 following
    #         img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    M = cv2.getPerspectiveTransform(points.astype('float32'), pts_std)
    dst_img = cv2.warpPerspective(
        img,
        M, (int_width, int_height),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC)

    if img_crop_height * 1.0 / img_crop_width >= 1.5:
        dst_img = np.rot90(dst_img)
        _label = 1
    else:
        _label = 0
    return dst_img, _label


def load_mtwi_label(file, language=None):
    with open(file) as f:
        labels = []
        for label in f:
            label = label.strip().split(',')
            text = label[-1]
            points = []
            for i in range(4):
                points.append((float(label[2 * i]), float(label[2 * i + 1])))
            if language is None:
                labels.append((text, points))
            else:
                if label[-2] in language:
                    labels.append((text, points))
    return labels


if __name__ == '__main__':
    image_path = sys.argv[1]
    label_path = sys.argv[2]
    save_path = sys.argv[3]
    language = sys.argv[4].split(',') if len(sys.argv) > 4 else None

    os.makedirs(save_path, exist_ok=True)
    results = open(save_path + '.txt', 'w')
    image_files = glob.glob('{}/*.jpg'.format(image_path))
    for i, image_file in enumerate(image_files):
        try:
            label_file = image_file.split('/')[-1]
            label_file = label_file.split('.')
            label_file[-1] = 'txt'
            label_file = '.'.join(label_file)
            label_file = os.path.join(label_path, label_file)

            image = cv2.imread(image_file)
            labels = load_mtwi_label(label_file, language)
            for j, label in enumerate(labels):
                dst_img, rotate = get_rotate_crop_image(image, label[1])
                img_file = os.path.join(save_path, '{}_{}_{}.jpg'.format(i, j, rotate))
                cv2.imwrite(img_file, dst_img)
                results.write('{}\t{}\n'.format(img_file, label[0]))
        except Exception as e:
            print(e)

    results.close()
