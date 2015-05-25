# coding=utf-8
__author__ = 'lixiaojian'

import paramiko
import os

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
    cmd = ['echo hello','ls -al']
    username = 'root'
    passwd = 'guai'
    ip = '192.168.1.152'
    # sftp = get_sftp(ip,22,username,passwd)
    # sftp.put('/Users/lixiaojian/Code/python/demo/com/nianyu/utils/ftp.py','/home/nianyuguai/sftp.py')
    scp_dir(ip,22,username,passwd,'/Users/lixiaojian/Code/python/demo/com/nianyu/utils/','/home/nianyuguai/Music')



