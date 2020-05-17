from django.db import connection
from django.shortcuts import render,redirect

def testform(request):
    return render(request, 'base_menu.html')


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def my_custom_sql(request):
   #print ('sart sql command')
    SGPA =5
    with connection.cursor() as cursor:
        #cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute('select f_name,l_name from STUDENTS WHERE GPA = %s',[SGPA])
        row = namedtuplefetchall(cursor)
        print(row)


    stu = {
         "students": row
     }

    return render(request, 'directsql.html',stu)