from urllib import request
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, RedirectView
from core.models import Categoria, Produto, ProdutoImagem


class LoginAcessoView(LoginView):
	template_name = 'registration/login.html'


class LoginRecuperarSenhaView(TemplateView):
	template_name = 'registration/recuperar_senha.html'


class LoginCadastroView(TemplateView):
	template_name = 'registration/cadastro.html'


class IndexView(TemplateView):
	template_name = 'publico/index.html'

	def get_context_data(self, context=None, **kwargs):
		self.kwargs['categorias'] = Categoria.objects.filter(ativo=True)  # Navbar
		return self.kwargs


class CategoriaView(TemplateView):
	template_name = 'publico/produto_listagem.html'

	def get_context_data(self, context=None, **kwargs):
		self.kwargs['categorias'] = Categoria.objects.filter(ativo=True)  # Navbar
		categoria_id = Categoria.objects.get(slug=kwargs['slug']).pk
		self.kwargs['categoria_nome'] = Categoria.objects.get(slug=kwargs['slug']).nome
		self.kwargs['produtos'] = Produto.objects.filter(categoria=categoria_id, ativo=True)
		self.kwargs['produtos_imagens'] = ProdutoImagem.objects.filter(padrao=True)
		return self.kwargs


class ProdutoDetalheView(TemplateView):
	template_name = 'publico/produto_detalhe.html'

	def get_context_data(self, context=None, **kwargs):
		self.kwargs['categorias'] = Categoria.objects.filter(
			ativo=True)  # Navbar
		produto = Produto.objects.get(slug=kwargs['slug'])
		self.kwargs['produto'] = produto
		self.kwargs['produtos_imagens'] = ProdutoImagem.objects.filter(
			produto=produto.pk, ativo=True)
		return self.kwargs


class CarrinhoView(TemplateView):
	template_name = 'publico/carrinho.html'


	def get_context_data(self, context=None, **kwargs):
			self.kwargs['categorias'] = Categoria.objects.filter(ativo=True)  # Navbar
			self.kwargs['carrinho'] = [
				{'nome': 'item 1'},
				{'nome': 'item 2'},
			]
			print("PRINT AQUIIIIII")
			return self.kwargs


class ContatoView(TemplateView):
	template_name = 'publico/contato.html'

	def get_context_data(self, context=None, **kwargs):
		self.kwargs['categorias'] = Categoria.objects.filter(ativo=True)  # Navbar
		return self.kwargs


class SobreAEmpresaView(TemplateView):
	template_name = 'publico/sobre_a_empresa.html'

	def get_context_data(self, context=None, **kwargs):
		self.kwargs['categorias'] = Categoria.objects.filter(ativo=True)  # Navbar
		return self.kwargs