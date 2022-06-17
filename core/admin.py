from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.forms import UserAdminForm, UserAdminCreationForm
from core.models import Usuario, UsuarioEndereco, Pais, Estado, Cidade, Categoria, Produto, ProdutoImagem # , ItemCarrinho, Venda, ItemVenda, Entrega


class UsuarioEnderecoInline(admin.TabularInline):
    model = UsuarioEndereco

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
	form = UserAdminForm
	fieldsets = (
		("Usuário", {
			"fields": (
				('is_active', 'is_staff', 'is_superuser', 'is_trusty', 'is_anonymous'),
				'username', ('password'), 'groups', 'user_permissions'
			),
		}),
		("Informações básicas", {
			"fields": (
				'tipo',
				('nome_fantasia', 'razao_social'), 
				'cpf_cnpj', 'data_nascimento', 'sexo',
				('telefone', 'email'), 'last_login'
			),
		}),
	)
	add_form = UserAdminCreationForm
	add_fieldsets = (
		("Usuário", {
			"fields": (
				('is_active', 'is_staff', 'is_superuser', 'is_trusty', 'is_anonymous'),
				'username', ('password1', 'password2'), 'groups', 'user_permissions'
			),
		}),
		("Informações básicas", {
			"fields": (
				'tipo',
				('nome_fantasia', 'razao_social'), 
				'cpf_cnpj', 'data_nascimento', 'sexo',
				('telefone', 'email')
			)
		})
	)
	
	list_display = [
		'username', 'is_staff', 'is_active', 'nome_fantasia', 'cpf_cnpj', 'telefone', 'email', 'data_cadastro'
	]

	inlines = [
		UsuarioEnderecoInline,
	]


@admin.register(UsuarioEndereco)
class UsuarioEnderecoAdmin(admin.ModelAdmin):
	pass


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ['pk', 'nome', 'sigla']
    list_display_links = ['pk', 'nome']

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    ordering = ['pais', 'nome']
    list_display = ['pk', 'nome', 'sigla', 'pais']
    list_display_links = ['pk', 'nome']

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    model = Cidade
    ordering = ['pk']
    list_display = ['pk', 'nome', 'estado']
    list_display_links = ['pk', 'nome']
    list_filter = ('estado',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	pass

class ProdutoImagemInline(admin.TabularInline):
	model = ProdutoImagem

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
	inlines = [
		ProdutoImagemInline,
	]

@admin.register(ProdutoImagem)
class ProdutoImagemAdmin(admin.ModelAdmin):
	pass

'''
@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    pass

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    inlines = [
        ItemVendaInline,
    ]


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    pass
'''
