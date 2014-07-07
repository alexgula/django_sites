import os
import zipfile
import deepzoom

curdir = os.path.dirname(os.path.realpath(__file__))

creator = deepzoom.ImageCreator(tile_size=256, tile_overlap=1, image_quality=0.6, resize_filter="bicubic")

for item in os.listdir(curdir):
    if os.path.isfile(item):
        base, ext = os.path.splitext(item)
        if ext.lower() in ('.jpg',):
            source = os.path.join(curdir, item)
            dest_dir = os.path.join(curdir, base)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
                print(source)
                creator.create(source, os.path.join(dest_dir, 'dzc_output.xml'))

# Create Deep Zoom Image creator with weird parameters
#creator = deepzoom.ImageCreator(tile_size=512, tile_overlap=2, tile_format="png", image_quality=0.8, resize_filter="bicubic")

# Create Deep Zoom image pyramid from source
#creator.create(SOURCE, "helloworld.dzi")
