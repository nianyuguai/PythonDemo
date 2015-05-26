# coding=utf-8
__author__ = 'lixiaojian'

import paramiko
import os

class SSH:
    """
    1、执行命令
    2、拷贝文件
    """
    _client = None
    _sftp = None
    _TIMEOUT = 5

    def __init__(self,ssh_config):

        try:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(ssh_config['host'],
                            ssh_config['port'],
                            ssh_config['user'],
                            ssh_config['passwd'],
                            timeout=self._TIMEOUT)
        except Exception,e:
            print "get client failed: ",e

        try:
            ssh = paramiko.Transport((ssh_config['host'],
                            ssh_config['port'],))

            ssh.connect(username=ssh_config['user'],password=ssh_config['passwd'])
            self._sftp = paramiko.SFTPClient.from_transport(ssh)

        except Exception,e:
            print "get sftp failed: ",e


    def exc_cmd(self,cmd):
        stdin, stdout, stderr = self._client.exec_command(cmd)
        print stdout.read()


    def scp_file(self,file,local_dir,remote_dir):

        self._sftp


    def scp_dir(self,local_dir,remote_dir):
        """
        how to use:
            ssh = SSH(ssh_config)
            ssh.scp_dir('/home/niayu','/home/nianyuguai/')
        """
        for parent,dirs,files in os.walk(local_dir):

            for file in files:
                local_file = os.path.join(parent,file)

                path = local_file.replace(local_dir,'')
                remote_file = os.path.join(remote_dir,path)

                try:
                    self._sftp.put(local_file,remote_file)
                except Exception,e:
                    p = os.path.split(remote_file)[0]
                    self._sftp.mkdir(p)
                    self._sftp.put(local_file,remote_file)

                for dir in dirs:
                    local_path = os.path.join(parent,dir)
                    print local_path
                    path = local_path.replace(local_dir,'')
                    print path
                    remote_path = os.path.join(remote_dir,path)
                    print remote_path
                    try:
                        self._sftp.mkdir(remote_path)
                        print "mkdir path %s" % remote_path
                    except Exception,e:
                        print 'mkdir failed: ',e

def get_client(ip,port,username,passwd):
    """
    return :
        ssh client
    how to use:
        client = get_client(ip,22,username,passwd)
        client.exec_command('ls -alh')
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip,port,username,passwd,timeout=5)
        return client
    except :
        print '[Error] : %s ssh connect Error\n'%(ip)


def get_sftp(ip,port,username,passwd):
    """
    return :
        sftp object
    how to use:
        sftp = sftp(ip,22,username,passwd)
        sftp.put(localdir,remotedir)
    """

    try:
        ssh = paramiko.Transport((ip,port))
        ssh.connect(username=username,password=passwd)
        sftp = paramiko.SFTPClient.from_transport(ssh)

        return sftp
    except:
        print '[Error] : %s sftp connect Error\n'%(ip)


def ssh_cmd(client,cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout.readlines():

        print line

def scp_dir(ip,port,username,passwd,local_dir,remote_dir):
    """
    how to use:
        scp_dir(ip,22,username,passwd,'/home/niayu','/home/nianyuguai/')
    """
    sftp = get_sftp(ip,port,username,passwd)
    client = get_client(ip,port,username,passwd)

    for parent,dirs,files in os.walk(local_dir):
        for dir in dirs:
            rdir = os.path.join(parent,dir).replace("\\","/")
            cmd = 'mkdir %s/%s' %(remote_dir,rdir)
            print cmd
            client.exec_command(cmd)

        for file in files:
            local_file = os.path.join(parent,file)
            remote_file = remote_dir + '/' + file
            print 'scp %s %s' % (local_file,remote_file)
            sftp.put(local_file,remote_file)
    sftp.close()
    client.close()



if __name__=='__main__':
    # cmd = ['echo hello','ls -al']
    # username = 'root'
    # passwd = 'guai'
    # ip = '192.168.1.152'
    # sftp = get_sftp(ip,22,username,passwd)
    # sftp.put('/Users/lixiaojian/Code/python/demo/com/nianyu/utils/ftp.py','/home/nianyuguai/sftp.py')
    # scp_dir(ip,22,username,passwd,'/Users/lixiaojian/Code/python/demo/com/nianyu/utils/','/home/nianyuguai/Music')


    # client = get_client(ip,22,username,passwd)
    # ssh_cmd(client,'ls -lh')
    # client.close()

    ssh_config = {
        'host':'192.168.1.152',
        'user':'root',
        'passwd':'guai',
        'port':22,
    }

    ssh = SSH(ssh_config)
    # ssh.exc_cmd('ls -lh')

    ssh.scp_dir('/Users/lixiaojian/Code/python/demo/com','/home/nianyuguai/Music/')