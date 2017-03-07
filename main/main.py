import optparse
import sys
from ipcamera.filereader import FileReader

VERSION = 0.1

def main():
    parser = optparse.OptionParser(usage='%prog --file=FILE',
                                   version='%prog ' + str(VERSION))
    parser.add_option('-f', '--file', dest='path',
                      help='ipcamera url list FILE', metavar='FILE')
    opts, args = parser.parse_args()
    if args:
        parser.error('No arguments are needed. See help.')
    if not opts.path:
        parser.error('File must be specified. See help.')

    try:
        file_reader = FileReader(opts.path)
        print(file_reader.get_camera_list())
    except Exception as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()