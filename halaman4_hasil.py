import streamlit as st
import pandas as pd
import os

st.title("📊 Hasil Diagnosis & Rekomendasi Menu")
st.markdown("---")

# 1. Validasi data input dari halaman konsultasi
if "user_inputs" not in st.session_state or "data_balita" not in st.session_state:
    st.warning("⚠️ Belum ada data konsultasi. Silakan masuk ke menu **Konsultasi Gizi** terlebih dahulu dan tekan tombol Analisis!")
else:
    balita = st.session_state.data_balita
    user_inputs = st.session_state.user_inputs
    rules_data = st.session_state.rules_data

    # Tampilkan identitas balita
    st.subheader("📋 Informasi Balita")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Nama:** {balita['nama']}")
    with col2:
        st.write(f"**Usia:** {balita['usia']} Bulan")
    with col3:
        st.write(f"**Jenis Kelamin:** {balita['jk']}")
        
    st.markdown("---")

    # ==========================================
    # LOGIKA PERHITUNGAN CERTAINTY FACTOR (CF)
    # ==========================================
    
    # Langkah 1 & 2: Hitung CF tunggal (CF [H,E] = CF User * CF Pakar)
    cf_tunggal = []
    for item in rules_data:
        cf_user = user_inputs[item['id_gejala']]
        if cf_user > 0:  # Hanya proses gejala yang dialami
            cf_he = cf_user * item['cf_pakar']
            cf_tunggal.append({
                "penyakit": item['penyakit'],
                "cf_nilai": cf_he
            })

    # Langkah 3: Kombinasikan nilai CF untuk penyakit yang sama (CF Combine)
    # Rumus: CF_combine = CF_lama + CF_baru * (1 - CF_lama)
    cf_combine_results = {}
    for item in cf_tunggal:
        penyakit = item['penyakit']
        cf_baru = item['cf_nilai']
        
        if penyakit not in cf_combine_results:
            cf_combine_results[penyakit] = cf_baru
        else:
            cf_lama = cf_combine_results[penyakit]
            # Skenario rumus CF Combine untuk nilai positif
            cf_combine_results[penyakit] = cf_lama + cf_baru * (1 - cf_lama)

    # Urutkan hasil dari persentase kepastian tertinggi
    hasil_terurut = sorted(cf_combine_results.items(), key=lambda x: x[1], reverse=True)

    if not hasil_terurut:
        st.success("🎉 Berdasarkan gejala yang dimasukkan, balita Anda dalam kondisi **Sehat** dan tidak terindikasi masalah malnutrisi gizi makro/mikro!")
    else:
        st.subheader("🩺 Hasil Analisis Kepastian Gizi")
        
        # Tampilkan diagnosis utama (tertinggi)
        diagnosis_utama = hasil_terurut[0][0]
        skor_kepastian = hasil_terurut[0][1] * 100
        
        st.error(f"Kesimpulan: Balita terindikasi mengalami **{diagnosis_utama}** dengan tingkat kepastian **{skor_kepastian:.2f}%**.")

        # Tampilkan grafik semua indikasi kondisi yang terdeteksi
        st.write("Daftar persentase indikasi masalah gizi lainnya:")
        chart_data = pd.DataFrame([
            {"Masalah Gizi": k, "Persentase Kepastian (%)": v * 100} for k, v in hasil_terurut
        ]).set_index("Masalah Gizi")
        st.bar_chart(chart_data)

        st.markdown("---")
        
        # ==========================================
        # INTEGRASI INTEGRAL DATASET FOODS.CSV (REKOMENDASI)
        # ==========================================
        st.subheader("🍲 Rekomendasi Menu Solutif")
        st.write(f"Berikut adalah daftar menu makanan terbaik untuk membantu memulihkan/menyeimbangkan kondisi **{diagnosis_utama}**:")

        # Tentukan kolom filter berdasarkan diagnosis utama
        kolom_target = ""
        ascending_sort = False # Default: urutkan dari yang gizi tertinggi

        if diagnosis_utama == "Kekurangan Energi":
            kolom_target = "Energy (kJ)"
        elif diagnosis_utama == "Kekurangan Protein":
            kolom_target = "Protein (g)"
        elif diagnosis_utama == "Kekurangan Lemak (Fat)":
            kolom_target = "Fat (g)"
        elif diagnosis_utama == "Kekurangan Serat (Dietary Fiber)":
            kolom_target = "Dietary Fiber (g)"
        elif diagnosis_utama == "Kekurangan Vitamin A":
            kolom_target = "Vitamin A (mg)"
        elif diagnosis_utama == "Kekurangan Vitamin C":
            kolom_target = "Vitamin C (mg)"
        elif diagnosis_utama == "Kekurangan Magnesium":
            kolom_target = "Magnesium (mg)"
        elif diagnosis_utama == "Kekurangan Zat Besi (Iron)":
            kolom_target = "Iron (mg)"
        elif diagnosis_utama == "Kelebihan Energi & Karbohidrat":
            kolom_target = "Carbohydrates (g)"
            ascending_sort = True # Kalau kelebihan, cari yang kandungan karbohidratnya paling rendah
        elif diagnosis_utama == "Kelebihan Serat (Dietary Fiber)":
            kolom_target = "Dietary Fiber (g)"
            ascending_sort = True # Cari yang paling rendah seratnya
        elif diagnosis_utama == "Kelebihan Vitamin C / Vitamin E":
            kolom_target = "Vitamin C (mg)"
            ascending_sort = True

        # Membaca file CSV makanan
        csv_path = os.path.join("dataset", "foods.csv")
        
        if os.path.exists(csv_path):
            df_foods = pd.read_csv(csv_path)
            
            # Bersihkan baris kosong dan urutkan berdasarkan target zat gizi
            if kolom_target in df_foods.columns:
                df_rekomendasi = df_foods[["Menu", kolom_target]].sort_values(by=kolom_target, ascending=ascending_sort)
                # Ambil 5 teratas
                top_5_foods = df_rekomendasi.head(5).reset_index(drop=True)
                
                # Tampilkan tabel rekomendasi makanan
                st.table(top_5_foods)
                st.info("💡 **Catatan Pakar:** Berikan variasi menu di atas secara terjadwal porsinya agar tumbuh kembang balita kembali optimal.")
            else:
                st.error(f"Kolom nutrisi '{kolom_target}' tidak ditemukan di dataset.")
        else:
            st.error("Gagal memuat rekomendasi menu. File 'dataset/foods.csv' tidak ditemukan.")