import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Mengatur tema untuk seaborn
sns.set_theme(style="whitegrid")

@st.cache_data
def load_data():
    # Memuat data gabungan
    all_data_df = pd.read_csv('all_data.csv')  # Sesuaikan path ke file CSV Anda

    # Mengonversi 'dteday' menjadi format datetime
    all_data_df['dteday'] = pd.to_datetime(all_data_df['dteday'])

    # Menghapus baris di mana 'dteday' adalah NaT (Not a Time) setelah konversi, jika ada
    all_data_df.dropna(subset=['dteday'], inplace=True)

    # Memetakan nilai 'weathersit' ke label yang sesuai
    weather_mapping = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan Ringan'}
    all_data_df['weathersit'] = all_data_df['weathersit'].map(weather_mapping)
    return all_data_df

# Memuat data
all_data_df = load_data()

# Sidebar Streamlit untuk input pengguna
with st.sidebar:
    # Menampilkan gambar
    st.image('logo sepeda.png')  # Sesuaikan path jika diperlukan
    # Input tanggal untuk memilih rentang tanggal
    start_date, end_date = st.date_input(
        "Pilih Rentang Tanggal",
        [all_data_df["dteday"].min(), all_data_df["dteday"].max()],
        min_value=all_data_df["dteday"].min(),
        max_value=all_data_df["dteday"].max()
    )
    # Memastikan perbandingan datetime konsisten
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_day_data = all_data_df[(all_data_df['dteday'] >= start_date) & 
                                (all_data_df['dteday'] <= end_date) & 
                                all_data_df['hr'].isna()]

filtered_hour_data = all_data_df[(all_data_df['dteday'] >= start_date) & 
                                 (all_data_df['dteday'] <= end_date) & 
                                 all_data_df['hr'].notna()]

# Warna tunggal untuk konsistensi
bar_color = 'skyblue'

# Judul Utama
st.title("Dashboard Penyewaan Sepeda :sparkles:")

# Menampilkan jumlah total penyewaan sepeda berdasarkan rentang tanggal yang dipilih
total_rentals = filtered_day_data['cnt'].sum()
st.subheader(f"Total : {total_rentals} penyewaan")

# Subheader dan barplot untuk data harian tanpa error bars
st.subheader("Hubungan antara Cuaca dan Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.barplot(data=filtered_day_data, x='weathersit', y='cnt', ax=ax, color=bar_color, ci=None)
ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Situasi Cuaca")
ax.set_xlabel("Situasi Cuaca")
ax.set_ylabel("Rata-Rata Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# Subheader dan barplot untuk data per jam tanpa error bars
st.subheader("Statistik Penyewaan Sepeda per Jam untuk Rentang Tanggal yang Dipilih")
# Mengonversi kolom jam menjadi int untuk pengelompokan
filtered_hour_data['hr'] = filtered_hour_data['hr'].astype(int)
hourly_aggregated = filtered_hour_data.groupby('hr')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=hourly_aggregated, x='hr', y='cnt', ax=ax, color=bar_color, ci=None)
ax.set_title("Total Penyewaan Sepeda per Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Total Jumlah Penyewaan Sepeda")
st.pyplot(fig)
