# coding=utf-8
import sys
import os

SPRITE_SPACING = 2

if sys.platform == "win32":
    SPRITE_COMPRESSOR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'pngcrush')
else:
    SPRITE_COMPRESSOR_PATH = None
