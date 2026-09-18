# ============================================================
# APLIKASI MEDIA PEMBELAJARAN KALKULUS INTEGRAL ETNOMATEMATIKA
# KONTEKS: PERTUMBUHAN TERUBUK
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARY
# ------------------------------------------------------------

# Library os digunakan untuk mengatur lokasi/path file,
# misalnya untuk mencari gambar terubuk di folder aplikasi.
import os

# NumPy digunakan untuk perhitungan matematika,
# seperti membuat model fungsi dan menghitung integral.
import numpy as np

# Pandas digunakan untuk membuat dan mengolah tabel data.
import pandas as pd

# Plotly digunakan untuk membuat grafik interaktif.
import plotly.graph_objects as go

# Streamlit digunakan untuk membuat aplikasi web
# berbasis Python.
import streamlit as st


# ------------------------------------------------------------
# 2. PENGATURAN HALAMAN STREAMLIT
# ------------------------------------------------------------

# Mengatur judul yang muncul pada tab browser,
# ikon aplikasi, dan tampilan halaman menjadi lebar.
st.set_page_config(
    page_title="Kalkulus Integral Etnomatematika Terubuk",
    page_icon="🌿",
    layout="wide"
)


# ------------------------------------------------------------
# 3. WARNA TEMA APLIKASI
# ------------------------------------------------------------

# Warna hijau tua sebagai warna utama aplikasi.
FOREST = "#1F3D2B"

# Warna hijau sebagai warna pendukung.
MOSS = "#4C7A57"

# Warna hijau muda.
MOSS_SOFT = "#DCE9DE"

# Warna emas untuk memberikan aksen.
GOLD = "#C9971C"

# Warna emas muda.
GOLD_SOFT = "#F4E8C3"

# Warna krem/cokelat muda.
CLAY = "#D8C8A8"

# Warna latar belakang aplikasi.
BG = "#F3F6EE"

# Warna teks yang lebih lembut.
INK_SOFT = "#5C655E"


# ------------------------------------------------------------
# 4. CSS / TAMPILAN APLIKASI
# ------------------------------------------------------------

# ------------------------------------------------------------
# 4. CSS / TAMPILAN APLIKASI
# ------------------------------------------------------------

# CSS digunakan untuk mengatur tampilan aplikasi,
# seperti warna background, ukuran tulisan, tombol,
# sidebar, input, tabel, dan elemen lainnya.
#
# CSS ini juga dibuat agar tampilan aplikasi tetap terang
# dan tulisan tetap terlihat jelas walaupun perangkat
# pengguna sedang menggunakan mode gelap (dark mode).

st.markdown(
    f"""
    <style>

    /* ========================================================
       BACKGROUND UTAMA APLIKASI
       ======================================================== */

    /* Background aplikasi tetap menggunakan warna BG.
       !important digunakan agar tidak berubah mengikuti
       pengaturan dark mode perangkat pengguna. */

    .stApp {{
        background-color: {BG} !important;
    }}


    /* ========================================================
       TEKS UTAMA
       ======================================================== */

    /* Tulisan pada aplikasi dipaksa tetap berwarna gelap.
       Dengan begitu, tulisan tidak berubah menjadi putih
       ketika perangkat menggunakan dark mode. */

    .stApp p,
    .stApp span,
    .stApp li,
    .stApp label {{
        color: #111111 !important;
    }}


    /* ========================================================
       JUDUL
       ======================================================== */

    /* Judul tetap menggunakan warna hijau tua
       sesuai tema aplikasi. */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {{
        color: {FOREST} !important;
    }}


    /* ========================================================
       SIDEBAR
       ======================================================== */

    /* Background sidebar tetap terang. */

    section[data-testid="stSidebar"] {{
        background-color: {BG} !important;
    }}

    /* Tulisan di dalam sidebar tetap gelap. */

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {{
        color: #111111 !important;
    }}

    /* Judul sidebar tetap menggunakan warna hijau. */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {FOREST} !important;
    }}


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    /* Kotak untuk memasukkan teks tetap berwarna putih
       dan tulisan yang diketik tetap hitam. */

    .stTextInput input {{
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }}

    /* Warna tulisan petunjuk pada input. */

    .stTextInput input::placeholder {{
        color: #666666 !important;
    }}


    /* ========================================================
       TEXT AREA
       ======================================================== */

    /* Kotak jawaban/refleksi tetap putih
       dan tulisan pengguna tetap hitam. */

    .stTextArea textarea {{
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }}

    .stTextArea textarea::placeholder {{
        color: #666666 !important;
    }}


    /* ========================================================
       NUMBER INPUT
       ======================================================== */

    /* Kotak untuk memasukkan angka tetap putih
       dan angka yang diketik tetap hitam. */

    .stNumberInput input {{
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }}


    /* ========================================================
       SELECTBOX
       ======================================================== */

    /* Tulisan pada pilihan selectbox tetap gelap. */

    .stSelectbox label {{
        color: #111111 !important;
    }}


    /* ========================================================
       RADIO BUTTON
       ======================================================== */

    /* Tulisan pilihan radio tetap gelap. */

    .stRadio label {{
        color: #111111 !important;
    }}


    /* ========================================================
       CHECKBOX
       ======================================================== */

    /* Tulisan checkbox tetap gelap. */

    .stCheckbox label {{
        color: #111111 !important;
    }}


    /* ========================================================
       SLIDER
       ======================================================== */

    /* Tulisan pada slider tetap gelap. */

    .stSlider label {{
        color: #111111 !important;
    }}


    /* ========================================================
       TOMBOL
       ======================================================== */

    /* Tombol tetap putih dengan tulisan hitam
       sehingga tetap terlihat jelas pada dark mode. */

    .stButton > button {{
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border-radius: 10px;
        font-weight: 600;
    }}


    /* ========================================================
       TABEL / DATA EDITOR
       ======================================================== */

    /* Tulisan pada tabel data tetap gelap. */

    [data-testid="stDataEditor"] {{
        color: #111111 !important;
    }}


    /* ========================================================
       MARKDOWN
       ======================================================== */

    /* Tulisan yang dibuat menggunakan st.markdown()
       tetap berwarna gelap. */

    .stMarkdown p,
    .stMarkdown li {{
        color: #111111 !important;
    }}


    /* ========================================================
       KOTAK INFORMASI / WARNING / SUCCESS / ERROR
       ======================================================== */

    /* Tulisan pada kotak informasi tetap dapat dibaca
       ketika perangkat menggunakan dark mode. */

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {{
        color: #111111 !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# 5. LOKASI GAMBAR TERUBUK
# ------------------------------------------------------------

# Mencari lokasi file app.py terlebih dahulu,
# kemudian mencari gambar terubuk di folder yang sama.
TERUBUK_IMG = os.path.join(
    os.path.dirname(__file__),
    "terubuk.png"
)


# ------------------------------------------------------------
# 6. DATA CONTOH PERTUMBUHAN TERUBUK
# ------------------------------------------------------------

# Data awal yang digunakan sebagai contoh.
# Minggu menunjukkan waktu pengamatan,
# sedangkan tinggi menunjukkan tinggi tanaman dalam cm.
SAMPLE = pd.DataFrame({
    "Minggu": [1, 2, 3, 4, 5, 6, 7, 8],
    "Tinggi_cm": [
        8.2,
        14.5,
        21.0,
        28.8,
        35.2,
        41.0,
        45.5,
        49.0
    ]
})


# ------------------------------------------------------------
# 7. SESSION STATE
# ------------------------------------------------------------

# session_state digunakan agar data yang dimasukkan pengguna
# tetap tersimpan ketika Streamlit melakukan refresh/rerun.

if "data" not in st.session_state:
    st.session_state.data = SAMPLE.copy()

# Menyimpan identitas pengguna.
if "identitas" not in st.session_state:
    st.session_state.identitas = {
        "nama": "",
        "kelas": ""
    }

# Menyimpan batas integral yang digunakan pengguna.
if "bounds" not in st.session_state:
    st.session_state.bounds = {
        "bawah": 1.0,
        "atas": 8.0
    }


# ============================================================
# 8. FUNGSI-FUNGSI MATEMATIKA
# ============================================================

def fit_quadratic(x, y):
    """
    Membuat model fungsi kuadrat berdasarkan data.

    Bentuk model:
        H(t) = at² + bt + c

    np.polyfit digunakan untuk mencari nilai a, b, dan c
    yang paling sesuai dengan data.
    """

    # Degree 2 berarti kita menggunakan fungsi kuadrat.
    a, b, c = np.polyfit(x, y, 2)

    # Mengembalikan koefisien model.
    return a, b, c


def H(t, a, b, c):
    """
    Menghitung tinggi tanaman berdasarkan model:
    
        H(t) = at² + bt + c
    """

    return a * t**2 + b * t + c


def Hprime(t, a, b):
    """
    Menghitung turunan pertama dari model.

    Jika:
        H(t) = at² + bt + c

    Maka:
        H'(t) = 2at + b
    """

    return 2 * a * t + b


def antiderivative_at(t, a, b, c):
    """
    Menghitung nilai antiturunan dari H(t).

    Jika:
        H(t) = at² + bt + c

    Maka antiturunannya:
        ∫H(t)dt = (a/3)t³ + (b/2)t² + ct
    """

    return (
        (a / 3) * t**3
        + (b / 2) * t**2
        + c * t
    )


def exact_integral(lo, hi, a, b, c):
    """
    Menghitung integral tentu secara analitik.

    Rumus:
        ∫ dari lo sampai hi H(t) dt
        = F(hi) - F(lo)
    """

    return (
        antiderivative_at(hi, a, b, c)
        - antiderivative_at(lo, a, b, c)
    )


def trapezoid_integral(x, y):
    """
    Menghitung integral secara numerik menggunakan
    metode trapesium.

    Metode ini digunakan untuk memperkirakan luas
    di bawah kurva berdasarkan data yang tersedia.
    """

    return np.trapezoid(y, x)


def numeric_gradient(x, y):
    """
    Menghitung perubahan/kemiringan data secara numerik.

    Hasilnya dapat digunakan untuk melihat
    kecepatan pertumbuhan tanaman.
    """

    return np.gradient(y, x)


def fmt(value, digits=2):
    """
    Mengubah angka menjadi format yang lebih rapi.

    Contoh:
        12.3456 -> 12.35
    """

    return f"{value:.{digits}f}"


def get_clean_data():
    """
    Mengambil data dari session_state kemudian
    membersihkan data yang kosong atau tidak valid.
    """

    # Mengambil data yang sedang tersimpan.
    df = st.session_state.data.copy()

    # Mengubah kolom menjadi tipe numerik.
    df["Minggu"] = pd.to_numeric(
        df["Minggu"],
        errors="coerce"
    )

    df["Tinggi_cm"] = pd.to_numeric(
        df["Tinggi_cm"],
        errors="coerce"
    )

    # Menghapus baris yang memiliki data kosong.
    df = df.dropna()

    # Mengurutkan data berdasarkan minggu.
    df = df.sort_values("Minggu")

    return df


# ============================================================
# 9. SIDEBAR / MENU APLIKASI
# ============================================================

# Judul pada sidebar.
st.sidebar.title("🌿 Kalkulus Terubuk")

# Keterangan singkat aplikasi.
st.sidebar.caption(
    "Media Pembelajaran Kalkulus Integral "
    "Berbasis Etnomatematika"
)

# Menu navigasi aplikasi.
menu = st.sidebar.radio(
    "Pilih Halaman",
    [
        "Beranda",
        "Materi",
        "Konteks Terubuk",
        "Data & Grafik",
        "Model Matematika",
        "∫ Integral",
        "Aktivitas",
        "Latihan",
        "Evaluasi",
        "Refleksi"
    ]
)


# ============================================================
# 10. MENYIAPKAN DATA DAN MODEL
# ============================================================

# Mengambil data yang sudah dibersihkan.
df_clean = get_clean_data()

# Jika jumlah data minimal 3,
# model kuadrat dapat dibuat.
if len(df_clean) >= 3:

    # Mengambil data minggu sebagai x.
    x_data = df_clean["Minggu"].to_numpy()

    # Mengambil data tinggi sebagai y.
    y_data = df_clean["Tinggi_cm"].to_numpy()

    # Membuat model fungsi kuadrat.
    a, b, c = fit_quadratic(
        x_data,
        y_data
    )

else:

    # Nilai default jika data belum cukup.
    a, b, c = 0, 0, 0


# Menentukan batas waktu minimum berdasarkan data.
if len(df_clean) > 0:
    min_t = float(df_clean["Minggu"].min())
    max_t = float(df_clean["Minggu"].max())
else:
    min_t = 1.0
    max_t = 8.0


# Mengambil batas integral dari session state.
default_lo = st.session_state.bounds["bawah"]
default_hi = st.session_state.bounds["atas"]


# ============================================================
# 11. HALAMAN BERANDA
# ============================================================

def page_beranda():

    # Judul utama halaman.
    st.title("🌿 Kalkulus Integral Etnomatematika Terubuk")

    # Deskripsi singkat aplikasi.
    st.write(
        "Media pembelajaran yang menghubungkan konsep "
        "kalkulus integral dengan pertumbuhan tanaman terubuk."
    )

    # Jika gambar terubuk tersedia,
    # tampilkan gambar tersebut.
    if os.path.exists(TERUBUK_IMG):

        st.image(
            TERUBUK_IMG,
            caption="Tanaman Terubuk"
        )

    else:

        # Jika gambar tidak ditemukan,
        # tampilkan pesan informasi.
        st.info(
            "Simpan foto tanaman terubuk "
            "di folder aplikasi."
        )

    # Membuat tiga kolom informasi.
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Data Pengamatan",
            f"{len(df_clean)} data"
        )

    with col2:
        st.metric(
            "Model",
            "Kuadrat"
        )

    with col3:
        st.metric(
            "Topik",
            "Integral"
        )


# ============================================================
# 12. HALAMAN MATERI
# ============================================================

def page_materi():

    st.title("📚 Materi Kalkulus Integral")

    # Penjelasan konsep dasar integral.
    st.subheader("Apa itu Integral?")

    st.write(
        "Integral dapat digunakan untuk menentukan luas "
        "di bawah kurva dan menghitung akumulasi suatu besaran."
    )

    # Menampilkan bentuk umum fungsi.
    st.latex(
        r"H(t)=at^2+bt+c"
    )

    # Menampilkan bentuk integral.
    st.latex(
        r"\int H(t)\,dt"
    )

    st.subheader("Hubungan dengan Pertumbuhan Terubuk")

    st.write(
        "Data pertumbuhan terubuk dapat dimodelkan "
        "menggunakan fungsi matematika. Model tersebut "
        "kemudian dapat digunakan untuk mempelajari "
        "turunan dan integral."
    )


# ============================================================
# 13. HALAMAN KONTEKS TERUBUK
# ============================================================

def page_konteks():

    st.title("🌱 Konteks Terubuk")

    st.write(
        "Terubuk merupakan salah satu tanaman yang "
        "dapat dikaji menggunakan pendekatan etnomatematika."
    )

    st.subheader("Mengapa menggunakan terubuk?")

    st.write(
        "Konteks tanaman terubuk digunakan agar konsep "
        "kalkulus tidak hanya dipelajari secara abstrak, "
        "tetapi dikaitkan dengan objek yang ada di lingkungan."
    )

    st.subheader("Hubungan dengan Matematika")

    st.markdown("""
    - Pengamatan pertumbuhan → data matematika
    - Data pertumbuhan → grafik
    - Grafik → model fungsi
    - Model fungsi → turunan
    - Model fungsi → integral
    - Integral → interpretasi luas/akumulasi
    """)


# ============================================================
# 14. HALAMAN DATA & GRAFIK
# ============================================================

def page_data():

    st.title("📊 Data & Grafik Pertumbuhan")

    st.write(
        "Data berikut dapat diedit sesuai hasil pengamatan."
    )

    # Menampilkan tabel yang dapat diedit.
    edited_df = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True
    )

    # Tombol untuk menyimpan perubahan data.
    if st.button("💾 Simpan Data"):

        st.session_state.data = edited_df

        # Setelah data disimpan,
        # aplikasi dijalankan kembali agar model terbaru digunakan.
        st.rerun()

    # Mengambil data terbaru.
    df = get_clean_data()

    # Jika data tersedia, buat grafik.
    if len(df) > 0:

        fig = go.Figure()

        # Menambahkan titik data asli.
        fig.add_trace(
            go.Scatter(
                x=df["Minggu"],
                y=df["Tinggi_cm"],
                mode="markers+lines",
                name="Data Pengamatan"
            )
        )

        # Mengatur judul dan label grafik.
        fig.update_layout(
            title="Grafik Pertumbuhan Terubuk",
            xaxis_title="Minggu",
            yaxis_title="Tinggi (cm)"
        )

        # Menampilkan grafik.
        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# 15. HALAMAN MODEL MATEMATIKA
# ============================================================

def page_model():

    st.title("📈 Model Matematika")

    # Mengecek apakah data cukup untuk membuat model.
    if len(df_clean) < 3:

        st.warning(
            "Minimal diperlukan 3 data untuk membuat "
            "model fungsi kuadrat."
        )

        return

    # Menampilkan bentuk model.
    st.subheader("Model Pertumbuhan")

    st.latex(
        r"H(t)=at^2+bt+c"
    )

    # Menampilkan nilai koefisien.
    st.write(f"Nilai a = {a:.4f}")
    st.write(f"Nilai b = {b:.4f}")
    st.write(f"Nilai c = {c:.4f}")

    # Menampilkan persamaan model.
    st.latex(
        rf"H(t)={a:.4f}t^2+{b:.4f}t+{c:.4f}"
    )

    st.subheader("Turunan Model")

    # Turunan fungsi kuadrat.
    st.latex(
        rf"H'(t)=2({a:.4f})t+({b:.4f})"
    )

    # Penjelasan sederhana.
    st.write(
        "Turunan dapat digunakan untuk melihat perubahan "
        "tinggi tanaman terhadap waktu."
    )

    # Membuat titik-titik untuk menggambar kurva model.
    t_model = np.linspace(
        min_t,
        max_t,
        200
    )

    # Menghitung tinggi berdasarkan model.
    y_model = H(
        t_model,
        a,
        b,
        c
    )

    # Membuat grafik model.
    fig = go.Figure()

    # Data asli.
    fig.add_trace(
        go.Scatter(
            x=df_clean["Minggu"],
            y=df_clean["Tinggi_cm"],
            mode="markers",
            name="Data"
        )
    )

    # Kurva model.
    fig.add_trace(
        go.Scatter(
            x=t_model,
            y=y_model,
            mode="lines",
            name="Model Kuadrat"
        )
    )

    fig.update_layout(
        title="Data dan Model Pertumbuhan",
        xaxis_title="Minggu",
        yaxis_title="Tinggi (cm)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 16. HALAMAN INTEGRAL
# ============================================================

def page_integral():

    st.title("∫ Integral Pertumbuhan Terubuk")

    st.write(
        "Gunakan slider berikut untuk menentukan batas "
        "integral berdasarkan waktu pengamatan."
    )

    # Input batas bawah integral.
    lo = st.slider(
        "Batas bawah",
        min_value=float(min_t),
        max_value=float(max_t),
        value=float(default_lo),
        step=0.1
    )

    # Input batas atas integral.
    hi = st.slider(
        "Batas atas",
        min_value=float(min_t),
        max_value=float(max_t),
        value=float(default_hi),
        step=0.1
    )

    # Memastikan batas bawah tidak lebih besar
    # daripada batas atas.
    if lo > hi:

        st.error(
            "Batas bawah tidak boleh lebih besar "
            "daripada batas atas."
        )

        return

    # Menghitung integral secara analitik.
    hasil_exact = exact_integral(
        lo,
        hi,
        a,
        b,
        c
    )

    st.subheader("Hasil Integral")

    # Menampilkan hasil.
    st.metric(
        "Nilai Integral",
        f"{hasil_exact:.2f}"
    )

    # Menampilkan rumus integral.
    st.latex(
        rf"\int_{{{lo:.2f}}}^{{{hi:.2f}}} H(t)\,dt"
        rf" = {hasil_exact:.2f}"
    )

    st.info(
        "Nilai integral dapat diinterpretasikan sebagai "
        "akumulasi tinggi berdasarkan model pada interval "
        "waktu yang dipilih."
    )

    # --------------------------------------------------------
    # Perbandingan dengan metode numerik
    # --------------------------------------------------------

    st.subheader("Perbandingan dengan Metode Numerik")

    # Membuat titik-titik pada interval integral.
    t_num = np.linspace(
        lo,
        hi,
        200
    )

    # Menghitung nilai model pada titik tersebut.
    y_num = H(
        t_num,
        a,
        b,
        c
    )

    # Menghitung integral numerik.
    hasil_numerik = trapezoid_integral(
        t_num,
        y_num
    )

    # Menampilkan hasil metode numerik.
    st.write(
        f"Integral analitik: {hasil_exact:.4f}"
    )

    st.write(
        f"Integral numerik: {hasil_numerik:.4f}"
    )

    # Selisih kedua metode.
    st.write(
        f"Selisih: "
        f"{abs(hasil_exact - hasil_numerik):.6f}"
    )


# ============================================================
# 17. HALAMAN AKTIVITAS
# ============================================================

def page_aktivitas():

    st.title("📝 Aktivitas Pembelajaran")

    st.write(
        "Gunakan data pertumbuhan terubuk untuk melakukan "
        "analisis matematika."
    )

    st.subheader("Langkah Aktivitas")

    st.markdown("""
    **1. Amati data**

    Perhatikan perubahan tinggi terubuk dari minggu ke minggu.

    **2. Buat grafik**

    Gunakan data untuk melihat pola pertumbuhan.

    **3. Tentukan model**

    Gunakan model fungsi kuadrat.

    **4. Tentukan turunan**

    Gunakan turunan untuk melihat perubahan pertumbuhan.

    **5. Hitung integral**

    Tentukan akumulasi pada interval tertentu.

    **6. Interpretasikan**

    Jelaskan arti hasil perhitungan dalam konteks pertumbuhan terubuk.
    """)


# ============================================================
# 18. HALAMAN LATIHAN
# ============================================================

def page_latihan():

    st.title("✏️ Latihan")

    st.subheader("Latihan 1")

    st.write(
        "Berdasarkan model pertumbuhan yang diperoleh, "
        "tentukan tinggi terubuk pada minggu ke-6."
    )

    jawaban1 = st.number_input(
        "Masukkan jawaban:",
        min_value=0.0,
        step=0.1,
        key="latihan1"
    )

    if st.button("Periksa Jawaban 1"):

        kunci1 = H(
            6,
            a,
            b,
            c
        )

        if abs(jawaban1 - kunci1) < 0.5:

            st.success(
                "Jawaban kamu mendekati hasil model."
            )

        else:

            st.warning(
                f"Hasil model sekitar "
                f"{kunci1:.2f} cm."
            )


# ============================================================
# 19. HALAMAN EVALUASI
# ============================================================

def page_evaluasi():

    st.title("📋 Evaluasi")

    st.write(
        "Jawablah pertanyaan berikut berdasarkan "
        "pemahaman terhadap materi."
    )

    # Menyimpan jawaban pengguna.
    nama = st.text_input(
        "Nama"
    )

    # Pertanyaan evaluasi.
    q1 = st.radio(
        "1. Apa fungsi integral dalam konteks aplikasi ini?",
        [
            "Menentukan warna aplikasi",
            "Menghitung akumulasi berdasarkan model",
            "Menghapus data",
            "Mengubah gambar"
        ]
    )

    q2 = st.radio(
        "2. Apa bentuk model yang digunakan?",
        [
            "Linear",
            "Kuadrat",
            "Eksponensial",
            "Konstan"
        ]
    )

    # Tombol untuk mengirim evaluasi.
    if st.button("Kirim Evaluasi"):

        st.success(
            f"Evaluasi {nama} berhasil dikirim."
        )


# ============================================================
# 20. HALAMAN REFLEKSI
# ============================================================

def page_refleksi():

    st.title("💭 Refleksi")

    st.write(
        "Tuliskan pengalaman dan pemahaman setelah "
        "menggunakan media pembelajaran."
    )

    # Kolom refleksi pengguna.
    refleksi = st.text_area(
        "Apa yang kamu pahami setelah menggunakan aplikasi?"
    )

    # Tombol simpan refleksi.
    if st.button("Simpan Refleksi"):

        if refleksi.strip():

            st.success(
                "Refleksi berhasil disimpan."
            )

        else:

            st.warning(
                "Silakan tuliskan refleksi terlebih dahulu."
            )


# ============================================================
# 21. ROUTING / MENENTUKAN HALAMAN YANG DITAMPILKAN
# ============================================================

# Dictionary digunakan untuk menghubungkan nama menu
# dengan fungsi halaman masing-masing.
PAGES = {
    "Beranda": page_beranda,
    "Materi": page_materi,
    "Konteks Terubuk": page_konteks,
    "Data & Grafik": page_data,
    "Model Matematika": page_model,
    "∫ Integral": page_integral,
    "Aktivitas": page_aktivitas,
    "Latihan": page_latihan,
    "Evaluasi": page_evaluasi,
    "Refleksi": page_refleksi
}


# Menjalankan fungsi halaman sesuai menu
# yang dipilih pengguna.
PAGES[menu]()


# ============================================================
# 22. FOOTER
# ============================================================

# Garis pemisah sebelum footer.
st.markdown("---")

# Footer aplikasi.
st.caption(
    "Media Pembelajaran Kalkulus Integral "
    "Berbasis Etnomatematika Terubuk 🌿"
)
