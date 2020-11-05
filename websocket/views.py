import shlex
import subprocess
import sys

from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko


# def exec_command(comm):
#     hostname = '192.168.0.162'
#     username = 'root'
#     password = 'root'
#
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname=hostname, username=username, password=password)
#     stdin, stdout, stderr = ssh.exec_command(comm,get_pty=True)
#     result = stdout.read()
#     ssh.close()
#     yield result
requestG =None
def send(param):
    requestG.websocket.send(param)


def cmd(command):
    subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    subp.wait(2)
    if subp.poll() == 0:
        return subp.communicate()[1]
    else:
        return "失败"

@accept_websocket
def echo_once(request):

    global requestG
    requestG = request
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            print(message)
            if message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                # while True:
                #     request.websocket.send("hello")
                # subp.wait(2)
                # cmd = ""

                # shell_cmd = 'python3 subprogram.py'
                shell_cmd = 'ping www.baidu.com'
                cmd = shlex.split(shell_cmd)
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
                while p.poll() is None:
                    line = p.stdout.readline()
                    line = line.strip()
                    if line:
                        print('Subprogram output: [{}]'.format(line))
                        request.websocket.send('Subprogram output: [{}]'.format(line))
                if p.returncode == 0:
                    print('Subprogram success')
                    request.websocket.send('Subprogram success')
                else:
                    print('Subprogram failed')
                    request.websocket.send('Subprogram failed')


                #
                # result = subprocess.Popen(cmd, stdout=subprocess.PIPE)  # 将输出内容存至缓存中
                #
                # while True:  # 将内容持续输出
                #     request.websocket.send(result.stdout.readline().decode("gbk").strip() + "\n")

            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))

