# 🖨️ Printers Getter

Este projeto tem como objetivo coletar informações de impressoras via SNMP e gerar relatórios em CSV, além de fornecer uma interface interativa de visualização usando Streamlit e Plotly.

## 📌 Funcionalidades

- Coleta de dados de impressoras via protocolo SNMP:
  - Número de série
  - Total de páginas impressas
- Armazena os dados coletados em arquivos CSV organizados por data.
- Geração de gráficos interativos com histórico de impressão por impressora.
- Dashboard visual com filtros e agrupamentos.

## 🗂️ Estrutura do Projeto

printers_getter/
├── dados/ # Arquivos CSV gerados com os dados de impressão
├── main.py # Script principal para coleta de dados via SNMP
├── dashboard.py # Aplicação Streamlit com gráficos interativos
├── requirements.txt # Lista de dependências do projeto
└── README.md # Este arquivo

## ⚙️ Requisitos

Instale as dependências com:

```bash
pip install -r requirements.txt
```
Principais bibliotecas utilizadas:

pysnmp — Para comunicação com as impressoras via SNMP

pandas — Para manipulação e análise dos dados

streamlit — Para o dashboard interativo

plotly — Para os gráficos

🚀 Como executar
1. Coletar dados das impressoras
Execute:
```bash
python main.py
```
Os dados serão salvos na pasta dados/, com um CSV.

2. Iniciar o dashboard
Para visualizar os dados em uma interface gráfica:
```bash
streamlit run dashboard.py
```
Isso abrirá uma página no navegador com os gráficos e filtros interativos.

📝 Observações
As OIDs SNMP utilizadas são:

Total de páginas: 1.3.6.1.2.1.43.10.2.1.4.1.1

Número de série: 1.3.6.1.2.1.43.5.1.1.17.1

Certifique-se de que as impressoras estão acessíveis via SNMP na rede.

O projeto pode ser expandido para coletar mais informações no futuro.

👨‍💻 Autor
Desenvolvido por Gabriel Paiva
🔗 github.com/GabrielPaivaM
