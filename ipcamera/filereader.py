import sys
import codecs
from ipcamera.ipcamera import IpCamera
from collections import namedtuple

class FileReader(object):

    def __init__(self, path):
        print('__init reader__')
        self.path = path
        print('read_camera_list', self.path)
        self.file = codecs.open(self.path, 'r', 'utf-8')

    def get_camera_list(self):

        lines = self.file.readlines()
        camera_info_list = []
        for idx in lines:
            camera_info = idx.split(',')
            camera_info_list.append(self.parse_info(camera_info))
        return camera_info_list

    def parse_info(self, line):
        camera_structure = namedtuple("camera_structure", "name id password ip")
        name = line[0].replace("\ufeff", "")
        id = line[1]
        password = line[2]
        ip = line[3].replace("\r\n", "")
        return camera_structure(name, id, password, ip)

    def log(self, str):
        print(sys.stderr, str)

