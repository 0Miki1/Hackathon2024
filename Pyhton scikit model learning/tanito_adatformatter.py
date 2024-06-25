import pandas as pd

# Tanító adat betöltése
tanito_adat = pd.read_csv('tanito_adat.csv', sep=';')

# Hiany_es_tobblet oszlop létrehozása
tanito_adat['hiany_es_tobblet'] = tanito_adat.apply(lambda row: f"{row['hiany_id']}_{row['tobblet_id']}", axis=1)

print(tanito_adat.head())  # Ellenőrzés céljából