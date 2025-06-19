import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

print("1. Memuat dataset pasien penyakit jantung...")
try:
    df = pd.read_csv("heart_disease_patients.csv")
    print("Dataset berhasil dimuat!")
    print(f"Jumlah pasien: {len(df)}")
    print(f"Fitur yang tersedia: {list(df.columns)}")
except FileNotFoundError:
    print("Error: File dataset tidak ditemukan.")
    exit()

print("\n2. Eksplorasi data awal:")
print("5 pasien pertama:")
print(df.head())
print("\nStatistik deskriptif:")
print(df.describe())
print("\nInformasi dataset:")
print(df.info())

print("\n3. Pra-pemrosesan data...")

fitur_numerik = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
df_numerik = df[fitur_numerik].copy()

print("\nMenangani nilai yang hilang...")
for col in df_numerik.columns:
    if df_numerik[col].isnull().sum() > 0:
        median_val = df_numerik[col].median()
        df_numerik[col].fillna(median_val, inplace=True)
        print(f"Kolom {col}: {df_numerik[col].isnull().sum()} nilai kosong diisi dengan median {median_val:.1f}")

print("\n4. Melakukan penskalaan fitur...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_numerik)
df_scaled = pd.DataFrame(X_scaled, columns=df_numerik.columns)

print("\nData setelah diskalakan (5 baris pertama):")
print(df_scaled.head())

print("\n5. Menentukan jumlah klaster optimal dengan metode Elbow...")
sse = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(df_scaled)
    sse.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(k_range, sse, marker='o', linestyle='--')
plt.title('Metode Elbow untuk Menentukan Jumlah Klaster Optimal')
plt.xlabel('Jumlah Klaster (K)')
plt.ylabel('Sum of Squared Errors (SSE)')
plt.xticks(k_range)
plt.grid()
plt.show()

optimal_k = 3  
print(f"\n6. Melakukan clustering dengan K={optimal_k}...")

kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(df_scaled)

df['cluster'] = clusters

print("\n7. Analisis hasil clustering:")

print("\nDistribusi pasien per klaster:")
print(df['cluster'].value_counts())

pca = PCA(n_components=2)
principal_components = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
df_pca['cluster'] = clusters

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='cluster', palette='viridis', s=100)
plt.title('Visualisasi Klaster Pasien Penyakit Jantung (PCA)')
plt.grid()
plt.show()

print("\n8. Profil rata-rata setiap klaster:")
fitur_analisis = fitur_numerik + ['target']
cluster_profile = df.groupby('cluster')[fitur_analisis].mean()
print(cluster_profile)

plt.figure(figsize=(12, 6))
cluster_profile.plot(kind='bar', figsize=(14, 6))
plt.title('Profil Rata-Rata Klaster Pasien Penyakit Jantung')
plt.ylabel('Nilai Rata-Rata')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()

print("\n9. Interpretasi klaster berdasarkan profil:")

interpretasi = {
    0: "Klaster Risiko Rendah: Usia lebih muda, tekanan darah dan kolesterol normal",
    1: "Klaster Risiko Sedang: Kolesterol tinggi tapi detak jantung maksimal baik",
    2: "Klaster Risiko Tinggi: Tekanan darah tinggi, kolesterol tinggi, dan ST depression"
}

for klaster, desc in interpretasi.items():
    print(f"\nKlaster {klaster}:")
    print(desc)
    print("Karakteristik utama:")
    print(f"- Usia rata-rata: {cluster_profile.loc[klaster, 'age']:.1f} tahun")
    print(f"- Tekanan darah istirahat: {cluster_profile.loc[klaster, 'trestbps']:.1f} mmHg")
    print(f"- Kolesterol: {cluster_profile.loc[klaster, 'chol']:.1f} mg/dl")
    print(f"- Detak jantung maksimal: {cluster_profile.loc[klaster, 'thalach']:.1f} bpm")
    print(f"- ST Depression: {cluster_profile.loc[klaster, 'oldpeak']:.1f} mm")
    if 'target' in cluster_profile.columns:
        print(f"- Persentase penyakit jantung: {cluster_profile.loc[klaster, 'target']*100:.1f}%")

output_file = "hasil_clustering_jantung.csv"
df.to_csv(output_file, index=False)
print(f"\n10. Hasil analisis disimpan dalam file: {output_file}")

print("\n=== ANALISIS SELESAI ===")