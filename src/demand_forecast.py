import pandas as pd
from sklearn.metrics import mean_absolute_error

df_vendas = pd.read_csv('datasets/vendas_2023_2024.csv')
df_produtos = pd.read_csv('datasets/produtos_raw.csv')

df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], format='mixed', dayfirst=True)

nome_produto = 'Motor de Popa Yamaha Evo Dash 155HP'
produto_alvo = df_produtos[df_produtos['name'] == nome_produto]

id_motor = produto_alvo['code'].iloc[0]
df_motor = df_vendas[df_vendas['id_product'] == id_motor]

df_diario = df_motor.groupby(df_motor['sale_date'].dt.date)['qtd'].sum().reset_index()
df_diario['sale_date'] = pd.to_datetime(df_diario['sale_date'])

data_inicio = df_vendas['sale_date'].min()
data_fim = pd.to_datetime('2024-01-31') 
calendario = pd.date_range(start=data_inicio, end=data_fim)

df_completo = pd.DataFrame({'sale_date': calendario})
df_completo = df_completo.merge(df_diario, on='sale_date', how='left').fillna(0)

df_completo['previsao_mm7'] = df_completo['qtd'].shift(1).rolling(window=7, min_periods=1).mean().fillna(0)

df_teste = df_completo[(df_completo['sale_date'] >= '2024-01-01') & (df_completo['sale_date'] <= '2024-01-31')]

mae = mean_absolute_error(df_teste['qtd'], df_teste['previsao_mm7'])

print(f"MAE para Janeiro de 2024: {mae:.2f} unidades de erro em média por dia.")
print(df_teste[['sale_date', 'qtd', 'previsao_mm7']].head())
