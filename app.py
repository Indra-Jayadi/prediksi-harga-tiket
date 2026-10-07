import datetime as dt
import joblib
import pandas as pd
import streamlit as st
import __main__
from pathlib import Path

def buang_late_night(X):
    return X.drop(columns=['departure_time_Late_Night'])
__main__.buang_late_night = buang_late_night      # supaya joblib menemukan fungsi ini

st.set_page_config(page_title='Cek Harga Tiket', page_icon='✈️', layout='centered')

BASE = Path(__file__).parent      # folder tempat app.py berada

@st.cache_resource
def muat():
    return joblib.load(BASE / 'flight_price_pipeline.pkl'), joblib.load(BASE / 'meta_app.pkl')
pipe, meta = muat()

MATA_UANG = '₹'    # cek dulu mata uang dataset sebelum dibagikan ke orang lain
JAM = {'Early_Morning': 'Subuh / pagi buta', 'Morning': 'Pagi', 'Afternoon': 'Siang',
       'Evening': 'Sore', 'Night': 'Malam', 'Late_Night': 'Tengah malam'}
TRANSIT = {'zero': 'Langsung', 'one': '1 kali transit', 'two_or_more': '2 kali transit atau lebih'}

def format_harga(x):
    return f'{MATA_UANG}{x:,.0f}'.replace(',', '.')

st.title('✈️ Cek Perkiraan Harga Tiket')
st.write('Isi rencana perjalananmu, lalu tekan tombol untuk melihat perkiraan harganya.')

col1, col2 = st.columns(2)
asal = col1.selectbox('Dari kota', meta['kota'], index=meta['kota'].index('Delhi'))
tujuan_opsi = [k for k in meta['kota'] if k != asal]
tujuan = col2.selectbox('Ke kota', tujuan_opsi,
                        index=tujuan_opsi.index('Mumbai') if 'Mumbai' in tujuan_opsi else 0)

hari_ini = dt.date.today()
tgl = st.date_input('Tanggal berangkat',
                    value=hari_ini + dt.timedelta(days=30),
                    min_value=hari_ini + dt.timedelta(days=meta['hari_min']),
                    max_value=hari_ini + dt.timedelta(days=meta['hari_max']))

kelas = st.radio('Kelas', ['Economy', 'Business'], horizontal=True)
maskapai = st.selectbox('Maskapai', meta['maskapai'][kelas])
transit = st.selectbox('Jumlah transit', meta['transit'], format_func=lambda k: TRANSIT[k])

col3, col4 = st.columns(2)
jam_berangkat = col3.selectbox('Jam berangkat', meta['jam'], index=meta['jam'].index('Morning'),
                               format_func=lambda k: JAM[k])
jam_tiba = col4.selectbox('Jam tiba', meta['jam'], index=meta['jam'].index('Evening'),
                          format_func=lambda k: JAM[k])

if st.button('Cek Harga', type='primary', use_container_width=True):
    durasi = meta['durasi'][(asal, tujuan, transit)]
    baris = pd.DataFrame([{
        'airline': maskapai, 'source_city': asal, 'departure_time': jam_berangkat,
        'stops': transit, 'arrival_time': jam_tiba, 'destination_city': tujuan,
        'class': kelas, 'duration': durasi, 'days_left': (tgl - hari_ini).days,
    }])
    harga = float(pipe.predict(baris)[0])
    p = meta['galat_p80'][kelas]

    st.metric('Perkiraan harga', format_harga(harga))
    st.write(f'Kemungkinan besar harganya berkisar dari **{format_harga(harga * (1 - p / 100))}** '
             f'sampai **{format_harga(harga * (1 + p / 100))}**.')
    st.caption('Ini hanya perkiraan, bukan harga resmi dari maskapai.')
    st.caption(f'Lama terbang diperkirakan sekitar {durasi:.1f} jam.')
