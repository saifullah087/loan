from django.urls import path
from . import views as user_views
from . import developer_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.HomeView, name='home'),
    path('register/',user_views.register,name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('devprofile/', developer_view.testform, name='devprofile'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('student/',user_views.student_disp,name='student'),
    path('test/', user_views.testform, name='test'),
    #path('article/', user_views.article_list, name='article'),
    #path('detail/<int:pk>/', user_views.article_detail, name='detail'),
    path('register/', user_views.register, name='register'),
    path('article/',user_views.ArticleAPIView.as_view(),name='article'),
    path('detail/<int:id>/',user_views.ArticleDetails.as_view(),name='detail'),
    path('generic/article/<int:id>/',user_views.GenericAPIView.as_view(),name='generic_article'),
    path('ReportLabPDF/', user_views.Report_lab_pdf_gen, name='ReportLabPDF'),
    #path('weasyprint/', user_views.html_to_pdf_view, name='weasyprint'),
    path('my_custom_sql/', developer_view.my_custom_sql, name='my_custom_sql'),
    path('blog/', user_views.blog_create, name='blog'),
    path('blog/edit/<int:pk>/', user_views.blog_edit, name='blog_edit'),
    path('student_entry/', user_views.student_entry, name='student_entry'),
    path('data_insert/', user_views.insertdata, name='data_insert'),
    path('data_update/', user_views.blog_data_updatet, name='data_update'),
    path('PDFreport/', user_views.reportlab, name='PDFreport'),
    path('apiclient/', user_views.clientapi, name='apiclient'),
    path('csv_reader/', user_views.readcsffiles, name='csv_reader'),
    path('Change_pwd/', user_views.changpwd, name='Change_pwd'),
    path('login_new/', auth_views.LoginView.as_view(template_name='login_temp.html'), name='login_new'),






]