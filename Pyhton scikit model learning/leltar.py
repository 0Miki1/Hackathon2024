import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Hiány és többlet tételek betöltése
hiany_tetelek = pd.read_csv("hiany_tetelek.csv", encoding='utf-8', sep=';')
tobblet_tetelek = pd.read_csv("tobblet_tetelek.csv", encoding='utf-8', sep=';')

#Adatok összefűzése
all_data = pd.concat([
    # hiany_tetelek[['hiany_eszkoznev', 'hiany_muszakicsopnev']].rename(columns={'hiany_eszkoznev': 'eszkoznev', 'hiany_muszakicsopnev': 'muszakicsopnev'}),
    # tobblet_tetelek[['tobblet_eszkoznev', 'toblet_muszakicsopnev']].rename(columns={'tobblet_eszkoznev': 'eszkoznev', 'toblet_muszakicsopnev': 'muszakicsopnev'})
    hiany_tetelek[['hiany_eszkoznev', 'hiany_muszakicsop', 'hiany_muszakicsopnev']].rename(columns={'hiany_eszkoznev': 'eszkoznev', 'hiany_muszakicsop': 'muszakicsop', 'hiany_muszakicsopnev': 'muszakicsopnev'}),
    tobblet_tetelek[['tobblet_eszkoznev', 'tobblet_muszakicsop', 'toblet_muszakicsopnev']].rename(columns={'tobblet_eszkoznev': 'eszkoznev', 'tobblet_muszakicsop': 'muszakicsop','toblet_muszakicsopnev': 'muszakicsopnev'})
])

#Vektorizálás
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_data['eszkoznev'] + ' ' + all_data['muszakicsop'] + ' ' + all_data['muszakicsopnev'])

#Klaszterezés
kmeans = KMeans(n_clusters=3, random_state=0).fit(tfidf_matrix)
all_data['cluster'] = kmeans.labels_

#Klaszterezés szerinti szétválogatás
hiany_tetelek['cluster'] = kmeans.predict(vectorizer.transform(hiany_tetelek['hiany_eszkoznev'] + ' ' + hiany_tetelek['hiany_muszakicsop'] + ' ' + hiany_tetelek['hiany_muszakicsopnev']))
tobblet_tetelek['cluster'] = kmeans.predict(vectorizer.transform(tobblet_tetelek['tobblet_eszkoznev'] + ' ' + tobblet_tetelek['tobblet_muszakicsop'] + ' ' + tobblet_tetelek['toblet_muszakicsopnev']))

#Párok keresése
javaslatok = []
for cluster in set(hiany_tetelek['cluster']):
    hiany_cluster = hiany_tetelek[hiany_tetelek['cluster'] == cluster]
    tobblet_cluster = tobblet_tetelek[tobblet_tetelek['cluster'] == cluster]
    
    if not hiany_cluster.empty and not tobblet_cluster.empty:
        hiany_vectors = vectorizer.transform(hiany_cluster['hiany_eszkoznev'] + ' ' + hiany_cluster['hiany_muszakicsopnev'])
        tobblet_vectors = vectorizer.transform(tobblet_cluster['tobblet_eszkoznev'] + ' ' + tobblet_cluster['toblet_muszakicsopnev'])
        
        similarities = cosine_similarity(hiany_vectors, tobblet_vectors)
        
        for i, hiany_index in enumerate(hiany_cluster.index):
            top_matches = similarities[i].argsort()[-2:][::-1]  # Az első öt legjobb találat
            for match in top_matches:
                javaslat = {
                    'hiany_id': hiany_tetelek.loc[hiany_index, 'hiany_id'],
                    'hiany_eszkoznev': hiany_tetelek.loc[hiany_index, 'hiany_eszkoznev'],
                    'hiany_muszakicsop': hiany_tetelek.loc[hiany_index, 'hiany_muszakicsop'],
                    'hiany_muszakicsopnev': hiany_tetelek.loc[hiany_index, 'hiany_muszakicsopnev'],
                    'tobblet_id': tobblet_tetelek.loc[tobblet_cluster.index[match], 'tobblet_id'],
                    'tobblet_eszkoznev': tobblet_tetelek.loc[tobblet_cluster.index[match], 'tobblet_eszkoznev'],
                    'tobblet_muszakicsop': tobblet_tetelek.loc[tobblet_cluster.index[match], 'tobblet_muszakicsop'],
                    'toblet_muszakicsopnev': tobblet_tetelek.loc[tobblet_cluster.index[match], 'toblet_muszakicsopnev']
                }
                javaslatok.append(javaslat)

# Javaslatok kiírása CSV fájlba
javaslatok_df = pd.DataFrame(javaslatok)
javaslatok_df.to_csv('javasolt_parok.csv', index=False, encoding='utf_8_sig', sep=';')

print("A párosítási javaslatok CSV fájlba lettek mentve.")