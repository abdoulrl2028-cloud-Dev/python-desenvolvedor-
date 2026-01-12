"""
HABILIDADE 1: LÓGICA DE PROGRAMAÇÃO

Este módulo demonstra o domínio de:
- Estruturas de controle (if/else, loops)
- Estruturas de dados (listas, dicionários, conjuntos)
- Algoritmos (busca, ordenação, recursão)
- Manipulação de dados

Autor: Desenvolvedor Python
Data: Janeiro 2026
"""

from typing import List, Dict, Tuple, Set


# ============================================================================
# 1. BUSCA BINÁRIA - Algoritmo eficiente para encontrar elementos
# ============================================================================

def busca_binaria(lista: List[int], alvo: int) -> int:
    """
    Encontra a posição de um elemento em uma lista ordenada usando busca binária.
    
    Args:
        lista: Lista ordenada de inteiros
        alvo: Elemento a ser procurado
        
    Returns:
        Índice do elemento ou -1 se não encontrado
        
    Complexidade: O(log n)
    """
    esquerda, direita = 0, len(lista) - 1
    
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        
        if lista[meio] == alvo:
            return meio
        elif lista[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
    return -1


# ============================================================================
# 2. ORDENAÇÃO - Implementação do algoritmo Merge Sort
# ============================================================================

def merge_sort(lista: List[int]) -> List[int]:
    """
    Ordena uma lista usando o algoritmo Merge Sort (dividir e conquistar).
    
    Args:
        lista: Lista de inteiros para ordenar
        
    Returns:
        Lista ordenada
        
    Complexidade: O(n log n)
    """
    if len(lista) <= 1:
        return lista
    
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    
    return mesclar(esquerda, direita)


def mesclar(esquerda: List[int], direita: List[int]) -> List[int]:
    """
    Mescla duas listas ordenadas em uma única lista ordenada.
    """
    resultado = []
    i = j = 0
    
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


# ============================================================================
# 3. RECURSÃO - Fibonacci com memoização
# ============================================================================

def fibonacci(n: int, memo: Dict[int, int] | None = None) -> int:
    """
    Calcula o n-ésimo número de Fibonacci usando recursão com memoização.
    
    Args:
        n: Posição na sequência de Fibonacci
        memo: Dicionário para armazenar valores já calculados
        
    Returns:
        O n-ésimo número de Fibonacci
        
    Complexidade: O(n) com memoização
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


# ============================================================================
# 4. MANIPULAÇÃO DE DICIONÁRIOS - Análise de frequência
# ============================================================================

def contar_frequencia(texto: str) -> Dict[str, int]:
    """
    Conta a frequência de cada palavra em um texto.
    
    Args:
        texto: Texto para análise
        
    Returns:
        Dicionário com palavras e suas frequências
    """
    palavras = texto.lower().split()
    frequencia = {}
    
    for palavra in palavras:
        frequencia[palavra] = frequencia.get(palavra, 0) + 1
    
    return frequencia


def top_n_palavras(texto: str, n: int = 5) -> List[Tuple[str, int]]:
    """
    Retorna as N palavras mais frequentes em um texto.
    
    Args:
        texto: Texto para análise
        n: Número de palavras a retornar
        
    Returns:
        Lista de tuplas (palavra, frequência) ordenada por frequência
    """
    frequencia = contar_frequencia(texto)
    return sorted(frequencia.items(), key=lambda x: x[1], reverse=True)[:n]


# ============================================================================
# 5. MANIPULAÇÃO DE LISTAS - Operações comuns
# ============================================================================

def remover_duplicatas(lista: List[int]) -> List[int]:
    """
    Remove elementos duplicados mantendo a ordem original.
    
    Args:
        lista: Lista com possíveis duplicatas
        
    Returns:
        Lista sem duplicatas
    """
    visto = set()
    resultado = []
    
    for elemento in lista:
        if elemento not in visto:
            visto.add(elemento)
            resultado.append(elemento)
    
    return resultado


def encontrar_pares(lista: List[int], alvo: int) -> List[Tuple[int, int]]:
    """
    Encontra todos os pares de números que somam um valor alvo.
    
    Args:
        lista: Lista de inteiros
        alvo: Valor alvo da soma
        
    Returns:
        Lista de tuplas com pares que somam o valor alvo
    """
    pares = []
    visto = set()
    
    for num in lista:
        complemento = alvo - num
        if complemento in visto:
            pares.append((min(num, complemento), max(num, complemento)))
        visto.add(num)
    
    return list(set(pares))


# ============================================================================
# 6. OPERAÇÕES COM CONJUNTOS - Álgebra de conjuntos
# ============================================================================

def operacoes_conjuntos(conjunto_a: Set[int], conjunto_b: Set[int]) -> Dict[str, Set[int]]:
    """
    Realiza operações básicas com conjuntos.
    
    Args:
        conjunto_a: Primeiro conjunto
        conjunto_b: Segundo conjunto
        
    Returns:
        Dicionário com resultados de operações
    """
    return {
        'uniao': conjunto_a | conjunto_b,
        'interseccao': conjunto_a & conjunto_b,
        'diferenca': conjunto_a - conjunto_b,
        'diferenca_simetrica': conjunto_a ^ conjunto_b,
    }


# ============================================================================
# DEMONSTRAÇÃO E TESTES
# ============================================================================

def main():
    """Executa exemplos de todas as operações."""
    
    print("=" * 70)
    print("HABILIDADE 1: LÓGICA DE PROGRAMAÇÃO")
    print("=" * 70)
    
    # 1. Busca Binária
    print("\n1. BUSCA BINÁRIA")
    print("-" * 70)
    lista_ordenada = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    alvo = 13
    resultado = busca_binaria(lista_ordenada, alvo)
    print(f"Lista: {lista_ordenada}")
    print(f"Procurando: {alvo}")
    print(f"Encontrado no índice: {resultado}")
    
    # 2. Ordenação com Merge Sort
    print("\n2. MERGE SORT (Ordenação)")
    print("-" * 70)
    lista_desordenada = [64, 34, 25, 12, 22, 11, 90]
    lista_ordenada = merge_sort(lista_desordenada)
    print(f"Lista original: {lista_desordenada}")
    print(f"Lista ordenada: {lista_ordenada}")
    
    # 3. Fibonacci
    print("\n3. FIBONACCI (Recursão com Memoização)")
    print("-" * 70)
    n = 10
    resultado = fibonacci(n)
    print(f"Fibonacci({n}) = {resultado}")
    
    # 4. Frequência de Palavras
    print("\n4. ANÁLISE DE FREQUÊNCIA")
    print("-" * 70)
    texto = "python é ótimo python é poderoso python é rápido"
    top_5 = top_n_palavras(texto, 3)
    print(f"Texto: '{texto}'")
    print(f"Top 3 palavras: {top_5}")
    
    # 5. Remover Duplicatas
    print("\n5. REMOVER DUPLICATAS")
    print("-" * 70)
    lista_com_duplicatas = [1, 2, 2, 3, 4, 4, 4, 5]
    lista_unica = remover_duplicatas(lista_com_duplicatas)
    print(f"Lista original: {lista_com_duplicatas}")
    print(f"Sem duplicatas: {lista_unica}")
    
    # 6. Encontrar Pares
    print("\n6. ENCONTRAR PARES COM SOMA ALVO")
    print("-" * 70)
    lista = [1, 2, 3, 4, 5, 6, 7]
    alvo_soma = 7
    pares = encontrar_pares(lista, alvo_soma)
    print(f"Lista: {lista}")
    print(f"Pares que somam {alvo_soma}: {pares}")
    
    # 7. Operações com Conjuntos
    print("\n7. OPERAÇÕES COM CONJUNTOS")
    print("-" * 70)
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    operacoes = operacoes_conjuntos(set_a, set_b)
    print(f"Conjunto A: {set_a}")
    print(f"Conjunto B: {set_b}")
    print(f"União: {operacoes['uniao']}")
    print(f"Interseção: {operacoes['interseccao']}")
    print(f"Diferença (A - B): {operacoes['diferenca']}")
    print(f"Diferença simétrica: {operacoes['diferenca_simetrica']}")
    
    print("\n" + "=" * 70)
    print("✅ Todos os exemplos executados com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()
