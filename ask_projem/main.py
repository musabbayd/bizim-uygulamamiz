import streamlit as st
import pandas as pd
import os
import random
from datetime import date
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="Bizim Sayfamız", layout="centered")

# --- GİRİŞ KONTROLÜ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


def login():
    # Resim yolu güncellendi: 'fotograflar' klasörü altındaki 'giris_fotosu.jpg'
    giris_resmi_yolu = os.path.join("fotograflar", "giris_fotosu.jpg")

    # Resim dosyası var mı kontrol edelim
    if os.path.exists(giris_resmi_yolu):
        st.image(giris_resmi_yolu, use_container_width=True)
    else:
        st.warning(f"Giriş fotoğrafı bulunamadı: {giris_resmi_yolu}")

    st.title("❤️ Hoş Geldin ❤️")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş"):
        # Bilgiler
        if username == "askim" and password == "12345":
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre!")


if not st.session_state['authenticated']:
    login()
else:
    # --- VERİLERİ YÜKLEME ---
    # Excel'den şiirleri oku
    df = pd.read_excel("siirler.xlsx")
    siir_listesi = df["Şiir"].tolist()

    # Klasörden fotoğrafları oku
    foto_klasoru = "fotograflar"
    foto_listesi = [f for f in os.listdir(foto_klasoru) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # --- MENÜ ---
    st.sidebar.title("Menü")
    page = st.sidebar.radio("Sayfalar", ["Günün Sürprizi", "Fotoğraflarımız", "Şiir Arşivi"])

    # --- 1. SAYFA: GÜNÜN SÜRPRİZİ ---
    if page == "Günün Sürprizi":
        st.header("Bugünün Bize Mesajı ❤️")

        # Her gün 00:00'da değişen seçim mekanizması
        today_seed = date.today().toordinal()
        random.seed(today_seed)

        gunun_siiri = random.choice(siir_listesi)
        gunun_fotosu_adi = random.choice(foto_listesi)

        img_path = os.path.join(foto_klasoru, gunun_fotosu_adi)
        img = Image.open(img_path)
        st.image(img, use_container_width=True)
        st.markdown(f"### *{gunun_siiri}*")

    # --- 2. SAYFA: FOTOĞRAFLARIMIZ ---
    elif page == "Fotoğraflarımız":
        st.header("Anılarımız 📸")
        for foto in foto_listesi:
            img_path = os.path.join(foto_klasoru, foto)
            img = Image.open(img_path)
            st.image(img, use_container_width=True)
            st.write("---")

    # --- 3. SAYFA: ŞİİR ARŞİVİ ---
    elif page == "Şiir Arşivi":
        st.header("Güzel Sözler & Şiirler 📜")
        for s in siir_listesi:
            st.info(s)

    if st.sidebar.button("Çıkış Yap"):
        st.session_state['authenticated'] = False
        st.rerun()
