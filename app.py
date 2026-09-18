# ============================================================
# APLIKASI MEDIA PEMBELAJARAN KALKULUS INTEGRAL ETNOMATEMATIKA
# KONTEKS: PERTUMBUHAN TERUBUK
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARY
# ------------------------------------------------------------

# Library os digunakan untuk mengatur lokasi/path file,
# misalnya untuk mencari gambar terubuk di folder aplikasi.
import os # mengimpor modul os untuk mengatur path/file

# NumPy digunakan untuk perhitungan matematika,
# seperti membuat model fungsi dan menghitung integral.
import numpy as np # mengimpor NumPy untuk perhitungan numerik

# Pandas digunakan untuk membuat dan mengolah tabel data.
import pandas as pd # mengimpor Pandas untuk mengolah data tabel

# Plotly digunakan untuk membuat grafik interaktif.
import plotly.graph_objects as go # mengimpor Plotly untuk membuat grafik interaktif

# Streamlit digunakan untuk membuat aplikasi web
# berbasis Python.
import streamlit as st # mengimpor Streamlit untuk membuat aplikasi web


# ------------------------------------------------------------
# 2. PENGATURAN HALAMAN STREAMLIT
# ------------------------------------------------------------

# Mengatur judul yang muncul pada tab browser,
# ikon aplikasi, dan tampilan halaman menjadi lebar.
st.set_page_config( # mengatur konfigurasi halaman Streamlit
    page_title="Kalkulus Integral Etnomatematika Terubuk", # menentukan judul tab browser
    page_icon="🌿", # menentukan ikon tab browser
    layout="wide", # membuat tampilan aplikasi menggunakan lebar layar
    initial_sidebar_state="expanded" # membuat sidebar terbuka saat aplikasi pertama kali dijalankan
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

st.markdown( # menampilkan teks/HTML/CSS pada aplikasi
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
       MENU RADIO SIDEBAR
       ======================================================== */

    /* Membuat tulisan menu sidebar tetap terlihat
       baik pada mode terang maupun mode gelap. */

    section[data-testid="stSidebar"] [role="radiogroup"] label {{
        color: #111111 !important;
    }}

    /* Tulisan nama setiap menu */

    section[data-testid="stSidebar"] [role="radiogroup"] label p {{
        color: #111111 !important;
    }}

    /* Label "Pilih Halaman" */

    section[data-testid="stSidebar"] .stRadio > label {{
        color: #111111 !important;
    }}

    /* Tulisan menu yang sedang dipilih */

    section[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] p {{
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
/* ========================================================
   TOMBOL BUKA SIDEBAR
   ======================================================== */

button[data-testid="stSidebarCollapsedControl"] {{
    background-color: #FFFFFF !important;
    border: 1px solid #D8D8D8 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}}

button[data-testid="stSidebarCollapsedControl"] svg {{
    color: #1F3D2B !important;
    fill: #1F3D2B !important;
}}
    </style>
    """,
    unsafe_allow_html=True # mengizinkan HTML/CSS ditampilkan oleh Streamlit
)

# ------------------------------------------------------------
# 5. LOKASI GAMBAR TERUBUK
# ------------------------------------------------------------

# Mencari lokasi file app.py terlebih dahulu,
# kemudian mencari gambar terubuk di folder yang sama.
TERUBUK_IMG = os.path.join( # membuat alamat/path file gambar terubuk
    os.path.dirname(__file__), # mengambil folder tempat file app.py berada
    "terubuk.png" # menentukan nama file gambar terubuk
)


# ------------------------------------------------------------
# 6. DATA CONTOH PERTUMBUHAN TERUBUK
# ------------------------------------------------------------

# Data awal yang digunakan sebagai contoh.
# Minggu menunjukkan waktu pengamatan,
# sedangkan tinggi menunjukkan tinggi tanaman dalam cm.
SAMPLE = pd.DataFrame({ # membuat DataFrame berisi data contoh pertumbuhan
    "Minggu": [1, 2, 3, 4, 5, 6, 7, 8], # menyimpan data waktu pengamatan dalam minggu
    "Tinggi_cm": [ # menyimpan data tinggi tanaman dalam cm
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

if "data" not in st.session_state: # mengecek apakah data belum tersimpan di session
    st.session_state.data = SAMPLE.copy() # menyimpan salinan data contoh ke session

# Menyimpan identitas pengguna.
if "identitas" not in st.session_state: # mengecek apakah identitas pengguna belum tersedia
    st.session_state.identitas = { # membuat tempat penyimpanan nama dan kelas
        "nama": "", # menyediakan nilai awal untuk nama
        "kelas": "" # menyediakan nilai awal untuk kelas
    }

# Menyimpan batas integral yang digunakan pengguna.
if "bounds" not in st.session_state: # mengecek apakah batas integral belum tersedia
    st.session_state.bounds = { # membuat tempat penyimpanan batas integral
        "bawah": 1.0, # menentukan batas bawah integral awal
        "atas": 8.0 # menentukan batas atas integral awal
    }


# ============================================================
# 8. FUNGSI-FUNGSI MATEMATIKA
# ============================================================

def fit_quadratic(x, y): # membuat fungsi untuk mencari model fungsi kuadrat
    """
    Membuat model fungsi kuadrat berdasarkan data.

    Bentuk model:
        H(t) = at² + bt + c

    np.polyfit digunakan untuk mencari nilai a, b, dan c
    yang paling sesuai dengan data.
    """

    # Degree 2 berarti kita menggunakan fungsi kuadrat.
    a, b, c = np.polyfit(x, y, 2) # menghitung koefisien a, b, c dari model kuadrat

    # Mengembalikan koefisien model.
    return a, b, c # mengembalikan koefisien model


def H(t, a, b, c): # membuat fungsi tinggi tanaman H(t)
    """
    Menghitung tinggi tanaman berdasarkan model:
    
        H(t) = at² + bt + c
    """

    return a * t**2 + b * t + c # menghitung nilai H(t) berdasarkan model kuadrat


def Hprime(t, a, b): # membuat fungsi turunan pertama H(t)
    """
    Menghitung turunan pertama dari model.

    Jika:
        H(t) = at² + bt + c

    Maka:
        H'(t) = 2at + b
    """

    return 2 * a * t + b # menghitung nilai turunan model


def antiderivative_at(t, a, b, c): # membuat fungsi antiturunan H(t)
    """
    Menghitung nilai antiturunan dari H(t).

    Jika:
        H(t) = at² + bt + c

    Maka antiturunannya:
        ∫H(t)dt = (a/3)t³ + (b/2)t² + ct
    """

    return ( # memulai perhitungan nilai antiturunan
        (a / 3) * t**3 # menghitung bagian integral dari at²
        + (b / 2) * t**2 # menghitung bagian integral dari bt
        + c * t # menghitung bagian integral dari c
    )


def exact_integral(lo, hi, a, b, c): # membuat fungsi integral tentu secara analitik
    """
    Menghitung integral tentu secara analitik.

    Rumus:
        ∫ dari lo sampai hi H(t) dt
        = F(hi) - F(lo)
    """

    return ( # memulai perhitungan nilai antiturunan
        antiderivative_at(hi, a, b, c) # menghitung antiturunan pada batas atas
        - antiderivative_at(lo, a, b, c)
    )


def trapezoid_integral(x, y): # membuat fungsi integral numerik metode trapesium
    """
    Menghitung integral secara numerik menggunakan
    metode trapesium.

    Metode ini digunakan untuk memperkirakan luas
    di bawah kurva berdasarkan data yang tersedia.
    """

    return np.trapezoid(y, x) # menghitung luas/akumulasi dengan metode trapesium


def numeric_gradient(x, y): # membuat fungsi perubahan data secara numerik
    """
    Menghitung perubahan/kemiringan data secara numerik.

    Hasilnya dapat digunakan untuk melihat
    kecepatan pertumbuhan tanaman.
    """

    return np.gradient(y, x) # menghitung kemiringan/perubahan data


def fmt(value, digits=2): # membuat fungsi untuk memformat angka
    """
    Mengubah angka menjadi format yang lebih rapi.

    Contoh:
        12.3456 -> 12.35
    """

    return f"{value:.{digits}f}" # mengubah angka menjadi format desimal yang rapi


def get_clean_data(): # membuat fungsi untuk mengambil dan membersihkan data
    """
    Mengambil data dari session_state kemudian
    membersihkan data yang kosong atau tidak valid.
    """

    # Mengambil data yang sedang tersimpan.
    df = st.session_state.data.copy() # mengambil salinan data dari session

    # Mengubah kolom menjadi tipe numerik.
    df["Minggu"] = pd.to_numeric( # mengubah kolom Minggu menjadi angka
        df["Minggu"],
        errors="coerce" # mengubah nilai yang tidak valid menjadi NaN
    )

    df["Tinggi_cm"] = pd.to_numeric( # mengubah kolom Tinggi_cm menjadi angka
        df["Tinggi_cm"],
        errors="coerce" # mengubah nilai yang tidak valid menjadi NaN
    )

    # Menghapus baris yang memiliki data kosong.
    df = df.dropna() # menghapus baris yang memiliki data kosong

    # Mengurutkan data berdasarkan minggu.
    df = df.sort_values("Minggu") # mengurutkan data berdasarkan minggu

    return df # mengembalikan data yang sudah bersih


# ============================================================
# 9. MENU HALAMAN
# ============================================================

st.markdown( # menampilkan teks/HTML/CSS pada aplikasi
    """
    <style>
    /* Tombol menu utama */
    div.stButton > button {
        background-color: #C49A45 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        font-weight: 600 !important;
    }

    div.stButton > button:hover {
        background-color: #4C7A57 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True # mengizinkan HTML/CSS ditampilkan oleh Streamlit
)

# Tombol untuk membuka menu
if "menu_buka" not in st.session_state:  # mengecek apakah status menu sudah disimpan
    st.session_state.menu_buka = False  # menu awalnya dalam keadaan tertutup

if st.button("☰  MENU HALAMAN"):  # membuat tombol yang bisa diklik untuk membuka/menutup menu # menjalankan blok kode ketika tombol diklik
    st.session_state.menu_buka = not st.session_state.menu_buka  # membalik status menu: tertutup ↔ terbuka


# Jika menu dibuka
if st.session_state.menu_buka:  # menampilkan pilihan halaman jika menu sedang terbuka

    st.markdown("### 🌿 Pilih Halaman")

    pilihan_menu = [
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

    menu = st.selectbox(  # membuat daftar pilihan halaman
        "Pilih halaman:",
        pilihan_menu,
        key="pilihan_halaman"
    )

else:

    # Halaman default
    if "pilihan_halaman" not in st.session_state:
        st.session_state.pilihan_halaman = "Beranda"

    menu = st.session_state.pilihan_halaman  # menggunakan halaman terakhir/default saat menu tertutup


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
    st.title("🌿 Kalkulus Integral Etnomatematika Terubuk") # menampilkan judul utama aplikasi

    # Deskripsi singkat aplikasi.
    st.write( # menampilkan teks biasa pada halaman
        "Media pembelajaran yang menghubungkan konsep "
        "kalkulus integral dengan pertumbuhan tanaman terubuk."
    )

    # Jika gambar terubuk tersedia,
    # tampilkan gambar tersebut.
    if os.path.exists(TERUBUK_IMG):

        st.image( # menampilkan gambar
            TERUBUK_IMG,
            caption="Tanaman Terubuk"
        )

    else:

        # Jika gambar tidak ditemukan,
        # tampilkan pesan informasi.
        st.info( # menampilkan kotak informasi
            "Simpan foto tanaman terubuk "
            "di folder aplikasi."
        )

    # Membuat tiga kolom informasi.
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric( # menampilkan angka/statistik dalam bentuk metric
            "Data Pengamatan",
            f"{len(df_clean)} data"
        )

    with col2:
        st.metric( # menampilkan angka/statistik dalam bentuk metric
            "Model",
            "Kuadrat"
        )

    with col3:
        st.metric( # menampilkan angka/statistik dalam bentuk metric
            "Topik",
            "Integral"
        )


# ============================================================
# 12. HALAMAN MATERI
# ============================================================

def page_materi():

    st.title("📚 Materi Kalkulus Integral")

    # Penjelasan konsep dasar integral.
    st.subheader("Apa itu Integral?") # menampilkan subjudul bagian

    st.write( # menampilkan teks biasa pada halaman
        "Integral dapat digunakan untuk menentukan luas "
        "di bawah kurva dan menghitung akumulasi suatu besaran."
    )

    # Menampilkan bentuk umum fungsi.
    st.latex( # menampilkan rumus matematika dalam format LaTeX
        r"H(t)=at^2+bt+c"
    )

    # Menampilkan bentuk integral.
    st.latex( # menampilkan rumus matematika dalam format LaTeX
        r"\int H(t)\,dt"
    )

    st.subheader("Hubungan dengan Pertumbuhan Terubuk")

    st.write( # menampilkan teks biasa pada halaman
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

    st.write( # menampilkan teks biasa pada halaman
        "Terubuk merupakan salah satu tanaman yang "
        "dapat dikaji menggunakan pendekatan etnomatematika."
    )

    st.subheader("Mengapa menggunakan terubuk?")

    st.write( # menampilkan teks biasa pada halaman
        "Konteks tanaman terubuk digunakan agar konsep "
        "kalkulus tidak hanya dipelajari secara abstrak, "
        "tetapi dikaitkan dengan objek yang ada di lingkungan."
    )

    st.subheader("Hubungan dengan Matematika")

    st.markdown(""" # menampilkan teks/HTML/CSS pada aplikasi
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

    st.write( # menampilkan teks biasa pada halaman
        "Data berikut dapat diedit sesuai hasil pengamatan."
    )

    # Menampilkan tabel yang dapat diedit.
    edited_df = st.data_editor(
        st.session_state.data,
        num_rows="dynamic", # mengizinkan pengguna menambah/menghapus baris tabel
        use_container_width=True
    )

    # Tombol untuk menyimpan perubahan data.
    if st.button("💾 Simpan Data"): # menjalankan blok kode ketika tombol diklik

        st.session_state.data = edited_df

        # Setelah data disimpan,
        # aplikasi dijalankan kembali agar model terbaru digunakan.
        st.rerun() # menjalankan ulang aplikasi agar perubahan data langsung dipakai

    # Mengambil data terbaru.
    df = get_clean_data()

    # Jika data tersedia, buat grafik.
    if len(df) > 0:

        fig = go.Figure()

        # Menambahkan titik data asli.
        fig.add_trace( # menambahkan data/kurva ke grafik
            go.Scatter( # membuat grafik titik/garis Scatter
                x=df["Minggu"],
                y=df["Tinggi_cm"],
                mode="markers+lines", # menampilkan titik sekaligus garis
                name="Data Pengamatan"
            )
        )

        # Mengatur judul dan label grafik.
        fig.update_layout( # mengatur judul dan label grafik
            title="Grafik Pertumbuhan Terubuk",
            xaxis_title="Minggu",
            yaxis_title="Tinggi (cm)"
        )

        # Menampilkan grafik.
        st.plotly_chart( # menampilkan grafik Plotly di aplikasi
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

        st.warning( # menampilkan peringatan
            "Minimal diperlukan 3 data untuk membuat "
            "model fungsi kuadrat."
        )

        return

    # Menampilkan bentuk model.
    st.subheader("Model Pertumbuhan")

    st.latex( # menampilkan rumus matematika dalam format LaTeX
        r"H(t)=at^2+bt+c"
    )

    # Menampilkan nilai koefisien.
    st.write(f"Nilai a = {a:.4f}") # menampilkan teks biasa pada halaman
    st.write(f"Nilai b = {b:.4f}") # menampilkan teks biasa pada halaman
    st.write(f"Nilai c = {c:.4f}") # menampilkan teks biasa pada halaman

    # Menampilkan persamaan model.
    st.latex( # menampilkan rumus matematika dalam format LaTeX
        rf"H(t)={a:.4f}t^2+{b:.4f}t+{c:.4f}"
    )

    st.subheader("Turunan Model")

    # Turunan fungsi kuadrat.
    st.latex( # menampilkan rumus matematika dalam format LaTeX
        rf"H'(t)=2({a:.4f})t+({b:.4f})"
    )

    # Penjelasan sederhana.
    st.write( # menampilkan teks biasa pada halaman
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
    fig.add_trace( # menambahkan data/kurva ke grafik
        go.Scatter( # membuat grafik titik/garis Scatter
            x=df_clean["Minggu"],
            y=df_clean["Tinggi_cm"],
            mode="markers", # menampilkan titik data
            name="Data"
        )
    )

    # Kurva model.
    fig.add_trace( # menambahkan data/kurva ke grafik
        go.Scatter( # membuat grafik titik/garis Scatter
            x=t_model,
            y=y_model,
            mode="lines", # menampilkan garis/kurva
            name="Model Kuadrat"
        )
    )

    fig.update_layout( # mengatur judul dan label grafik
        title="Data dan Model Pertumbuhan",
        xaxis_title="Minggu",
        yaxis_title="Tinggi (cm)"
    )

    st.plotly_chart( # menampilkan grafik Plotly di aplikasi
        fig,
        use_container_width=True
    )


# ============================================================
# 16. HALAMAN INTEGRAL
# ============================================================

def page_integral():

    st.title("∫ Integral Pertumbuhan Terubuk")

    st.write( # menampilkan teks biasa pada halaman
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

        st.error( # menampilkan pesan kesalahan
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
    st.metric( # menampilkan angka/statistik dalam bentuk metric
        "Nilai Integral",
        f"{hasil_exact:.2f}"
    )

    # Menampilkan rumus integral.
    st.latex( # menampilkan rumus matematika dalam format LaTeX
        rf"\int_{{{lo:.2f}}}^{{{hi:.2f}}} H(t)\,dt"
        rf" = {hasil_exact:.2f}"
    )

    st.info( # menampilkan kotak informasi
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
    st.write( # menampilkan teks biasa pada halaman
        f"Integral analitik: {hasil_exact:.4f}"
    )

    st.write( # menampilkan teks biasa pada halaman
        f"Integral numerik: {hasil_numerik:.4f}"
    )

    # Selisih kedua metode.
    st.write( # menampilkan teks biasa pada halaman
        f"Selisih: "
        f"{abs(hasil_exact - hasil_numerik):.6f}"
    )


# ============================================================
# 17. HALAMAN AKTIVITAS
# ============================================================

def page_aktivitas():

    st.title("📝 Aktivitas Pembelajaran")

    st.write( # menampilkan teks biasa pada halaman
        "Gunakan data pertumbuhan terubuk untuk melakukan "
        "analisis matematika."
    )

    st.subheader("Langkah Aktivitas")

    st.markdown(""" # menampilkan teks/HTML/CSS pada aplikasi
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

    st.write( # menampilkan teks biasa pada halaman
        "Berdasarkan model pertumbuhan yang diperoleh, "
        "tentukan tinggi terubuk pada minggu ke-6."
    )

    jawaban1 = st.number_input(
        "Masukkan jawaban:",
        min_value=0.0,
        step=0.1,
        key="latihan1"
    )

    if st.button("Periksa Jawaban 1"): # menjalankan blok kode ketika tombol diklik

        kunci1 = H(
            6,
            a,
            b,
            c
        )

        if abs(jawaban1 - kunci1) < 0.5:

            st.success( # menampilkan pesan berhasil
                "Jawaban kamu mendekati hasil model."
            )

        else:

            st.warning( # menampilkan peringatan
                f"Hasil model sekitar "
                f"{kunci1:.2f} cm."
            )


# ============================================================
# 19. HALAMAN EVALUASI
# ============================================================

def page_evaluasi():

    st.title("📋 Evaluasi")

    st.write( # menampilkan teks biasa pada halaman
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
    if st.button("Kirim Evaluasi"): # menjalankan blok kode ketika tombol diklik

        st.success( # menampilkan pesan berhasil
            f"Evaluasi {nama} berhasil dikirim."
        )


# ============================================================
# 20. HALAMAN REFLEKSI
# ============================================================

def page_refleksi():

    st.title("💭 Refleksi")

    st.write( # menampilkan teks biasa pada halaman
        "Tuliskan pengalaman dan pemahaman setelah "
        "menggunakan media pembelajaran."
    )

    # Kolom refleksi pengguna.
    refleksi = st.text_area(
        "Apa yang kamu pahami setelah menggunakan aplikasi?"
    )

    # Tombol simpan refleksi.
    if st.button("Simpan Refleksi"): # menjalankan blok kode ketika tombol diklik

        if refleksi.strip(): # mengecek apakah jawaban refleksi tidak kosong

            st.success( # menampilkan pesan berhasil
                "Refleksi berhasil disimpan."
            )

        else:

            st.warning( # menampilkan peringatan
                "Silakan tuliskan refleksi terlebih dahulu."
            )


# ============================================================
# 21. ROUTING / MENENTUKAN HALAMAN YANG DITAMPILKAN
# ============================================================

# Dictionary digunakan untuk menghubungkan nama menu
# dengan fungsi halaman masing-masing.
PAGES = { # membuat dictionary untuk menghubungkan menu dengan fungsi halaman
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
PAGES[menu]() # menjalankan halaman sesuai menu yang dipilih


# ============================================================
# 22. FOOTER
# ============================================================

# Garis pemisah sebelum footer.
st.markdown("---") # menampilkan teks/HTML/CSS pada aplikasi

# Footer aplikasi.
st.caption(
    "Media Pembelajaran Kalkulus Integral "
    "Berbasis Etnomatematika Terubuk 🌿"
)
