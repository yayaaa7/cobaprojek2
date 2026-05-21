import streamlit as st

st.title("👶 Sistem Pakar Deteksi Risiko Malnutrisi Balita")
st.subheader("Selamat Datang di Layanan Konsultasi Gizi Anak Usia 1-5 Tahun")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Mengapa Deteksi Dini Gizi Balita itu Penting?
    Masa usia 1 hingga 5 tahun merupakan *golden age* bagi pertumbuhan fisik dan perkembangan otak anak. 
    Kekurangan atau kelebihan gizi makro dan mikro yang tidak disadari sejak dini dapat berdampak panjang bagi masa depan anak, seperti risiko **Stunting**, penurunan imunitas, hingga gangguan fungsi kognitif.
    
    ### Bagaimana Sistem Ini Membantu Anda?
    1. **Menganalisis Gejala Klinis:** Menggunakan metode penalaran **Certainty Factor (CF)** untuk menghitung derajat kepastian keluhan fisik anak Anda.
    2. **Memberikan Hasil Akurat:** Menentukan zat gizi gizi makro/mikro apa yang sedang mengalami defisiensi (kekurangan) atau eksidensi (kelebihan).
    3. **Rekomendasi Menu Solutif:** Menyarankan menu makanan terbaik yang diekstrak langsung dari **1.126 data nutrisi makanan** berdasarkan kebutuhan spesifik balita Anda.
    """)
    
    st.info("💡 **Tips:** Silakan langsung menuju menu **Konsultasi Gizi** di samping untuk mulai memeriksa kondisi balita Anda.")

with col2:
    st.header("Statistik Dataset")
    st.metric(label="Total Referensi Menu Makanan", value="1.126 Menu")
    st.metric(label="Zat Gizi Diuji (Makro & Mikro)", value="21 Jenis")