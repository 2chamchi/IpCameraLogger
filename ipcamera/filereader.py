import codecs
from collections import namedtuple

class FileReader(object):
    def __init__(self, path):
        self.path = path
        self.file = codecs.open(self.path, 'r', 'utf-8')

    def get_camera_list(self):
        lines = self.file.readlines()
        self.camera_info_list = []
        for idx in lines:
            camera_info = idx.split(',')
            self.camera_info_list.append(self.parse_info(camera_info))
        self.file.close()

    def parse_info(self, line):
        camera_structure = namedtuple("camera_structure", "name id password ip")
        name = self.str_filter(line[0])
        id = self.str_filter(line[1])
        password = self.str_filter(line[2])
        ip = self.str_filter(line[3])
        return camera_structure(name, id, password, ip)

    def str_filter(self, line_str):
        result = line_str.replace("\ufeff", "")
        result = result.replace("\r", "")
        result = result.replace("\n", "")
        return result

