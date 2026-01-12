"""
HABILIDADE 5: TRABALHO EM EQUIPE E REMOTO

Este módulo demonstra:
- Documentação clara para outros desenvolvedores
- Código modular e reutilizável
- Estrutura organizada e padrões consistentes
- Type hints completos
- Tratamento de erros adequado
- Comentários educacionais
- Exemplos práticos de colaboração

Autor: Desenvolvedor Python
Data: Janeiro 2026

NOTA: Para trabalho em equipe remoto, práticas como commitsg boas
mensagens são fundamentais. Veja as boas práticas no final deste arquivo.
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


# ============================================================================
# DOCUMENTAÇÃO E CONVENÇÕES
# ============================================================================

"""
CONVENÇÕES DO PROJETO:

1. NOMES:
   - Classes: PascalCase (ExemploClasse)
   - Funções/variáveis: snake_case (exemplo_funcao, variavel_local)
   - Constantes: MAIUSCULAS_COM_UNDERLINE (VALOR_PADRAO)

2. ESTRUTURA:
   - Imports no topo
   - Constantes após imports
   - Classes e funções organizadas logicamente
   - Testes no final

3. DOCUMENTAÇÃO:
   - Module docstring no início do arquivo
   - Docstrings em classes e funções públicas
   - Comentários para lógica complexa
   - Type hints em todos os lugares

4. GIT:
   - Mensagens de commit claras e descritivas
   - Um feature por commit quando possível
   - Pull requests com descrição detalhada
   - Referências a issues quando aplicável
"""


# ============================================================================
# CONSTANTES - Fácil manutenção e centralização
# ============================================================================

MAX_TENTATIVAS_CONEXAO = 3
TIMEOUT_PADRAO_SEGUNDOS = 30
VERSAO_API = "1.0.0"


# ============================================================================
# ENUMERAÇÕES - Valores semânticos
# ============================================================================

class StatusConexao(Enum):
    """Estados possíveis de uma conexão."""
    CONECTADA = "conectada"
    DESCONECTADA = "desconectada"
    ERRO = "erro"
    RECONECTANDO = "reconectando"


class TipoMensagem(Enum):
    """Tipos de mensagens no sistema."""
    INFORMACAO = "info"
    AVISO = "warning"
    ERRO = "error"
    SUCESSO = "success"


# ============================================================================
# MODELOS DE DADOS - Reutilizáveis e bem estruturados
# ============================================================================

@dataclass
class Usuario:
    """
    Representa um usuário do sistema.
    
    Atributos:
        id: Identificador único
        nome: Nome completo
        email: Email corporativo
        departamento: Departamento/time
        ativo: Se o usuário está ativo
        data_criacao: Quando foi criado
    """
    id: str
    nome: str
    email: str
    departamento: str
    ativo: bool = True
    data_criacao: datetime = field(default_factory=datetime.now)
    
    def ativar(self) -> None:
        """Ativa o usuário no sistema."""
        self.ativo = True
    
    def desativar(self) -> None:
        """Desativa o usuário no sistema."""
        self.ativo = False
    
    def para_dict(self) -> Dict[str, Any]:
        """
        Converte o usuário para dicionário.
        
        Útil para serialização em JSON/API responses.
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'departamento': self.departamento,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat()
        }


@dataclass
class Mensagem:
    """
    Representa uma mensagem no sistema.
    
    Atributos:
        id: Identificador único
        remetente: Usuário que enviou
        conteudo: Texto da mensagem
        tipo: Tipo de mensagem
        timestamp: Quando foi criada
        lida: Se foi lida
    """
    id: str
    remetente: Usuario
    conteudo: str
    tipo: TipoMensagem
    timestamp: datetime = field(default_factory=datetime.now)
    lida: bool = False
    
    def marcar_como_lida(self) -> None:
        """Marca a mensagem como lida."""
        self.lida = True
    
    def eh_recente(self, horas: int = 24) -> bool:
        """
        Verifica se a mensagem é recente.
        
        Args:
            horas: Limite de horas para considerar recente
            
        Returns:
            True se foi enviada há menos de N horas
        """
        tempo_limite = datetime.now().timestamp() - (horas * 3600)
        return self.timestamp.timestamp() > tempo_limite


# ============================================================================
# SERVIÇOS - Lógica compartilhada
# ============================================================================

class GerenciadorUsuarios:
    """
    Gerencia operações com usuários.
    
    Responsabilidades:
    - Criar e atualizar usuários
    - Validação de dados
    - Armazenamento em memória (em produção seria banco de dados)
    """
    
    def __init__(self):
        """Inicializa o gerenciador."""
        self._usuarios: Dict[str, Usuario] = {}
    
    def criar_usuario(
        self,
        id_usuario: str,
        nome: str,
        email: str,
        departamento: str
    ) -> Usuario:
        """
        Cria um novo usuário.
        
        Args:
            id_usuario: ID único para o usuário
            nome: Nome completo
            email: Email corporativo
            departamento: Departamento onde trabalha
            
        Returns:
            Novo usuário criado
            
        Raises:
            ValueError: Se ID já existe
        """
        if id_usuario in self._usuarios:
            raise ValueError(f"Usuário {id_usuario} já existe!")
        
        usuario = Usuario(
            id=id_usuario,
            nome=nome,
            email=email,
            departamento=departamento
        )
        self._usuarios[id_usuario] = usuario
        return usuario
    
    def obter_usuario(self, id_usuario: str) -> Optional[Usuario]:
        """
        Obtém um usuário pelo ID.
        
        Args:
            id_usuario: ID do usuário
            
        Returns:
            Usuário ou None se não encontrado
        """
        return self._usuarios.get(id_usuario)
    
    def listar_usuarios_ativos(self) -> List[Usuario]:
        """
        Lista todos os usuários ativos.
        
        Returns:
            Lista de usuários ativos
        """
        return [u for u in self._usuarios.values() if u.ativo]
    
    def obter_por_departamento(self, departamento: str) -> List[Usuario]:
        """
        Obtém todos os usuários de um departamento.
        
        Args:
            departamento: Nome do departamento
            
        Returns:
            Lista de usuários
        """
        return [u for u in self._usuarios.values() if u.departamento == departamento]


class GerenciadorMensagens:
    """
    Gerencia mensagens do sistema.
    
    Responsabilidades:
    - Armazenar e recuperar mensagens
    - Marcar como lidas
    - Filtrar por tipo/usuário
    """
    
    def __init__(self):
        """Inicializa o gerenciador."""
        self._mensagens: Dict[str, Mensagem] = {}
        self._contador_id = 0
    
    def enviar_mensagem(
        self,
        remetente: Usuario,
        conteudo: str,
        tipo: TipoMensagem = TipoMensagem.INFORMACAO
    ) -> Mensagem:
        """
        Envia uma nova mensagem.
        
        Args:
            remetente: Usuário que envia
            conteudo: Texto da mensagem
            tipo: Tipo de mensagem
            
        Returns:
            Mensagem criada
        """
        self._contador_id += 1
        mensagem = Mensagem(
            id=f"MSG{self._contador_id:06d}",
            remetente=remetente,
            conteudo=conteudo,
            tipo=tipo
        )
        self._mensagens[mensagem.id] = mensagem
        return mensagem
    
    def obter_nao_lidas(self) -> List[Mensagem]:
        """
        Obtém todas as mensagens não lidas.
        
        Returns:
            Lista de mensagens não lidas
        """
        return [m for m in self._mensagens.values() if not m.lida]
    
    def marcar_lida(self, id_mensagem: str) -> bool:
        """
        Marca uma mensagem como lida.
        
        Args:
            id_mensagem: ID da mensagem
            
        Returns:
            True se conseguiu marcar, False se não encontrou
        """
        mensagem = self._mensagens.get(id_mensagem)
        if mensagem:
            mensagem.marcar_como_lida()
            return True
        return False


# ============================================================================
# RELATÓRIOS - Para comunicação em equipe
# ============================================================================

class RelatorioEquipe:
    """
    Gera relatórios sobre atividades da equipe.
    
    Útil para reuniões e acompanhamento de trabalho.
    """
    
    def __init__(self, gerenciador_usuarios: GerenciadorUsuarios):
        """Inicializa com acesso aos usuários."""
        self.gerenciador_usuarios = gerenciador_usuarios
    
    def relatorio_departamento(self, departamento: str) -> Dict[str, Any]:
        """
        Gera relatório sobre um departamento.
        
        Args:
            departamento: Nome do departamento
            
        Returns:
            Dicionário com informações do departamento
        """
        usuarios = self.gerenciador_usuarios.obter_por_departamento(departamento)
        usuarios_ativos = [u for u in usuarios if u.ativo]
        
        return {
            'departamento': departamento,
            'total_usuarios': len(usuarios),
            'usuarios_ativos': len(usuarios_ativos),
            'usuarios_inativos': len(usuarios) - len(usuarios_ativos),
            'membros': [u.para_dict() for u in usuarios]
        }
    
    def relatorio_geral(self) -> Dict[str, Any]:
        """
        Gera relatório geral da organização.
        
        Returns:
            Dicionário com informações gerais
        """
        todos_usuarios = self.gerenciador_usuarios.listar_usuarios_ativos()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'versao_api': VERSAO_API,
            'total_usuarios_ativos': len(todos_usuarios),
            'departamentos': self._contar_por_departamento(todos_usuarios)
        }
    
    def _contar_por_departamento(self, usuarios: List[Usuario]) -> Dict[str, int]:
        """
        Conta usuários por departamento.
        
        Args:
            usuarios: Lista de usuários
            
        Returns:
            Dicionário com contagem por departamento
        """
        contagem = {}
        for usuario in usuarios:
            contagem[usuario.departamento] = contagem.get(usuario.departamento, 0) + 1
        return contagem


# ============================================================================
# LOGGER CENTRALIZADO - Para rastrear ações
# ============================================================================

class LoggerSistema:
    """
    Sistema de logging centralizado.
    
    Importante em trabalho remoto para rastrear ações e debug.
    """
    
    def __init__(self):
        """Inicializa o logger."""
        self._logs: List[Dict[str, Any]] = []
    
    def registrar(self, nivel: str, mensagem: str, dados: Dict[str, Any] | None = None) -> None:
        """
        Registra uma ação no log.
        
        Args:
            nivel: ERRO, AVISO, INFO, DEBUG
            mensagem: Mensagem descritiva
            dados: Dados adicionais contextuais
        """
        log = {
            'timestamp': datetime.now().isoformat(),
            'nivel': nivel,
            'mensagem': mensagem,
            'dados': dados or {}
        }
        self._logs.append(log)
    
    def obter_logs_recentes(self, quantidade: int = 10) -> List[Dict[str, Any]]:
        """Obtém os logs mais recentes."""
        return self._logs[-quantidade:]


# ============================================================================
# DEMONSTRAÇÃO E TESTES
# ============================================================================

def main():
    """Executa exemplos de trabalho em equipe."""
    
    print("=" * 70)
    print("HABILIDADE 5: TRABALHO EM EQUIPE E REMOTO")
    print("=" * 70)
    
    # Inicializar serviços
    gerenciador_usuarios = GerenciadorUsuarios()
    gerenciador_mensagens = GerenciadorMensagens()
    logger = LoggerSistema()
    
    # 1. CRIAR USUÁRIOS
    print("\n1. CRIANDO USUÁRIOS")
    print("-" * 70)
    usuarios = []
    nomes = [
        ("USR001", "João Silva", "joao@empresa.com", "Desenvolvimento"),
        ("USR002", "Maria Santos", "maria@empresa.com", "Desenvolvimento"),
        ("USR003", "Carlos Oliveira", "carlos@empresa.com", "Marketing"),
    ]
    
    for id_user, nome, email, depto in nomes:
        usuario = gerenciador_usuarios.criar_usuario(id_user, nome, email, depto)
        usuarios.append(usuario)
        logger.registrar("INFO", f"Usuário criado", {"id": id_user, "nome": nome})
        print(f"✅ {nome} ({depto})")
    
    # 2. ENVIAR MENSAGENS
    print("\n2. ENVIANDO MENSAGENS")
    print("-" * 70)
    msg1 = gerenciador_mensagens.enviar_mensagem(
        usuarios[0],
        "Iniciando novo projeto!",
        TipoMensagem.INFORMACAO
    )
    msg2 = gerenciador_mensagens.enviar_mensagem(
        usuarios[1],
        "Deploy finalizado com sucesso",
        TipoMensagem.SUCESSO
    )
    print(f"✅ Mensagem 1: {msg1.conteudo}")
    print(f"✅ Mensagem 2: {msg2.conteudo}")
    
    # 3. MENSAGENS NÃO LIDAS
    print("\n3. MENSAGENS NÃO LIDAS")
    print("-" * 70)
    nao_lidas = gerenciador_mensagens.obter_nao_lidas()
    print(f"Mensagens não lidas: {len(nao_lidas)}")
    for msg in nao_lidas:
        print(f"  • {msg.remetente.nome}: {msg.conteudo}")
    
    # 4. MARCAR COMO LIDA
    print("\n4. MARCANDO MENSAGENS COMO LIDAS")
    print("-" * 70)
    gerenciador_mensagens.marcar_lida(msg1.id)
    print(f"✅ Mensagem {msg1.id} marcada como lida")
    
    # 5. RELATÓRIO DO DEPARTAMENTO
    print("\n5. RELATÓRIO DO DEPARTAMENTO")
    print("-" * 70)
    relatorio = RelatorioEquipe(gerenciador_usuarios)
    dados_dev = relatorio.relatorio_departamento("Desenvolvimento")
    print(f"Departamento: {dados_dev['departamento']}")
    print(f"Total de usuários: {dados_dev['total_usuarios']}")
    print(f"Ativos: {dados_dev['usuarios_ativos']}")
    print(f"Membros: {[u['nome'] for u in dados_dev['membros']]}")
    
    # 6. RELATÓRIO GERAL
    print("\n6. RELATÓRIO GERAL")
    print("-" * 70)
    relatorio_geral = relatorio.relatorio_geral()
    print(f"Total de usuários ativos: {relatorio_geral['total_usuarios_ativos']}")
    print(f"Departamentos: {relatorio_geral['departamentos']}")
    
    # 7. LOGS DO SISTEMA
    print("\n7. LOGS DO SISTEMA (últimos 3)")
    print("-" * 70)
    logs = logger.obter_logs_recentes(3)
    for log in logs:
        print(f"[{log['nivel']}] {log['mensagem']}")
    
    print("\n" + "=" * 70)
    print("✅ Trabalho em equipe demonstrado com sucesso!")
    print("=" * 70)
    
    # ========================================================================
    # BOAS PRÁTICAS DE GIT PARA TRABALHO REMOTO
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("📋 BOAS PRÁTICAS DE GIT PARA TRABALHO REMOTO")
    print("=" * 70)
    
    praticas = """
1. COMMITS CLAROS:
   ✅ git commit -m "feat: adicionar validação de email"
   ✅ git commit -m "fix: corrigir bug de conexão"
   ✅ git commit -m "docs: atualizar README com instrções"
   ❌ git commit -m "ajustes"
   ❌ git commit -m "corrigido"

2. BRANCHING:
   ✅ git checkout -b feat/novo-sistema-notificacoes
   ✅ git checkout -b fix/bug-conexao
   ✅ git checkout -b docs/api-reference
   ❌ git checkout -b meu-branch
   ❌ git checkout -b teste123

3. PULL REQUESTS:
   ✅ Descrição detalhada do que foi feito
   ✅ Referência a issues: "Fecha #123"
   ✅ Screenshots/GIFs quando relevante
   ✅ Checklist de testes executados

4. REVIEW DE CÓDIGO:
   ✅ Revisar antes de mergear
   ✅ Deixar feedback construtivo
   ✅ Aprovar ou solicitar mudanças
   ✅ Comunicar-se com respeito

5. DOCUMENTAÇÃO:
   ✅ README atualizado
   ✅ Docstrings em código
   ✅ Exemplos de uso
   ✅ Guia de desenvolvimento

6. COMUNICAÇÃO:
   ✅ Usar issues para discussões
   ✅ Deixar comentários no PR
   ✅ Usar mention (@usuario) quando necessário
   ✅ Responder comentários prontamente
    """
    print(praticas)


if __name__ == "__main__":
    main()
