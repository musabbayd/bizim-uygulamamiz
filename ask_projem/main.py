import streamlit as st
import pandas as pd
import os
import random
from datetime import date
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="Bizim Sayfamız", layout="centered")

# --- GİRİŞ BİLGİLERİ ---
# Bilgileri buraya tanımlıyoruz (Küçük harfe duyarlı yaptık)
DOĞRU_KULLANICI = "musabsila"
DOĞRU_SIFRE = "17.04.2025"

# --- OTURUM YÖNETİMİ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    # Görsel Yolu
    giris_resmi_yolu = os.path.join("fotograflar", "giris_fotosu.jpg")
    
    if os.path.exists(giris_resmi_yolu):
        st.image(giris_resmi_yolu, use_container_width=True)
    
    st.title("❤️ Hoş Geldin ❤️")
    
    # Giriş Kutuları (strip() ile görünmez boşlukları siliyoruz)
    user_input = st.text_input("Kullanıcı Adı").lower().strip()
    pass_input = st.text_input("Şifre", type="password").strip()
    
    if st.button("Giriş"):
        if user_input == DOĞRU_KULLANICI and pass_input == DOĞRU_SIFRE:
            st.session_state['authenticated'] = True
            st.success("Harika! Giriş yapıldı...")
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
            # HATA AYIKLAMA (Eğer giriş yapamazsan buradaki bilgileri kontrol et)
            st.info(f"Yazdığın Kullanıcı: '{user_input}'")
            st.info(f"Yazdığın Şifre Karakter Sayısı: {len(pass_input)}")

if not st.session_state['authenticated']:
    login()
else:
    # --- UYGULAMA İÇERİĞİ (Giriş Başarılıysa) ---
    st.sidebar.title("Menü")
    
    # Veri yükleme işlemleri
    try:
        df = pd.read_excel("siirler.xlsx")
        siir_listesi = df["Şiir"].tolist()
    except:
        siir_listesi = ["Henüz bir şiir eklenmemiş."]

    foto_klasoru = "fotograflar"
    foto_listesi = []
    if os.path.exists(foto_klasoru):
        foto_listesi = [f for f in os.listdir(foto_klasoru) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    page = st.sidebar.radio("Sayfalar", ["Günün Sürprizi", "Fotoğraflarımız", "Şiir Arşivi"])

    if page == "Günün Sürprizi":
        st.header("Bugünün Bize Mesajı ❤️")
        if siir_listesi and foto_listesi:
            random.seed(date.today().toordinal())
            st.image(os.path.join(foto_klasoru, random.choice(foto_listesi)), use_container_width=True)
            st.markdown(f"### *{random.choice(siir_listesi)}*")

    elif page == "Fotoğraflarımız":
        st.header("Anılarımız 📸")
        for foto in foto_listesi:
            st.image(os.path.join(foto_klasoru, foto), use_container_width=True)
            st.write("---")

    elif page == "Şiir Arşivi":
        st.header("Güzel Sözler & Şiirler 📜")
        for s in siir_listesi:
            st.info(s)

    if st.sidebar.button("Çıkış Yap"):
        st.session_state['authenticated'] = False
        st.rerun()
