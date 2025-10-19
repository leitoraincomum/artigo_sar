import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações de plotagem
sns.set_theme(style="whitegrid")

# ==============================================================================
# 1. Carregamento e Limpeza (Engenharia de Dados)
# ==============================================================================

# Carrega o CSV, especificando o delimitador ';' e ignorando linhas malformadas
df = pd.read_csv(
    'obras.csv', 
    delimiter=';', 
    on_bad_lines='skip'
)

# 1.1. Limpeza e conversão de 'Valor do Contrato'
# Remove o ponto (separador de milhar) e troca a vírgula (separador decimal) por ponto
df['Valor do Contrato'] = (
    df['Valor do Contrato']
    .astype(str)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
)

# Converte para float, transformando erros em NaN
df['Valor do Contrato'] = pd.to_numeric(df['Valor do Contrato'], errors='coerce')

# Remove as linhas que não conseguiram ser convertidas
df.dropna(subset=['Valor do Contrato'], inplace=True)

# 1.2. Padronização de 'Âmbito'
df['Âmbito'] = df['Âmbito'].str.strip().str.upper()

# ==============================================================================
# 2. Agregação e Cálculo
# ==============================================================================

# Agrupa por Ano e Âmbito e soma o Valor do Contrato
soma_por_ano_e_ambito = df.groupby(['Ano do Contrato', 'Âmbito'])['Valor do Contrato'].sum().reset_index()

# Coluna auxiliar para o gráfico em Bilhões
soma_por_ano_e_ambito['R$_Bilhoes'] = soma_por_ano_e_ambito['Valor do Contrato'] / 1_000_000_000

# ==============================================================================
# 3. Plotagem (Tendência Comparativa)
# ==============================================================================

plt.figure(figsize=(12, 7))

# Cria o gráfico de linhas, usando 'Âmbito' para definir as cores
sns.lineplot(
    data=soma_por_ano_e_ambito, 
    x='Ano do Contrato', 
    y='R$_Bilhoes', 
    hue='Âmbito', # Separa as linhas por Âmbito
    marker='o', 
    linewidth=2
)

# Configuração de títulos e eixos
plt.title('Tendência Anual de Investimento em Obras (R$ Bilhões) por Âmbito', fontsize=16)
plt.xlabel('Ano do Contrato', fontsize=12)
plt.ylabel('Valor Total do Contrato (R$ Bilhões)', fontsize=12)

# Garante que apenas anos inteiros apareçam no eixo X
anos = soma_por_ano_e_ambito['Ano do Contrato'].astype(int).unique()
plt.xticks(anos)

plt.legend(title='Âmbito', loc='upper left')
plt.grid(True, axis='y', linestyle='--')
plt.tight_layout()

# Salva o gráfico
plt.savefig('investimento_anual_por_ambito.png')