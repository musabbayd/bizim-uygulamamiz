import streamlit as st
import pandas as pd
import os
import random
from datetime import date
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="Bizim Sayfamız", layout="centered")

# --- GİRİŞ BİLGİLERİ ---
DOĞRU_KULLANICI = "musabsila"
DOĞRU_SIFRE = "17.04.2025"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    # Giriş fotoğrafı ana dizinde
    giris_resmi = "giris_fotosu.jpg"
    
    if os.path.exists(giris_resmi):
        st.image(giris_resmi, use_container_width=True)
    else:
        st.warning(f"⚠️ '{giris_resmi}' bulunamadı. Lütfen GitHub'da dosya adının tam olarak bu olduğundan emin ol.")
    
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
    # --- VERİ YÜKLEME ---
    foto_klasoru = "fotograflar"
    siir_dosyasi = "siirler.xlsx"
    
    # Fotoğrafları Listele
    foto_listesi = []
    if os.path.exists(foto_klasoru):
        # .jpeg, .jpg, .png ve büyük harf versiyonlarını (.JPG) destekle
        foto_listesi = [f for f in os.listdir(foto_klasoru) 
                        if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
    
    # Şiirleri Yükle
    siir_listesi = []
    if os.path.exists(siir_dosyasi):
        try:
            df = pd.read_excel(siir_dosyasi)
            siir_listesi = df.iloc[:, 0].dropna().tolist()
        except Exception as e:
            st.error(f"Excel okuma hatası: {e}")
    
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
            st.image(os.path.join(foto_klasoru, s_foto), use_container_width=True)
            st.markdown(f"### *{s_siir}*")
        else:
            st.warning("Günün sürprizi için şiir veya fotoğraf yüklenemedi.")

    elif page == "Fotoğraflarımız":
        st.header("Anılarımız 📸")
        if foto_listesi:
            for foto in foto_listesi:
                st.image(os.path.join(foto_klasoru, foto), use_container_width=True)
                st.write("---")
        else:
            st.info(f"'{foto_klasoru}' klasörü içinde uygun formatta fotoğraf bulunamadı.")

    elif page == "Şiir Arşivi":
        st.header("Güzel Sözler & Şiirler 📜")
        if siir_listesi:
            for s in siir_listesi:
                st.info(s)
        else:
            st.info("Şiir listesi boş görünüyor.")

    # --- TEŞHİS PANELİ (Hata Çözmek İçin) ---
    st.markdown("---")
    with st.expander("🔍 Dosya Kontrol Paneli (Hata buradaysa tıkla)"):
        st.write("**Mevcut Klasör Yolu:**", os.getcwd())
        st.write("**Ana Dizindeki Dosyalar:**", os.listdir("."))
        if os.path.exists(foto_klasoru):
            st.write(f"**'{foto_klasoru}' İçindeki Dosyalar:**", os.listdir(foto_klasoru))
        else:
            st.error(f"'{foto_klasoru}' klasörü sistemde fiziksel olarak yok!")

    if st.sidebar.button("Çıkış Yap"):
        st.session_state['authenticated'] = False
        st.rerun()
