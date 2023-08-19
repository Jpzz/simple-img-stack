import argparse
import sys
import os
import cv2
import natsort
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='frames input directory', type=str, default='01')
parser.add_argument('--output', help='stacked frames output file name', type=str, default='01.png')
parser.add_argument('--width', help='set width resized img', type=int, default=512)
parser.add_argument('--height', help='set height resized img', type=int, default=512)
parser.add_argument('--row', help='merge frames number of rows', type=int, default=1)
parser.add_argument('--col', help='merge frames number of cols', type=int, default=1)

args = parser.parse_args()

def stack_img(argv, args):
    row = args.row
    col = args.col
    file_path = os.path.join('./frames', args.input)
    output_path = os.path.join('./stack-output', args.output)

    if os.path.exists('./stack-output'):
        print('exist output path')
    else:
        print('make directory {}'.format('./stack-output'))
        os.mkdir('./stack-output')

    resized_width = args.width
    resized_height = args.height

    files = os.listdir(file_path)
    sorted_files = natsort.natsorted(files)

    sum_frames = row * col
    num_of_files = len(files)

    if sum_frames > num_of_files:
        print('not enough number of files')

    merge_files = np.asarray(sorted_files[:sum_frames])
    merge_files = merge_files.reshape(row, col)

    stack_imgs = None
    for row in range(len(merge_files)):
        h_stack_img = None
        for idx, frame in enumerate(merge_files[row]):
            img_path = os.path.join(file_path, frame)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (resized_width, resized_height))
            if idx == 0:
                h_stack_img = img
            else:
                h_stack_img = cv2.hconcat([h_stack_img, img])
            print('completed stack horizontal images')
        if row == 0:
            stack_imgs = h_stack_img
        else:
            stack_imgs = cv2.vconcat([stack_imgs, h_stack_img])
        print('completed stack images')
        cv2.imwrite(output_path, stack_imgs)

if __name__ == '__main__':
    argv = sys.argv
    stack_img(argv, args)