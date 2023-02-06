import os.path


class FileReader:

    @staticmethod
    def read(path, modifier):
        results = []
        if os.path.isfile(path):
            results.append(modifier(path))
            return results
        else:
            for filename in os.listdir(path):
                f = os.path.join(path, filename)
                if os.path.isfile(f) and (filename.endswith('.mp3') or filename.endswith('.m4a')):
                    print(f'Analyzing file {f}')
                    r = modifier(f)
                    r['filename'] = filename
                    results.append(r)
            return results
