#!/usr/bin/env python3
"""
Script de instalação completa para a interface web.

Este script instala todas as dependências e configura
o ambiente para a interface web do Gêmeo Digital.
"""
import subprocess
import sys
import os
import platform

def verificar_python():
    """Verifica a versão do Python."""
    print("🐍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def instalar_dependencias():
    """Instala todas as dependências necessárias."""
    print("\n📦 Instalando dependências...")
    
    # Lista de dependências
    dependencias = [
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "pandas>=2.1.0",
        "numpy>=1.25.0",
        "simpy>=4.0.1",
        "matplotlib>=3.7.1",
        "scipy>=1.11.1",
        "scikit-learn>=1.3.0",
        "seaborn>=0.12.0"
    ]
    
    for dep in dependencias:
        print(f"Instalando {dep}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Falha ao instalar {dep}")
            return False
    
    return True

def criar_diretorios():
    """Cria diretórios necessários."""
    print("\n📁 Criando diretórios...")
    
    diretorios = [
        ".streamlit",
        "output",
        "logs"
    ]
    
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"✅ Diretório criado: {diretorio}")
        else:
            print(f"✅ Diretório já existe: {diretorio}")

def verificar_arquivos():
    """Verifica se todos os arquivos necessários estão presentes."""
    print("\n🔍 Verificando arquivos...")
    
    arquivos_necessarios = [
        "interface_web.py",
        "main.py",
        "config.py",
        "requirements_interface.txt",
        "README_INTERFACE.md"
    ]
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} não encontrado")
            return False
    
    return True

def testar_importacoes():
    """Testa se todas as importações funcionam."""
    print("\n🧪 Testando importações...")
    
    try:
        import streamlit
        print("✅ Streamlit")
        
        import plotly
        print("✅ Plotly")
        
        import pandas
        print("✅ Pandas")
        
        import numpy
        print("✅ NumPy")
        
        import simpy
        print("✅ SimPy")
        
        import matplotlib
        print("✅ Matplotlib")
        
        import scipy
        print("✅ SciPy")
        
        import sklearn
        print("✅ Scikit-learn")
        
        import seaborn
        print("✅ Seaborn")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False

def mostrar_instrucoes_finais():
    """Mostra instruções finais para o usuário."""
    print("\n" + "=" * 60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: python iniciar_interface.py")
    print("2. Ou execute: python demo_interface.py")
    print("3. Acesse: http://localhost:8501")
    print("\n📚 DOCUMENTAÇÃO:")
    print("- README_INTERFACE.md - Guia da interface")
    print("- README.md - Documentação completa")
    print("\n🆘 SUPORTE:")
    print("- Verifique os logs em caso de erro")
    print("- Consulte a documentação")
    print("- Entre em contato com a equipe")
    print("=" * 60)

def main():
    """Função principal de instalação."""
    print("🏭 Instalador da Interface Web - Gêmeo Digital Industrial")
    print("=" * 70)
    
    # Verificar Python
    if not verificar_python():
        return
    
    # Criar diretórios
    criar_diretorios()
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("\n❌ Arquivos necessários não encontrados!")
        return
    
    # Instalar dependências
    if not instalar_dependencias():
        print("\n❌ Falha na instalação das dependências!")
        return
    
    # Testar importações
    if not testar_importacoes():
        print("\n❌ Falha nos testes de importação!")
        return
    
    # Mostrar instruções finais
    mostrar_instrucoes_finais()

if __name__ == "__main__":
    main()
