#!/usr/bin/env python3
"""
Demonstração da Interface Web do Sistema de Gêmeo Digital.

Este script executa uma demonstração automatizada da interface,
mostrando todas as funcionalidades principais.
"""
import subprocess
import time
import webbrowser
import os
import sys

def verificar_arquivos():
    """Verifica se todos os arquivos necessários estão presentes."""
    arquivos_necessarios = [
        "interface_web.py",
        "main.py",
        "config.py",
        "requirements_interface.txt"
    ]
    
    print("🔍 Verificando arquivos necessários...")
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return False
        else:
            print(f"✅ {arquivo}")
    
    return True

def instalar_dependencias():
    """Instala as dependências necessárias."""
    print("\n📦 Instalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_interface.txt"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def iniciar_demonstracao():
    """Inicia a demonstração da interface."""
    print("\n🚀 Iniciando demonstração da interface...")
    print("=" * 60)
    print("📱 A interface será aberta no seu navegador")
    print("🌐 URL: http://localhost:8501")
    print("⏹️  Para parar, pressione Ctrl+C")
    print("=" * 60)
    
    try:
        # Iniciar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "interface_web.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Demonstração encerrada pelo usuário.")
    except Exception as e:
        print(f"❌ Erro ao iniciar demonstração: {e}")

def mostrar_instrucoes():
    """Mostra instruções de uso da interface."""
    print("\n📋 INSTRUÇÕES DE USO DA INTERFACE")
    print("=" * 60)
    print("1. ⚙️  Configure os parâmetros na barra lateral")
    print("2. 🔧 Ajuste as configurações das máquinas")
    print("3. 🚀 Clique em 'Executar Simulação'")
    print("4. 📊 Visualize os resultados nos gráficos")
    print("5. 📋 Analise o relatório detalhado")
    print("6. 📥 Baixe o relatório completo")
    print("=" * 60)

def main():
    """Função principal da demonstração."""
    print("🏭 Demonstração da Interface Web - Gêmeo Digital Industrial")
    print("=" * 70)
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("\n❌ Arquivos necessários não encontrados!")
        print("Certifique-se de estar no diretório correto do projeto.")
        return
    
    # Instalar dependências
    if not instalar_dependencias():
        print("\n❌ Falha ao instalar dependências!")
        print("Execute manualmente: pip install -r requirements_interface.txt")
        return
    
    # Mostrar instruções
    mostrar_instrucoes()
    
    # Aguardar confirmação do usuário
    input("\n⏳ Pressione Enter para iniciar a demonstração...")
    
    # Iniciar demonstração
    iniciar_demonstracao()

if __name__ == "__main__":
    main()
