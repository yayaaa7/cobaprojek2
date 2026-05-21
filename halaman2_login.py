import streamlit as st

st.title("🔐 Login Sistem")
st.write("Silakan login untuk mengakses fitur penuh sesuai hak akses Anda.")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Masuk")

if submit:
    if username == "admin" and password == "admin123":
        st.session_state.logged_in = True
        st.session_state.user_role = "admin"
        st.session_state.username = "Pakar Gizi"
        st.success("Login Berhasil sebagai Admin Pakar!")
        st.rerun()
    elif username == "user" and password == "user123":
        st.session_state.logged_in = True
        st.session_state.user_role = "user"
        st.session_state.username = "Orang Tua Balita"
        st.success("Login Berhasil!")
        st.rerun()
    else:
        st.error("Username atau Password salah. Silakan coba lagi.")