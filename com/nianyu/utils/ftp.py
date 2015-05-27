# coding=utf-8
__author__ = 'lixiaojian'

import paramiko
import os

class SSH(object):
    """
    1、执行命令
    2、拷贝文件
    """
    _client = None  #ssh客户端
    _sftp = None  #sftp
    _TIMEOUT = 5  #连接超时时间

    def __init__(self,ssh_conf):

        try:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(
                            ssh_conf['host'],
                            ssh_conf['port'],
                            ssh_conf['user'],
                            ssh_conf['passwd'],
                            timeout=self._TIMEOUT)
        except Exception,e:
            print "get client failed: ",e

        try:
            ssh = paramiko.Transport((ssh_conf['host'],
                            ssh_conf['port'],))

            ssh.connect(username=ssh_conf['user'],password=ssh_conf['passwd'])
            self._sftp = paramiko.SFTPClient.from_transport(ssh)

        except Exception,e:
            print "get sftp failed: ",e


    def excCmd(self,cmd):
        """
        执行命令
        """
        stdin, stdout, stderr = self._client.exec_command(cmd)
        print stdout.read()


    def scpFile(self,local_file,remote_dir):
        """
        上传文件到指定目录
        """
        remote_file = os.path.join(remote_dir,os.path.split(local_file)[1])
        try:
            self._sftp.put(local_file,remote_file)
            print 'upload %s' % remote_file
        except Exception,e:
            print 'upload failed : ',e


    def scpDir(self,local_dir,remote_dir):
        """
        拷贝目录下的文件到指定目录下
        """

        for parent,dirs,files in os.walk(local_dir):

            for file in files:

                local_file = os.path.join(parent,file)
                path = local_file.replace(local_dir,remote_dir)

                remote_file = os.path.join(remote_dir,path)
                try:
                    self._sftp.put(local_file,remote_file)
                    print 'upload %s' % remote_file
                except Exception,e:
                    self._sftp.mkdir(os.path.split(remote_file)[0])
                    self._sftp.put(local_file,remote_file)
                    print 'upload %s' % remote_file

            for dir in dirs:
                local_path = os.path.join(parent,dir)
                path = local_path.replace(local_dir,remote_dir)
                remote_path = os.path.join(remote_dir,path)
                try:
                    cmd = 'mkdir %s' % remote_path.replace("//","/")
                    self._client.exec_command(cmd)
                    print cmd
                except Exception,e:
                    print '%s failed: ' % cmd


    def close(self):
        """
        关闭客户端 和 sftp
        """
        self._sftp.close()
        self._client.close()

if __name__=='__main__':

    ssh_conf = {
        'host':'192.168.1.152',
        'user':'root',
        'passwd':'guai',
        'port':22,
    }

    ssh = SSH(ssh_conf)
    # ssh.excCmd('ls -lh')
    # ssh.scpDir('/Users/lixiaojian/Code/python/demo/com/','/home/nianyuguai/Music/')
    ssh.scpFile('/Users/lixiaojian/Code/python/demo/com/__init__.py','/home/nianyuguai/')
    ssh.close()