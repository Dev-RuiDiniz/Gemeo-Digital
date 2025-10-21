#!/usr/bin/env python3
"""
Executador de testes para o sistema de Gêmeo Digital.

Este script executa todos os testes do sistema, incluindo
testes unitários e de integração.
"""
import unittest
import sys
import os

# Adicionar raiz do projeto ao caminho Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Executa todos os testes na suite de testes."""
    # Descobrir e executar testes
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de saída
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
