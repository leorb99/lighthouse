import pandas as pd


def rename_column(text: str):
    if text.startswith('elet'):
        return 'eletrônicos'
    elif text.startswith('prop'):
        return 'propulsão'
    elif text.startswith('enc') or text.startswith('anc'):
        return 'ancoragem'

df_products = pd.read_csv('datasets/produtos_raw.csv')
df_products['code'] = df_products['code'].astype(int)
df_products['price'] = df_products['price'].str.removeprefix('R$ ').astype(float)
df_products['actual_category'] = df_products['actual_category'].str.replace(' ', '').str.lower()
df_products['actual_category'] = df_products['actual_category'].apply(rename_column)
print(len(df_products))
df_products.drop_duplicates(inplace=True)
print(len(df_products))
