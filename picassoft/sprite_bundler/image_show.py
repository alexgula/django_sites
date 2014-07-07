# coding=utf-8
import os
import sys


def show(filename):
    command = get_command(filename)
    os.system(command)


if sys.platform == "win32":

    def get_command(filename):
        return "start /wait {}".format(filename)

elif sys.platform == "darwin":

    def get_command(filename):
        return "(open -a /Applications/Preview.app {})&".format(filename)

else:

    def get_command(filename):
        return "(display {})&".format(filename)

if __name__ == "__main__":
    print(show(sys.argv[1]))
