# coding=utf-8
__author__ = 'lixiaojian'

import os

abspath = os.path.dirname(os.path.abspath(__file__))

print abspath


#生成zip包到制定路径
path = '/Users/lixiaojian/Code/python/demo/'
#生成文件

with open(path + 'test.txt','w+') as f:
    f.write("hahah")




#往文件写内容


