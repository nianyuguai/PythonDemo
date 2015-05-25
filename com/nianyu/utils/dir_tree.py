# coding=utf-8
__author__ = 'nianyu'

from os.path import basename, isdir, exists
from os import listdir
from sys import argv


def show_tree(path,depth=0):
    print depth* '| ' + '|_', basename(path)
    if(isdir(path)):
        for item in listdir(path):
            show_tree(path+'/'+item, depth+1)


def isExist(path):
    if path[0] is not '/':
        return False

    if not exists(path):
        return False

    return True


if __name__ == "__main__":

    args = argv
    if len(args)>2:
        print "more than one argument."
        exit(0)

    path = str(args[1])
    if not isExist(path):
        print "the file path do not exist."
        exit(0)

    # show_tree("./")
    show_tree(path)