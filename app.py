import streamlit as st

# Set konfigurasi halaman utama
st.set_page_config(
    page_title="Sistem Pakar Gizi Balita",
    page_icon="👶",
    layout="wide"
)

# Inisialisasi session state untuk login jika belum ada
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "username" not in st.session_state:
    st.session_state.username = ""

# Fungsi untuk logout
def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = ""
    st.rerun()

# Definisikan halaman-halaman aplikasi
dashboard_page = st.Page("halaman1_dashboard.py", title="Beranda", icon="🏠")
login_page = st.Page("halaman2_login.py", title="Login Akun", icon="🔐")
konsultasi_page = st.Page("halaman3_konsultasi.py", title="Konsultasi Gizi", icon="🩺")
hasil_page = st.Page("halaman4_hasil.py", title="Hasil Diagnosis", icon="📊")
katalog_page = st.Page("halaman5_katalog.py", title="Katalog Nutrisi Makanan", icon="🍲")
manajemen_page = st.Page("halaman6_manajemen.py", title="Kelola Bobot Pakar", icon="⚙️")

# Atur navigasi berdasarkan status login dan role
if st.session_state.logged_in:
    if st.session_state.user_role == "admin":
        pages = [dashboard_page, konsultasi_page, hasil_page, katalog_page, manajemen_page]
    else:
        pages = [dashboard_page, konsultasi_page, hasil_page, katalog_page]
    
    st.sidebar.write(f"Halo, **{st.session_state.username}** ({st.session_state.user_role})")
    if st.sidebar.button("Log Out"):
        logout()
else:
    pages = [dashboard_page, login_page, konsultasi_page, hasil_page, katalog_page]

# Jalankan navigasi
pg = st.navigation(pages)
pg.run()