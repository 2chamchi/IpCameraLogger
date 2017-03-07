import sys

class IpCamera(object):

    def __init__(self, camera_info):
        self.name = camera_info.name
        self.id = camera_info.id
        self.pwd = camera_info.password
        self.ip = camera_info.ip

    def log(self, str):
        print(sys.stderr, str)

    def get_info(self):
        return 'ffprobe -i ' +  + ' -print_format json -pretty -show_entries \"stream=width,height,codec_name\"'