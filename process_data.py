import pandas as pd
import glob

files = glob.glob('data/*.csv')
dfs = [pd.read_csv(f) for f in files]

df = pd.concat(dfs, ignore_index=True)

df = df[df['product'] == 'pink morsel']

df['price'] = df['price'].str.replace('$', '').astype(float)
df['sales'] = df['quantity'] * df['price']

df = df[['sales', 'date', 'region']]

df.to_csv('data/output.csv', index=False)

print("Done! Output saved to data/output.csv")