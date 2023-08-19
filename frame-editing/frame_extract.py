import sys
import cv2
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input mp4 or video file name ', type=str, default='01.mp4')
parser.add_argument('--output', help='output frames directory in frame folder', type=str, default='01')
parser.add_argument('--interval', help='frame interval', type=int, default=1)
args = parser.parse_args()


def extract(argv, args):
    save_dir = os.path.join('./frames', args.output)
    if os.path.exists(save_dir):
        print('good')
    else:
        print('make directory {}'.format(save_dir))
        os.mkdir(save_dir)

    video_path = os.path.join('./video', args.input)
    video = cv2.VideoCapture(video_path)
    success, img = video.read()
    count = 0
    if success:
        print('success reading video')
    else:
        print('fail reading video')
    while success:
        success, img = video.read()

        if count % args.interval == 0:
            frame = 'frames_{}.png'.format(count)
            path = os.path.join(save_dir, frame)
            cv2.imwrite(path, img)
            print('extract frame {}.png'.format(count))
        count += 1


if __name__ == '__main__':
    argv = sys.argv
    extract(argv, args)
