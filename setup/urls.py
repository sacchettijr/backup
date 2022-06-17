from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.conf.urls.static import static
from django.urls import include, path
from core.views import LoginRecuperarSenhaView, LoginCadastroView, IndexView, CategoriaView, ProdutoDetalheView, CarrinhoView, ContatoView, SobreAEmpresaView


router = routers.DefaultRouter()

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
	# LOGIN
	path('login/', LoginView.as_view(), name='login_sm'),
	path('accounts/login/', LoginView.as_view(), name='login'),
	path('accounts/recuperar-senha/', LoginRecuperarSenhaView.as_view(), name='recuperar_senha'),
	path('accounts/cadastro/', LoginCadastroView.as_view(), name='cadastro'),
	path('accounts/logout/', LogoutView.as_view(), name='logout'),
	# PUBLICO
	path('', IndexView.as_view(), name='index'),
	path('categoria/<slug:slug>/', CategoriaView.as_view(), name='categoria'),
	path('produto/<slug:slug>/', ProdutoDetalheView.as_view(), name='produto'),
	path('carrinho/', CarrinhoView.as_view(), name='carrinho'),
	path('contato/', ContatoView.as_view(), name='contato'),
	path('sobre-a-empresa/', SobreAEmpresaView.as_view(), name='sobre_a_empresa'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)