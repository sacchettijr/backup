from decimal import Decimal
from copy import deepcopy
from core.models import Produto

class Carrinho:
	def __init__(self, request):
		if request.session.get("carrinho") is None:
			request.session['carrinho'] = {}

		self.carrinho = request.session["carrinho"]
		self.session = request.session

	def __iter__(self):
		carrinho = deepcopy(self.carrinho)
		produtos = Produto.objects.filter(id__in=carrinho)
		for produto in produtos:
			carrinho[str(produto.id)]["produto"] = produto

		for item in carrinho.values():
			item['valor_unitario'] = Decimal(item["valor_unitario"])
			item['valor_total'] = item["valor_unitario"] * item["quantidade"]
			
			yield item

	def __len__(self):
		return sum(
			item["quantidade"] for item in self.carrinho.values()
		)

	def add(self, produto, quantidade=1, override_quantity=False):
		produto_id = str(produto.id)

		if produto_id not in self.carrinho:
			self.carrinho[produto_id] = {
				"quantidade": 0,
				"valor_unitario": str(produto.valor_unitario)
			}

		if override_quantity:
			self.cart[produto_id]["quantidade"] = quantidade
		else:
			self.cart[produto_id]["quantidade"] += quantidade

		self.save()
	
	def remove(self, produto): 
		produto_id = str(produto.id)

		if produto_id in self.carrinho:
			del self.carrinho[produto_id]
			self.save()

	def save(self):
		self.session.modified = True