# -*- coding: utf-8 -*-
import subprocess as SUB
import re
from os import listdir, remove
from os.path import getsize

"""to use this class you must have FFMPEG installed"""

class Video_manager():
    """a class that deals with video files"""

    def __init__(self, path, split_path=None):
        """a constractor that can optionally get a path"""
        self.path = path
        #the default split will be for the same file as the given path
        if split_path:
            self.split_path = split_path
        '''else:
            self.split_path = self.path[-self.path.index('\\'):]'''

    def get_part_video_num(self, num):
        """gets a number to a 3 digit string"""
        if len(str(num)) == 1:
            return '00' + str(num)
        elif len(str(num)) == 2:
            return '0' + str(num)
        else:
            return str(num)

    def get_length(self):
        """returns the length of a video in seconds"""
        if self.path:
            #calls a process that reads video data
            process = SUB.Popen(['ffmpeg',  '-i', self.path], stdout=SUB.PIPE, stderr=SUB.STDOUT)
            #gets process output
            stdout, stderr = process.communicate()
            #gets needed data
            matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

            return (int(matches['hours']) *3600 + int(matches['minutes']) * 60 + int(float(matches['seconds'])))

    def get_parts(self):
        """returns the parts to divide the video to"""
        if self.path:
            part_size = 1
            length = self.get_length()
            #prevents too many parts
            if length > 100:
                part_size = int(length/100)
            return part_size

    def divide_video(self):
        """gets a video to convert to video and audio parts"""
        if self.path and self.split_path:
            segment_size = self.get_parts()
            print
            print ('ffmpeg -i %s -c copy -map 0 -segment_time %s -f segment %s' % (self.path, segment_size, self.split_path) + '%03d.mp4')
            print
            print
            print
            #divide video to parts of the calculated length, NOTE: not every part will be exactly at the same length
            p = SUB.call('ffmpeg -i %s -c copy -map 0 -segment_time %s -f segment %s' % (self.path, segment_size, self.split_path) + '%03d.mp4')

            n = 0

            files = listdir(self.split_path)
            #gets max part
            for i in reversed(files):
                if len(i) >= 3 and i[:3].isdigit():
                    max_part = int(i[:3])
                    break
            else:
                max_part = -1

            while n <= max_part:
                #convert to audio parts
                p = SUB.call('ffmpeg -i %s.mp4 %s.wav' % (self.split_path+self.get_part_video_num(n), self.split_path+self.get_part_video_num(n)))
                n += 1

            n = 0
            while n <= max_part:
                #converts to video parts
                p = SUB.call('ffmpeg -i %s.mp4 -target ntsc-vcd -vcodec mpeg1video -an %s.mpg' % (self.split_path+self.get_part_video_num(n), self.split_path+self.get_part_video_num(n)))
                n += 1

            for f in files:
                try:
                    #deletes the unnecessary original video parts
                    remove(self.split_path + f)
                except:
                    pass

            print 'nehenaknu im gui'

    def get_num_of_parts(self):
        """returns number of parts of video"""
        if self.split_path:
            theparts = listdir(self.split_path)
            partnum = 0
            for i in theparts:
                if i[-4:] == '.mpg':
                    partnum += 1
            return partnum

    def get_size(self, size=20):
        """returns the file size in mega bytes by default or in other size if size is given"""
        if self.path:
            return int(getsize(self.path) >> size)


def main():
    """
    Add Documentation here
    """
    pass  # Add Your Code Here


if __name__ == '__main__':
    main()