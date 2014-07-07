import os
import zipfile

curdir = os.path.dirname(os.path.realpath(__file__))

for item in os.listdir(curdir):
    if os.path.isdir(item):
        dir = os.path.join(curdir, item)
        zip_name = '.'.join([dir,'zip'])
        if os.path.exists(zip_name):
            os.remove(zip_name)
        print("Zip file: {0}".format(zip_name))
        zip = zipfile.ZipFile(zip_name,'a')

        def add_file(file_path, file_name, rel_dir):
            full_path = os.path.join(file_path, file_name)
            if os.path.isfile(full_path):
                rel_path = os.path.relpath(full_path, rel_dir)
                zip.write(full_path, rel_path)

        def add_files(rel_dir, d, flst):
            for f in flst:
                add_file(d, f, rel_dir)

        def walk(path):
            for file_name in os.listdir(path):
                full_path = os.path.join(path, file_name)
                if os.path.isdir(full_path):
                    if file_name == "dzc_output_files":
                        os.path.walk(full_path, add_files, path)
                    else:
                        walk(full_path)
                elif file_name == "dzc_output.xml" and os.path.isfile(full_path):
                    add_file(path, file_name, path)

        try:
            walk(dir)
        finally:
            zip.close()
