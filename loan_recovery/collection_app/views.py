from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegiterForm,BlogForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Students,Article,Blog
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import connection,transaction
import requests
from .utils import render_to_pdf
from django.views.generic import View


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from textwrap import wrap
from reportlab.platypus import Paragraph

import csv

#user management
from django.contrib.auth.models import User


#from cx_Oracle import

# Create your views here.
#Generic API start

class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



    def get(self,request,id= None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self,request,id):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)






#generic API end.




#class based API

class ArticleAPIView(APIView):

    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=ArticleSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get_object(self,id):
        try:
            return Article.objects.get(id=id)

        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #end class base api

def HomeView(request):
    return render(request, 'home.html')

def register(request):
    if request.method=='POST':
        #form = UserCreationForm(request.POST)
        form = UserRegiterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #first_name = form.cleaned_data.get('first_name')
            messages.success(request,f'Your Account has been created ! You are now able to login')
            return redirect('login')
    else:
        form=UserRegiterForm()
    return render(request,'register.html',{'form':form})
   # return render(request,'collection_app/register.html',{'form':form})

    #context=  {
    #    "name":"saifullah",
    #    "number":"01911192627"
   # }

   # return render(request,'home.html',context)
@login_required
def profile(request):
    return render(request, 'profile.html')


def data_show(request):
    conn=cx_Oracle.connect('saifullah/123@localhost/xepdb1')
    curr=conn.cursor()
    curr.execute('select sysdate from dual')
    for line in curr:
        print(line)
    return render(request, 'dbdata.html')


def student_disp(request):
    query = request.GET.get('name')
    data = Students.objects.all()

    stu = {
        "student_number": data
    }
    return render(request, 'student_display.html',stu)

   # return render_to_response('student_display', stu)


def testform(request):
    return render(request, 'login_temp.html')

#@csrf_exempt
@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
       #data=JSONParser().parse(request)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
    #except :
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method =='GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = ArticleSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' :
        article.delete()
        #return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)

def Report_lab_pdf_gen(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    #p = canvas.Canvas(buffer)


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    print
    id
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="PatientReport.pdf"'
    c = canvas.Canvas(response, pagesize=letter)
    t = c.beginText()
    t.setFont('Helvetica-Bold', 10)
    t.setCharSpace(3)
    t.setTextOrigin(50, 700)
    t.textLines('''Lorem Ipsum is simply dummy text of the printing and 
    typesetting industry. Lorem Ipsum has been the industry's standard dummy text 
    ever since the 1500s, when an unknown printer took a galley of type and 
    scrambled it to make a type specimen book.''')
    
    wraped_text = "\n".join(wrap(text, 80))  # 80 is line width

    t.textLines(wraped_text)
    c.drawText(t)
    c.showPage()
    c.save()
    return response
    #for ss in Blog.objects.raw('SELECT id,title FROM Blog where id=4'):

      # p.drawString(100, 300, ss.title )
       #p.drawString(250, 800, 'Report Title')
       #p.drawString(1, 1, ss.title)


   #p.drawString(100, 100, "Hello world.Hello world.Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='hello.pdf')



def get_name(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Students(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            f_name = form.cleaned_data.get('f_name')
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

          # if a GET (or any other method) we'll create a blank form
        else:
            form = Students()

        return render(request, 'name.html', {'form': form})


def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogForm()
    return render(request,
                  'blog_create.html',
                  {
                      'form': form
                  })


def blog_edit(request, pk=None):
    blog = get_object_or_404(Blog, pk=pk)
    city = request.POST.get('city')
    print(city)
    if request.method == "POST":
        form = BlogForm(request.POST,
                        instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogForm(instance=blog)

    return render(request,
                  'blog_edit.html',
                  {
                      'form': form,
                      'blog': blog
                  })


def student_entry(request):
    #print(request.GET)
    #print(request.POST)
    my_phone = request.POST.get('phone')
    #print( my_new_title)
    #blog_list = Blog.objects.raw('SELECT * FROM Blog WHERE id = %d', [id_no])
    for p in Blog.objects.raw('SELECT id,title FROM Blog'):
       print(p.title ,p.id)

    with connection.cursor() as cursor:

        cursor.execute('SELECT ID,TITLE FROM Blog where id=%s',[my_phone])
        for row in cursor.fetchall():

            print (row[0],row[1])
    #print(p)
    context = {}
    return render(request, "student_registation.html", context)
    #blog_list = Blog.objects.raw('SELECT ID,TITLE FROM Blog')
    # blog_list = Blog.objects.raw('SELECT ID,TITLE FROM Blog     where id= %s', params=['phone'])
    # emp_list = Blog.objects.all(blog_list)
    #print(blog_list)
    #print((emp_list))

    #for i in blog_list:
    #   rec =i.title,i.id
    # print(i.title)
    #  print(rec)

def blog_data_updatet(request):

    if request.method == "POST":
        v_title = request.POST.get('title')
        v_blog_id = request.POST.get('blog_id')

       # print(dbcommand)
        with connection.cursor() as cursor:
           # cursor.execute(dbcommand)
            cursor.execute("UPDATE blog SET title = 'User itle' where id=%s" ,[v_blog_id])


            #call oracle procedure
            test =""
            print(cursor.callproc('test_procedure', [test]))
            print(test)
            #print(cursor.callproc('FUNCTION1')
    context = {}
    return render(request, "update_data.html", context)

def insertdata(request):
    if request.method == "POST":
        cursor = connection.cursor()

        query = ''' INSERT INTO Blog 
                (title,author) 
                VALUES (%s,%s) '''

        #queryList = buildQueryList()

        v_title = request.POST.get('title')
        v_author = request.POST.get('author')
        valueList = (v_title,v_author)
        # here buildQueryList() represents some function to populate
        # the list with multiple records
        # in the tuple format (value1,value2,value3).

        #cursor.executemany(query, queryList)
        cursor.execute(query, valueList)

        transaction.commit()
    context = {}
    return render(request, "insert_data.html", context)
def drawmyruler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')
    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')

def reportlab(request):
    buffer = io.BytesIO()

    fileName = 'MyDoc.pdf'
    documentTitle = 'My Document Title'
    title = 'Tasmanian devil'
    subTtile = 'The largest arnivorous marsupial'

    textLines = ['''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the
    industry's standard dummy text 
ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.''']

    pdf = canvas.Canvas(buffer)

    pdf.setTitle(documentTitle)
    pdf.setFontSize(18)
   # pdf.drawString(230,800,title)
    pdf.setFillColorRGB(0,0,255)
    pdf.drawCentredString(250,800,title)
    pdf.setFontSize(15)
    pdf.drawCentredString(250,780,subTtile)
    pdf.line(30,770,550,770)

    text = pdf.beginText(40,680)
    pdf.setFontSize(12)
    text.setFillColor(colors.red)
    for line in textLines:
        text.textLine(line)
    pdf.drawText(text)




    drawmyruler(pdf)
    pdf.save()

    pdf.showPage()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='hello.pdf')


def clientapi(request):

    url = 'http://127.0.0.1:8000/article/'
    response = requests.get(url)

    #print(response.text)
    print(response.url)
    print(response.cookies)
    print(response.reason)

    stu = {
        'data':response.text
    }
    return render(request, 'profile.html', stu)


def readcsffiles(request):
    with open('templates\mycsv.csv','r') as csvfile:

        csv_reader = csv.reader(csvfile)
        i =0
        csvdata = []
        csvdata1 = []
        for line in csv_reader:

           # csvdata =line[i]
            #csvdata1[i] = csvdata.append(line[i])
            print(line[i])
            i = i + 1

    stu = {
        'data': line
    }
    return render(request, 'profile.html', stu)

def changpwd(request):
    u = User.objects.get(username='saifullah')
    u.set_password('1234')
    u.save()
    stu = {
        'data': 'sss'
    }
    return render(request, 'profile.html', stu)

'''its comments '''