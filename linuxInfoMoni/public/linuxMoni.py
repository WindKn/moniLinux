import paramiko, os,csv
from linuxInfoMoni import models

class moniLinuxServer():
    def startTrace(self,serverID='',type='all'):
        if type=='all':
            getServerList = models.serverInfo.objects.exclude(isTraced="Y")
        elif type=='one':
            getServerList=models.serverInfo.objects.exclude(isTraced="Y").filter(id=serverID)
        try:
            for i in getServerList:
                uname, pwd, ip, cmdPath = i.uname, i.pwd, i.ip, i.resultPath
                cmdList1 = 'rm ' + cmdPath + '/linuxInfo.csv'
                cmdList2='nohup dstat -t -a -m --out '+ cmdPath + "/linuxInfo.csv & "
                # cmdList2 = "nohup dstat -t -c -d -n -N em1 -g -y -m  --out " + cmdPath + "/linuxInfo.csv & "
                cmdList = cmdList1 + ';' + cmdList2
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip, port=22, username=uname, password=pwd)
                stdin, stdout, stderr = ssh.exec_command(cmdList)
                models.serverInfo.objects.filter(id=i.id).update(isTraced='Y')
        except Exception as e:
            print(e)

    def stopTrace(self,serverID='',type='all'):
        if type=='all':
            getServerList = models.serverInfo.objects.filter(isTraced="Y")
        elif type=='one':
            getServerList=models.serverInfo.objects.filter(isTraced="Y",id=serverID)
        try:
            for i in getServerList:
                uname, pwd, ip, cmdPath = i.uname, i.pwd, i.ip, i.resultPath
                cmdList1 = " ps -ef|grep dstat|grep linuxInfo|grep -v grep|awk '{print \"kill \" $2}'|sh "
                cmdList2="ps -ef|grep \"sshd: "+i.uname+"\"|grep -v grep|awk '{print \"kill \" $2}'|sh "
                cmdList=cmdList1+';'+cmdList2
                print(cmdList)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip, port=22, username=uname, password=pwd)
                ssh.exec_command(cmdList)
                ssh.close()
                models.serverInfo.objects.filter(id=i.id).update(isTraced='N')
        except Exception as e:
            print(e)


class getMoniResult():
    def __init__(self):
        self.path=os.path.dirname(__file__)+ '/shellSrc/linuxInfo.csv'

    def callback(self,current, total):
        print("file size is ：{}，already download：{}".format(total, current))

    def getMoniFile(self,serverID):
        getServInfo=models.serverInfo.objects.filter(id=serverID)
        try:
            for i in getServInfo:
                uname, pwd, ip, cmdPath = i.uname, i.pwd, i.ip, i.resultPath
                fromPath=cmdPath+'/linuxInfo.csv'
                toPath=self.path
                client  = paramiko.SSHClient()
                client .set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client .connect(hostname=ip, port=22, username=uname, password=pwd)
                sftp_client = paramiko.SFTPClient.from_transport(client .get_transport())
                sftp_client.get(fromPath, toPath, callback=self.callback)
                sftp_client.close()
                client.close()
        except Exception as e:
            print(e)

    def handleMonifFile(self):
        # infopath = self.path + 'linuxInfo.csv'
        csv_file = csv.reader(open(self.path, 'r'))
        timeList = []
        usr_cpu = []
        sys_cpu = []
        total_cpu = []
        recvList = []
        sendList = []
        total_dk = []
        mem_used = []
        mem_free = []
        mem_cache = []
        for i, info in enumerate(csv_file):
            if i > 6:
                timeList.append(info[0][6:])
                usr_cpu.append(info[1])
                sys_cpu.append(info[2])
                total = 100 - float(info[3])
                total_cpu.append(total)
                recvDK = (float(info[9])) / (128 * 1024)
                recvDK = str(int(recvDK))
                recvList.append(recvDK)
                sendDK = (float(info[10])) / (128 * 1024)
                sendDK = str(int(sendDK))
                sendList.append(sendDK)
                totalDk = int(recvDK) + int(sendDK)
                total_dk.append(totalDk)
                toGB = 1024 * 1024#这个算出来为MB
                usedvalue = int(info[15][:-2])
                mem_used_G = round(usedvalue / toGB, 2)#后续修改为MB，变量命名就没改了
                mem_used.append(mem_used_G)
                freeValue = int(info[18][:-2])
                mem_free_G = round(freeValue / toGB, 2)
                mem_free.append(mem_free_G)
                cacheValue = int(info[17][:-2])
                mem_cache_G = round(cacheValue / toGB, 2)
                mem_cache.append(mem_cache_G)
        return timeList, usr_cpu, sys_cpu, total_cpu, recvList, sendList, total_dk, mem_used, mem_free, mem_cache



