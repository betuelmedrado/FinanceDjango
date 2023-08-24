
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/gerenciar/', views.gerenciar, name='gerenciar'),
    path('cadastrar_banco/', views.cadastrar_banco, name='cadastrar_banco'),
    path('home/gerenciar/deletar_banco/<int:id>', views.deletar_banco, name='deletar_banco'),
    path('home/gerenciar/cadastrar_categoria', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('home/gerenciar/update_categoria/<int:id>', views.update_categoria, name='update_categoria'),
    path('dashboard/', views.dashboard, name='dashboard')
]

urlpatterns += static(settings.MEDIA_URL,documment_root=settings.MEDIA_ROOT)