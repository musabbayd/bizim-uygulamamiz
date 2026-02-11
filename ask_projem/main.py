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
    return make_hashes(password) == hashed_text

# --- GİRİŞ BİLGİLERİ ---
# Şifre: 17.04.2025
hashed_password = "405f6e80b4356c3818e692a83e05391e4429623e1059f3d6718d0526e082877a"
target_username = "musabsila"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    giris_resmi_yolu = os.path.join("fotograflar", "giris_fotosu.jpg")
    
    if os.path.exists(giris_resmi_yolu):
        st.image(giris_resmi_yolu, use_container_width=True)
    
    st.title("❤️ Hoş Geldin ❤️")
    
    # .strip() ekleyerek yanlışlıkla girilen boşlukları temizliyoruz
    username = st.text_input("Kullanıcı Adı").strip()
    password = st.text_input("Şifre", type="password").strip()
    
    if st.button("Giriş"):
        if username == target_username and check_hashes(password, hashed_password):
            st.session_state['authenticated'] = True
            st.success("Giriş başarılı! Yükleniyor...")
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
            # Hata devam ederse burayı aktif edip ne yazdığını kontrol edebilirsin:
            # st.write(f"Yazılan: {username}, Şifre Hash: {make_hashes(password)}")

if not st.session_state['authenticated']:
    login()
else:
    # --- VERİLERİ YÜKLEME ---
    try:
        df = pd.read_excel("siirler.xlsx")
        siir_listesi = df["Şiir"].tolist()
    except:
        siir_listesi = ["Şiir dosyası bulunamadı."]

    foto_klasoru = "fotograflar"
    foto_listesi = []
    if os.path.exists(foto_klasoru):
        foto_listesi = [f for f in os.listdir(foto_klasoru) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # --- MENÜ ---
    st.sidebar.title("Menü")
    page = st.sidebar.radio("Sayfalar", ["Günün Sürprizi", "Fotoğraflarımız", "Şiir Arşivi"])

    # --- SAYFA İÇERİKLERİ ---
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
