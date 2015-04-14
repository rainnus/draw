# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from draw.models import student, numList, adminUser
from django.core.context_processors import csrf
from django.http import HttpResponse,HttpResponseRedirect
from StringIO import StringIO
import random
import xlwt

# Create your views here.

def drawView(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("base.html", c)



def drawView2(request, message):
    c = {}
    c.update(csrf(request))
    return render_to_response("base.html", dict({"message": message}, **c))


def searchView(request):
    if 'IDCard' in request.POST:
        message = request.POST['IDCard']
        try:
            Users = student.objects.all()
            stuNum = numList.objects.all()
            Count = numList.objects.count()
        except StandardError:
            return drawView2(request, "身份证号输入不正确或不存在")

        try:
            user = student.objects.get(IDCard=message)
        except student.DoesNotExist:
            return drawView2(request, "身份证号输入不正确或不存在")

        if user.ifDraw == 1:
            return render_to_response("success.html", {"number": user.stuNum, "message": "您已抽取过号码"})

        else:
            num = random.randint(1, Count)
            try:
                numTemp = stuNum[num - 1].stuNumber
            except IndexError:
                return render_to_response("false.html")

            user.stuNum = numTemp
            user.ifDraw = 1
            numList.objects.get(stuNumber=numTemp).delete()
            user.save()
            print numTemp
            return render_to_response("success.html", {"number": numTemp, "message": "成功抽取号码！"})

    else:
        return render_to_response("false.html")


def restart(request):
    if request.user.is_authenticated():
        numList.objects.all().delete()
        count = student.objects.count()
        for i in range(1, count + 1):
            num = numList(stuNumber=i)
            num.save()
        student.objects.all().update(stuNum=0)
        student.objects.all().update(ifDraw=0)
        return render_to_response("success.html")
    else:
        return loginView(request)


def restartView(request):
    if request.user.is_authenticated():
        return render_to_response("restart.html",{"adminName":request.user})
    else:
        return loginView(request)


def loginView(request):
    if request.user.is_authenticated():
        return adminView(request)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response("login.html", c)


def loginView2(request, message):
    c = {}
    c.update(csrf(request))
    return render_to_response("login.html", dict({"message": message}, **c))


def logoutView(request):
    if request.user.is_authenticated():
        logout(request)
        return loginView(request)
    else:
        return loginView(request)

def adminView(request, message=''):
    if request.user.is_authenticated():
        try:
            Users = student.objects.all()
            Count = student.objects.count()
            CountYes = student.objects.filter(ifDraw=1)
        except StandardError:
            return render_to_response("false.html")
        if Count == 0:
            process = 0
        else:
            process = len(CountYes) * 100 / Count
        c = {}
        c.update(csrf(request))
        return render_to_response("admin.html",
                                  dict({"Users": Users, "process": process, "yes": len(CountYes), "totle": Count,
                                   "adminName": request.user,"message":message},**c))
    else:
        return loginView(request)


def validate(request):
    if "UserName" in request.POST and "UserPWD" in request.POST:
        user = authenticate(username=request.POST['UserName'], password=request.POST['UserPWD'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/adminView/')
            else:
                return loginView2(request, "用户名或密码不正确")
        else:
            return loginView2(request, "用户名或密码不正确")
    else:
        return loginView2(request, "用户名或密码不正确")


def exportView(request):
    if request.user.is_authenticated():
        return render_to_response("export.html",{"adminName":request.user})
    else:
        return loginView(request)

def export(request):
    if request.user.is_authenticated():

        def stream():
            xls = xlwt.Workbook(encoding='utf-8')
            sheet = xls.add_sheet("Sheet1")
            temp_file = StringIO()
            stu = student.objects.all()
            sheet.write(0,0,"姓名")
            sheet.write(0,1,"身份证号")
            sheet.write(0,2,"抽取号码")
            for i in range(1,31):
                sheet.write(i,0,stu[i-1].stuName)
                sheet.write(i,1,stu[i-1].IDCard)
                sheet.write(i,2,stu[i-1].stuNum)
            xls.save(temp_file)
            return temp_file.getvalue()

        response = HttpResponse(stream(),mimetype="application/octet-straem")
        response['Content-Disposition'] = 'attachment;filename=%s' % "list.xls"
        return response
        # return render_to_response("export.html")
    else:
        return loginView(request)

# def importView(request):
#     if request.user.is_authenticated():
#         return render_to_response("import.html")
#     else:
#         return loginView(request)

def myimport(request):
    if request.user.is_authenticated():
        return render_to_response("import.html")
    else:
        return loginView(request)

def addUser(request):
    if request.user.is_authenticated:
        if "name" in request.POST and "card" in request.POST:
            name = request.POST.get('name',False)
            card = request.POST.get('card',False)
            if name == '' or card == '':
                return HttpResponseRedirect('/adminView/添加失败')
            else:
                count = student.objects.count()
                if count < 30:
                    try:
                        stu = student(stuName=name,IDCard=card,ifDraw=0,stuNum=0)
                        stu.save()
                        num = numList(stuNumber=count+1)
                        num.save()
                    except StandardError:
                        return HttpResponseRedirect('/adminView/添加失败')
                    str = "success"
                    return HttpResponseRedirect('/adminView/添加成功')
                else:
                    return HttpResponseRedirect('/adminView/人数已达到30人')
        else:
            return HttpResponseRedirect('/adminView/添加失败')
    else:
        return loginView(request)



#===========================================
def searchViewTest(request):
    if 'IDCard' in request.GET:
        message = request.GET['IDCard']
        try:
            Users = student.objects.all()
            stuNum = numList.objects.all()
            Count = numList.objects.count()
        except StandardError:
            return drawView2(request, "身份证号输入不正确或不存在")

        try:
            user = student.objects.get(IDCard=message)
        except student.DoesNotExist:
            return drawView2(request, "身份证号输入不正确或不存在")

        if user.ifDraw == 1:
            return render_to_response("success.html", {"number": user.stuNum, "message": "您已抽取过号码"})

        else:
            num = random.randint(1, Count)
            try:
                numTemp = stuNum[num - 1].stuNumber
            except IndexError:
                return render_to_response("false.html")

            user.stuNum = numTemp
            user.ifDraw = 1
            numList.objects.get(stuNumber=numTemp).delete()
            user.save()
            print numTemp
            return render_to_response("success.html", {"number": numTemp, "message": "成功抽取号码！"})

    else:
        return render_to_response("false.html")

def test(request):
    stu = student.objects.all()
    return render_to_response("test.html",{"stu":stu})

def drawViewTest(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("TestDraw.html", c)