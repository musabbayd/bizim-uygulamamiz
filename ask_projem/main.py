import streamlit as st
import pandas as pd
import os
import random
from datetime import date
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="Bizim Sayfamız", layout="centered")

# --- YOL AYARLARI ---
# Kodun çalıştığı klasörü (ask_projem) temel dizin olarak belirliyoruz
BASE_DIR = os.path.dirname(__file__)
FOTO_KLASORU = os.path.join(BASE_DIR, "fotograflar")
SIIR_DOSYASI = os.path.join(BASE_DIR, "siirler.xlsx")

# --- GİRİŞ BİLGİLERİ ---
DOĞRU_KULLANICI = "musabsila"
DOĞRU_SIFRE = "17.04.2025"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    # Giriş fotoğrafı: ask_projem/fotograflar/giris_fotosu.jpg
    giris_resmi = os.path.join(FOTO_KLASORU, "giris_fotosu.jpg")
    
    if os.path.exists(giris_resmi):
        st.image(giris_resmi, use_container_width=True)
    else:
        st.warning(f"⚠️ Giriş fotoğrafı bulunamadı. Aranan yol: {giris_resmi}")
    
    st.title("❤️ Hoş Geldin ❤️")
    user_input = st.text_input("Kullanıcı Adı").lower().strip()
    pass_input = st.text_input("Şifre", type="password").strip()
    
    if st.button("Giriş"):
        if user_input == DOĞRU_KULLANICI and pass_input == DOĞRU_SIFRE:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")

if not st.session_state['authenticated']:
    login()
else:
    # --- VERİLERİ YÜKLEME ---
    
    # Fotoğrafları listele (jpeg, jpg, png ve büyük harf halleri)
    foto_listesi = []
    if os.path.exists(FOTO_KLASORU):
        foto_listesi = [f for f in os.listdir(FOTO_KLASORU) 
                        if f.lower().endswith(('.jpeg', '.jpg', '.png')) 
                        and f != "giris_fotosu.jpg"]
    else:
        st.error(f"Klasör bulunamadı: {FOTO_KLASORU}")

    # Şiirleri yükle
    siir_listesi = []
    if os.path.exists(SIIR_DOSYASI):
        try:
            df = pd.read_excel(SIIR_DOSYASI)
            siir_listesi = df.iloc[:, 0].dropna().tolist()
        except Exception as e:
            st.error(f"Excel okunurken hata: {e}")
    else:
        st.error(f"Excel bulunamadı: {SIIR_DOSYASI}")

    # --- MENÜ ---
    st.sidebar.title("Menü")
    page = st.sidebar.radio("Sayfalar", ["Günün Sürprizi", "Fotoğraflarımız", "Şiir Arşivi"])

    # --- SAYFALAR ---
    if page == "Günün Sürprizi":
        st.header("Bugünün Bize Mesajı ❤️")
        if siir_listesi and foto_listesi:
            random.seed(date.today().toordinal())
            s_siir = random.choice(siir_listesi)
            s_foto = random.choice(foto_listesi)
            st.image(os.path.join(FOTO_KLASORU, s_foto), use_container_width=True)
            st.markdown(f"### *{s_siir}*")
        else:
            st.warning("Günün sürprizi için şiir veya fotoğraf yüklenemedi.")

    elif page == "Fotoğraflarımız":
        st.header("Anılarımız 📸")
        if foto_listesi:
            for foto in foto_listesi:
                st.image(os.path.join(FOTO_KLASORU, foto), use_container_width=True)
                st.write("---")
        else:
            st.info("Gösterilecek başka fotoğraf bulunamadı.")

    elif page == "Şiir Arşivi":
        st.header("Güzel Sözler & Şiirler 📜")
        if siir_listesi:
            for s in siir_listesi:
                st.info(s)
        else:
            st.info("Arşivde şiir bulunamadı.")

    if st.sidebar.button("Çıkış Yap"):
        st.session_state['authenticated'] = False
        st.rerun()
