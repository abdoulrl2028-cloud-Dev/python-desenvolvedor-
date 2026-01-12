"""
HABILIDADE 4: FACILIDADE DE APRENDIZADO

Este módulo demonstra:
- Implementação de padrões de design
- Uso educacional de bibliotecas externas
- Documentação clara e didática
- Exemplos com entrada e saída
- Explicações em português para facilitar compreensão

Autor: Desenvolvedor Python
Data: Janeiro 2026
"""

from typing import List, Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import json


# ============================================================================
# PADRÃO 1: SINGLETON - Uma única instância em toda aplicação
# ============================================================================

class ConfiguracaoAplicacao:
    """
    Implementa o padrão Singleton para garantir única instância de config.
    
    Uso: Quando há recursos compartilhados que devem ser únicos.
    Exemplo: Conexão com banco de dados, configurações globais.
    """
    
    _instancia: Optional['ConfiguracaoAplicacao'] = None
    
    def __new__(cls):
        """Cria uma nova instância apenas se não existir."""
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        """Inicializa as configurações."""
        self.versao = "1.0.0"
        self.ambiente = "desenvolvimento"
        self.debug = True
        print("⚙️  ConfiguracaoAplicacao inicializada")
    
    def obter_configuracao(self, chave: str) -> Any:
        """Retorna uma configuração específica."""
        return getattr(self, chave, None)


# ============================================================================
# PADRÃO 2: BUILDER - Construir objetos complexos passo a passo
# ============================================================================

class ContrutorRelatorio:
    """
    Implementa o padrão Builder para criar relatórios passo a passo.
    
    Vantagem: Permite criação de objetos complexos de forma legível.
    """
    
    def __init__(self):
        """Inicializa o construtor com valores padrão."""
        self._titulo = ""
        self._descricao = ""
        self._dados = []
        self._rodape = ""
    
    def com_titulo(self, titulo: str) -> 'ContrutorRelatorio':
        """Define o título do relatório."""
        self._titulo = titulo
        return self
    
    def com_descricao(self, descricao: str) -> 'ContrutorRelatorio':
        """Define a descrição do relatório."""
        self._descricao = descricao
        return self
    
    def adicionar_dado(self, dado: Dict[str, Any]) -> 'ContrutorRelatorio':
        """Adiciona um dado ao relatório."""
        self._dados.append(dado)
        return self
    
    def com_rodape(self, rodape: str) -> 'ContrutorRelatorio':
        """Define o rodapé do relatório."""
        self._rodape = rodape
        return self
    
    def construir(self) -> Dict[str, Any]:
        """Constrói e retorna o relatório final."""
        return {
            'titulo': self._titulo,
            'descricao': self._descricao,
            'dados': self._dados,
            'rodape': self._rodape,
            'data_geracao': datetime.now().isoformat()
        }


# ============================================================================
# PADRÃO 3: STRATEGY - Diferentes estratégias de ordenação
# ============================================================================

class EstrategiaOrdenacao(ABC):
    """Interface abstrata para estratégias de ordenação."""
    
    @abstractmethod
    def ordenar(self, dados: List[int]) -> List[int]:
        """Ordena uma lista de inteiros."""
        pass


class OrdenacaoAscendente(EstrategiaOrdenacao):
    """Estratégia para ordenação crescente."""
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Ordena em ordem crescente."""
        return sorted(dados)


class OrdenacaoDescendente(EstrategiaOrdenacao):
    """Estratégia para ordenação decrescente."""
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Ordena em ordem decrescente."""
        return sorted(dados, reverse=True)


class OrdenadorDados:
    """Usa a estratégia para ordenar dados."""
    
    def __init__(self, estrategia: EstrategiaOrdenacao):
        """Define a estratégia de ordenação."""
        self._estrategia = estrategia
    
    def executar(self, dados: List[int]) -> List[int]:
        """Executa a ordenação com a estratégia escolhida."""
        return self._estrategia.ordenar(dados)


# ============================================================================
# PADRÃO 4: FACTORY - Criar objetos sem especificar a classe exata
# ============================================================================

class Notificacao(ABC):
    """Interface para notificações."""
    
    @abstractmethod
    def enviar(self, mensagem: str) -> bool:
        """Envia uma notificação."""
        pass


class NotificacaoEmail(Notificacao):
    """Implementação de notificação por email."""
    
    def enviar(self, mensagem: str) -> bool:
        """Envia notificação via email."""
        print("📧 Email enviado: " + mensagem)
        return True


class NotificacaoSMS(Notificacao):
    """Implementação de notificação por SMS."""
    
    def enviar(self, mensagem: str) -> bool:
        """Envia notificação via SMS."""
        print("📱 SMS enviado: " + mensagem)
        return True


class NotificacaoPush(Notificacao):
    """Implementação de notificação push."""
    
    def enviar(self, mensagem: str) -> bool:
        """Envia notificação push."""
        print("🔔 Push enviado: " + mensagem)
        return True


class FabricaNotificacoes:
    """Factory para criar notificações."""
    
    _tipos = {
        'email': NotificacaoEmail,
        'sms': NotificacaoSMS,
        'push': NotificacaoPush,
    }
    
    @classmethod
    def criar(cls, tipo: str) -> Notificacao:
        """
        Cria uma notificação do tipo especificado.
        
        Args:
            tipo: 'email', 'sms' ou 'push'
            
        Returns:
            Instância de Notificacao
        """
        classe = cls._tipos.get(tipo.lower())
        if classe is None:
            raise ValueError("Tipo de notificação inválido: " + tipo)
        return classe()


# ============================================================================
# PADRÃO 5: OBSERVER - Notificar múltiplos observadores de mudanças
# ============================================================================

class Observador(ABC):
    """Interface para observadores."""
    
    @abstractmethod
    def atualizar(self, evento: str, dados: Dict[str, Any]) -> None:
        """Chamado quando há uma atualização."""
        pass


class LoggerObservador(Observador):
    """Observador que registra eventos em log."""
    
    def atualizar(self, evento: str, dados: Dict[str, Any]) -> None:
        """Registra o evento."""
        print("📋 Log: " + evento + " -> " + str(dados))


class CacheObservador(Observador):
    """Observador que limpa cache ao evento."""
    
    def atualizar(self, evento: str, dados: Dict[str, Any]) -> None:
        """Limpa cache."""
        print("💾 Cache: Limpando cache para evento '" + evento + "'")


class SistemaNotificacoes:
    """Implementa o padrão Observer."""
    
    def __init__(self):
        """Inicializa com lista vazia de observadores."""
        self._observadores: List[Observador] = []
    
    def registrar_observador(self, observador: Observador) -> None:
        """Registra um observador."""
        self._observadores.append(observador)
    
    def remover_observador(self, observador: Observador) -> None:
        """Remove um observador."""
        self._observadores.remove(observador)
    
    def notificar_observadores(self, evento: str, dados: Dict[str, Any]) -> None:
        """Notifica todos os observadores."""
        for observador in self._observadores:
            observador.atualizar(evento, dados)


# ============================================================================
# EXEMPLO EDUCACIONAL: DECORADORES PYTHON
# ============================================================================

def medir_tempo_execucao(funcao: Callable) -> Callable:
    """
    Decorador que mede e exibe o tempo de execução de uma função.
    
    Educacional: Demonstra o uso de decoradores para adicionar
    funcionalidade sem modificar a função original.
    """
    def wrapper(*args, **kwargs):
        inicio = datetime.now()
        resultado = funcao(*args, **kwargs)
        duracao = (datetime.now() - inicio).total_seconds()
        print("⏱️  " + funcao.__name__ + " levou " + str(round(duracao, 4)) + " segundos")
        return resultado
    return wrapper


@medir_tempo_execucao
def processar_dados_grande(tamanho: int) -> int:
    """Função que processa muitos dados."""
    total = 0
    for i in range(tamanho):
        total += i
    return total


# ============================================================================
# EXEMPLO EDUCACIONAL: TRABALHAR COM JSON
# ============================================================================

def serializar_dados(dados: Dict[str, Any]) -> str:
    """
    Converte dados Python para JSON string.
    
    Educacional: JSON é formato universal para troca de dados.
    """
    return json.dumps(dados, ensure_ascii=False, indent=2)


def desserializar_dados(json_str: str) -> Dict[str, Any]:
    """
    Converte JSON string para dados Python.
    
    Educacional: Permite trabalhar com dados estruturados.
    """
    return json.loads(json_str)


# ============================================================================
# DEMONSTRAÇÃO E TESTES
# ============================================================================

def main():
    """Executa exemplos educacionais de padrões de design."""
    
    print("=" * 70)
    print("HABILIDADE 4: FACILIDADE DE APRENDIZADO")
    print("=" * 70)
    
    # 1. PADRÃO SINGLETON
    print("\n1. PADRÃO SINGLETON")
    print("-" * 70)
    config1 = ConfiguracaoAplicacao()
    config2 = ConfiguracaoAplicacao()
    print("Config1 e Config2 sao o mesmo objeto? " + str(config1 is config2))
    print("Versao: " + config1.obter_configuracao('versao'))
    
    # 2. PADRÃO BUILDER
    print("\n2. PADRÃO BUILDER")
    print("-" * 70)
    relatorio = (ContrutorRelatorio()
                 .com_titulo("Relatório de Vendas")
                 .com_descricao("Vendas do mês de janeiro")
                 .adicionar_dado({"produto": "Notebook", "quantidade": 5})
                 .adicionar_dado({"produto": "Mouse", "quantidade": 20})
                 .com_rodape("Fim do relatório")
                 .construir())
    
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    
    # 3. PADRÃO STRATEGY
    print("\n3. PADRÃO STRATEGY")
    print("-" * 70)
    dados = [3, 1, 4, 1, 5, 9, 2, 6]
    
    ordenador_asc = OrdenadorDados(OrdenacaoAscendente())
    print("Ordem crescente: " + str(ordenador_asc.executar(dados)))
    
    ordenador_desc = OrdenadorDados(OrdenacaoDescendente())
    print("Ordem decrescente: " + str(ordenador_desc.executar(dados)))
    
    # 4. PADRÃO FACTORY
    print("\n4. PADRÃO FACTORY")
    print("-" * 70)
    tipos = ['email', 'sms', 'push']
    for tipo in tipos:
        notificacao = FabricaNotificacoes.criar(tipo)
        notificacao.enviar("Olá, tudo bem?")
    
    # 5. PADRÃO OBSERVER
    print("\n5. PADRÃO OBSERVER")
    print("-" * 70)
    sistema = SistemaNotificacoes()
    sistema.registrar_observador(LoggerObservador())
    sistema.registrar_observador(CacheObservador())
    
    sistema.notificar_observadores("usuario_criado", {"id": 123, "nome": "João"})
    
    # 6. DECORADOR PYTHON
    print("\n6. DECORADOR PYTHON - MEDIR TEMPO")
    print("-" * 70)
    resultado = processar_dados_grande(1000000)
    print("Resultado: " + str(resultado))
    
    # 7. TRABALHAR COM JSON
    print("\n7. TRABALHAR COM JSON")
    print("-" * 70)
    dados_python = {
        "usuario": "João Silva",
        "idade": 30,
        "habilidades": ["Python", "JavaScript", "SQL"]
    }
    
    json_str = serializar_dados(dados_python)
    print("Dados em JSON:")
    print(json_str)
    
    dados_recuperados = desserializar_dados(json_str)
    print("Dados recuperados: " + str(dados_recuperados))
    
    print("\n" + "=" * 70)
    print("✅ Padrões de design demonstrados com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()
