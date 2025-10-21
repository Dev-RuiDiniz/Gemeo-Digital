#!/usr/bin/env python3
"""
Script de inicialização para a interface web do Gêmeo Digital.

Este script verifica as dependências e inicia a interface web
de forma automatizada.
"""
import subprocess
import sys
import os

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas."""
    print("🔍 Verificando dependências...")
    
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        print("✅ Dependências da interface verificadas!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def instalar_dependencias():
    """Instala as dependências necessárias."""
    print("📦 Instalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_interface.txt"
        ])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def iniciar_interface():
    """Inicia a interface web."""
    print("🚀 Iniciando interface web...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "interface_web.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Interface encerrada pelo usuário.")
    except Exception as e:
        print(f"❌ Erro ao iniciar interface: {e}")

def main():
    """Função principal."""
    print("🏭 Sistema de Gêmeo Digital - Interface Web")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("interface_web.py"):
        print("❌ Arquivo interface_web.py não encontrado!")
        print("Certifique-se de estar no diretório correto do projeto.")
        return
    
    # Verificar dependências
    if not verificar_dependencias():
        print("\n📦 Instalando dependências faltantes...")
        if not instalar_dependencias():
            print("❌ Falha ao instalar dependências. Execute manualmente:")
            print("pip install -r requirements_interface.txt")
            return
    
    print("\n🌐 A interface web será aberta no seu navegador.")
    print("📱 Acesse: http://localhost:8501")
    print("⏹️  Para parar a interface, pressione Ctrl+C")
    print("\n" + "=" * 50)
    
    # Iniciar interface
    iniciar_interface()

if __name__ == "__main__":
    main()
