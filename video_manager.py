# -*- coding: utf-8 -*-
import subprocess as SUB
import re
from os import listdir, remove


class Video_manager():
    """a class that deals with video files"""

    def __init__(self, path=None, split_path=None, filename=None):
        """a constractor that can optionally get a path"""
        self.path = path
        if split_path:
            self.split_path = split_path
        else:
            self.split_path = self.path
        self.filename = filename

    def get_part_video_num(self, num):
        """gets a number to a 3 digit string"""
        if len(str(num)) == 1:
            return '00' + str(num)
        elif len(str(num)) == 2:
            return '0' + str(num)
        else:
            return str(num)

    def get_length(self):
        """returns the length of a video"""
        if self.path and self.filename:
            process = SUB.Popen(['ffmpeg',  '-i', self.path + self.filename], stdout=SUB.PIPE, stderr=SUB.STDOUT)
            stdout, stderr = process.communicate()
            matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

            return (int(matches['hours']) *3600 + int(matches['minutes']) * 60 + int(float(matches['seconds'])))

    def get_parts(self):
        """returns the parts to divide the video to"""
        if self.path and self.filename:
            part_size = 1
            length = self.get_length()
            if length > 100:
                part_size = int(length/100)
            return part_size

    def divide_video(self):
        """   """
        if self.path and self.split_path and self.filename:
            segment_size = self.get_parts()
            print segment_size
            p = SUB.call('ffmpeg -i %s -c copy -map 0 -segment_time %s -f segment %s' % (self.path + self.filename, segment_size, self.split_path) + '%03d.mp4')

            #COPY_PATH = "D:\\mpsplits\\"
            #PASTE_PATH = "D:\\mas\\"
            n = 0

            files = listdir(self.split_path)
            print files
            max_part = int(max(files)[:3])

            while n <= max_part:
                p = SUB.call('ffmpeg -i %s.mp4 %s.wav' % (self.split_path+self.get_part_video_num(n), self.split_path+self.get_part_video_num(n)))
                n += 1

            n = 0
            while n <= max_part:
                p = SUB.call('ffmpeg -i %s.mp4 -target ntsc-vcd -vcodec mpeg1video -an %s.mpg' % (self.split_path+self.get_part_video_num(n), self.split_path+self.get_part_video_num(n)))
                n += 1

            for f in files:
                remove(self.split_path + f)

            print 'nehenaknu im gui'


def main():
    """
    Add Documentation here
    """
    pass  # Add Your Code Here

    vid = Video_manager(path="D:\\", split_path="D:\\mpsplits\\", filename='The_Hobbit_Trailer.mp4')
    vid.divide_video()


if __name__ == '__main__':
    main()