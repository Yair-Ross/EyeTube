# -*- coding: utf-8 -*-
import subprocess
import re


class Video_manager():
    """a class that deals with video files"""

    def __init__(self, path=None, split_path=None):
        """a constractor that can optionally get a path"""
        self.path = path
        self.split_path = split_path

    def get_length(self, path):
        process = subprocess.Popen(['ffmpeg',  '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

        return (int(matches['hours']) *3600 + int(matches['minutes']) * 60 + int(float(matches['seconds'])))

    def get_parts(self):
        """returns the parts to divide the video to"""
        if self.path:
            part_size = 1
            length = self.get_length(self.path)
            if length > 100:
                part_size = int(length/100)
            return part_size

    def divide_video(self):
        if self.path and self.split_path:
            segment_size = self.get_parts()
            print segment_size
            #p = subprocess.call('ffmpeg -i %s -c copy -map 0 -segment_time %s -f segment %s%03d.mpg' %
            #                    (self.path, segment_size, self.split_path))



def main():
    """
    Add Documentation here
    """
    pass  # Add Your Code Here

    vid = Video_manager("D:\The_Hobbit_Trailer.mp4", 'a')
    vid.divide_video()


if __name__ == '__main__':
    main()