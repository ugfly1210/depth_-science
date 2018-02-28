from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import serializers
from skj import models
# Create your views here.

class LoginViews(views.APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def post(self, request, *args, **kwargs):
        # 接收到的用户名和密码
        username, password = request.data.get('username'),request.data.get('password')
        user_obj = models.Account.objects.filter(username=username,password=password).first()
        if user_obj:
            ret = {
                'code':1000,
                'username': username,
                'token': user_obj.token
            }
        else:
            ret = {
                'code': 403,
                'msg': '用户名或者密码错误！！！'
            }
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        return response


# 关于文章的序列化
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'
        depth = 2

class NewsViews(views.APIView):
    def get(self, request, *args, **kwargs):
        # print(request)
        news_list = models.Article.objects.all()
        n_obj = news_list.first()
        ser = NewsSerializer(instance=news_list, many=True, context={'request':request})
        response = Response(ser.data)
        response['Access-Control-Allow-Origin'] = '*'
        return response



from rest_framework.request import Request
