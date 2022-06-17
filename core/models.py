import re
from datetime import date
from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

class Base(models.Model):
	data_cadastro = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	data_ultima_modificacao = models.DateTimeField(auto_now=True, blank=True, null=True)

	class Meta:
		abstract = True


class Pais(Base):
	nome = models.CharField(max_length=100)
	sigla = models.CharField(max_length=2)

	class Meta:
		verbose_name = 'País'
		verbose_name_plural = 'Países'
		db_table = 'pais'

	def __str__(self):
		return self.nome + '(' + self.sigla + ')'


class Estado(Base):
	nome = models.CharField(max_length=100)
	sigla = models.CharField(max_length=2)
	pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING, default=1)

	class Meta:
		verbose_name = 'Estado'
		verbose_name_plural = 'Estados'
		db_table = 'estado'

	def __str__(self):
		return self.nome + ' - ' + self.pais.sigla


class Cidade(Base):
	nome = models.CharField(max_length=100)
	estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)

	class Meta:
		verbose_name = 'Cidade'
		verbose_name_plural = 'Cidades'
		db_table = 'cidade'

	def __str__(self):
		return self.nome + ' - ' + self.estado.sigla


class Endereco(Base):
	padrao = models.BooleanField(verbose_name='Padrão', default=False)
	rua = models.CharField(verbose_name='Rua', max_length=255, null=False, blank=False)
	numero = models.CharField(verbose_name='Número', max_length=10, null=False, blank=False)
	complemento = models.CharField(verbose_name='Complemento', max_length=255, null=True, blank=True)
	referencia = models.CharField(verbose_name='Referência', max_length=255, null=True, blank=True)
	cep = models.CharField(verbose_name='CEP', max_length=10, null=False, blank=False)
	bairro = models.CharField(verbose_name='Bairro', max_length=200, null=False, blank=False)
	cidade = models.ForeignKey(Cidade, verbose_name='Cidade', on_delete=models.DO_NOTHING, null=False, blank=False)

	class Meta:
		abstract = True


class Usuario(AbstractBaseUser, PermissionsMixin):
	objects = UserManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'cpf_cnpj']

	# USUÁRIO
	username = models.CharField(
		'Usuário', max_length=50, unique=True, validators=[
			validators.RegexValidator(
				re.compile('^[\w.@+-]+$'),
				'Informe um usuário válido.'
				'Este valor deve conter apenas letras e números '
				'e os caracteres @/./+/-/_.',
				'invalid'
			)
		], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
	)
	is_staff = models.BooleanField('Equipe', default=False)
	is_active = models.BooleanField('Ativo', default=True)
	is_superuser  = models.BooleanField('Superusuário', default=False)
	is_anonymous = models.BooleanField('Anonimo', default=False)
	is_trusty = models.BooleanField('E-Mail confirmado', default=False)
	# PESSOAL
	TIPO_CHOICE = (
		('F', 'Física'),
		('J', 'Jurídica')
	)
	tipo = models.CharField('Tipo', max_length=1, choices=TIPO_CHOICE, default='F')
	nome_fantasia = models.CharField('Nome Fantasia', max_length=255, blank=True, null=True)
	razao_social = models.CharField('Razão Social', max_length=255, blank=True, null=True)
	cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, unique=True)
	data_nascimento = models.DateField('Data de Nascimento', default=date.today, null=True, blank=True)
	SEXO_CHOICES = (
		("M", "Masculino"),
		("F", "Feminino"),
		("N", "Nenhuma das opções")
	)
	sexo = models.CharField('Sexo', max_length=1, null=True, blank=True, choices=SEXO_CHOICES, default='N')
	# CONTATO
	telefone = models.CharField('Telefone', max_length=20, null=True, blank=True)
	email = models.EmailField('E-Mail', unique=True)
	# LOG
	data_cadastro = models.DateTimeField('Data de cadastro', auto_now_add=True, null=True, blank=True)
	data_ultima_modificacao = models.DateTimeField('Data da ultima modificação', auto_now=True, null=True, blank=True)

	class Meta:
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'
		db_table = 'usuario'

	def __str__(self):
		return self.username or self.get_short_name()

	def get_full_name(self):
		return str(self.nome_fantasia)

	def get_short_name(self):
		return str(self.nome_fantasia).split(" ")[0]

	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email])


class UsuarioEndereco(Endereco):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	padrao = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Endereço do usuário'
		verbose_name_plural = 'Endereços dos usuários'
		db_table = 'usuario_endereco'

	def __str__(self):
		informacao = 'Usuário: ' + str(
			self.usuario) + ' - Endereço: ' + self.rua + ', nº ' + self.numero + ', ' + self.bairro + ', CEP ' + self.cep
		if self.complemento:
			informacao = informacao + ', ' + self.complemento
		if self.referencia:
			informacao = informacao + ', ' + self.referencia
		return informacao

	def save(self):
		#  SÓ UM ENDEREÇO COMO PADRÃO
		if self.padrao:
			usuarios_enderecos = UsuarioEndereco.objects.filter(padrao=True, produto=self.endereco.pk)
			for usuario_endereco in usuarios_enderecos:
				usuario_endereco.padrao = False
				usuario_endereco.save()
		super().save()


class Categoria(Base):
	ativo = models.BooleanField(verbose_name='Ativo', default=False)
	nome = models.CharField(verbose_name='Nome', unique=True, max_length=255)
	slug = models.SlugField(verbose_name='URL', unique=True)
	descricao = models.CharField(verbose_name='Descrição', max_length=150, null=True, blank=True)
	imagem_destaque = models.ImageField(
		verbose_name='Imagem de destaque', 
		upload_to='produto/categoria/',
		max_length=250, null=True, blank=True
	)

	class Meta:
		verbose_name = 'Categoria'
		verbose_name_plural = 'Categorias'
		db_table = 'produto_categoria'

	def __str__(self):
		return self.nome


class Produto(Base):
	# SITE
	ativo = models.BooleanField(default=False)
	slug = models.SlugField('Identificador', max_length=100)
	nome = models.CharField(max_length=255, unique=True)
	descricao = models.CharField(max_length=2000, null=True, blank=True)
	categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, null=True, blank=True)
	# VALOR
	valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)
	# MEDIDAS
	altura = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
	largura = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
	comprimento = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
	peso = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)

	class Meta:
		verbose_name = 'Produto'
		verbose_name_plural = 'Produtos'
		db_table = 'produto'

	def __str__(self):
		return str(self.pk) + ' - ' + str(self.nome)


class ProdutoImagem(Base):
	produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=False, blank=False)
	padrao = models.BooleanField(default=False)
	imagem = models.ImageField(upload_to='produto/produto', max_length=255, null=False, blank=False)
	alt = models.CharField(max_length=150, default='Imagem de produto', null=True, blank=True)
	ativo = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Imagem do produto'
		verbose_name_plural = 'Imagens dos produtos'
		db_table = 'produto_imagem'

	def __str__(self):
		return str(self.pk) + ' - ' + str(self.produto)

	def save(self):

		#  SÓ UMA IMAGEM COMO PADRÃO
		if self.padrao:
			produto_imagens = ProdutoImagem.objects.filter(padrao=True, produto=self.produto.pk)
			for produto_imagem in produto_imagens:
				produto_imagem.padrao = False
				produto_imagem.save()
		super().save()
