import json

import pandas as pd

with open('datasets/custos_importacao.json', 'r') as f:
    import_costs = json.load(f)

line = {}
lines = []
columns = ['product_id', 'product_name', 'category', 'start_date', 'usd_price']
for elem in import_costs:
    for i in range(len(elem['historic_data'])):
        line['product_id'] = elem['product_id']
        line['product_name'] = elem['product_name']
        line['category'] = elem['category']
        line['start_date'] = elem['historic_data'][i]['start_date']
        line['usd_price'] = elem['historic_data'][i]['usd_price']
        lines.append(line.copy())
        
df = pd.DataFrame(lines)
df['start_date'] = pd.to_datetime(df['start_date'], dayfirst=True)
df.to_csv('datasets/custos_importacao.csv', sep=',', index=False,)