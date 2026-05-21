import streamlit as st
import pandas as pd
import os

st.title("🍲 Katalog Nutrisi Makanan Balita")
st.write("Halaman ini menampilkan daftar lengkap referensi menu makanan beserta kandungan gizi makro dan mikronya berdasarkan dataset terverifikasi.")

st.markdown("---")

# Definisikan jalur file CSV makanan
csv_path = os.path.join("dataset", "foods.csv")

if os.path.exists(csv_path):
    # Membaca data makanan menggunakan pandas
    df_foods = pd.read_csv(csv_path)
    
    # Menghapus kolom indeks bawaan jika tidak sengaja terbaca
    if "Unnamed: 0" in df_foods.columns:
        df_foods = df_foods.drop(columns=["Unnamed: 0"])
        
    # Fitur Pencarian Interaktif
    search_query = st.text_input("🔍 Cari Nama Menu Makanan:", placeholder="Ketik kata kunci, contoh: bubur, sup, susu, telur...")
    
    # Filter data berdasarkan pencarian
    if search_query:
        df_filtered = df_foods[df_foods['Menu'].str.contains(search_query, case=False, na=False)]
    else:
        df_filtered = df_foods

    # Menampilkan total data hasil filter
    st.write(f"Menampilkan **{len(df_filtered)}** dari total {len(df_foods)} pilihan menu makanan.")
    
    # Tampilkan tabel interaktif Streamlit yang bisa di-scroll dan disortir kolomnya
    st.dataframe(df_filtered, use_container_width=True)
    
else:
    st.error("❌ Gagal memuat katalog. File 'dataset/foods.csv' tidak ditemukan. Pastikan penamaan folder Anda sudah benar.")