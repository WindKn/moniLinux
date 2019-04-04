from django.shortcuts import render,HttpResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from linuxInfoMoni import models
import json,time
from datetime import datetime
from .public.linuxMoni import moniLinuxServer,getMoniResult
# Create your views here.

class linuxInfo(View):
    def get(self, request):
        serverInfo=models.serverInfo.objects.all()
        paginator = Paginator(serverInfo,5)
        page = request.GET.get('page')
        serverList = paginator.get_page(page)
        return render(request, 'linuxInfo.html',{'serverList': serverList})
    def post(self, request):
        ret = {'status': True, 'data': None}
        operaType=request.POST.get('type')
        if operaType=='edit':
            serverName=request.POST.get('serverName')
            ip = request.POST.get('ip')
            port = request.POST.get('port')
            uname = request.POST.get('uname')
            pwd = request.POST.get('pwd')
            Path = request.POST.get('Path')
            serverName = request.POST.get('serverName')
            type = request.POST.get('type')
            serverID = request.POST.get('serverID')
            updateDict={
                'serverName':serverName,
                'ip':ip,
                'port':port,
                'uname':uname,
                'pwd':pwd,
                'resultPath':Path
            }
            try:
                models.serverInfo.objects.filter(id=serverID).update(**updateDict)
            except Exception as e:
                ret['status']=False
                ret['data']=str(e)
        elif operaType=='del':
            serverID = request.POST.get('serverID')
            serverID=int(serverID)
            try:
                models.serverInfo.objects.filter(id=serverID).delete()
            except Exception as e:
                ret['status']=False
                ret['data']=str(e)
        elif operaType=='add':
            serverName = request.POST.get('serverName')
            ip = request.POST.get('ip')
            port = request.POST.get('port')
            uname = request.POST.get('uname')
            pwd = request.POST.get('pwd')
            Path = request.POST.get('Path')
            serverName = request.POST.get('serverName')
            type = request.POST.get('type')
            serverID = request.POST.get('serverID')
            addDict = {
                'serverName': serverName,
                'ip': ip,
                'port': port,
                'uname': uname,
                'pwd': pwd,
                'resultPath': Path
            }
            try:
                models.serverInfo.objects.create(**addDict)
            except Exception as e:
                ret['status'] = False
                ret['data'] = str(e)
        print(ret)
        return HttpResponse(json.dumps(ret))

class linuxMoni(View):
    def get(self,request):
        serverList=models.serverInfo.objects.all()
        getTracedServer = models.serverInfo.objects.filter(isTraced="Y")
        getTraceServeF=models.serverInfo.objects.first()
        recordList = models.trace_info.objects.filter(server_id=getTraceServeF.id)
        return render(request,'linuxMoni.html',{'serverList':serverList,'tracedServer':getTracedServer,'recordList':recordList})
    def post(self,request):
        moniType=request.POST.get('type')
        server=request.POST.get('server')
        if moniType=='start':
            if server=='all':
                moniLinuxServer().startTrace()
            else:
                moniLinuxServer().startTrace(serverID=server,type='one')
        if moniType=='stop':
            if server == 'all':
                moniLinuxServer().stopTrace()
            else:
                moniLinuxServer().stopTrace(serverID=server, type='one')
        getTracedServer = models.serverInfo.objects.filter(isTraced="Y")
        tracedServer=[]
        for i in getTracedServer:
            tracedServer.append(i.serverName)
        ret={'tracedServer':tracedServer}
        return HttpResponse(json.dumps(ret))

class linuxMoniO(View):
    def post(self,request):
        serverID=request.POST.get('serverID')
        recordList = models.trace_info.objects.filter(server_id=serverID)
        valueID=[]
        value=[]
        for i in recordList:
            valueID.append(i.id)
            value.append(i.trace_name)
        ret={
            'valueID':valueID,
            'value':value
        }
        return HttpResponse(json.dumps(ret))



class showMoni(View):
    def getLinuxTraceFile(self,serverID):
        getMoniResult().getMoniFile(serverID)
        timeList, usr_cpu, sys_cpu, total_cpu, recvList, sendList, total_dk, mem_used, mem_free, mem_cache = getMoniResult().handleMonifFile()
        return timeList, usr_cpu, sys_cpu, total_cpu, recvList, sendList, total_dk, mem_used, mem_free, mem_cache
    def post(self,request):
        ret = {'status': True}
        type=request.POST.get('type')
        serverID=request.POST.get('serverID')
        timeList, usr_cpu, sys_cpu, total_cpu, recvList, sendList, total_dk, mem_used, mem_free, mem_cache = self.getLinuxTraceFile(serverID)
        if type=='show':
            ret = {'timeList': timeList,
                   'usr_cpu': usr_cpu,
                   'sys_cpu': sys_cpu,
                   'total_cpu': total_cpu,
                   'recvList': recvList,
                   'sendList': sendList,
                   'total_dk': total_dk,
                   'mem_used': mem_used,
                   'mem_free': mem_free,
                   'mem_cache': mem_cache
                   }
        elif type=='save':
            traceName=request.POST.get('saveName')
            # serverID=request.POST.get('serverID')
            # timeList, usr_cpu, sys_cpu, total_cpu, recvList, sendList, total_dk, mem_used, mem_free, mem_cache =  self.getLinuxTraceFile(serverID)
            try:
                today=time.strftime('%Y-%m-%d')
                serverIns=models.serverInfo.objects.get(id=serverID)
                traceInfo=models.trace_info(trace_name=traceName,server_id=serverIns,data=today)
                traceInfo.save()
                getSaveTraceID=traceInfo.id
                insertDataList=[]
                for index,value in enumerate(timeList):
                    insertDataList.append(models.trace_detail(
                    time=value,
                    usr_cpu=usr_cpu[index],
                    sys_cpu = sys_cpu[index],
                    total_cpu = total_cpu[index],
                    recvList = recvList[index],
                    sendList = sendList[index],
                    total_dk = total_dk[index],
                    mem_used = mem_used[index],
                    mem_free = mem_free[index],
                    mem_cache = mem_cache[index],
                    trace_id = traceInfo,
                    ))
                models.trace_detail.objects.bulk_create(insertDataList)
            except Exception as e:
                print(e)
        return HttpResponse(json.dumps(ret))

class showMoniO(View):
    def getTraceInfo(self,traceID,method='all',stime='',etime=''):
        timeList=[]
        usr_cpu=[]
        sys_cpu=[]
        total_cpu=[]
        recvList=[]
        sendList=[]
        total_dk=[]
        mem_used=[]
        mem_free=[]
        mem_cache=[]
        if method=='all':
            traceInfo=models.trace_detail.objects.filter(trace_id=traceID)
        elif method=='filter':
            traceInfo = models.trace_detail.objects.filter(trace_id=traceID,time__gte=stime,time__lte=etime)
        for i in traceInfo:
            timeList.append(i.time)
            usr_cpu.append(i.usr_cpu)
            sys_cpu.append(i.sys_cpu)
            total_cpu.append(i.total_cpu)
            recvList.append(i.recvList)
            sendList.append(i.sendList)
            total_dk.append(i.total_dk)
            mem_used.append(i.mem_used)
            mem_free.append(i.mem_free)
            mem_cache.append(i.mem_cache)
        return timeList, usr_cpu, sys_cpu, total_cpu, recvList, sendList, total_dk, mem_used, mem_free, mem_cache
    def post(self, request):
        ret={'status':True}
        type=request.POST.get('type')
        if type == 'delHis':
            traceID = request.POST.get('traceID')
            models.trace_info.objects.filter(id=traceID).delete()
        elif type=='showHis':
            traceID = request.POST.get('traceID')
            # timeListNew, usr_cpuNew, sys_cpuNew, total_cpuNew, recvListNew, sendListNew, total_dkNew, mem_usedNew, mem_freeNew, mem_cacheNew=[],[],[],[],[],[],[],[],[],[]
            timeListNew, usr_cpuNew, sys_cpuNew, total_cpuNew, recvListNew, sendListNew, total_dkNew, mem_usedNew, mem_freeNew, mem_cacheNew=self.getTraceInfo(traceID)
            ret = {'timeList': timeListNew,
                   'usr_cpu': usr_cpuNew,
                   'sys_cpu': sys_cpuNew,
                   'total_cpu': total_cpuNew,
                   'recvList': recvListNew,
                   'sendList': sendListNew,
                   'total_dk': total_dkNew,
                   'mem_used': mem_usedNew,
                   'mem_free': mem_freeNew,
                   'mem_cache': mem_cacheNew,
                   }
        elif type=='filterShow':
            stime=request.POST.get('stime')
            etime=request.POST.get('etime')
            traceID=request.POST.get('traceID')
            timeListNew, usr_cpuNew, sys_cpuNew, total_cpuNew, recvListNew, sendListNew, total_dkNew, mem_usedNew, mem_freeNew, mem_cacheNew = self.getTraceInfo(
                traceID,'filter',stime,etime)
            ret = {'timeList': timeListNew,
                   'usr_cpu': usr_cpuNew,
                   'sys_cpu': sys_cpuNew,
                   'total_cpu': total_cpuNew,
                   'recvList': recvListNew,
                   'sendList': sendListNew,
                   'total_dk': total_dkNew,
                   'mem_used': mem_usedNew,
                   'mem_free': mem_freeNew,
                   'mem_cache': mem_cacheNew,
                   }
        elif type=='timeInterval':
            ret = {'dtime': 0, 'result': True}
            try:
                stime = request.POST.get('stime').strip()
                stime = datetime.strptime(stime, "%H:%M:%S")
                etime = request.POST.get('etime').strip()
                etime = datetime.strptime(etime, "%H:%M:%S")
                dtime = (etime - stime).seconds
                ret['dtime'] = dtime
            except Exception as e:
                print(e)
        return HttpResponse(json.dumps(ret))




