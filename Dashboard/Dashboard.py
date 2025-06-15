import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset
# jantung_data = pd.read_csv("Data_Bersih.csv")
jantung_data = pd.read_csv("./Dashboard/Data_Bersih.csv")

 
    # Menambahkan judul dan subjudul
st.title('Proyek Akhir: Analisis Data jantung :heart:')
st.header('Nama:') # Ini adalah header utama
st.write('M Arief Wiguna | 231712084')
st.write('Muhammad Bagas Dwi Syahputra | 231712074')
st.write('Naufal Alfatih Amriansyah | 231712105')

st.header('Proyek Akhir: Analisis Data jantung :heart:')
st.subheader('1. Distribusi Kolesterol Berdasarkan Kategori Usia')

st.write('''
Berdasarkan boxplot di bawah ini, terlihat bahwa distribusi kolesterol relatif mirip di antara ketiga kelompok usia (Muda, Paruh Baya, dan Lansia).
Namun, kelompok **Paruh Baya** menunjukkan kecenderungan memiliki nilai kolesterol yang sedikit lebih tinggi pada nilai tengah (median) dibanding dua kelompok lainnya.

Selain itu, semua kelompok usia memiliki **outlier** kolesterol tinggi, yang menandakan adanya individu dengan risiko kolesterol tinggi di semua rentang usia.

Hal ini menunjukkan bahwa kolesterol tinggi bukan hanya risiko di usia lanjut, tetapi juga dapat terjadi pada usia paruh baya dan bahkan usia muda.
''')

# Visualisasi Boxplot
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=jantung_data, x='KategoriUsia', y='Cholesterol', ax=ax)
ax.set_title('Distribusi Kolesterol berdasarkan Kategori Usia')
ax.set_xlabel('Kategori Usia')
ax.set_ylabel('Kolesterol')
st.pyplot(fig)

st.subheader('2. Analisis Usia dan Gender terhadap Penyakit Jantung')

st.write('''
Berdasarkan visualisasi di bawah ini, terlihat bahwa kelompok **Paruh Baya** adalah yang paling banyak menderita penyakit jantung,
baik pada laki-laki maupun perempuan.

Namun, secara keseluruhan, **jumlah penderita laki-laki jauh lebih tinggi** dibanding perempuan.

Hal ini diperkuat dengan diagram pie di bawah, yang menunjukkan bahwa sekitar **90% penderita penyakit jantung adalah laki-laki**,
sementara hanya sekitar **10% adalah perempuan**. Ini mengindikasikan bahwa laki-laki memiliki risiko yang jauh lebih tinggi terkena penyakit jantung dalam dataset ini.
''')

# Hitung total pasien dan jumlah penderita per kombinasi Gender dan KategoriUsia
summary_table = jantung_data.groupby(['Gender', 'KategoriUsia']).agg(
    total_pasien=('HeartDisease', 'count'),
    penderita=('HeartDisease', 'sum')
).reset_index()

# Hitung persentase
summary_table['persentase_penderita'] = (summary_table['penderita'] / summary_table['total_pasien']) * 100

# Tampilkan tabel
summary_table.columns = ['Gender', 'Kategori Usia', 'Jumlah Pasien', 'Jumlah Penderita', 'Persentase Penderita (%)']
st.write("### Tabel Distribusi Penyakit Jantung Berdasarkan Gender dan Kategori Usia")
st.dataframe(summary_table)

# Barplot usia vs penyakit jantung berdasarkan gender
fig = sns.catplot(
    data=jantung_data,
    x='KategoriUsia',
    hue='HeartDisease',
    col='Gender',
    kind='count',
    height=4,
    aspect=1
)

# Tampilkan ke Streamlit
st.pyplot(fig)

# Pie Chart Persentase penderita berdasarkan gender
jantung_positif = jantung_data[jantung_data['HeartDisease'] == 1]
gender_dist = jantung_positif['Gender'].value_counts(normalize=True) * 100

fig2, ax = plt.subplots(figsize=(6, 6))
colors = ['#66b3ff', '#ff9999']
ax.pie(gender_dist, labels=gender_dist.index.map({'M': 'Laki-laki', 'F': 'Perempuan'}),
       autopct='%1.1f%%', startangle=90, colors=colors, explode=(0.05, 0))
ax.set_title('Persentase Penderita Penyakit Jantung Berdasarkan Gender')
ax.axis('equal')
st.pyplot(fig2)

st.subheader('3. Nilai Oldpeak Tertinggi Berdasarkan Usia')
st.write('''
Berdasarkan grafik boxplot di bawah ini, terlihat bahwa kelompok usia **Lansia** memiliki nilai *Oldpeak* yang cenderung lebih tinggi dibandingkan kelompok usia lainnya. 
*Oldpeak* sendiri merupakan indikator depresi segmen ST pada elektrokardiogram (EKG) setelah aktivitas fisik.

Nilai *Oldpeak* yang tinggi menunjukkan adanya kemungkinan iskemia miokard, atau berkurangnya aliran darah ke jantung. Dengan demikian, dapat disimpulkan bahwa kelompok lansia lebih berisiko mengalami gangguan jantung yang ditandai dengan peningkatan nilai *Oldpeak*.
''')

# Visualisasi boxplot Oldpeak
fig3, ax3 = plt.subplots()
sns.boxplot(data=jantung_data, x='KategoriUsia', y='Oldpeak', ax=ax3)
st.pyplot(fig3)


st.subheader('4. Distribusi ExerciseAngina Berdasarkan Usia')
st.write('''
Grafik batang berikut menunjukkan distribusi kondisi angina saat olahraga (*ExerciseAngina*) berdasarkan kategori usia. Terlihat bahwa kelompok usia **Lansia** memiliki jumlah penderita angina saat berolahraga yang cukup signifikan.

Hal ini mengindikasikan bahwa lansia cenderung lebih sering mengalami nyeri dada selama aktivitas fisik, yang merupakan gejala umum penyakit jantung koroner. Sementara itu, kelompok usia muda jauh lebih jarang mengalami kondisi ini, menunjukkan tingkat kebugaran jantung yang relatif lebih baik.
''')

# Visualisasi countplot ExerciseAngina
fig4, ax4 = plt.subplots()
sns.countplot(data=jantung_data, x='KategoriUsia', hue='ExerciseAngina', ax=ax4)
st.pyplot(fig4)

st.subheader('5. Distribusi Jenis Nyeri Dada Berdasarkan Gender')
st.write('Pria lebih sering mengalami nyeri dada tipe Typical Angina, sedangkan wanita cenderung memiliki distribusi yang lebih merata di semua jenis nyeri dada.')

# Visualisasi
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=jantung_data, x='Gender', hue='ChestPainType', ax=ax)
plt.title('Distribusi Chest Pain Type berdasarkan Gender')
plt.xlabel('Gender')
plt.ylabel('Jumlah')
plt.legend(title='Chest Pain Type')
st.pyplot(fig)