import streamlit as st
import pandas as pd
import os
import random
from datetime import date, datetime
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="Musab & Sıla ❤️", layout="centered")

# --- YOLLAR ---
# Dosyaların ask_projem klasörü içinde olduğunu varsayarak yolu sağlama alıyoruz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOTO_KLASORU = os.path.join(BASE_DIR, "fotograflar")
SIIR_DOSYASI = os.path.join(BASE_DIR, "siirler.xlsx")

# --- ÖZEL DOSYA TANIMI ---
# 14 Şubat'ta görünecek özel fotoğraf ismi
OZEL_FOTO_ADI = "WhatsApp Image 2026-02-12 at 17.05.21.jpeg"

# --- GİRİŞ BİLGİLERİ ---
DOĞRU_KULLANICI = "musabsila"
DOĞRU_SIFRE = "17.04.2025"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    # Giriş ekranındaki fotoğraf
    giris_resmi = os.path.join(FOTO_KLASORU, "giris_fotosu.jpg")
    if os.path.exists(giris_resmi):
        st.image(giris_resmi, use_container_width=True)

    st.title("❤️ Hoş Geldin ❤️")
    user_input = st.text_input("Kullanıcı Adı").lower().strip()
    pass_input = st.text_input("Şifre", type="password").strip()

    if st.button("Giriş"):
        if user_input == DOĞRU_KULLANICI and pass_input == DOĞRU_SIFRE:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre!")

# --- ANA UYGULAMA MANTIĞI ---
if not st.session_state['authenticated']:
    login()
else:
    # --- TARİH VE ÖZEL GÜN KONTROLÜ ---
    bugun = date.today()
    is_valentine = (bugun.month == 2 and bugun.day == 14)

    # --- VERİLERİ YÜKLEME ---
    # Normal günlerin fotoğraf listesi (Giriş fotosunu ve 14 Şubat fotosunu hariç tutar)
    foto_listesi = []
    if os.path.exists(FOTO_KLASORU):
        foto_listesi = [f for f in os.listdir(FOTO_KLASORU)
                        if f.lower().endswith(('.jpeg', '.jpg', '.png'))
                        and f != "giris_fotosu.jpg"
                        and f != OZEL_FOTO_ADI]

    # Şiirleri Yükle
    siir_listesi = []
    df = None
    if os.path.exists(SIIR_DOSYASI):
        try:
            df = pd.read_excel(SIIR_DOSYASI)
            siir_listesi = df.iloc[:, 0].dropna().tolist()
        except:
            siir_listesi = ["Şiirler şu an yüklenemedi."]

    # --- TEK SAYFA İÇERİĞİ ---
    if is_valentine:
        # --- 14 ŞUBAT ÖZEL GÖRÜNÜMÜ ---
        st.balloons()
        st.header("🌹 Bugün Çok Özel Bir Gün! 🌹")
        st.toast("Sevgililer Günümüz Kutlu Olsun! ❤️")

        # Özel Fotoğraf Yolu
        ozel_foto_yolu = os.path.join(FOTO_KLASORU, OZEL_FOTO_ADI)

        # Özel Şiir (A4 Hücresi: Index 2)
        try:
            ozel_siir = df.iloc[2, 0]  # Excel'deki 4. satır (Başlık varsa A4)
        except:
            ozel_siir = "Seninle her gün sevgililer günü..."

        if os.path.exists(ozel_foto_yolu):
            st.image(ozel_foto_yolu, use_container_width=True)
        else:
            st.warning(f"Özel fotoğraf bulunamadı: {OZEL_FOTO_ADI}")

        st.markdown(f"### *{ozel_siir}*")
        st.markdown("---")
        st.markdown("### ❤️ Sevgililer Günümüz Kutlu Olsun Sıla! ❤️")

    else:
        # --- NORMAL GÜNLERDEKİ GÖRÜNÜM ---
        st.header("Bugünün Bize Mesajı ❤️")
        if siir_listesi and foto_listesi:
            # Seçimi güne sabitlemek için seed kullanıyoruz
            random.seed(bugun.toordinal())
            secilen_siir = random.choice(siir_listesi)
            secilen_foto = random.choice(foto_listesi)
            
            st.image(os.path.join(FOTO_KLASORU, secilen_foto), use_container_width=True)
            st.markdown(f"### *{secilen_siir}*")
        else:
            st.info("Bugünün sürprizi hazırlanıyor...")

    # --- GERİ SAYIM (HER GÜN ALTTA GÖRÜNÜR) ---
    st.markdown("---")
    yildonumu = datetime(2026, 4, 17)
    fark = yildonumu - datetime.now()
    if fark.days > 0:
        st.write(f"💑 Yıl dönümümüze **{fark.days}** gün kaldı!")
    
    # Çıkış Butonu (Sidebar olmadığı için sayfa altına küçük bir buton)
    if st.button("Güvenli Çıkış"):
        st.session_state['authenticated'] = False
        st.rerun()
