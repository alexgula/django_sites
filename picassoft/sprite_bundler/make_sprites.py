# coding=utf-8
import sys
import os


if __name__ == '__main__':
    from . import builder
    from . import image_show

    working_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    filename = builder.make(
        format="sprite-{name}",
        source=os.path.join(working_path, 'sprites', '*.*'),
        url="../img/sprites.png",
        sprite_file=os.path.join(working_path, 'sprites.png'),
        css_file=os.path.join(working_path, 'sprites.css'))

    print ("Success: sprite file {}".format(filename))
    image_show.show(filename)
