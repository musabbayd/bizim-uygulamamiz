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
    # Giriş fotoğrafı artık doğrudan ana dizinde
    giris_resmi = "giris_fotosu.jpg"
    
    if os.path.exists(giris_resmi):
        st.image(giris_resmi, use_container_width=True)
    else:
        # Dosya bulunamazsa hata vermemesi için uyarı gösterir
        st.warning(f"Giriş fotoğrafı ({giris_resmi}) ana dizinde bulunamadı.")
    
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
    # Fotoğraflar klasörü yolu
    foto_klasoru = "fotograflar"
    
    # fotograflar klasöründeki jpeg, jpg ve png dosyalarını listele
    foto_listesi = []
    if os.path.exists(foto_klasoru):
        foto_listesi = [f for f in os.listdir(foto_klasoru) 
                        if f.lower().endswith(('.jpeg', '.jpg', '.png'))]

    # Şiirleri yükle
    siir_listesi = []
    if os.path.exists("siirler.xlsx"):
        try:
            df = pd.read_excel("siirler.xlsx")
            # İlk sütunu şiir içeriği olarak kabul et
            siir_listesi = df.iloc[:, 0].dropna().tolist()
        except Exception as e:
            siir_listesi = [f"Şiirler yüklenirken bir hata oluştu: {e}"]
    else:
        siir_listesi = ["siirler.xlsx dosyası bulunamadı."]

    # --- MENÜ ---
    st.sidebar.title("Menü")
    page = st.sidebar.radio("Sayfalar", ["Günün Sürprizi", "Fotoğraflarımız", "Şiir Arşivi"])

    # --- 1. SAYFA: GÜNÜN SÜRPRİZİ ---
    if page == "Günün Sürprizi":
        st.header("Bugünün Bize Mesajı ❤️")
        if siir_listesi and foto_listesi:
            # Seçimi güne sabitlemek için günün tarihini seed olarak kullan
            random.seed(date.today().toordinal())
            secilen_siir = random.choice(siir_listesi)
            secilen_foto = random.choice(foto_listesi)
            
            st.image(os.path.join(foto_klasoru, secilen_foto), use_container_width=True)
            st.markdown(f"### *{secilen_siir}*")
        else:
            st.warning("Görüntülenecek içerik (şiir veya fotoğraf) bulunamadı.")

    # --- 2. SAYFA: FOTOĞRAFLARIMIZ ---
    elif page == "Fotoğraflarımız":
        st.header("Anılarımız 📸")
        if foto_listesi:
            for foto in foto_listesi:
                st.image(os.path.join(foto_klasoru, foto), use_container_width=True)
                st.write("---")
        else:
            st.info("fotograflar klasöründe görüntülenecek fotoğraf bulunamadı.")

    # --- 3. SAYFA: ŞİİR ARŞİVİ ---
    elif page == "Şiir Arşivi":
        st.header("Güzel Sözler & Şiirler 📜")
        if siir_listesi:
            for s in siir_listesi:
                st.info(s)
        else:
            st.info("Arşivde gösterilecek şiir bulunamadı.")

    # Çıkış Yap Butonu
    if st.sidebar.button("Çıkış Yap"):
        st.session_state['authenticated'] = False
        st.rerun()
