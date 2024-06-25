import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Adatok betöltése
hiany_tetelek = pd.read_csv('hiany_tetelek.csv', encoding='utf-8', sep=';')
tobblet_tetelek = pd.read_csv('tobblet_tetelek.csv', encoding='utf-8', sep=';')
tanito_adat = pd.read_csv('tanito_adat.csv', encoding='utf-8', sep=';')

# Adatok előkészítése
tanito_adat['hiany_es_tobblet'] = tanito_adat.apply(lambda row: str(row['hiany_id']) + '_' + str(row['tobblet_id']), axis=1)
X = tanito_adat[['hiany_id', 'tobblet_id']]
y = tanito_adat['hiany_es_tobblet']

# Adatok felosztása tanító és tesztelő halmazokra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.head())

# Modell létrehozása és tanítása
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Modell kiértékelése a teszt adathalmazon
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')