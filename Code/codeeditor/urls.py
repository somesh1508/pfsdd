
from django.urls import path
from .views import home, register, user_login, code_editor, about, get_ai_suggestion, logout_successful, user_logout

urlpatterns = [
path('logout/', user_logout, name='logout'),  # Logout URL
path('logout/success/', logout_successful, name='logout_successful'),
path('editor/', code_editor, name='code_editor'),
    path('get_ai_suggestion/', get_ai_suggestion, name='get_ai_suggestion'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('editor/', code_editor, name='editor'),
    path('about/', about, name='about'),
]


