 
#!/usr/bin/env python3
import argparse
import redis as server
import json
import pickle
import lzma

PORT = 6379
DB = 0


class LzmaCompressor(object):
    min_length = 100
    preset = 4

    def compress(self, value):
        if len(value) > self.min_length:
            return lzma.compress(value, preset=self.preset)
        return value

    def decompress(self, value):
        try:
            return lzma.decompress(value)
        except lzma.LZMAError:
            return value


_compressor = LzmaCompressor()


def _export(redis, filename):
    with open(filename, 'w') as ljson:
        for key in redis.scan_iter():
            value = _compressor.decompress(redis.get(key))
            value = pickle.loads(value)
            ljson.write(json.dumps({key: value}) + "\n")


def _import(redis, filename):
    with open(filename, 'r') as ljson:
        for line in ljson:
            print(line)
            obj = json.loads(line)
            for key, value in obj.items():
                value = _compressor.compress(pickle.dumps(value))
                redis.set(key, value, px=None, nx=False, xx=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dump/restore into file for Redis')
    parser.add_argument('action', metavar='action', help='May be only "import" or "export"')
    parser.add_argument('host', metavar='host', help='The host of the source redis which is to be dumped')
    parser.add_argument('-f', '--file', action='store', dest='file', default='export.ljson', help='File for import/export')
    args = parser.parse_args()

    redis = server.StrictRedis(host=args.host, port=PORT, db=DB, decode_responses=True)

    if args.action == 'export':
        _export(redis, args.file)
    elif args.action == 'import':
        _import(redis, args.file)
    else:
        raise Exception('Unknown action {}'.args.action) 