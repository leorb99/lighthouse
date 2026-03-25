import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df_vendas = pd.read_csv('datasets/vendas_2023_2024.csv')
df_produtos = pd.read_csv('datasets/produtos_raw.csv')

nome_referencia = 'GPS Garmin Vortex Maré Drift'
produto_alvo = df_produtos[df_produtos['name'] == nome_referencia]
id_gps = produto_alvo['code'].iloc[0]

interacoes = df_vendas[['id_client', 'id_product']].drop_duplicates()
interacoes['comprou'] = 1

matriz_interacao = interacoes.pivot(
    index='id_client', 
    columns='id_product', 
    values='comprou'
).fillna(0)

matriz_produtos = matriz_interacao.T
matriz_similaridade = cosine_similarity(matriz_produtos)

df_similaridade = pd.DataFrame(
    matriz_similaridade, 
    index=matriz_produtos.index, 
    columns=matriz_produtos.index
)

similaridade_gps = df_similaridade[id_gps]

df_ranking = similaridade_gps.reset_index()
df_ranking.columns = ['id_product', 'score_similaridade']

df_ranking = df_ranking[df_ranking['id_product'] != id_gps]

top_5_similares = df_ranking.sort_values(
    by='score_similaridade', 
    ascending=False
).head(5) # type: ignore

top_5_recomendacoes = top_5_similares.merge(
    df_produtos[['code', 'name']], 
    left_on='id_product', 
    right_on='code', 
    how='left'
)

print(f"Produto de Referência: {nome_referencia} (ID: {id_gps})\n")
print("Top 5 Produtos Recomendados:")

for i, row in enumerate(top_5_recomendacoes.itertuples(), start=1):
    print(f"{i}º -> {row.name} (Score: {row.score_similaridade:.4f})")