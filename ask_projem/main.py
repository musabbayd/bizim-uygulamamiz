import streamlit as st
import pandas as pd
import os
import random
import hashlib
from datetime import date
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="Bizim Sayfamız", layout="centered")

# --- GÜVENLİK FONKSİYONU ---
def make_hashes(password):
    """Şifreyi güvenli bir hash dizisine dönüştürür."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    """Girilmiş şifrenin doğruluğunu kontrol eder."""
    if make_hashes(password) == hashed_text:
        return True
    return False

# --- GİRİŞ KONTROLÜ ---
# Belirlediğin şifrenin (17.04.2025) hash hali:
# 405f6e80b4356c3818e692a83e05391e4429623e1059f3d6718d0526e082877a
hashed_password = "405f6e80b4356c3818e692a83e05391e4429623e1059f3d6718d0526e082877a"
target_username = "musabsila"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    # Resim yolu: 'fotograflar' klasörü altındaki 'giris_fotosu.jpg'
    giris_resmi_yolu = os.path.join("fotograflar", "giris_fotosu.jpg")
    
    if os.path.exists(giris_resmi_yolu):
        st.image(giris_resmi_yolu, use_container_width=True)
    
    st.title("❤️ Hoş Geldin ❤️")
    
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    
    if st.button("Giriş"):
        if username == target_username and check_hashes(password, hashed_password):
            st.session_state['authenticated'] = True
            st.success(f"Hoş geldin {username}!")
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")

if not st.session_state['authenticated']:
    login()
else:
    # --- VERİLERİ YÜKLEME ---
    try:
        df = pd.read_excel("siirler.xlsx")
        siir_listesi = df["Şiir"].tolist()
    except Exception:
        siir_listesi = ["Şiirler yüklenemedi, lütfen siirler.xlsx dosyasını kontrol edin."]

    foto_klasoru = "fotograflar"
    if os.path.exists(foto_klasoru):
        foto_listesi = [f for f in os.listdir(foto_klasoru) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    else:
        foto_listesi = []

    # --- MENÜ ---
    st.sidebar.title("Menü")
    page = st.sidebar.radio("Sayfalar", ["Günün Sürprizi", "Fotoğraflarımız", "Şiir Arşivi"])

    # --- 1. SAYFA: GÜNÜN SÜRPRİZİ ---
    if page == "Günün Sürprizi":
        st.header("Bugünün Bize Mesajı ❤️")
        
        if siir_listesi and foto_listesi:
            today_seed = date.today().toordinal()
            random.seed(today_seed)
            
            gunun_siiri = random.choice(siir_listesi)
            gunun_fotosu_adi = random.choice(foto_listesi)
            
            img_path = os.path.join(foto_klasoru, gunun_fotosu_adi)
            img = Image.open(img_path)
            st.image(img, use_container_width=True)
            st.markdown(f"### *{gunun_siiri}*")
        else:
            st.warning("Şiir veya fotoğraf listesi boş!")

    # --- 2. SAYFA: FOTOĞRAFLARIMIZ ---
    elif page == "Fotoğraflarımız":
        st.header("Anılarımız 📸")
        if foto_listesi:
            for foto in foto_listesi:
                img_path = os.path.join(foto_klasoru, foto)
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
                st.write("---")
        else:
            st.warning("Henüz fotoğraf eklenmemiş.")

    # --- 3. SAYFA: ŞİİR ARŞİVİ ---
    elif page == "Şiir Arşivi":
        st.header("Güzel Sözler & Şiirler 📜")
        for s in siir_listesi:
            st.info(s)

    if st.sidebar.button("Çıkış Yap"):
        st.session_state['authenticated'] = False
        st.rerun()
