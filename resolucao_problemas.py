"""
HABILIDADE 2: RESOLUÇÃO DE PROBLEMAS

Este módulo demonstra a capacidade de:
- Analisar e entender requisitos
- Decompor problemas em partes menores
- Implementar soluções eficientes
- Validar entradas e tratamento de erros
- Testar casos extremos

Autor: Desenvolvedor Python
Data: Janeiro 2026
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


# ============================================================================
# PROBLEMA 1: VALIDAÇÃO DE EMAIL
# ============================================================================

def validar_email(email: str) -> bool:
    """
    Valida um endereço de email usando expressão regular.
    
    Requisitos:
    - Deve conter @ e ponto
    - Nome de usuário antes do @
    - Domínio após @ e antes do ponto
    - Extensão após o ponto
    
    Args:
        email: Endereço de email para validar
        
    Returns:
        True se válido, False caso contrário
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))


# ============================================================================
# PROBLEMA 2: VALIDAÇÃO DE SENHA FORTE
# ============================================================================

def validar_senha_forte(senha: str) -> Tuple[bool, List[str]]:
    """
    Valida se uma senha é forte baseado em critérios específicos.
    
    Critérios:
    - Mínimo 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    
    Args:
        senha: Senha para validar
        
    Returns:
        Tupla (é_valida, lista_de_problemas)
    """
    problemas = []
    
    if len(senha) < 8:
        problemas.append("❌ Mínimo 8 caracteres")
    
    if not re.search(r'[A-Z]', senha):
        problemas.append("❌ Falta letra maiúscula")
    
    if not re.search(r'[a-z]', senha):
        problemas.append("❌ Falta letra minúscula")
    
    if not re.search(r'\d', senha):
        problemas.append("❌ Falta número")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        problemas.append("❌ Falta caractere especial")
    
    return len(problemas) == 0, problemas


# ============================================================================
# PROBLEMA 3: CÁLCULO DE JUROS COMPOSTOS
# ============================================================================

def calcular_juros_compostos(
    capital_inicial: float,
    taxa_anual: float,
    tempo_anos: int,
    frequencia_capitalizacao: int = 12
) -> Dict[str, float]:
    """
    Calcula juros compostos de um investimento.
    
    Fórmula: M = C * (1 + i/n)^(n*t)
    
    Args:
        capital_inicial: Capital inicial do investimento
        taxa_anual: Taxa de juros anual (em %)
        tempo_anos: Tempo do investimento (em anos)
        frequencia_capitalizacao: Vezes por ano (padrão: 12 - mensal)
        
    Returns:
        Dicionário com montante final e juros ganhos
    """
    taxa_decimal = taxa_anual / 100
    montante_final = capital_inicial * (1 + taxa_decimal / frequencia_capitalizacao) ** (
        frequencia_capitalizacao * tempo_anos
    )
    juros_ganhos = montante_final - capital_inicial
    
    return {
        'capital_inicial': capital_inicial,
        'montante_final': round(montante_final, 2),
        'juros_ganhos': round(juros_ganhos, 2),
        'taxa_anual': taxa_anual,
        'tempo_anos': tempo_anos,
    }


# ============================================================================
# PROBLEMA 4: NÚMERO PERFEITO E NÚMEROS AMIGOS
# ============================================================================

def encontrar_divisores(numero: int) -> List[int]:
    """
    Encontra todos os divisores próprios de um número.
    Divisores próprios são todos os divisores exceto o próprio número.
    
    Args:
        numero: Número para encontrar divisores
        
    Returns:
        Lista de divisores próprios
    """
    divisores = []
    for i in range(1, numero):
        if numero % i == 0:
            divisores.append(i)
    return divisores


def eh_numero_perfeito(numero: int) -> bool:
    """
    Um número perfeito é igual à soma de seus divisores próprios.
    Exemplo: 6 = 1 + 2 + 3
    
    Args:
        numero: Número para verificar
        
    Returns:
        True se é número perfeito
    """
    return numero == sum(encontrar_divisores(numero))


def sao_numeros_amigos(a: int, b: int) -> bool:
    """
    Dois números são amigos se a soma dos divisores próprios de um
    é igual ao outro e vice-versa.
    Exemplo: 220 e 284 são amigos.
    
    Args:
        a: Primeiro número
        b: Segundo número
        
    Returns:
        True se são números amigos
    """
    soma_divisores_a = sum(encontrar_divisores(a))
    soma_divisores_b = sum(encontrar_divisores(b))
    
    return soma_divisores_a == b and soma_divisores_b == a


# ============================================================================
# PROBLEMA 5: VERIFICAÇÃO DE PALÍNDROMO
# ============================================================================

def eh_palindromo(texto: str) -> bool:
    """
    Verifica se um texto é um palíndromo (lê igual de trás para frente).
    
    Args:
        texto: Texto para verificar
        
    Returns:
        True se é palíndromo
    """
    texto_limpo = re.sub(r'[^a-z0-9]', '', texto.lower())
    return texto_limpo == texto_limpo[::-1]


# ============================================================================
# PROBLEMA 6: MAIOR SUBSEQUÊNCIA COMUM
# ============================================================================

def mdc_sequencias(seq1: str, seq2: str) -> str:
    """
    Encontra a maior subsequência comum entre duas sequências.
    Usa programação dinâmica.
    
    Args:
        seq1: Primeira sequência
        seq2: Segunda sequência
        
    Returns:
        A maior subsequência comum
    """
    m, n = len(seq1), len(seq2)
    
    # Criar matriz de programação dinâmica
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Reconstruir a subsequência
    resultado = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            resultado.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(resultado))


# ============================================================================
# PROBLEMA 7: BALANCEAMENTO DE PARÊNTESES
# ============================================================================

def balanceamento_parenteses(expressao: str) -> bool:
    """
    Verifica se os parênteses, colchetes e chaves estão balanceados.
    
    Args:
        expressao: Expressão para verificar
        
    Returns:
        True se está balanceada
    """
    pilha = []
    pares = {'(': ')', '[': ']', '{': '}'}
    
    for char in expressao:
        if char in pares:
            pilha.append(char)
        elif char in pares.values():
            if not pilha or pares[pilha.pop()] != char:
                return False
    
    return len(pilha) == 0


# ============================================================================
# PROBLEMA 8: ROTAÇÃO DE ARRAY
# ============================================================================

def rotacionar_array(array: List[int], posicoes: int) -> List[int]:
    """
    Rotaciona um array para a direita um número especificado de posições.
    
    Exemplo: [1, 2, 3, 4, 5] rotacionado 2 = [4, 5, 1, 2, 3]
    
    Args:
        array: Array para rotacionar
        posicoes: Número de posições para rotacionar
        
    Returns:
        Array rotacionado
    """
    if not array:
        return array
    
    posicoes = posicoes % len(array)
    return array[-posicoes:] + array[:-posicoes]


# ============================================================================
# DEMONSTRAÇÃO E TESTES
# ============================================================================

def main():
    """Executa exemplos de resolução de problemas."""
    
    print("=" * 70)
    print("HABILIDADE 2: RESOLUÇÃO DE PROBLEMAS")
    print("=" * 70)
    
    # 1. Validação de Email
    print("\n1. VALIDAÇÃO DE EMAIL")
    print("-" * 70)
    emails = [
        "usuario@exemplo.com",
        "email-invalido@",
        "user.name@dominio.co.br",
        "sem.arroba.com"
    ]
    for email in emails:
        valido = validar_email(email)
        status = "✅ Válido" if valido else "❌ Inválido"
        print(f"{email:<30} {status}")
    
    # 2. Validação de Senha
    print("\n2. VALIDAÇÃO DE SENHA FORTE")
    print("-" * 70)
    senhas = [
        "abc123",
        "Senha@123",
        "SeNH4@Forte",
    ]
    for senha in senhas:
        valida, problemas = validar_senha_forte(senha)
        status = "✅ Forte" if valida else "❌ Fraca"
        print(f"Senha: {senha}")
        print(f"Status: {status}")
        if problemas:
            for p in problemas:
                print(f"  {p}")
        print()
    
    # 3. Juros Compostos
    print("\n3. CÁLCULO DE JUROS COMPOSTOS")
    print("-" * 70)
    resultado = calcular_juros_compostos(
        capital_inicial=1000,
        taxa_anual=5,
        tempo_anos=10
    )
    print(f"Capital inicial: R$ {resultado['capital_inicial']:.2f}")
    print(f"Taxa anual: {resultado['taxa_anual']}%")
    print(f"Tempo: {resultado['tempo_anos']} anos")
    print(f"Montante final: R$ {resultado['montante_final']:.2f}")
    print(f"Juros ganhos: R$ {resultado['juros_ganhos']:.2f}")
    
    # 4. Números Perfeitos
    print("\n4. NÚMEROS PERFEITOS")
    print("-" * 70)
    numeros = [6, 28, 12, 496]
    for num in numeros:
        eh_perfeito = eh_numero_perfeito(num)
        divisores = encontrar_divisores(num)
        status = "✅ Perfeito" if eh_perfeito else "❌ Não é perfeito"
        print(f"{num}: {status} | Divisores: {divisores} | Soma: {sum(divisores)}")
    
    # 5. Números Amigos
    print("\n5. NÚMEROS AMIGOS")
    print("-" * 70)
    pares = [(220, 284), (1184, 1210), (6, 8)]
    for a, b in pares:
        sao_amigos = sao_numeros_amigos(a, b)
        status = "✅ Amigos" if sao_amigos else "❌ Não são amigos"
        print(f"{a} e {b}: {status}")
    
    # 6. Palíndromo
    print("\n6. VERIFICAÇÃO DE PALÍNDROMO")
    print("-" * 70)
    textos = [
        "A man, a plan, a canal: Panama",
        "Python",
        "Ama a dama na cama",
    ]
    for texto in textos:
        eh_pal = eh_palindromo(texto)
        status = "✅ Palíndromo" if eh_pal else "❌ Não é"
        print(f"{texto:<35} {status}")
    
    # 7. Maior Subsequência Comum
    print("\n7. MAIOR SUBSEQUÊNCIA COMUM")
    print("-" * 70)
    seq1 = "AGGTAB"
    seq2 = "GXTXAYB"
    resultado = mdc_sequencias(seq1, seq2)
    print(f"Sequência 1: {seq1}")
    print(f"Sequência 2: {seq2}")
    print(f"Maior subseq. comum: {resultado}")
    
    # 8. Balanceamento de Parênteses
    print("\n8. BALANCEAMENTO DE PARÊNTESES")
    print("-" * 70)
    expressoes = [
        "({[]})",
        "({[}])",
        "{[()]}",
        "((("
    ]
    for exp in expressoes:
        balanceado = balanceamento_parenteses(exp)
        status = "✅ Balanceado" if balanceado else "❌ Desbalanceado"
        print(f"{exp:<15} {status}")
    
    # 9. Rotação de Array
    print("\n9. ROTAÇÃO DE ARRAY")
    print("-" * 70)
    array = [1, 2, 3, 4, 5]
    rotacoes = 2
    resultado = rotacionar_array(array, rotacoes)
    print(f"Array original: {array}")
    print(f"Rotações: {rotacoes}")
    print(f"Resultado: {resultado}")
    
    print("\n" + "=" * 70)
    print("✅ Todos os problemas resolvidos com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()
