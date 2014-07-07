# coding=utf-8
import os
import yaml
from picassoft.sprite_bundler import builder

PATH = os.path.dirname(os.path.realpath(__file__))

os.chdir(PATH)

with open('sprites.yaml', 'r') as file:
    for sprite_settings in yaml.load(file):
        print("making {}".format(sprite_settings))
        builder.make(**sprite_settings)
