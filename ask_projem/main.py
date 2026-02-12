import streamlit as st
import pandas as pd
import os
import random
from datetime import date, datetime
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="Musab & Sıla ❤️", layout="centered")

# --- KRİTİK YOL AYARI ---
# Bu kısım klasör içinde klasör olsa bile dosyaları bulmanı sağlar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOTO_KLASORU = os.path.join(BASE_DIR, "fotograflar")
SIIR_DOSYASI = os.path.join(BASE_DIR, "siirler.xlsx")

# --- GİRİŞ BİLGİLERİ ---
DOĞRU_KULLANICI = "musabsila"
DOĞRU_SIFRE = "17.04.2025"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    # Giriş fotoğrafı 'fotograflar' klasörünün içinde
    giris_resmi = os.path.join(FOTO_KLASORU, "giris_fotosu.jpg")
    
    if os.path.exists(giris_resmi):
        st.image(giris_resmi, use_container_width=True)
    else:
        st.warning(f"⚠️ Giriş resmi bulunamadı. Aranan yol: {giris_resmi}")
    
    st.title("❤️ Hoş Geldin ❤️")
    user_input = st.text_input("Kullanıcı Adı").lower().strip()
    pass_input = st.text_input("Şifre", type="password").strip()
    
    if st.button("Giriş"):
        if user_input == DOĞRU_KULLANICI and pass_input == DOĞRU_SIFRE:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre!")

if not st.session_state['authenticated']:
    login()
else:
    # --- TARİH VE ÖZEL GÜN KONTROLÜ ---
    bugun = date.today()
    # Sevgililer Günü mü? (14 Şubat)
    is_valentine = (bugun.month == 2 and bugun.day == 14)
    
    # --- VERİLERİ YÜKLEME ---
    foto_listesi = []
    if os.path.exists(FOTO_KLASORU):
        foto_listesi = [f for f in os.listdir(FOTO_KLASORU) 
                        if f.lower().endswith(('.jpeg', '.jpg', '.png')) 
                        and f != "giris_fotosu.jpg"]

    siir_listesi = []
    df = None # Excel verisini saklamak için
    if os.path.exists(SIIR_DOSYASI):
        try:
            df = pd.read_excel(SIIR_DOSYASI)
            siir_listesi = df.iloc[:, 0].dropna().tolist()
        except Exception as e:
            st.error(f"Excel okunurken hata: {e}")

    # --- MENÜ ---
    st.sidebar.title("💖 Bizim Dünyamız")
    page = st.sidebar.radio("Sayfalar", ["Günün Sürprizi", "Fotoğraflarımız", "Şiir Arşivi"])

    if is_valentine:
        st.balloons()
        st.toast("Sevgililer Günümüz Kutlu Olsun! ❤️", icon="🌹")

    # --- 1. SAYFA: GÜNÜN SÜRPRİZİ ---
    if page == "Günün Sürprizi":
        if is_valentine:
            st.header("🌹 Bugün Çok Özel Bir Gün! 🌹")
            
            # --- 14 ŞUBAT ÖZEL SEÇİMİ ---
            ozel_foto_adi = "WhatsApp Image 2026-02-12 at 17.05.21.jpeg"
            ozel_foto_yolu = os.path.join(FOTO_KLASORU, ozel_foto_adi)
            
            # Excel'deki A4 hücresi (0'dan başladığı için 4. satır index 2'dir - eğer başlık varsa)
            # Eğer hata alırsan iloc[3,0] olarak deneyebilirsin.
            try:
                ozel_siir = df.iloc[2, 0] 
            except:
                ozel_siir = "Seninle geçen her an en güzel şiir..."

            if os.path.exists(ozel_foto_yolu):
                st.image(ozel_foto_yolu, use_container_width=True)
            else:
                st.warning(f"Özel fotoğraf bulunamadı: {ozel_foto_adi}")
            
            st.markdown(f"### *{ozel_siir}*")
            st.markdown("---")
            st.markdown("### ❤️ Sevgililer Günümüz Kutlu Olsun Sıla! ❤️")
        else:
            st.header("Bugünün Bize Mesajı ❤️")
            if siir_listesi and foto_listesi:
                random.seed(bugun.toordinal())
                st.image(os.path.join(FOTO_KLASORU, random.choice(foto_listesi)), use_container_width=True)
                st.markdown(f"### *{random.choice(siir_listesi)}*")
        
        # Yıl Dönümü Sayacı
        st.markdown("---")
        yildonumu = datetime(2026, 4, 17)
        fark = yildonumu - datetime.now()
        if fark.days > 0:
            st.write(f"💑 Yıl dönümümüze **{fark.days}** gün kaldı!")

    # --- 2. SAYFA: FOTOĞRAFLARIMIZ ---
    elif page == "Fotoğraflarımız":
        st.header("Anılarımız 📸")
        if foto_listesi:
            for foto in foto_listesi:
                st.image(os.path.join(FOTO_KLASORU, foto), use_container_width=True)
                st.write("---")
        else:
            st.info("Henüz fotoğraf yüklenmemiş.")

    # --- 3. SAYFA: ŞİİR ARŞİVİ ---
    elif page == "Şiir Arşivi":
        st.header("Güzel Sözler & Şiirler 📜")
        if siir_listesi:
            for s in siir_listesi:
                st.info(s)

    if st.sidebar.button("Çıkış Yap"):
        st.session_state['authenticated'] = False
        st.rerun()
