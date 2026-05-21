import streamlit as st
import pandas as pd

st.title("⚙️ Kelola Bobot Kepastian Pakar")
st.write("Halaman khusus Admin/Pakar untuk memperbarui nilai Certainty Factor Pakar ($CF_{pakar}$) secara dinamis pada basis aturan.")

st.markdown("---")

# Mengamankan inisialisasi basis aturan jika halaman ini diakses pertama kali
if "rules_data" not in st.session_state:
    st.session_state.rules_data = [
        {"id_gejala": "G01", "gejala": "Anak tampak sangat lesu, lemas, dan cepat lelah", "penyakit": "Kekurangan Energi", "cf_pakar": 0.8},
        {"id_gejala": "G02", "gejala": "Berat badan anak menurun drastis atau di bawah grafik normal", "penyakit": "Kekurangan Energi", "cf_pakar": 0.7},
        {"id_gejala": "G03", "gejala": "Tinggi badan anak terhambat / terlihat lebih pendek dari usianya (Risiko Stunting)", "penyakit": "Kekurangan Protein", "cf_pakar": 0.85},
        {"id_gejala": "G04", "gejala": "Daya tahan tubuh lemah (Anak sangat sering batuk, pilek, atau demam)", "penyakit": "Kekurangan Protein", "cf_pakar": 0.75},
        {"id_gejala": "G05", "gejala": "Kulit anak tampak sangat kering, kasar, atau bersisik", "penyakit": "Kekurangan Lemak (Fat)", "cf_pakar": 0.7},
        {"id_gejala": "G06", "gejala": "Anak sering mengalami sembelit / susah buang air besar", "penyakit": "Kekurangan Serat (Dietary Fiber)", "cf_pakar": 0.8},
        {"id_gejala": "G07", "gejala": "Anak kesulitan melihat dengan jelas di sore/malam hari (Rabun Senja)", "penyakit": "Kekurangan Vitamin A", "cf_pakar": 0.9},
        {"id_gejala": "G08", "gejala": "Anak tampak pucat, sering pusing, dan didiagnosis kurang darah", "penyakit": "Kekurangan Zat Besi (Iron)", "cf_pakar": 0.8},
        {"id_gejala": "G09", "gejala": "Gusi anak mudah berdarah atau muncul sariawan akut (Skorbut)", "penyakit": "Kekurangan Vitamin C", "cf_pakar": 0.85},
        {"id_gejala": "G10", "gejala": "Anak sering mengalami kram otot secara mendadak", "penyakit": "Kekurangan Magnesium", "cf_pakar": 0.75},
        {"id_gejala": "G11", "gejala": "Anak mengalami kelebihan berat badan signifikan / Obesitas", "penyakit": "Kelebihan Energi & Karbohidrat", "cf_pakar": 0.9},
        {"id_gejala": "G12", "gejala": "Perut anak sering kembung dan mengalami gangguan pencernaan", "penyakit": "Kelebihan Serat (Dietary Fiber)", "cf_pakar": 0.7},
        {"id_gejala": "G13", "gejala": "Anak sering diare mendadak disertai rasa mual", "penyakit": "Kelebihan Vitamin C / Vitamin E", "cf_pakar": 0.75}
    ]

# 1. Menampilkan Tabel Aturan Berjalan
st.subheader("📋 Daftar Aturan Medis & Nilas Kesimpulan Saat Ini")
df_rules = pd.DataFrame(st.session_state.rules_data)
st.dataframe(df_rules, use_container_width=True)

st.markdown("---")

# 2. Form untuk Mengubah Nilai Bobot Pakar
st.subheader("✏️ Ubah Derajat Keyakinan Pakar ($CF$)")
st.write("Pilih kode gejala untuk menyesuaikan nilai keyakinan medisnya:")

list_id_gejala = [item['id_gejala'] for item in st.session_state.rules_data]

with st.form("form_manajemen_pakar"):
    selected_id = st.selectbox("Pilih Kode Gejala:", list_id_gejala)
    
    # Mengambil objek data aturan yang dipilih secara real-time
    aturan_terpilih = next(item for item in st.session_state.rules_data if item['id_gejala'] == selected_id)
    
    # Tampilkan info detail aturan terpilih
    st.info(f"**Gejala Klinis:** {aturan_terpilih['gejala']} \n\n **Diagnosis Masalah:** {aturan_terpilih['penyakit']}")
    
    # Input nomor untuk mengubah CF Pakar
    new_cf_value = st.number_input(
        f"Setel Nilai $CF_{{pakar}}$ Baru (Skala 0.0 sampai 1.0):",
        min_value=0.0,
        max_value=1.0,
        value=float(aturan_terpilih['cf_pakar']),
        step=0.05
    )
    
    submit_button = st.form_submit_button("Simpan Perubahan Aturan")

# Logika eksekusi perubahan data ke session state
if submit_button:
    for item in st.session_state.rules_data:
        if item['id_gejala'] == selected_id:
            item['cf_pakar'] = new_cf_value
            break
    st.success(f"🎉 Sukses! Aturan {selected_id} diperbarui. Nilai $CF_{{pakar}}$ sekarang menjadi {new_cf_value}.")
    st.rerun()