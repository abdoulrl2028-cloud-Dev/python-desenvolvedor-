"""
HABILIDADE 3: CÓDIGO LIMPO E ORGANIZADO

Este módulo demonstra:
- Nomes descritivos para variáveis e funções
- Funções com responsabilidade única
- Comentários e docstrings adequados
- Estrutura modular e reutilizável
- Type hints para maior clareza
- Princípios SOLID

Autor: Desenvolvedor Python
Data: Janeiro 2026
"""

from dataclasses import dataclass
from typing import List, Optional, Protocol
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================================
# ENUMERAÇÕES - Para valores predefinidos
# ============================================================================

class StatusPedido(Enum):
    """Estados possíveis de um pedido."""
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


# ============================================================================
# MODELOS DE DADOS - Usando dataclasses
# ============================================================================

@dataclass
class Endereco:
    """Representa um endereço completo."""
    rua: str
    numero: int
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None
    
    def __str__(self) -> str:
        """Retorna representação formatada do endereço."""
        endereco = f"{self.rua}, {self.numero} - {self.cidade}, {self.estado} {self.cep}"
        if self.complemento:
            endereco += f" ({self.complemento})"
        return endereco


@dataclass
class Produto:
    """Representa um produto disponível para venda."""
    id_produto: str
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int
    
    def pode_vender(self, quantidade: int) -> bool:
        """
        Verifica se há quantidade suficiente em estoque.
        
        Args:
            quantidade: Quantidade desejada
            
        Returns:
            True se há estoque suficiente
        """
        return self.quantidade_estoque >= quantidade
    
    def reduzir_estoque(self, quantidade: int) -> bool:
        """
        Reduz a quantidade em estoque.
        
        Args:
            quantidade: Quantidade a reduzir
            
        Returns:
            True se a redução foi bem-sucedida
        """
        if self.pode_vender(quantidade):
            self.quantidade_estoque -= quantidade
            return True
        return False


@dataclass
class ItemPedido:
    """Representa um item dentro de um pedido."""
    produto: Produto
    quantidade: int
    
    def calcular_subtotal(self) -> float:
        """
        Calcula o subtotal deste item.
        
        Returns:
            Preço do produto × quantidade
        """
        return self.produto.preco * self.quantidade


# ============================================================================
# CLASSES COM RESPONSABILIDADE ÚNICA
# ============================================================================

class Pedido:
    """
    Representa um pedido de cliente.
    
    Responsabilidade única: Gerenciar dados e estado do pedido.
    """
    
    def __init__(self, id_pedido: str, cliente_nome: str, endereco_entrega: Endereco):
        """
        Inicializa um novo pedido.
        
        Args:
            id_pedido: Identificador único do pedido
            cliente_nome: Nome do cliente
            endereco_entrega: Endereço para entrega
        """
        self.id_pedido = id_pedido
        self.cliente_nome = cliente_nome
        self.endereco_entrega = endereco_entrega
        self.items: List[ItemPedido] = []
        self.status = StatusPedido.PENDENTE
        self.data_criacao = datetime.now()
    
    def adicionar_item(self, item: ItemPedido) -> None:
        """
        Adiciona um item ao pedido.
        
        Args:
            item: ItemPedido a adicionar
        """
        self.items.append(item)
    
    def obter_total(self) -> float:
        """
        Calcula o valor total do pedido.
        
        Returns:
            Soma de todos os subtotais dos itens
        """
        return sum(item.calcular_subtotal() for item in self.items)
    
    def obter_numero_itens(self) -> int:
        """
        Retorna a quantidade total de itens.
        
        Returns:
            Número de itens diferentes no pedido
        """
        return len(self.items)
    
    def esta_vazio(self) -> bool:
        """
        Verifica se o pedido não contém itens.
        
        Returns:
            True se não há itens
        """
        return self.obter_numero_itens() == 0


class CalculadoraFrete:
    """
    Responsável pelo cálculo de frete.
    
    Responsabilidade única: Calcular valores de frete.
    """
    
    _VALOR_BASE_FRETE = 10.0
    _TAXA_DISTANCIA = 0.5  # Por quilômetro
    
    @staticmethod
    def calcular_frete(peso_kg: float, distancia_km: float) -> float:
        """
        Calcula o valor do frete baseado em peso e distância.
        
        Args:
            peso_kg: Peso total em quilogramas
            distancia_km: Distância em quilômetros
            
        Returns:
            Valor do frete em reais
        """
        valor_peso = peso_kg * 2.0
        valor_distancia = distancia_km * CalculadoraFrete._TAXA_DISTANCIA
        return CalculadoraFrete._VALOR_BASE_FRETE + valor_peso + valor_distancia


class GerenciadorEstoque:
    """
    Responsável por gerenciar o estoque de produtos.
    
    Responsabilidade única: Gerenciar quantidade de produtos.
    """
    
    def __init__(self):
        """Inicializa o gerenciador com um dicionário vazio de produtos."""
        self.produtos: dict[str, Produto] = {}
    
    def adicionar_produto(self, produto: Produto) -> None:
        """
        Adiciona um produto ao estoque.
        
        Args:
            produto: Produto a ser adicionado
        """
        self.produtos[produto.id_produto] = produto
    
    def obter_produto(self, id_produto: str) -> Optional[Produto]:
        """
        Recupera um produto pelo ID.
        
        Args:
            id_produto: Identificador do produto
            
        Returns:
            O produto ou None se não encontrado
        """
        return self.produtos.get(id_produto)
    
    def verificar_disponibilidade(self, id_produto: str, quantidade: int) -> bool:
        """
        Verifica se há quantidade disponível em estoque.
        
        Args:
            id_produto: Identificador do produto
            quantidade: Quantidade desejada
            
        Returns:
            True se há quantidade suficiente
        """
        produto = self.obter_produto(id_produto)
        if produto is None:
            return False
        return produto.pode_vender(quantidade)


class ProcessadorPagamento:
    """
    Responsável pelo processamento de pagamentos.
    
    Responsabilidade única: Processar pagamentos.
    """
    
    def processar_pagamento(self, valor: float, metodo: str) -> bool:
        """
        Processa um pagamento.
        
        Args:
            valor: Valor a cobrar
            metodo: Método de pagamento (cartao, boleto, pix)
            
        Returns:
            True se o pagamento foi aprovado
        """
        if valor <= 0:
            return False
        
        # Simulação de processamento
        # Em produção, integraria com gateway de pagamento real
        print(f"Processando pagamento de R$ {valor:.2f} via {metodo}...")
        return True


class NotificadorPedido:
    """
    Responsável por notificações sobre pedidos.
    
    Responsabilidade única: Enviar notificações.
    """
    
    @staticmethod
    def notificar_confirmacao(pedido: Pedido) -> None:
        """
        Envia notificação de confirmação do pedido.
        
        Args:
            pedido: Pedido confirmado
        """
        mensagem = f"Pedido {pedido.id_pedido} confirmado para {pedido.cliente_nome}"
        print(f"📧 Notificação: {mensagem}")
    
    @staticmethod
    def notificar_envio(pedido: Pedido) -> None:
        """
        Envia notificação de envio do pedido.
        
        Args:
            pedido: Pedido enviado
        """
        mensagem = f"Pedido {pedido.id_pedido} foi enviado para {pedido.endereco_entrega.cidade}"
        print(f"📦 Notificação: {mensagem}")
    
    @staticmethod
    def notificar_entrega(pedido: Pedido) -> None:
        """
        Envia notificação de entrega.
        
        Args:
            pedido: Pedido entregue
        """
        mensagem = f"Pedido {pedido.id_pedido} entregue para {pedido.cliente_nome}"
        print(f"✅ Notificação: {mensagem}")


# ============================================================================
# ORQUESTRAÇÃO - Classe que coordena os serviços
# ============================================================================

class ServicoVendas:
    """
    Orquestra todos os serviços necessários para processar uma venda.
    
    Segue o padrão Facade para simplificar a interface.
    """
    
    def __init__(self):
        """Inicializa o serviço com seus dependências."""
        self.estoque = GerenciadorEstoque()
        self.processador_pagamento = ProcessadorPagamento()
        self.notificador = NotificadorPedido()
    
    def processar_pedido(
        self,
        pedido: Pedido,
        metodo_pagamento: str
    ) -> bool:
        """
        Processa um pedido completo do início ao fim.
        
        Args:
            pedido: Pedido para processar
            metodo_pagamento: Método de pagamento escolhido
            
        Returns:
            True se o pedido foi processado com sucesso
        """
        # Validar pedido
        if pedido.esta_vazio():
            print("❌ Erro: Pedido vazio!")
            return False
        
        # Validar disponibilidade de estoque
        for item in pedido.items:
            if not self.estoque.verificar_disponibilidade(
                item.produto.id_produto,
                item.quantidade
            ):
                print(f"❌ Erro: Produto {item.produto.nome} indisponível!")
                return False
        
        # Processar pagamento
        total = pedido.obter_total()
        if not self.processador_pagamento.processar_pagamento(total, metodo_pagamento):
            print("❌ Erro: Falha ao processar pagamento!")
            return False
        
        # Reduzir estoque
        for item in pedido.items:
            item.produto.reduzir_estoque(item.quantidade)
        
        # Atualizar status e notificar
        pedido.status = StatusPedido.PROCESSANDO
        self.notificador.notificar_confirmacao(pedido)
        
        return True


# ============================================================================
# DEMONSTRAÇÃO E TESTES
# ============================================================================

def main():
    """Executa exemplos de código limpo e organizado."""
    
    print("=" * 70)
    print("HABILIDADE 3: CÓDIGO LIMPO E ORGANIZADO")
    print("=" * 70)
    
    # Criar produtos
    print("\n1. CRIANDO PRODUTOS")
    print("-" * 70)
    produto1 = Produto(
        id_produto="PROD001",
        nome="Notebook",
        descricao="Notebook para desenvolvimento",
        preco=3500.00,
        quantidade_estoque=10
    )
    produto2 = Produto(
        id_produto="PROD002",
        nome="Mouse",
        descricao="Mouse sem fio",
        preco=80.00,
        quantidade_estoque=50
    )
    print(f"✅ {produto1.nome}: R$ {produto1.preco:.2f}")
    print(f"✅ {produto2.nome}: R$ {produto2.preco:.2f}")
    
    # Criar endereço
    print("\n2. CRIANDO ENDEREÇO DE ENTREGA")
    print("-" * 70)
    endereco = Endereco(
        rua="Avenida Paulista",
        numero=1000,
        cidade="São Paulo",
        estado="SP",
        cep="01310-100"
    )
    print(f"✅ Endereço: {endereco}")
    
    # Criar pedido
    print("\n3. CRIANDO PEDIDO")
    print("-" * 70)
    pedido = Pedido(
        id_pedido="PED001",
        cliente_nome="João Silva",
        endereco_entrega=endereco
    )
    pedido.adicionar_item(ItemPedido(produto1, quantidade=1))
    pedido.adicionar_item(ItemPedido(produto2, quantidade=2))
    
    print(f"✅ Pedido ID: {pedido.id_pedido}")
    print(f"✅ Cliente: {pedido.cliente_nome}")
    print(f"✅ Itens: {pedido.obter_numero_itens()}")
    print(f"✅ Total: R$ {pedido.obter_total():.2f}")
    
    # Calcular frete
    print("\n4. CÁLCULO DE FRETE")
    print("-" * 70)
    frete = CalculadoraFrete.calcular_frete(peso_kg=5.0, distancia_km=25.0)
    print(f"✅ Frete (5kg, 25km): R$ {frete:.2f}")
    
    # Processar vendas
    print("\n5. PROCESSANDO PEDIDO")
    print("-" * 70)
    servico_vendas = ServicoVendas()
    servico_vendas.estoque.adicionar_produto(produto1)
    servico_vendas.estoque.adicionar_produto(produto2)
    
    sucesso = servico_vendas.processar_pedido(pedido, "cartao")
    if sucesso:
        print("✅ Pedido processado com sucesso!")
        print(f"✅ Status: {pedido.status.value}")
    
    print("\n" + "=" * 70)
    print("✅ Código limpo demonstrado com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()
