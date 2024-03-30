import paramiko
from io import StringIO


class Parmiko_Module(object):

    def run_cmd(self, private_key, ip, server_user, linux_cmd):
        # 不要用域名，用ip地址，如果要用域名需要本地的host里配置域名地址
        private_key = paramiko.RSAKey(file_obj=StringIO(private_key))  # 读取秘钥
        # private_key = paramiko.RSAKey.from_private_key_file('./id_rsa')  # 同sshclient一样。这是私钥文件
        trans_obj = paramiko.Transport((ip, 22))
        trans_obj.connect(username=server_user, pkey=private_key)

        ssh = paramiko.SSHClient()
        ssh._transport = trans_obj

        stdin, stdout, stderr = ssh.exec_command(linux_cmd)
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        # 关闭连接
        ssh.close()

    def ssh_download_file(self, action_type, private_key, ip, server_user, remote_path, local_path):
        # 通过秘钥登录下载文件
        """
        :param private_key:  私钥
        :return:
        """
        # 不要用域名，用ip地址，如果要用域名需要本地的host里配置域名地址
        private_key = paramiko.RSAKey(file_obj=StringIO(private_key))  # 读取秘钥
        # private_key = paramiko.RSAKey.from_private_key_file('./id_rsa')  # 同sshclient一样。这是私钥文件
        trans_obj = paramiko.Transport((ip, 22))
        trans_obj.connect(username=server_user, pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(trans_obj)
        # 将location.py 上传至服务器 /tmp/test.py
        # # 下载文件到本地; remote_path ,local_path为路径加文件名
        if action_type == "get":
            sftp.get(remote_path, local_path)
        else:
            sftp.put(local_path, remote_path)

        trans_obj.close()


if __name__ == '__main__':
    pass
    # remote_path="/home/webapp/evofile/wop/WOP_Auto_JCoinPay_01/out/20200907/MOP_Auto_GrabPay_01/WOP_Auto_JCoinPay_01-Settlement-Details-MOP_Auto_GrabPay_01-20200907-001.csv"
    # local_path="./WOP_Auto_JCoinPay_01-Settlement-Details-MOP_Auto_GrabPay_01-20200907-001.csv"
    #
    # tyo_test_wop_key = """-----BEGIN RSA PRIVATE KEY-----
    #     MIIEpAIBAAKCAQEA1dnsLbIC9UNKajiL36FrBxsvJB78+QYRkfKyZo1ZfpswIZ1j
    #     E2uqCEz4C51EgBdtsRtzUsUUQFfTszQWX8dz7A16cxXHb/JHnDfhRBvL9s8lg/Pl
    #     GdmT3LVbsBO+4I3h2V0B7K6LZIxKC6YDfwFG+GBviBPHSwiHGZjOwjqtbtvu1/xX
    #     F9UAijK1bH15vlcm1F9GTKmkZCl/YTqJoqu9F05kLvDQ7/7WFMSPwVK4fciPrL4U
    #     33PGaa94oHEMlT68YSUFcjIw3eDpUVnT+sIVwq7JJL/Fgb6IaViIzp/0AVr2Gv+m
    #     wNzY25E4BWxlvHLIiuhGjoiu4O89jrwAQH07JwIDAQABAoIBAC0kJTC4JNu06p5l
    #     dVEtd7Q2TssnJ2tBlq/iNTpkmAGbrJtL58APuAKsjKeW+QC48VSzYLKWG2JBp9Rq
    #     KFbreVLYvYJRlJnS4L7fJNQFshZVP6wM7c15Gjc6qTIP2Pj5ujTx5xgY+B+vZWn0
    #     D0Td9icz5BcrZaQ3Fp2Wnf5t+HIv46YmjkD9oCNsKpf+rFg73Tw5ruGxb36bAKRT
    #     kpkvplOtGAkcp0FUqfeqnQ0sWcBY+OLPtY/OsCSWdaqugQ21Hlay5aOG3ELjhwez
    #     Q3CT27Jn0Hg3x+KpGk6GujaSWTvaXWY7VrS6DeWthA6HFUZIOJPnRiCZYLOQHsq+
    #     FYBdWwECgYEA/qz2+I+WkyoA8zLimU5sLjS7/ka1JIo4Tkk0W1PxGlFUOKbFkK9+
    #     hPhPa59UgIXCJJkvn/83WWGbTsn9nS3mLhnSkJ/P31YLvkUcKfsOP/jeBxhPQOoO
    #     8AmyTjohq25LQSaLm0YdxzlQXGkY7Z0mUA4wyH7Wb2l8RGTE+aSvImcCgYEA1vac
    #     U59gpA66qMvFp3+kstIQ2Sbs4+0kKzi8vEPOcgGcihbeJtz7bQw8gI0mGTzG2UwF
    #     6zTpMNRKTgM67ObOW8zLla3YfwVWoa4U0hV6PfekqZ8IVQayzBV2LQKgHU5ERnfc
    #     85tNI8YXFANz21vIZvEnX7caVW7r6pDf0NyFKUECgYEAryQoHDwzIzXJvXaLGz8x
    #     an1do7rgrCZaHox9cylBMAYqU2NtjtkBu1RA2hSSumhCYYTvmaqcV92mPwLuZP/B
    #     woaDpm4hOMgl/03r1nsPC7OMjXiMWGoep7kjZGTZ7tlE66Mkcz4/EFk8CLFGMXLX
    #     fEqmBdwkgC4dBbP/OmelAZUCgYBffqqv02uhNhHiDrQ91syZzAxEC7DNCHo64Ten
    #     AxBhQSoDhmkmJqFjLj5qdUnpiEBmJAm1FYpKcOSZh4HT4CzoRzBhzBsTQpHbvXPu
    #     aDAn+y2hVM7kxtcDJr2a/UGYAz79dx4m8mTwcX2rHGWJm1qJsLPnJ3aBYYdYawei
    #     x3Q4gQKBgQCyilLQM3NVBx+C2QHv7EUOOY3FBxII13QjXe6EShOpFdonrr6t5iDC
    #     /i3zKqrenC3n/ag4V3HiY8OzaW2DMrCt1V/bsKhrZyom8qOenJEKt4sDZG9p6lfu
    #     WgdRHIpdH7aFNHQ4tffdXtJv0ST6SsjonCesY+yZumEAC1YyPMNcFg==
    #     -----END RSA PRIVATE KEY-----"""
    #
    #
    # # action_type, private_key, ip, server_user, remote_path, local_path
    # pa=Parmiko_Module()
    # pa.ssh_download_file("get",tyo_test_wop_key,"jp3evonet-Testing","webapp",remote_path,local_path)
