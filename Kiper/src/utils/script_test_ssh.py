import os


def download_log(file_name='*.*', psswd='KhompS057989Y2015B20R00T02RootPassword'):
    try:
        cmd = 'sshpass -p ' + psswd + ' scp -oStrictHostKeyChecking=no  -oKexAlgorithms=+diffie-hellman-group1-sha1  -P 4022 root@10.15.15.101:/var/log/khomp/' + file_name + ' ' + os.getcwd()
        print(cmd)
        return os.system(cmd)
        # os.system('tar -cvf kiperlog.tar /home/benhur/kiperlog')
    except OSError:
        os.system('rm /root/.ssh/known_hosts')
        cmd = 'sshpass -p ' + psswd + ' scp -oStrictHostKeyChecking=no  -oKexAlgorithms=+diffie-hellman-group1-sha1  -P 4022 root@10.15.15.101:/var/log/khomp/' + file_name + ' ' + os.getcwd()
        print(cmd)
        return os.system(cmd)


if __name__ == '__main__':
    download_log('*.*')
