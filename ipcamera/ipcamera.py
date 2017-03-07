import json
import subprocess
import codecs
from collections import namedtuple

class IpCamera(object):
    def __init__(self, camera_info_list, url_path):
        self.stream_info_list = []
        self.stream_error_list = []
        self.list = camera_info_list
        with open(url_path) as json_file:
            self.urls = json.load(json_file, strict=False)
        print(self.urls)

    def get_ffprobe_cmd(self, cam, url):
        return '../ffmpeg/ffprobe -i ' + "rtsp://" + cam.id + ":" + cam.password + "@" + cam.ip + url + ' -print_format json -pretty -show_entries \"stream=width,height,codec_name\"'

    def get_info_list(self):
        for cam in self.list:
            for url in self.urls:
                if self.get_stream_info(cam, url):
                    break
        self.write_stream_info_list()
        self.write_error_info_list()

    def get_stream_info(self, cam, url):
        try:
            ffprobe_popen = subprocess.run(self.get_ffprobe_cmd(cam, url), stdout=subprocess.PIPE, timeout=15)
            result = str(ffprobe_popen.stdout).split('\'')[1]
            self.stream_info_list.append(self.parse_info(result))
            return True
        except subprocess.TimeoutExpired as e:
            error_info_structure = namedtuple("error_info_structure", "camera_name ip info")
            error_info_structure(cam.id, cam.ip, e)
            self.stream_error_list.append(error_info_structure)
            return False
        except Exception as e:
            error_info_structure = namedtuple("error_info_structure", "camera_name ip info")
            error_info_structure(cam.id, cam.ip, e)
            self.stream_error_list.append(error_info_structure)
            return False

    def parse_info(self, stream_info):
        stream_info_structure = namedtuple("stream_info_structure", "codec_name width height")
        codec_name = stream_info["streams"][0]["codec_name"]
        width = stream_info["streams"][0]["width"]
        height = stream_info["streams"][0]["height"]
        return stream_info_structure(codec_name, width, height)

    def write_stream_info_list(self):
        file = codecs.open("./resources/stream_info_list.txt", 'w', 'utf-8')
        for idx in self.stream_info_list:
            file.write(idx + "\n")
        file.close()

    def write_error_info_list(self):
        file = codecs.open("./resources/error_info_list.txt", 'w', 'utf-8')
        for idx in self.stream_error_list:
            file.write(idx + "\n")
        file.close()