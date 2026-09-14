# -*- coding: utf-8 -*-
"""
Kalkulus Integral Etnomatematika Terubuk — versi Streamlit
Dikonversi dari bahan ajar HTML dengan konten, alur, dan perhitungan yang sama.
Jalankan dengan:  streamlit run app.py
"""

import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Kalkulus Integral Etnomatematika Terubuk",
    page_icon="🌿",
    layout="wide",
)

FOREST = "#1F3D2B"
MOSS = "#4C7A57"
MOSS_SOFT = "#DCE9DE"
GOLD = "#C9971C"
GOLD_SOFT = "#F5E6C0"
CLAY = "#A65D42"
BG = "#F3F6EE"
INK_SOFT = "#4B564C"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {BG}; }}
    h1, h2, h3 {{ color: {FOREST} !important; font-family: Georgia, 'Times New Roman', serif; }}
    .kicker {{ color: {MOSS}; font-weight: 600; font-size: 0.8rem; text-transform: none; }}
    .badge {{ display:inline-block; padding: 3px 11px; border-radius: 999px;
              font-size: 0.75rem; font-weight: 600; background: {MOSS_SOFT}; color: {FOREST};
              margin-bottom: 6px; }}
    .equation {{ font-family: 'Courier New', monospace; font-size: 1.1rem; color: {FOREST};
                 background: {GOLD_SOFT}; display:inline-block; padding: 10px 16px;
                 border-radius: 10px; margin: 8px 0; }}
    .info-box {{ background: {MOSS_SOFT}; border-radius: 10px; padding: 14px 18px;
                 color: {FOREST}; font-size: 0.95rem; }}
    .interp-box {{ background: #FBFBF8; border-left: 4px solid {GOLD}; border-radius: 8px;
                   padding: 14px 18px; font-size: 0.95rem; }}
    .result-card {{ background: {FOREST}; color: #EFF5EE; border-radius: 14px;
                    padding: 20px 24px; margin-top: 10px; }}
    .result-card .big {{ font-size: 1.8rem; font-weight: 700; }}
    .result-card .label {{ font-size: 0.8rem; color: #B9D0BE; }}
    .result-card .sub {{ font-size: 0.85rem; color: #C9DACB; margin-top: 6px; }}
    .stButton>button {{ background-color: {FOREST}; color: white; border-radius: 8px; border: none; }}
    .stButton>button:hover {{ background-color: #16301F; color: white; }}
    section[data-testid="stSidebar"] {{ background-color: #EAF1E4; }}
    </style>
    """,
    unsafe_allow_html=True,
)
TERUBUK_IMG = os.path.join(os.path.dirname(__file__), "terubuk.png")

# ============================================================
# DATA CONTOH & STATE
# ============================================================
SAMPLE = pd.DataFrame(
    {
        "Minggu": [1, 2, 3, 4, 5, 6, 7, 8],
        "Tinggi Terubuk (cm)": [8.2, 14.5, 21.0, 28.8, 35.2, 41.0, 45.5, 49.0],
    }
)

if "data" not in st.session_state:
    st.session_state.data = SAMPLE.copy()

if "identitas" not in st.session_state:
    st.session_state.identitas = {
        "sasaran": "Peserta didik kelas XI / semester yang mempelajari kalkulus integral",
        "alokasi": "2 x 45 menit",
    }

if "bounds" not in st.session_state:
    st.session_state.bounds = None  # diisi setelah data pertama kali diproses


# ============================================================
# FUNGSI MATEMATIKA
# ============================================================
def fit_quadratic(df: pd.DataFrame):
    """Regresi kuadrat H(t) = a t^2 + b t + c menggunakan metode kuadrat terkecil."""
    x = df["Minggu"].to_numpy(dtype=float)
    y = df["Tinggi Terubuk (cm)"].to_numpy(dtype=float)
    if len(x) < 3 or np.unique(x).size < 3:
        return 0.0, 0.0, float(np.mean(y)) if len(y) else 0.0
    a, b, c = np.polyfit(x, y, 2)
    return float(a), float(b), float(c)


def H(t, a, b, c):
    return a * t**2 + b * t + c


def Hprime(t, a, b):
    return 2 * a * t + b


def antiderivative_at(t, a, b, c):
    return (a / 3) * t**3 + (b / 2) * t**2 + c * t


def exact_integral(lo, hi, a, b, c):
    return antiderivative_at(hi, a, b, c) - antiderivative_at(lo, a, b, c)


def trapezoid_integral(lo, hi, a, b, c, n=1000):
    xs = np.linspace(lo, hi, n + 1)
    ys = H(xs, a, b, c)
    return float(np.trapezoid(ys, xs))


def numeric_gradient(df: pd.DataFrame):
    """Laju rata-rata antar-titik data (beda hingga tengah untuk titik dalam)."""
    d = df.sort_values("Minggu").reset_index(drop=True)
    xs = d["Minggu"].to_numpy(dtype=float)
    ys = d["Tinggi Terubuk (cm)"].to_numpy(dtype=float)
    n = len(d)
    slopes = np.zeros(n)
    for i in range(n):
        if n < 2:
            slopes[i] = 0
        elif i == 0:
            slopes[i] = (ys[1] - ys[0]) / (xs[1] - xs[0])
        elif i == n - 1:
            slopes[i] = (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1])
        else:
            slopes[i] = (ys[i + 1] - ys[i - 1]) / (xs[i + 1] - xs[i - 1])
    return xs, slopes


def fmt(x, d=2):
    try:
        return f"{float(x):.{d}f}"
    except (ValueError, TypeError):
        return str(x)


def get_clean_data():
    df = st.session_state.data.copy()
    df = df.dropna()
    df = df[pd.to_numeric(df["Minggu"], errors="coerce").notna()]
    df = df[pd.to_numeric(df["Tinggi Terubuk (cm)"], errors="coerce").notna()]
    df["Minggu"] = df["Minggu"].astype(float)
    df["Tinggi Terubuk (cm)"] = df["Tinggi Terubuk (cm)"].astype(float)
    df = df.sort_values("Minggu").reset_index(drop=True)
    return df


# ============================================================
# SIDEBAR — NAVIGASI
# ============================================================
st.sidebar.markdown("### 🌿 Peta Belajar")
menu = st.sidebar.radio(
    "Navigasi bahan ajar",
    [
        "📖 Beranda",
        "📚 Materi",
        "🌿 Konteks Terubuk",
        "📊 Data & Grafik",
        "📈 Model Matematika",
        "∫ Integral",
        "✏️ Aktivitas",
        "📝 Latihan",
        "🎯 Evaluasi",
        "💭 Refleksi",
    ],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption(
    "Bahan ajar Kalkulus Integral berbasis etnomatematika Terubuk — "
    "dari konsep, contoh, aktivitas, hingga evaluasi."
)

# Data & model dihitung ulang otomatis setiap kali skrip berjalan (Streamlit rerun)
df_clean = get_clean_data()
a, b, c = fit_quadratic(df_clean) if len(df_clean) >= 3 else (0.0, 0.0, 0.0)

if len(df_clean) > 0:
    domain_lo, domain_hi = float(df_clean["Minggu"].min()), float(df_clean["Minggu"].max())
else:
    domain_lo, domain_hi = 1.0, 8.0

if st.session_state.bounds is None:
    st.session_state.bounds = (domain_lo, domain_hi)


# ============================================================
# HALAMAN: BERANDA
# ============================================================
def page_beranda():
    st.markdown(
        f"""
        <div style="padding: 28px 30px; border-radius: 16px;
                    background: linear-gradient(180deg, #EAF1E4 0%, {BG} 100%);
                    border: 1px solid #D8E0D5; margin-bottom: 18px;">
            <div class="kicker">Bahan Ajar Kalkulus Integral · Etnomatematika</div>
            <h1 style="font-size: 2.1rem; margin: 6px 0;">Membaca Pertumbuhan Terubuk Lewat Bahasa Integral</h1>
            <p style="color:{INK_SOFT}; max-width: 70ch;">
            Terubuk adalah tanaman lokal yang biasa diamati dalam pembelajaran etnomatematika karena
            polanya yang mudah diukur dari minggu ke minggu. Bahan ajar ini mengajakmu belajar integral
            secara runtut — mulai dari konsep dasar, contoh soal, sampai mengolah data pertumbuhan Terubuk
            sendiri: membuat model matematis, menurunkannya untuk melihat laju pertumbuhan, lalu
            mengintegralkannya untuk menghitung akumulasi pada rentang waktu yang kamu pilih.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Daftar isi bahan ajar")
    st.caption(
        "Bahan ajar ini disusun runtut dari konsep dasar sampai evaluasi. Ikuti urutannya supaya "
        "alurnya nyambung, tapi kamu juga boleh lompat ke bagian tertentu lewat menu di sebelah kiri."
    )
    toc = [
        "Identitas bahan ajar", "Tujuan pembelajaran", "Prasyarat",
        "Apersepsi / pertanyaan pemantik", "Mengenal konteks Terubuk",
        "Materi: konsep integral, integral tentu, Teorema Dasar Kalkulus",
        "Contoh soal dan pembahasan", "Aktivitas 1 — Data pengamatan",
        "Grafik pertumbuhan", "Aktivitas 2 — Model matematika",
        "Turunan dan laju pertumbuhan", "Aktivitas 3 — Turunan & integral",
        "Integral interaktif", "Aktivitas interpretasi", "Rangkuman",
        "Latihan", "Evaluasi", "Refleksi",
    ]
    col1, col2 = st.columns(2)
    half = len(toc) // 2 + len(toc) % 2
    with col1:
        for i, item in enumerate(toc[:half], start=1):
            st.markdown(f"{i}. {item}")
    with col2:
        for i, item in enumerate(toc[half:], start=half + 1):
            st.markdown(f"{i}. {item}")

    st.markdown("---")
    st.markdown('<span class="badge">Identitas</span>', unsafe_allow_html=True)
    st.markdown("### Identitas bahan ajar")
    idc1, idc2 = st.columns(2)
    with idc1:
        st.markdown(f"**Mata pelajaran**  \nKalkulus")
        st.markdown(f"**Materi**  \nIntegral (integral tak tentu & integral tentu)")
        st.markdown(f"**Pendekatan**  \nEtnomatematika")
    with idc2:
        st.session_state.identitas["sasaran"] = st.text_input(
            "Sasaran peserta didik", value=st.session_state.identitas["sasaran"]
        )
        st.session_state.identitas["alokasi"] = st.text_input(
            "Alokasi waktu", value=st.session_state.identitas["alokasi"]
        )
        st.markdown(f"**Konteks**  \nPertumbuhan tanaman Terubuk")
    st.caption("Kolom sasaran peserta didik dan alokasi waktu dapat diedit sesuai kebutuhan kelas.")

    st.markdown("---")
    st.markdown('<span class="badge">Tujuan</span>', unsafe_allow_html=True)
    st.markdown("### Tujuan pembelajaran")
    st.caption("Setelah mempelajari bahan ajar ini, peserta didik diharapkan mampu:")
    tujuan = [
        "Menjelaskan konsep integral sebagai kebalikan (antiturunan) dari proses turunan.",
        "Menjelaskan pengertian integral tentu dan maknanya sebagai luas daerah di bawah kurva.",
        "Menggunakan Teorema Dasar Kalkulus untuk menghitung nilai integral tentu suatu fungsi.",
        "Menghitung integral tak tentu dan integral tentu dari fungsi polinomial sederhana.",
        "Menginterpretasikan hasil integral dalam konteks pertumbuhan tanaman Terubuk, termasuk satuannya.",
        "Menghubungkan konsep turunan dan integral dengan fenomena pertumbuhan yang dapat diamati di lingkungan sekitar.",
    ]
    for t in tujuan:
        st.markdown(f"- {t}")

    st.markdown("---")
    st.markdown('<span class="badge">Prasyarat</span>', unsafe_allow_html=True)
    st.markdown("### Prasyarat")
    prereq = [
        ("Fungsi dan grafik", "membaca dan menggambar grafik fungsi, terutama fungsi kuadrat."),
        ("Operasi aljabar", "penjumlahan, perkalian, dan pemangkatan suku aljabar."),
        ("Konsep turunan", "aturan pangkat turunan dan makna turunan sebagai laju perubahan."),
        ("Luas daerah di bawah kurva", "gagasan bahwa luas dapat didekati dengan menjumlahkan "
                                        "potongan-potongan kecil (misalnya persegi panjang tipis)."),
    ]
    for label, desc in prereq:
        st.markdown(f"- **{label}** — {desc}")

    st.markdown("---")
    st.markdown('<span class="badge">Apersepsi</span>', unsafe_allow_html=True)
    st.markdown("### Sebelum mulai, coba pikirkan dulu")
    st.caption("Jawab dengan pemahamanmu sendiri dulu — belum ada jawaban benar/salah di sini, "
               "ini hanya pemantik supaya kamu siap masuk ke materi.")
    st.text_area("1. Bagaimana cara kamu mengetahui perubahan tinggi Terubuk dari waktu ke waktu?",
                 key="aper_1", height=70)
    st.text_area("2. Jika tinggi tanaman berubah setiap minggu, bagaimana kita bisa menggambarkan "
                 "perubahan itu secara matematis?", key="aper_2", height=70)
    st.text_area('3. Menurutmu, apa yang dimaksud dengan "akumulasi" dalam suatu proses yang '
                 "berlangsung terhadap waktu?", key="aper_3", height=70)


# ============================================================
# HALAMAN: MATERI
# ============================================================
def page_materi():
    st.markdown('<span class="badge">Materi</span>', unsafe_allow_html=True)
    st.markdown("## Konsep integral")

    with st.expander("Apa itu integral?", expanded=True):
        st.write(
            "Integral adalah salah satu operasi dasar dalam kalkulus yang merupakan kebalikan dari "
            "turunan. Jika turunan mengubah suatu fungsi menjadi fungsi laju perubahannya, integral "
            "melakukan proses sebaliknya: dari fungsi laju perubahan, kita mencari kembali fungsi "
            "aslinya."
        )
    with st.expander("Integral sebagai antiturunan"):
        st.write(
            "Jika F'(t) = f(t), maka F(t) disebut antiturunan (atau integral tak tentu) dari f(t). "
            "Proses mencari F(t) dari f(t) disebut mengintegralkan."
        )
    with st.expander("Integral tak tentu"):
        st.write(
            "Integral tak tentu ditulis sebagai ∫f(t) dt = F(t) + C, dengan C adalah konstanta "
            "integrasi (karena turunan dari konstanta selalu nol, banyak fungsi F(t)+C yang punya "
            "turunan sama)."
        )
        st.markdown('<div class="equation">∫tⁿ dt = (tⁿ⁺¹)/(n+1) + C,&nbsp; n ≠ -1</div>', unsafe_allow_html=True)

    st.markdown("## Integral tentu")
    st.markdown('<div class="equation">∫ₐᵇ f(t) dt</div>', unsafe_allow_html=True)
    st.write(
        "Berbeda dengan integral tak tentu yang hasilnya berupa fungsi, hasil integral tentu berupa "
        "sebuah **nilai (bilangan)** yang menyatakan akumulasi f(t) sepanjang interval [a, b]. Secara "
        "grafis, nilai ini sama dengan luas daerah di bawah kurva f(t) antara t = a dan t = b."
    )
    st.caption(
        "Gagasan ini berasal dari menjumlahkan banyak potongan persegi panjang tipis di bawah kurva "
        "(jumlah Riemann) — semakin tipis potongannya, semakin akurat pendekatan luasnya."
    )

    st.markdown("## Teorema Dasar Kalkulus")
    st.write(
        "Teorema Dasar Kalkulus menghubungkan turunan dan integral: jika F(t) adalah antiturunan dari "
        "f(t), maka integral tentu f(t) pada interval [a, b] dapat dihitung tanpa menjumlahkan potongan "
        "kecil satu per satu, cukup dengan:"
    )
    st.markdown('<div class="equation">∫ₐᵇ f(t) dt = F(b) − F(a)</div>', unsafe_allow_html=True)
    st.write(
        "Artinya, untuk menghitung akumulasi suatu besaran pada suatu interval waktu, kita cukup "
        "mencari antiturunannya lalu menghitung selisih nilainya di batas atas dan batas bawah."
    )

    st.markdown("---")
    st.markdown('<span class="badge">Contoh</span>', unsafe_allow_html=True)
    st.markdown("## Contoh soal dan pembahasan")
    st.caption("Perhatikan langkah-langkah penyelesaiannya, bukan cuma hasil akhirnya.")

    with st.container(border=True):
        st.markdown("#### Contoh 1 — Integral tak tentu")
        st.write("**Soal:** Tentukan ∫(3t² + 2t) dt.")
        st.markdown(
            "1. Gunakan aturan pangkat untuk tiap suku: ∫tⁿ dt = tⁿ⁺¹/(n+1).\n"
            "2. ∫3t² dt = 3 · (t³/3) = t³\n"
            "3. ∫2t dt = 2 · (t²/2) = t²\n"
            "4. Jumlahkan hasilnya dan tambahkan konstanta C."
        )
        st.markdown('<div class="equation">Hasil: ∫(3t² + 2t) dt = t³ + t² + C</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("#### Contoh 2 — Integral tentu")
        st.write("**Soal:** Hitung ∫₁³ (2t + 1) dt.")
        st.markdown(
            "1. Cari antiturunan: F(t) = t² + t.\n"
            "2. Hitung F(3) = 3² + 3 = 12.\n"
            "3. Hitung F(1) = 1² + 1 = 2.\n"
            "4. Gunakan Teorema Dasar Kalkulus: F(3) − F(1) = 12 − 2 = 10."
        )
        st.markdown('<div class="equation">Hasil: ∫₁³ (2t + 1) dt = 10</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("#### Contoh 3 — Konteks pertumbuhan Terubuk")
        st.write(
            "Sebagai ilustrasi (terpisah dari kalkulator interaktif di halaman **∫ Integral**), "
            "misalkan dari sekelompok data pengamatan diperoleh model pertumbuhan Terubuk:"
        )
        st.markdown('<div class="equation">H(t) = −0.3t² + 8t + 2</div>', unsafe_allow_html=True)
        st.write("dengan H(t) dalam cm dan t dalam minggu.")
        st.markdown(
            "- **Diketahui:** H(t) = −0.3t² + 8t + 2, rentang waktu t = 1 sampai t = 4 minggu.\n"
            "- **Ditanyakan:** Nilai ∫₁⁴ H(t) dt dan maknanya.\n"
            "- **Model yang digunakan:** antiturunan F(t) = −0.1t³ + 4t² + 2t.\n"
            "- **Proses:** F(4) = −0.1(64) + 4(16) + 2(4) = −6.4 + 64 + 8 = 65.6. "
            "F(1) = −0.1(1) + 4(1) + 2(1) = −0.1 + 4 + 2 = 5.9. F(4) − F(1) = 65.6 − 5.9 = 59.7.\n"
            "- **Hasil:** ∫₁⁴ H(t) dt = 59.7 cm·minggu.\n"
            "- **Interpretasi:** Nilai 59.7 cm·minggu menyatakan akumulasi tinggi Terubuk terhadap "
            "waktu sepanjang minggu ke-1 hingga ke-4 menurut model — bukan tinggi tanaman pada satu "
            "titik waktu. Perhatikan satuannya adalah cm·minggu (cm dikali minggu), karena integral "
            "mengalikan nilai H(t) (cm) dengan rentang waktu dt (minggu)."
        )

    st.markdown("---")
    st.markdown("### Rangkuman")
    st.markdown(
        "- **Integral** adalah kebalikan dari turunan; mencari fungsi asal dari fungsi laju perubahannya.\n"
        "- **Integral tak tentu** ∫f(t)dt = F(t) + C menghasilkan fungsi (dengan konstanta C).\n"
        "- **Integral tentu** ∫ₐᵇ f(t)dt menghasilkan sebuah nilai yang menyatakan luas daerah di "
        "bawah kurva f(t) pada interval [a, b].\n"
        "- **Teorema Dasar Kalkulus** menyatakan ∫ₐᵇ f(t)dt = F(b) − F(a), dengan F antiturunan dari f.\n"
        "- **Turunan dan integral saling berkebalikan:** turunan mengukur laju perubahan sesaat, "
        "integral mengukur akumulasi perubahan itu sepanjang suatu interval.\n"
        "- Pada konteks Terubuk, integral H(t) pada rentang [a, b] menyatakan **akumulasi tinggi "
        "terhadap waktu**, dengan satuan **cm·minggu** — bukan tinggi tanaman itu sendiri."
    )


# ============================================================
# HALAMAN: KONTEKS TERUBUK
# ============================================================
def page_konteks():
    st.markdown('<span class="badge">Konteks</span>', unsafe_allow_html=True)
    st.markdown("## 🌿 Mengenal Tanaman Terubuk")

    col_img, col_text = st.columns([1, 1.4])
    with col_img:
        if os.path.exists(TERUBUK_IMG):
            st.image(TERUBUK_IMG, use_container_width=True)
            st.caption("Tanaman terubuk (Saccharum edule)")

        else:
            st.info(
                "Gambar belum tersedia. Simpan foto tanaman terubuk sebagai  "
                "di folder proyek, lengkap dengan kredit sumbernya."
            )

    with col_text:
        st.write(
            "Terubuk dikenal juga sebagai **tebu telur**, dengan nama ilmiah **_Saccharum edule_**. "
            "Bentuknya beruas-ruas dan menyerupai tanaman tebu, tetapi konteks pemanfaatannya berbeda: "
            "bagian yang biasa diambil adalah massa bunga muda yang masih terbungkus pelepah daun, "
            "bukan batangnya untuk diambil sarinya seperti tebu biasa."
        )
        st.write(
            "Terubuk dipilih sebagai konteks belajar karena pertumbuhannya dapat diamati dan diukur "
            "secara berkala dari minggu ke minggu, sehingga cocok dijadikan data nyata untuk belajar "
            "kalkulus."
        )

    st.markdown(
        """
        <div class="info-box">
        Mengamati pertumbuhan tanaman yang dikenal di lingkungan sekitar adalah salah satu bentuk
        <strong>etnomatematika</strong>: cara memandang aktivitas atau pengetahuan lokal melalui
        kacamata matematika. Dengan mengukur tinggi Terubuk setiap minggu, kita sebenarnya sedang
        mengumpulkan data yang bisa diolah menjadi fungsi matematis, lalu dianalisis lajunya
        (turunan) dan akumulasinya (integral).
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "Catatan: bagian ini dapat dilengkapi guru dengan informasi budaya atau kearifan lokal "
        "spesifik mengenai Terubuk sesuai daerah masing-masing."
    )

    st.markdown("#### Alur belajar etnomatematika pada bahan ajar ini")
    st.markdown(
        "**Pengamatan tanaman → Pengumpulan data → Pemodelan matematika → Turunan → Integral → "
        "Interpretasi**"
    )


# ============================================================
# HALAMAN: DATA & GRAFIK
# ============================================================
def page_data():
    st.markdown('<span class="badge">Aktivitas 1</span>', unsafe_allow_html=True)
    st.markdown("## Mengamati data pertumbuhan")
    st.caption(
        "Isi tinggi Terubuk (cm) untuk tiap minggu pengamatan. Sudah tersedia data contoh — silakan "
        "ubah nilainya langsung di tabel, tambah baris baru di bagian bawah tabel, atau hapus baris "
        "lewat kotak centang di kolom paling kiri lalu tekan tombol hapus (ikon tempat sampah)."
    )

    edited = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        key="data_editor",
        column_config={
            "Minggu": st.column_config.NumberColumn("Minggu", step=1, min_value=0),
            "Tinggi Terubuk (cm)": st.column_config.NumberColumn("Tinggi Terubuk (cm)", step=0.1, min_value=0.0),
        },
    )
    st.session_state.data = edited

    bcol1, bcol2, bcol3 = st.columns(3)
    with bcol1:
        if st.button("＋ Tambah minggu"):
            df = st.session_state.data
            last_week = df["Minggu"].max() if len(df) else 0
            new_row = pd.DataFrame({"Minggu": [last_week + 1], "Tinggi Terubuk (cm)": [0.0]})
            st.session_state.data = pd.concat([df, new_row], ignore_index=True)
            st.rerun()
    with bcol2:
        st.caption("Model dihitung ulang otomatis setiap kali data berubah.")
    with bcol3:
        if st.button("↺ Pakai data contoh"):
            st.session_state.data = SAMPLE.copy()
            st.session_state.bounds = None
            st.rerun()

    if len(df_clean) < 3:
        st.warning("Minimal 3 titik data (dengan nilai minggu berbeda) diperlukan untuk model kuadratik.")

    st.markdown("#### Catatan pertumbuhan per minggu")
    if len(df_clean) > 0:
        prev_h = None
        for _, row in df_clean.iterrows():
            wk, h = row["Minggu"], row["Tinggi Terubuk (cm)"]
            if prev_h is None:
                note = "titik awal pengamatan"
            else:
                delta = h - prev_h
                arrow = "▲" if delta >= 0 else "▼"
                note = f"{arrow} {fmt(abs(delta), 1)} cm dari minggu sebelumnya"
            st.markdown(
                f"<div style='background:#FBFBF8; border-left:3px solid {MOSS}; border-radius:6px; "
                f"padding:8px 12px; margin-bottom:6px;'>"
                f"<b>Minggu {fmt(wk,0)}</b> — tinggi {fmt(h,1)} cm — {note}</div>",
                unsafe_allow_html=True,
            )
            prev_h = h

    st.markdown("---")
    st.markdown("### Grafik pertumbuhan hasil pengamatan")
    st.caption(
        "Titik-titik di bawah ini persis data yang kamu masukkan — belum ada model matematika, murni "
        "hasil ukur di lapangan."
    )
    if len(df_clean) > 0:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df_clean["Minggu"], y=df_clean["Tinggi Terubuk (cm)"],
                mode="lines+markers", name="Data pengamatan",
                line=dict(color=MOSS, width=2), marker=dict(color=FOREST, size=9),
            )
        )
        fig.update_layout(
            xaxis_title="Waktu (minggu)", yaxis_title="Tinggi Terubuk (cm)",
            plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", height=400,
            margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data yang bisa ditampilkan.")

    st.markdown("---")
    st.markdown("**Pertanyaan aktivitas:** Dari tabel dan daftar di atas, minggu mana yang mengalami "
                "pertambahan tinggi paling besar? Menurutmu kenapa pertambahannya tidak sama tiap minggu?")
    st.text_area("Tulis pengamatanmu di sini...", key="akt1_jawaban", height=80)


# ============================================================
# HALAMAN: MODEL MATEMATIKA
# ============================================================
def page_model():
    st.markdown('<span class="badge">Aktivitas 2</span>', unsafe_allow_html=True)
    st.markdown("## Menemukan model matematis pertumbuhan")
    st.caption(
        "Data pengamatan didekati dengan model polinomial derajat dua menggunakan metode kuadrat "
        "terkecil, supaya kita punya satu fungsi H(t) yang mewakili pola pertumbuhan Terubuk secara "
        "keseluruhan."
    )

    if len(df_clean) < 3:
        st.warning("Minimal 3 titik data diperlukan untuk membentuk model kuadratik. Lengkapi data "
                   "di halaman **Data & Grafik** terlebih dahulu.")
        return

    st.markdown(
        f'<div class="equation">H(t) = {fmt(a,4)}t² + {fmt(b,4)}t + {fmt(c,4)}</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "**H(t)** menyatakan perkiraan tinggi Terubuk (cm) pada waktu t (minggu) menurut model hasil "
        "regresi — bukan nilai pengukuran langsung, melainkan pendekatan terbaik dari seluruh titik data."
    )

    lo, hi = domain_lo, domain_hi
    ts = np.linspace(lo, hi, 150)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df_clean["Minggu"], y=df_clean["Tinggi Terubuk (cm)"], mode="markers",
                   name="Data pengamatan", marker=dict(color=FOREST, size=9))
    )
    fig.add_trace(
        go.Scatter(x=ts, y=H(ts, a, b, c), mode="lines", name="Model H(t)",
                   line=dict(color=GOLD, width=3))
    )
    fig.update_layout(
        xaxis_title="Waktu (minggu)", yaxis_title="Tinggi Terubuk (cm)",
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", height=400,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Titik = data pengamatan · Garis = model H(t) hasil regresi.")

    st.markdown("---")
    st.markdown("### Turunan: seberapa cepat Terubuk tumbuh?")
    st.write(
        "Turunan H'(t) menunjukkan laju pertumbuhan sesaat (cm per minggu) pada waktu t — ini jawaban "
        'atas pertanyaan "minggu ini Terubuk sedang tumbuh cepat atau melambat?". Karena H\'(t) adalah '
        "turunan dari H(t), maka H(t) adalah salah satu antiturunan dari H'(t) — hubungan inilah yang "
        "nanti dipakai untuk menghitung integral."
    )
    st.markdown(
        f'<div class="equation">H\'(t) = {fmt(2*a,4)}t + {fmt(b,4)}</div>',
        unsafe_allow_html=True,
    )

    xs_grad, slopes = numeric_gradient(df_clean)
    ts2 = np.linspace(lo, hi, 100)
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(x=ts2, y=Hprime(ts2, a, b), mode="lines", name="H'(t) model",
                   line=dict(color=MOSS, width=3))
    )
    fig2.add_trace(
        go.Scatter(x=xs_grad, y=slopes, mode="markers", name="Laju dari data",
                   marker=dict(color=CLAY, size=9))
    )
    fig2.update_layout(
        xaxis_title="Waktu (minggu)", yaxis_title="Laju pertumbuhan (cm/minggu)",
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", height=380,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Garis = H'(t) dari model · Titik = laju rata-rata antar-minggu dari data asli.")

    st.markdown("---")
    st.markdown("**Pertanyaan aktivitas:** Perhatikan grafik model di atas. Apakah kurva H(t) naik "
                "terus, atau ada bagian yang melandai? Kaitkan bentuk kurva ini dengan nilai koefisien "
                "a pada H(t) = at² + bt + c.")
    st.text_area("Tulis analisismu di sini...", key="akt2_jawaban", height=80)

    st.markdown("---")
    st.markdown('<span class="badge">Aktivitas 3</span>', unsafe_allow_html=True)
    st.markdown("### Menghubungkan turunan dan integral")
    st.caption(
        "Sebelum masuk ke kalkulator integral, samakan dulu pemahaman tentang tiga hal yang saling "
        "berkaitan tapi punya makna berbeda:"
    )
    idc1, idc2 = st.columns([1, 3])
    rows = [
        ("H(t)", "Tinggi Terubuk pada waktu t (satuan cm)"),
        ("H'(t)", "Laju pertumbuhan pada waktu t (satuan cm/minggu)"),
        ("∫ₐᵇ H(t) dt", "Akumulasi H(t) pada rentang [a, b] (satuan cm·minggu)"),
    ]
    for label, desc in rows:
        st.markdown(f"**{label}** — {desc}")
    st.markdown(
        '**Pertanyaan aktivitas:** Jelaskan dengan kalimatmu sendiri, apa bedanya mengetahui '
        '"tinggi Terubuk minggu ke-5" dengan mengetahui "akumulasi H(t) dari minggu 1 sampai 5"?'
    )
    st.text_area("Tulis penjelasanmu di sini...", key="akt3_jawaban", height=90)


# ============================================================
# HALAMAN: INTEGRAL
# ============================================================
def page_integral():
    st.markdown('<span class="badge">Integral interaktif</span>', unsafe_allow_html=True)
    st.markdown("## Integral: akumulasi tinggi pada rentang waktu pilihanmu")

    if len(df_clean) < 3:
        st.warning("Minimal 3 titik data diperlukan untuk membentuk model kuadratik. Lengkapi data "
                   "di halaman **Data & Grafik** terlebih dahulu.")
        return

    st.caption(
        "Geser batas bawah dan batas atas untuk memilih rentang minggu yang ingin dianalisis. Daerah "
        "yang diarsir pada grafik adalah nilai ∫ H(t) dt — luas di bawah kurva model pada rentang tersebut."
    )
    st.markdown(
        f"""
        <div class="info-box">
        <strong>∫ₐᵇ H(t) dt</strong> merepresentasikan akumulasi nilai H(t) terhadap waktu pada interval
        [a, b], dan secara grafik adalah luas daerah di bawah kurva H(t) pada interval tersebut. Karena
        H(t) bersatuan cm dan t bersatuan minggu, hasil integralnya <strong>bukan</strong> tinggi
        tanaman dalam cm, melainkan besaran akumulatif dengan satuan <strong>cm·minggu</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    lo_default, hi_default = st.session_state.bounds
    lo_default = max(domain_lo, min(lo_default, domain_hi))
    hi_default = max(domain_lo, min(hi_default, domain_hi))

    c1, c2 = st.columns(2)
    with c1:
        lo = st.slider("Batas bawah (minggu)", min_value=float(domain_lo), max_value=float(domain_hi),
                        value=float(lo_default), step=0.1, key="slider_lo")
    with c2:
        hi = st.slider("Batas atas (minggu)", min_value=float(domain_lo), max_value=float(domain_hi),
                        value=float(hi_default), step=0.1, key="slider_hi")

    if lo >= hi:
        st.error("Batas bawah harus lebih kecil dari batas atas.")
        return
    st.session_state.bounds = (lo, hi)

    ts_full = np.linspace(domain_lo, domain_hi, 200)
    ts_shade = np.linspace(lo, hi, 100)
    ys_full = H(ts_full, a, b, c)
    ys_shade = H(ts_shade, a, b, c)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts_full, y=ys_full, mode="lines", name="Model H(t)",
                              line=dict(color=FOREST, width=2.5)))
    fig.add_trace(go.Scatter(x=ts_shade, y=ys_shade, mode="lines", name="Daerah integral",
                              fill="tozeroy", line=dict(color=GOLD, width=2),
                              fillcolor="rgba(201,151,28,0.35)"))
    max_y = max(float(np.max(ys_full)), float(df_clean["Tinggi Terubuk (cm)"].max())) * 1.15
    fig.add_shape(type="line", x0=lo, x1=lo, y0=0, y1=max_y, line=dict(color=CLAY, dash="dash"))
    fig.add_shape(type="line", x0=hi, x1=hi, y0=0, y1=max_y, line=dict(color=CLAY, dash="dash"))
    fig.update_layout(
        xaxis_title="Waktu (minggu)", yaxis_title="Tinggi Terubuk (cm)",
        xaxis=dict(range=[domain_lo, domain_hi]), yaxis=dict(range=[0, max_y]),
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", height=420,
        margin=dict(l=10, r=10, t=20, b=10), showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    exact = exact_integral(lo, hi, a, b, c)
    numeric = trapezoid_integral(lo, hi, a, b, c, n=1000)

    st.markdown(
        f"""
        <div class="result-card">
            <div class="label">∫ H(t) dt dari {fmt(lo,1)} sampai {fmt(hi,1)} minggu</div>
            <div class="big">{fmt(exact,3)} <span style="font-size:1rem; font-weight:500;">cm·minggu</span></div>
            <div class="sub">Hasil eksak (Teorema Dasar Kalkulus): {fmt(exact,3)} cm·minggu &nbsp;·&nbsp;
            Hasil numerik (metode trapesium, n=1000): {fmt(numeric,3)} cm·minggu &nbsp;·&nbsp;
            Selisih: {fmt(abs(exact-numeric),5)} cm·minggu</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Statistik hasil integral")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Rata-rata H(t) pada rentang", f"{fmt(exact/(hi-lo),2)} cm")
    s2.metric("Tinggi di batas bawah H(a)", f"{fmt(H(lo,a,b,c),2)} cm")
    s3.metric("Tinggi di batas atas H(b)", f"{fmt(H(hi,a,b,c),2)} cm")
    s4.metric("Lebar rentang", f"{fmt(hi-lo,1)} minggu")

    st.markdown("#### Fungsi, antiturunan, dan langkah perhitungan")
    st.markdown(f"1. Fungsi model: H(t) = {fmt(a,4)}t² + {fmt(b,4)}t + {fmt(c,4)}")
    st.markdown(
        f"2. Antiturunan: F(t) = {fmt(a/3,4)}t³ + {fmt(b/2,4)}t² + {fmt(c,4)}t"
    )
    st.markdown(f"3. F({fmt(hi,1)}) = {fmt(antiderivative_at(hi,a,b,c),4)}")
    st.markdown(f"4. F({fmt(lo,1)}) = {fmt(antiderivative_at(lo,a,b,c),4)}")
    st.markdown(
        f"5. ∫ₐᵇ H(t) dt = F({fmt(hi,1)}) − F({fmt(lo,1)}) = **{fmt(exact,3)} cm·minggu**"
    )

    st.markdown("---")
    st.markdown('<span class="badge">Aktivitas interpretasi</span>', unsafe_allow_html=True)
    st.markdown("### Interpretasi hasil")
    st.caption(
        "Interpretasi otomatis di bawah dibuat berdasarkan model dan rentang yang kamu pilih. Baca "
        "dulu, lalu tuliskan pemahamanmu sendiri di kotak yang disediakan."
    )
    growth_note = (
        "Nilai koefisien a yang negatif menunjukkan laju pertumbuhan Terubuk melambat seiring waktu "
        "pada model ini."
        if a < 0 else
        "Nilai koefisien a yang positif menunjukkan laju pertumbuhan Terubuk cenderung meningkat pada "
        "model ini — perlu dicek apakah ini realistis untuk rentang minggu yang diamati."
    )
    st.markdown(
        f"""
        <div class="interp-box">
        Model pertumbuhan yang diperoleh dari data adalah
        <strong>H(t) = {fmt(a,4)}t² + {fmt(b,4)}t + {fmt(c,4)}</strong>.
        Pada rentang minggu <strong>{fmt(lo,1)}</strong> sampai <strong>{fmt(hi,1)}</strong>, nilai
        integral ∫H(t)dt yang dihitung adalah <strong>{fmt(exact,3)} cm·minggu</strong>. Secara konsep,
        nilai ini adalah luas daerah di bawah kurva H(t) pada rentang tersebut — gambaran akumulasi
        H(t) terhadap waktu sepanjang periode itu. Perhatikan satuannya cm·minggu,
        <strong>bukan</strong> tinggi Terubuk dalam cm, karena nilai ini diperoleh dari mengalikan
        tinggi (cm) dengan rentang waktu (minggu). {growth_note}
        <br><br>
        Dalam konteks etnomatematika, pengamatan pertumbuhan tanaman lokal seperti Terubuk memberi
        contoh nyata bahwa konsep turunan (laju perubahan) dan integral (akumulasi) tidak hanya
        berlaku pada rumus abstrak, tetapi juga pada proses yang dikenal sehari-hari oleh masyarakat.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "**Tugasmu:** Jelaskan dengan kalimatmu sendiri apa makna nilai integral yang kamu peroleh "
        "untuk rentang minggu yang kamu pilih. Sebutkan juga satuannya dengan benar."
    )
    st.text_area("Tulis interpretasimu di sini...", key="interp_jawaban", height=90)


# ============================================================
# HALAMAN: AKTIVITAS (konsolidasi 5 aktivitas dengan variasi widget)
# ============================================================
def page_aktivitas():
    st.markdown('<span class="badge">Aktivitas</span>', unsafe_allow_html=True)
    st.markdown("## ✏️ Aktivitas siswa")
    st.caption(
        "Halaman ini merangkum lima aktivitas utama. Beberapa di antaranya juga muncul di halaman "
        "lain (Data & Grafik, Model Matematika, Integral) tepat di konteks materinya — silakan "
        "kerjakan di sana atau di sini, keduanya tersimpan selama sesi berjalan."
    )

    st.markdown("### Aktivitas 1 — Mengamati data pertumbuhan Terubuk")
    if len(df_clean) > 1:
        pilihan_minggu = df_clean["Minggu"].astype(int).astype(str).tolist()[1:]
        minggu_terpilih = st.selectbox(
            "Menurutmu, minggu ke berapa pertambahan tingginya paling besar?", pilihan_minggu,
            key="akt1_pilih_minggu",
        )
    st.text_area("Alasanmu:", key="akt1_alasan", height=70)

    st.markdown("---")
    st.markdown("### Aktivitas 2 — Menentukan perubahan tinggi")
    if len(df_clean) > 1:
        weeks = df_clean["Minggu"].astype(int).tolist()
        wcol1, wcol2 = st.columns(2)
        with wcol1:
            wa = st.selectbox("Minggu awal", weeks, index=0, key="akt2_minggu_awal")
        with wcol2:
            wb = st.selectbox("Minggu akhir", weeks, index=len(weeks) - 1, key="akt2_minggu_akhir")
        jawaban_delta = st.number_input(
            "Berapa perubahan tinggi Terubuk (cm) dari minggu awal ke minggu akhir yang kamu pilih?",
            step=0.1, key="akt2_delta_input",
        )
        if st.button("Cek jawaban", key="akt2_cek"):
            try:
                ha = float(df_clean.loc[df_clean["Minggu"] == wa, "Tinggi Terubuk (cm)"].iloc[0])
                hb = float(df_clean.loc[df_clean["Minggu"] == wb, "Tinggi Terubuk (cm)"].iloc[0])
                actual_delta = hb - ha
                if abs(jawaban_delta - actual_delta) <= 0.2:
                    st.success(f"✓ Benar. Perubahan tingginya adalah {fmt(actual_delta,1)} cm.")
                else:
                    st.error(f"✗ Belum tepat. Perubahan sebenarnya adalah {fmt(actual_delta,1)} cm "
                              f"(tinggi minggu {wb} dikurangi tinggi minggu {wa}).")
            except IndexError:
                st.warning("Data untuk minggu yang dipilih tidak lengkap.")

    st.markdown("---")
    st.markdown("### Aktivitas 3 — Mengamati model H(t)")
    st.radio(
        "Menurut pengamatanmu terhadap grafik model di halaman Model Matematika, bagaimana bentuk "
        "kurva H(t)?",
        ["Naik terus tanpa melandai", "Naik lalu melandai / menurun", "Belum yakin"],
        key="akt3_radio",
    )
    st.text_area("Kaitkan pilihanmu dengan nilai koefisien a pada H(t) = at² + bt + c:",
                 key="akt3_analisis", height=70)

    st.markdown("---")
    st.markdown("### Aktivitas 4 — Menghubungkan H(t), H'(t), dan integral")
    st.text_input(
        "Dalam satu kalimat, apa perbedaan mendasar antara H(t) dan H'(t)?",
        key="akt4_kalimat",
    )
    st.text_area(
        "Lalu, bagaimana ∫ₐᵇ H(t) dt berbeda dari keduanya? Jelaskan dengan kalimatmu sendiri.",
        key="akt4_penjelasan", height=80,
    )

    st.markdown("---")
    st.markdown("### Aktivitas 5 — Menginterpretasikan hasil integral")
    st.write(
        "Kembali ke halaman **∫ Integral**, pilih rentang minggu yang menurutmu paling menarik, lalu "
        "tuliskan interpretasinya di sini."
    )
    st.text_area("Interpretasi hasil integral pilihanmu:", key="akt5_interpretasi", height=90)


# ============================================================
# HALAMAN: LATIHAN
# ============================================================
def page_latihan():
    st.markdown('<span class="badge">Latihan</span>', unsafe_allow_html=True)
    st.markdown("## Latihan bertingkat")
    st.caption(
        "Kerjakan dari level 1 ke level 4. Untuk soal pilihan ganda dan isian angka, kamu akan "
        "langsung mendapat umpan balik setelah menekan tombol cek jawaban."
    )

    st.markdown("#### Level 1 · Pemahaman konsep")
    st.write("1. Secara grafis, ∫ₐᵇ f(t) dt paling tepat menggambarkan...")
    l1 = st.radio(
        "Pilih salah satu:",
        [
            "Luas daerah di bawah kurva f(t) dari t = a sampai t = b",
            "Kemiringan garis singgung kurva di titik t = b",
            "Nilai maksimum f(t) pada interval [a, b]",
            "Titik potong kurva dengan sumbu t",
        ],
        key="l1q1", index=None,
    )
    if st.button("Cek jawaban", key="btn_l1q1"):
        if l1 is None:
            st.info("Pilih salah satu jawaban dulu, ya.")
        elif l1.startswith("Luas daerah"):
            st.success("✓ Benar. ∫ₐᵇ f(t)dt didefinisikan sebagai luas daerah di bawah kurva f(t) "
                       "pada interval [a,b].")
        else:
            st.error("✗ Belum tepat. ∫ₐᵇ f(t)dt didefinisikan sebagai luas daerah di bawah kurva f(t) "
                     "pada interval [a,b].")

    st.markdown("---")
    st.markdown("#### Level 2 · Perhitungan integral")
    st.write("2. Hitung ∫₀² (4t) dt.")
    l2a = st.number_input("Jawaban", step=0.1, key="l2q1")
    if st.button("Cek jawaban", key="btn_l2q1"):
        if abs(l2a - 8) <= 0.2:
            st.success("✓ Benar. Antiturunan 4t adalah 2t². F(2)−F(0) = 8−0 = 8.")
        else:
            st.error("✗ Belum tepat, jawaban yang diharapkan sekitar 8. Antiturunan 4t adalah 2t². "
                     "F(2)−F(0) = 8−0 = 8.")

    st.write("3. Hitung ∫₁² (6t²) dt.")
    l2b = st.number_input("Jawaban", step=0.1, key="l2q2")
    if st.button("Cek jawaban", key="btn_l2q2"):
        if abs(l2b - 14) <= 0.2:
            st.success("✓ Benar. Antiturunan 6t² adalah 2t³. F(2)−F(1) = 16−2 = 14.")
        else:
            st.error("✗ Belum tepat, jawaban yang diharapkan sekitar 14. Antiturunan 6t² adalah 2t³. "
                     "F(2)−F(1) = 16−2 = 14.")

    st.markdown("---")
    st.markdown("#### Level 3 · Soal kontekstual")
    st.write(
        "4. Gunakan model pada Contoh 3 (H(t) = −0.3t² + 8t + 2). Hitung ∫₀³ H(t) dt. Tuliskan hanya "
        "angkanya (satuannya cm·minggu)."
    )
    l3 = st.number_input("Jawaban", step=0.1, key="l3q1")
    if st.button("Cek jawaban", key="btn_l3q1"):
        if abs(l3 - 39.3) <= 0.5:
            st.success("✓ Benar. Antiturunan F(t) = −0.1t³ + 4t² + 2t. F(3) = 39.3, F(0) = 0, "
                       "sehingga hasilnya 39.3 cm·minggu.")
        else:
            st.error("✗ Belum tepat, jawaban yang diharapkan sekitar 39.3 cm·minggu. Antiturunan "
                     "F(t) = −0.1t³ + 4t² + 2t. F(3) = 39.3, F(0) = 0.")

    st.markdown("---")
    st.markdown("#### Level 4 · Interpretasi / analisis")
    st.write(
        "5. Jika kamu membandingkan ∫₁³ H(t) dt dengan ∫₃⁵ H(t) dt (lebar interval sama, yaitu 2 "
        "minggu) dan hasilnya berbeda, apa yang bisa kamu simpulkan tentang pertumbuhan Terubuk pada "
        "kedua rentang tersebut? Kaitkan dengan bentuk grafik H(t)."
    )
    st.text_area("Tulis analisismu di sini...", key="l4_jawaban", height=90)


# ============================================================
# HALAMAN: EVALUASI
# ============================================================
def page_evaluasi():
    st.markdown('<span class="badge">Evaluasi</span>', unsafe_allow_html=True)
    st.markdown("## Evaluasi akhir")
    st.caption(
        "Evaluasi ini mengukur pemahamanmu secara menyeluruh, dari konsep sampai penerapan pada "
        "konteks Terubuk. Jawab seluruh soal, lalu tekan tombol **Selesai & lihat skor** di bagian bawah."
    )

    st.write("1. Manakah pernyataan yang paling tepat tentang Teorema Dasar Kalkulus?")
    e1 = st.radio(
        "Pilih salah satu:",
        [
            "Teorema ini menghubungkan integral tentu dengan selisih nilai antiturunan, F(b) − F(a)",
            "Teorema ini menyatakan bahwa semua fungsi memiliki turunan yang sama",
            "Teorema ini hanya berlaku untuk fungsi trigonometri",
            "Teorema ini digunakan untuk mencari titik potong dua kurva",
        ],
        key="e1", index=None,
    )

    st.write("2. Hitung ∫₀³ (2t + 1) dt.")
    e2 = st.number_input("Jawaban", step=0.1, key="e2")

    st.write(
        "3. Diketahui F(t) = t² + 3t adalah antiturunan dari f(t) = 2t + 3. Gunakan Teorema Dasar "
        "Kalkulus untuk menghitung ∫₂⁴ f(t) dt."
    )
    e3 = st.number_input("Jawaban", step=0.1, key="e3")

    st.write(
        "4. Gunakan model pada Contoh 3 (H(t) = −0.3t² + 8t + 2). Hitung ∫₂⁵ H(t) dt. Tuliskan hanya "
        "angkanya (satuan cm·minggu)."
    )
    e4 = st.number_input("Jawaban", step=0.1, key="e4")

    st.write("5. Jelaskan mengapa satuan hasil integral pada konteks Terubuk adalah cm·minggu, bukan cm.")
    st.text_area("Jawabanmu:", key="e5_text", height=90)
    with st.expander("Lihat kunci pembahasan"):
        st.write(
            "Karena H(t) memiliki satuan cm dan integral melibatkan perkalian H(t) dengan dt yang "
            "bersatuan minggu (∫H(t)·dt), maka hasil integral memiliki satuan gabungan cm × minggu = "
            "cm·minggu. Ini menunjukkan bahwa hasil integral adalah besaran akumulatif terhadap "
            "waktu, bukan tinggi tanaman pada satu titik waktu tertentu."
        )

    st.markdown("---")
    if st.button("Selesai & lihat skor", key="btn_evaluasi_selesai"):
        skor = 0
        total_auto = 4
        detail = []

        ok1 = e1 is not None and e1.startswith("Teorema ini menghubungkan")
        skor += int(ok1)
        detail.append(("Soal 1", ok1, "Teorema Dasar Kalkulus: ∫ₐᵇ f(t)dt = F(b) − F(a), dengan F "
                                        "antiturunan dari f."))

        ok2 = abs(e2 - 12) <= 0.2
        skor += int(ok2)
        detail.append(("Soal 2", ok2, "Antiturunan 2t+1 adalah t²+t. F(3)−F(0) = 12−0 = 12."))

        ok3 = abs(e3 - 18) <= 0.2
        skor += int(ok3)
        detail.append(("Soal 3", ok3, "F(4) = 16+12 = 28. F(2) = 4+6 = 10. F(4) − F(2) = 18."))

        ok4 = abs(e4 - 78.3) <= 0.6
        skor += int(ok4)
        detail.append(("Soal 4", ok4, "F(t) = −0.1t³+4t²+2t. F(5) = 97.5, F(2) = 19.2, selisihnya "
                                        "78.3 cm·minggu."))

        nilai = round(skor / total_auto * 100)
        st.markdown(
            f"""
            <div class="result-card">
                <div class="label">Skor soal pilihan ganda &amp; isian angka (soal 1–4)</div>
                <div class="big">{skor} / {total_auto} benar &nbsp;·&nbsp; {nilai}</div>
                <div class="sub">Soal 5 (uraian) dinilai berdasarkan pemahaman konsep — bandingkan
                jawabanmu dengan kunci pembahasan di atas, atau minta gurumu menilainya.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for label, ok, penjelasan in detail:
            if ok:
                st.success(f"✓ {label} benar. {penjelasan}")
            else:
                st.error(f"✗ {label} belum tepat. {penjelasan}")


# ============================================================
# HALAMAN: REFLEKSI
# ============================================================
def page_refleksi():
    st.markdown('<span class="badge">Refleksi</span>', unsafe_allow_html=True)
    st.markdown("## Refleksi")
    st.caption(
        "Tulis dengan jujur — refleksi ini untuk membantumu menyadari sejauh mana pemahamanmu, bukan "
        "untuk dinilai benar/salah."
    )
    st.text_area("1. Apa konsep yang kamu pahami hari ini?", key="ref_1", height=70)
    st.text_area("2. Apa hubungan integral dengan pertumbuhan Terubuk?", key="ref_2", height=70)
    st.text_area("3. Bagian mana yang masih terasa sulit?", key="ref_3", height=70)
    st.text_area("4. Apa manfaat mempelajari integral melalui fenomena di sekitar, seperti "
                 "pertumbuhan Terubuk?", key="ref_4", height=70)


# ============================================================
# ROUTING
# ============================================================
PAGES = {
    "📖 Beranda": page_beranda,
    "📚 Materi": page_materi,
    "🌿 Konteks Terubuk": page_konteks,
    "📊 Data & Grafik": page_data,
    "📈 Model Matematika": page_model,
    "∫ Integral": page_integral,
    "✏️ Aktivitas": page_aktivitas,
    "📝 Latihan": page_latihan,
    "🎯 Evaluasi": page_evaluasi,
    "💭 Refleksi": page_refleksi,
}

PAGES[menu]()

st.markdown("---")
st.caption(
    "Bahan ajar kalkulus integral berbasis etnomatematika Terubuk — dari konsep, contoh, aktivitas, "
    "hingga evaluasi."
)
