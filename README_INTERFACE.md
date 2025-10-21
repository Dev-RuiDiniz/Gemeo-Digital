# 🌐 Interface Web - Sistema de Gêmeo Digital Industrial

## 📋 Visão Geral

Esta interface web fornece uma experiência visual intuitiva para o sistema de Gêmeo Digital Industrial, permitindo que clientes finais visualizem e interajam com simulações de forma simples e eficiente.

## 🚀 Características Principais

### 🎨 **Interface Moderna**
- Design responsivo e intuitivo
- Gráficos interativos com Plotly
- Visualizações em tempo real
- Dashboard personalizável

### 📊 **Visualizações Avançadas**
- Gráficos de tempos de operação
- Análise de eficiência das máquinas
- Identificação de gargalos
- Previsões dos modelos de IA

### ⚙️ **Configuração Flexível**
- Parâmetros ajustáveis via interface
- Configuração de máquinas personalizada
- Duração de simulação configurável
- Número de máquinas variável

### 📈 **Métricas em Tempo Real**
- Total de ciclos completados
- Eficiência da linha de produção
- Identificação de gargalos
- Melhoria da otimização

## 🛠️ Instalação e Configuração

### 1. **Instalar Dependências**
```bash
pip install -r requirements_interface.txt
```

### 2. **Executar Interface**
```bash
python iniciar_interface.py
```

### 3. **Acessar Interface**
Abra seu navegador e acesse: `http://localhost:8501`

## 📱 Como Usar

### **1. Configuração Inicial**
- Ajuste a duração da simulação (1-24 horas)
- Configure o número de máquinas (2-6)
- Defina parâmetros individuais para cada máquina

### **2. Parâmetros das Máquinas**
Para cada máquina, configure:
- **Tempo Mínimo**: Tempo mínimo de operação (horas)
- **Tempo Máximo**: Tempo máximo de operação (horas)
- **Eficiência**: Eficiência da máquina (0.5-1.0)
- **Taxa de Falha**: Probabilidade de falha por hora

### **3. Execução da Simulação**
- Clique em "🚀 Executar Simulação"
- Aguarde o processamento
- Visualize os resultados em tempo real

## 📊 Funcionalidades da Interface

### **📈 Métricas Principais**
- **Total de Ciclos**: Número de ciclos completados
- **Eficiência da Linha**: Performance geral do sistema
- **Gargalo**: Máquina que limita a produção
- **Melhoria da Otimização**: Percentual de melhoria obtida

### **📊 Gráficos Interativos**
- **Tempos de Operação**: Evolução dos tempos ao longo dos ciclos
- **Eficiência das Máquinas**: Comparação de performance
- **Análise de Gargalos**: Frequência de gargalos por máquina
- **Previsões**: Tempos previstos para próximos ciclos

### **📋 Relatório Detalhado**
- Estatísticas completas de cada máquina
- Métricas de disponibilidade e inatividade
- Dados de performance histórica
- Download do relatório em JSON

## 🎯 Casos de Uso

### **🏭 Gestores de Produção**
- Monitorar eficiência da linha
- Identificar gargalos de produção
- Otimizar tempos de operação
- Planejar manutenções

### **📊 Analistas de Dados**
- Analisar tendências de performance
- Validar modelos preditivos
- Comparar cenários diferentes
- Gerar relatórios detalhados

### **🔧 Engenheiros de Processo**
- Simular diferentes configurações
- Testar melhorias de eficiência
- Avaliar impacto de mudanças
- Otimizar processos

## ⚙️ Configurações Avançadas

### **Arquivo de Configuração**
Edite `config_interface.json` para personalizar:
- Tema da interface
- Parâmetros padrão
- Configurações de gráficos
- Opções de relatórios

### **Personalização Visual**
- Cores dos gráficos
- Tamanhos das visualizações
- Temas dos gráficos
- Layout da interface

## 🔧 Solução de Problemas

### **Erro de Dependências**
```bash
pip install --upgrade -r requirements_interface.txt
```

### **Porta em Uso**
```bash
streamlit run interface_web.py --server.port 8502
```

### **Problemas de Performance**
- Reduza a duração da simulação
- Diminua o número de máquinas
- Ajuste os parâmetros de configuração

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique os logs no terminal
- Consulte a documentação do sistema
- Entre em contato com a equipe de desenvolvimento

## 🚀 Próximas Funcionalidades

- **Histórico de Simulações**: Salvar e carregar simulações anteriores
- **Comparação de Cenários**: Comparar múltiplas configurações
- **Alertas em Tempo Real**: Notificações de problemas
- **Exportação Avançada**: Relatórios em PDF e Excel

---

**Interface desenvolvida com ❤️ para facilitar o uso do Sistema de Gêmeo Digital Industrial**
