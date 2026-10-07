# ✈️ Prediksi Harga Tiket Pesawat

Aplikasi web yang memperkirakan harga tiket pesawat domestik India berdasarkan rute, maskapai, kelas, jumlah transit, jam terbang, dan waktu pemesanan. Perkiraan dibuat dengan model machine learning (Random Forest) yang dilatih pada sekitar 300 ribu data tiket.

**🔗 Coba aplikasinya:** 
<img width="647" height="786" alt="prediksi-tiket" src="https://github.com/user-attachments/assets/bcf83ade-e3e8-4a88-9f2f-083e5547a4a7" />
[[LINK-APLIKASI-STREAMLIT]](https://prediksi-harga-tiket-jvy2v7xcluf5rxktcirrcc.streamlit.app/)


## Ringkasan hasil

| Metrik (data uji) | Nilai |
|---|---|
| R² | 0,9847 |
| MAE (rata-rata selisih harga) | 1.090,7 |
| RMSE | 2.808,3 |

Sebagai pembanding, model linear hanya mencapai R² 0,91 dengan MAE sekitar 4.533, jadi hubungan antara fitur dan harga memang tidak linear.

Rata-rata, perkiraan model meleset sekitar 8,6% untuk kelas Economy dan 3,8% untuk kelas Business. Sekitar 8 dari 10 perkiraan meleset kurang dari 13% (Economy) dan 7% (Business). Angka per kelas ini diukur pada model 100 pohon, sedangkan model 40 pohon yang dipakai di aplikasi memberi hasil keseluruhan yang hampir identik.

## Data

- Sekitar 300 ribu tiket (300.153 baris), 6 maskapai, 6 kota, 30 rute, penerbangan domestik India.
- Fitur: maskapai, kota asal dan tujuan, jam berangkat dan tiba, jumlah transit, kelas, durasi, dan jumlah hari sebelum berangkat.
- Target: harga tiket.
- Sumber data: https://www.kaggle.com/datasets/rohitgrewal/airlines-flights-data

## Temuan utama

- Penentu harga terbesar adalah **kelas** (Economy atau Business), lalu durasi, waktu pemesanan, dan maskapai.
- Untuk **Economy**, tiket yang dipesan 15 hari atau lebih sebelum berangkat memiliki median harga sekitar 53% lebih rendah (4.971 dibanding 10.643). Untuk **Business**, selisihnya hanya sekitar 3%.
- Ini adalah pola yang terlihat di data, bukan bukti bahwa harga akan turun jika menunggu.

## Metodologi

1. Pembagian data 80/20, dan data uji hanya dipakai satu kali di akhir.
2. Pra-pemrosesan: one-hot encoding untuk kolom kategori, ordinal encoding untuk transit dan kelas, Yeo-Johnson untuk durasi, dan standardisasi untuk jumlah hari.
3. Seleksi fitur: variance threshold (membuang satu fitur berfrekuensi sangat rendah), VIF (maksimum 6,0, tidak ada multikolinearitas serius), serta tree importance dan Lasso yang tidak menemukan fitur lain yang aman dibuang. Tersisa 28 fitur.
4. Perbandingan model dengan validasi silang 5 fold:

| Model | R² validasi | MAE validasi |
|---|---|---|
| Linear Regression | 0,9104 | 4.533 |
| Decision Tree | 0,9758 | 1.209 |
| HistGradientBoosting (default) | 0,9701 | 2.338 |
| Extra Trees | 0,9827 | 1.164 |
| **Random Forest** | **0,9850** | **1.116** |

5. Tuning Random Forest dan Extra Trees (`min_samples_leaf`, `max_features`) menunjukkan bahwa pengaturan bawaan sudah optimal. Random Forest dipilih sebagai model akhir.
6. Model di aplikasi dikecilkan dari 100 menjadi 40 pohon agar muat di batas ukuran file GitHub (74 MB), dengan akurasi yang hampir sama.

## Aplikasi

Pengguna memilih kota asal dan tujuan, tanggal berangkat, kelas, maskapai, jumlah transit, serta jam berangkat dan tiba. Aplikasi menampilkan perkiraan harga beserta kisaran yang kemungkinan besar mencakup harga sebenarnya. Durasi penerbangan diisi otomatis dari median durasi rute yang sama.

## Struktur repositori

| File | Fungsi |
|---|---|
| `app.py` | Aplikasi Streamlit |
| `flight_price_pipeline.pkl` | Pipeline lengkap (pra-pemrosesan dan model) |
| `meta_app.pkl` | Daftar pilihan, tabel durasi, dan batas kesalahan |
| `requirements.txt` | Versi paket yang dipakai |

## Menjalankan di komputer sendiri

```bash
pip install -r requirements.txt
streamlit run app.py
```

Versi paket dikunci (misalnya scikit-learn 1.6.1), jadi gunakan Python 3.12 agar semua paket tersedia.

## Batasan

- Data adalah potret satu periode dan satu sumber, khusus penerbangan domestik India. Untuk rute, maskapai, atau musim lain, model perlu dilatih ulang.
- Model memprediksi harga yang tercatat, bukan harga optimal, dan tidak memakai data permintaan atau jumlah kursi.
- Pembagian data dilakukan acak, sehingga penerbangan yang sama bisa muncul di data latih dan uji. Untuk rute atau tanggal yang benar-benar baru, akurasinya bisa lebih rendah.
- Sekitar separuh kombinasi (rute, transit, jam berangkat, jam tiba) jarang atau tidak ada di data, dan perkiraan untuk kombinasi itu kurang pasti.
- Durasi diisi dari median per rute dan jumlah transit, sehingga hanya perkiraan kasar.
- Harga ditampilkan dalam ₹ (rupee). [PASTIKAN MATA UANG DARI SUMBER DATASET]
- Hasilnya hanya perkiraan, bukan harga resmi dari maskapai.

## Rencana pengembangan

- Saran waktu pemesanan (khusus Economy) dan penilaian murah, wajar, atau mahal dibanding rata-rata rute.
- Perbandingan maskapai di rute yang sama dari data tiket nyata.
- Peringatan untuk kombinasi yang jarang di data.
- Evaluasi dengan pembagian per rute atau per waktu, serta pelatihan ulang berkala dengan data baru.

## Pembuat

[INDRA JAYADI]
