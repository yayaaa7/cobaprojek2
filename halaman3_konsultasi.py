import streamlit as st

st.title("🩺 Form Konsultasi Gizi Balita")
st.write("Silakan isi data balita dan pilih tingkat keyakinan Anda terhadap gejala yang terlihat pada anak dalam 1-3 bulan terakhir.")

st.markdown("---")

# 1. Input Data Diri Balita
st.subheader("1. Identitas Balita")
col_nama, col_usia, col_jk = st.columns(3)

with col_nama:
    nama_anak = st.text_input("Nama Balita", placeholder="Contoh: Budi")
with col_usia:
    usia_anak = st.number_input("Usia (Bulan)", min_value=12, max_value=60, value=24, step=1)
with col_jk:
    jk_anak = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

st.markdown("---")

# 2. Definisikan Gejala dan Basis Aturan Berdasarkan Dataset
# Kita buat dictionary aturan yang menghubungkan gejala (G) ke penyakit nutrisi (K)
if "rules_data" not in st.session_state:
    st.session_state.rules_data = [
        # DEFISIENSI (KEKURANGAN GIZI)
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
        
        # EKSIDENSIAL (KELEBIHAN GIZI)
        {"id_gejala": "G11", "gejala": "Anak mengalami kelebihan berat badan signifikan / Obesitas", "penyakit": "Kelebihan Energi & Karbohidrat", "cf_pakar": 0.9},
        {"id_gejala": "G12", "gejala": "Perut anak sering kembung dan mengalami gangguan pencernaan", "penyakit": "Kelebihan Serat (Dietary Fiber)", "cf_pakar": 0.7},
        {"id_gejala": "G13", "gejala": "Anak sering diare mendadak disertai rasa mual", "penyakit": "Kelebihan Vitamin C / Vitamin E", "cf_pakar": 0.75}
    ]

st.subheader("2. Gejala Klinis Balita")
st.write("Pilih tingkat keyakinan Anda untuk setiap gejala di bawah ini:")

# Tingkat keyakinan pilihan user (CF User)
cf_options = {
    "Tidak Merasakan / Tidak Tahu": 0.0,
    "Sedikit Yakin": 0.4,
    "Cukup Yakin": 0.6,
    "Yakin": 0.8,
    "Sangat Yakin": 1.0
}

# Membuat form input gejala interaktif
user_inputs = {}
for item in st.session_state.rules_data:
    pilihan = st.selectbox(
        f"[{item['id_gejala']}] {item['gejala']}?",
        options=list(cf_options.keys()),
        key=item['id_gejala']
    )
    # Simpan nilai CF float pilihan user
    user_inputs[item['id_gejala']] = cf_options[pilihan]

st.markdown("---")

# Tombol untuk memicu kalkulasi Certainty Factor
if st.button("🚀 Mulai Analisis Kepastian Gizi", type="primary"):
    # Cek apakah ada gejala yang dipilih oleh user
    if all(val == 0.0 for val in user_inputs.values()):
        st.warning("⚠️ Silakan pilih minimal satu gejala dengan tingkat keyakinan di atas 'Tidak Tahu' sebelum memulai analisis!")
    else:
        # Simpan data inputan ke session_state agar bisa dibaca di halaman_4_hasil.py
        st.session_state.data_balita = {
            "nama": nama_anak if nama_anak else "Balita",
            "usia": usia_anak,
            "jk": jk_anak
        }
        st.session_state.user_inputs = user_inputs
        st.success("Analisis berhasil diproses! Silakan klik menu **Hasil Diagnosis** di sidebar sebelah kiri untuk melihat hasilnya.")