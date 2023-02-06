import json
import os.path
import time


class JSONFileWriter:

    @staticmethod
    def write(objects, path):
        timestamp = int(time.time() * 1000)
        with open(os.path.join(path, f'{timestamp}.json'), 'w') as f:
            for obj in objects:
                f.write(json.dumps(obj))
                f.write('\n')
