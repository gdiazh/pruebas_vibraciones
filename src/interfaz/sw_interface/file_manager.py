#!/usr/bin/python

__author__ = 'gdiaz'

import rospy
import time
from time import gmtime, strftime

class fileManager(object):
    def __init__(self, file_name, debug = False):
        self.debug = debug
        self.file_path = "data/"
        self.file_name = file_name
        self.file_ext = ".csv"
        self.time_stamp = strftime("%Y-%m-%d_%H:%M:%S_", gmtime())
        self.full_name = self.file_path+self.time_stamp+self.file_name+self.file_ext
        self.data_file = open(self.full_name, "ab+")

    def init(self):
        self.data_file = open(self.full_name, "ab+")
        self.data_file.write("a1x"); self.data_file.write(",")
        self.data_file.write("a1y"); self.data_file.write(",")
        self.data_file.write("a1z"); self.data_file.write(",")
        self.data_file.write("a2x"); self.data_file.write(",")
        self.data_file.write("a2y"); self.data_file.write(",")
        self.data_file.write("a2z"); self.data_file.write(",")
        self.data_file.write("time"); self.data_file.write(",")
        self.data_file.write("tail1"); self.data_file.write(",")
        self.data_file.write("tail2"); self.data_file.write(",")
        self.data_file.write("tail3"); self.data_file.write(",")
        self.data_file.write("checksum"); self.data_file.write(",")

    def stop(self):
        self.data_file.close();

    def to_file(self, data, sz):
        self.data_file = open(self.full_name, "ab+")
        for i in range(0,sz):
            self.data_file.write(str(data[i]))
            self.data_file.write(",")
        self.data_file.write("\n")
        self.data_file.close()

if __name__ == '__main__':
    file_name = raw_input("file_name: ")
    file_manager = fileManager(file_name, debug = True)
    # test
    file_manager.to_file([1,2,3,4], 4)
    print "test finish ..."
    file_manager.stop()