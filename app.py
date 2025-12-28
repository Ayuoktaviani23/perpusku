import streamlit as st
import difflib
import re
import random
import time
from datetime import datetime
from difflib import SequenceMatcher
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="PerpusCode USK - Lengkap",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# INITIALIZE SESSION STATE
# =========================
if 'practice_scores' not in st.session_state:
    st.session_state.practice_scores = {}
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = []
if 'last_viewed' not in st.session_state:
    st.session_state.last_viewed = []
if 'study_progress' not in st.session_state:
    st.session_state.study_progress = {
        "hari_1": False,
        "hari_2": False,
        "hari_3": False,
        "hari_4": False,
        "hari_5": False,
        "hari_6": False,
        "hari_7": False
    }

# =========================
# DATASET MATERI LENGKAP
# =========================
materi = {
    # ---------- SESSION ----------
    "Login Page (HTML)": {
        "deskripsi": "Halaman login dengan form HTML dan styling CSS",
        "tipe": "html",
        "kode": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<style>
*{
    margin: 0px;
    padding: 0px;
    box-sizing: border-box;
    font-family: Arial, Helvetica, sans-serif;
}
body{
    background-color: #eee;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.form-box{
    background-color: white;
    width: 300px;
    padding: 20px;
    border: 2px solid #ccc;
    border-radius: 6px;
}
.form-box h2{
    text-align: center;
    margin-bottom: 15px;
}
label {
    font-size: 14px;
}
input[type="text"],
input[type="password"]{
    width: 100%;
    padding: 7px;
    margin: 5px 0 12px;
    border: 1px solid #9999;
    border-radius: 4px;
}
input:focus{
    outline: none;
    border-color: #4CAF50;
}
input[type="submit"]{
    width: 100%;
    padding: 8px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
input[type="submit"]:hover{
    background-color: #43a047;
}
</style>
<body>
<div class="form-box">
    <h2>Login</h2>
    <form action="proses_login.php" method="post">
        <label>Username</label>
        <input type="text" name="username" required>
        <label>Password</label>
        <input type="password" name="password" required>
        <input type="submit" value="Login">
    </form>
</div>
</body>
</html>""",
        "penjelasan": {
            "title": "Struktur Halaman Login",
            "points": [
                "**DOCTYPE html** → Deklarasi tipe dokumen HTML5",
                "**<meta name='viewport'>** → Untuk responsive design",
                "**CSS Box Model** → Penggunaan *{margin:0; padding:0; box-sizing:border-box}",
                "**Flexbox** → display:flex untuk penempatan tengah",
                "**Form Styling** → Styling input text dan submit button",
                "**:hover** → Efek hover pada tombol login"
            ]
        },
        "critical_parts": [
            "session_start()",
            "method=\"post\"",
            "action=\"proses_login.php\"",
            "required",
            "name=\"username\"",
            "name=\"password\""
        ]
    },

    "Proses Login (Session)": {
        "deskripsi": "Proses validasi login dan membuat session",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$username = $_POST['username'];
$password = $_POST['password'];

$sql = "SELECT * FROM user 
        WHERE username='$username' 
        AND password=md5('$password')";
$query = mysqli_query($koneksi,$sql);

if(mysqli_num_rows($query)==1){
    $user=mysqli_fetch_assoc($query);
    
    // BUAT SESSION
    $_SESSION['id_user']=$user['id_user'];
    $_SESSION['username']=$user['username'];
    
    header("location:index.php?login=sukses");
    exit;
}else{
    header("location:login.php?login=gagal");
    exit;
}
?>""",
        "penjelasan": {
            "title": "Mekanisme Session Login",
            "points": [
                "**session_start()** → WAJIB dipanggil pertama kali untuk mulai session",
                "**$_POST** → Mengambil data dari form login",
                "**md5()** → Fungsi hash untuk enkripsi password",
                "**mysqli_num_rows()** → Mengecek jumlah data yang ditemukan",
                "**$_SESSION[]** → Menyimpan data user ke dalam session",
                "**header()** → Redirect ke halaman lain",
                "**exit** → Menghentikan eksekusi script setelah redirect"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_POST['username']",
            "$_POST['password']",
            "md5('$password')",
            "mysqli_num_rows($query)==1",
            "mysqli_fetch_assoc($query)",
            "$_SESSION['id_user']",
            "$_SESSION['username']",
            "header(\"location:index.php\")",
            "exit"
        ]
    },

    "Logout (Session Destroy)": {
        "deskripsi": "Menghapus session dan logout user",
        "tipe": "php",
        "kode": """<?php
session_start();
session_destroy();
header("location:login.php");
?>""",
        "penjelasan": {
            "title": "Cara Logout yang Benar",
            "points": [
                "**session_start()** → Harus dipanggil untuk mengakses session",
                "**session_destroy()** → Menghancurkan semua data session",
                "**header()** → Redirect kembali ke halaman login"
            ]
        },
        "critical_parts": [
            "session_start()",
            "session_destroy()",
            "header(\"location:login.php\")"
        ]
    },

    # ---------- CRUD (READ) ----------
    "Index Page (Read + Filter)": {
        "deskripsi": "Halaman utama menampilkan data dengan filter dan proteksi session",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

// PROTEKSI SESSION
if(!isset($_SESSION['id_user'])){
    header("location:login.php?logindulu");
    exit;
}

$id_user=$_SESSION['id_user'];

/* FILTER CATEGORY */
$filter_category = $_GET['category'] ?? '';

// Ambil data kategori untuk dropdown
$sql_category = "SELECT * FROM category";
$query_category = mysqli_query($koneksi, $sql_category);

// Query utama dengan JOIN dan optional filter
$sql = "SELECT todo.*, category.category 
        FROM todo 
        JOIN category ON todo.id_category = category.id_category";

if($filter_category != ''){
    $sql .= " WHERE todo.id_category = '$filter_category'";
}

$query = mysqli_query($koneksi, $sql);
?>""",
        "penjelasan": {
            "title": "Konsep Read dengan Filter",
            "points": [
                "**isset($_SESSION)** → Mengecek apakah user sudah login",
                "**$_GET['category']** → Mengambil parameter filter dari URL",
                "**?? ''** → Null coalescing operator (PHP 7+)",
                "**JOIN** → Menggabungkan tabel todo dan category",
                "**WHERE** → Filter data berdasarkan kategori",
                "**OPTIONAL FILTER** → Jika tidak kosong, tambahkan WHERE clause"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "if(!isset($_SESSION['id_user']))",
            "header(\"location:login.php\")",
            "exit",
            "$_SESSION['id_user']",
            "$_GET['category'] ?? ''",
            "SELECT * FROM category",
            "mysqli_query($koneksi, $sql_category)",
            "SELECT todo.*, category.category",
            "JOIN category ON todo.id_category = category.id_category",
            "WHERE todo.id_category = '$filter_category'",
            "mysqli_query($koneksi, $sql)"
        ]
    },

    "CSS Grid Layout": {
        "deskripsi": "Styling card dengan CSS Grid untuk layout responsive",
        "tipe": "css",
        "kode": """<style>
/* GRID LAYOUT */
.todo-grid{
    display: grid;
    grid-template-columns: repeat(auto-fill, 240px);
    justify-content: center;
    gap: 20px;
    padding-bottom: 40px;
}

/* CARD STYLING */
.card{
    padding: 15px;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card-light{
    background: white;
    color: black;
    border: 1px solid #ddd;
}
.card-dark{
    background: #111;
    color: white;
}

/* CARD CONTENT */
.card h4{
    margin-bottom: 6px;
    font-size: 18px;
}
.card p{
    font-size: 14px;
    margin: 4px 0;
    line-height: 1.4;
}

/* STATUS INDICATOR */
.status-pending {
    color: #f59e0b;
}
.status-done {
    color: #10b981;
}
</style>""",
        "penjelasan": {
            "title": "CSS Modern Layout",
            "points": [
                "**display: grid** → Menggunakan CSS Grid untuk layout",
                "**repeat(auto-fill, 240px)** → Membuat kolom otomatis dengan lebar 240px",
                "**justify-content: center** → Pusatkan grid items",
                "**gap: 20px** → Jarak antar item (ganti margin)",
                "**.card-light / .card-dark** → Conditional styling berdasarkan status",
                "**box-shadow** → Efek bayangan untuk depth",
                "**rgba()** → Warna dengan transparansi"
            ]
        },
        "critical_parts": [
            "display: grid",
            "grid-template-columns: repeat(auto-fill, 240px)",
            "justify-content: center",
            "gap: 20px",
            "box-shadow: 0 2px 8px rgba(0,0,0,0.1)"
        ]
    },

    # ---------- CRUD (CREATE) ----------
    "Form Tambah Data (Create)": {
        "deskripsi": "Form HTML untuk menambah data baru dengan validasi session",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

// PROTEKSI SESSION
if (!isset($_SESSION['id_user'])) {
    header("location:login.php");
    exit;
}

$sql_category = "SELECT * FROM category";
$query_category = mysqli_query($koneksi, $sql_category);
?>

<!DOCTYPE html>
<html>
<head>
<title>Tambah Todo</title>
<style>
/* BOX LAYOUT */
.box {
    width: 350px;
    background: white;
    border: 2px solid black;
    padding: 20px;
    margin: 60px auto;
    border-radius: 8px;
}

/* FORM ELEMENTS */
input, textarea, select {
    width: 100%;
    padding: 8px;
    margin: 8px 0 16px;
    border: 1px solid #111;
    border-radius: 4px;
    font-size: 14px;
}

/* LABEL */
label {
    font-weight: bold;
    font-size: 14px;
}

/* BUTTON */
button {
    background: #111;
    color: white;
    border: none;
    padding: 10px;
    width: 100%;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}
button:hover {
    background: #333;
}
</style>
</head>
<body>
<div class="box">
    <h3>Tambah Todo</h3>
    <form action="proses_tambah.php" method="post">
        <label>Judul</label>
        <input type="text" name="title" required>
        <label>Deskripsi</label>
        <textarea name="description" rows="3"></textarea>
        <label>Kategori</label>
        <select name="id_category">
            <?php while($c = mysqli_fetch_assoc($query_category)): ?>
                <option value="<?= $c['id_category']; ?>">
                    <?= $c['category']; ?>
                </option>
            <?php endwhile; ?>
        </select>
        <button type="submit">Simpan</button>
    </form>
</div>
</body>
</html>""",
        "penjelasan": {
            "title": "Form Create dengan PHP",
            "points": [
                "**required attribute** → Validasi wajib diisi di client side",
                "**<textarea>** → Untuk input teks multi-line",
                "**<select>** → Dropdown untuk pilihan kategori",
                "**while loop** → Menampilkan option kategori dari database",
                "**margin: auto** → Center align box secara horizontal",
                "**transition** → Efek transisi pada hover",
                "**cursor: pointer** → Mengubah kursor saat hover"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "if (!isset($_SESSION['id_user']))",
            "header(\"location:login.php\")",
            "exit",
            "$sql_category = \"SELECT * FROM category\"",
            "mysqli_query($koneksi, $sql_category)",
            "action=\"proses_tambah.php\"",
            "method=\"post\"",
            "name=\"title\"",
            "name=\"description\"",
            "name=\"id_category\"",
            "required",
            "<?php while($c = mysqli_fetch_assoc($query_category)): ?>",
            "<?= $c['id_category']; ?>",
            "<?= $c['category']; ?>",
            "<?php endwhile; ?>"
        ]
    },

    "Proses Tambah (INSERT)": {
        "deskripsi": "Proses menyimpan data ke database",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$id_user = $_SESSION['id_user'];
$title = $_POST['title'];
$description = $_POST['description'];
$id_category = $_POST['id_category'];

$sql = "INSERT INTO todo (id_user, title, description, id_category, status)
        VALUES ('$id_user', '$title', '$description', '$id_category', 'pending')";

mysqli_query($koneksi, $sql);

header("location:index.php");
?>""",
        "penjelasan": {
            "title": "INSERT Query Structure",
            "points": [
                "**$_SESSION['id_user']** → Mengambil ID user dari session",
                "**$_POST[]** → Mengambil data dari form",
                "**INSERT INTO** → Syntax untuk menambah data",
                "**VALUES()** → Nilai yang akan diinsert",
                "**'pending'** → Default value untuk status",
                "**mysqli_query()** → Eksekusi query ke database",
                "**header()** → Redirect setelah sukses"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_SESSION['id_user']",
            "$_POST['title']",
            "$_POST['description']",
            "$_POST['id_category']",
            "INSERT INTO todo",
            "VALUES ('$id_user', '$title', '$description', '$id_category', 'pending')",
            "mysqli_query($koneksi, $sql)",
            "header(\"location:index.php\")"
        ]
    },

    # ---------- CRUD (UPDATE) ----------
    "Form Edit Data": {
        "deskripsi": "Form untuk mengedit data yang sudah ada",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

// PROTEKSI SESSION
if (!isset($_SESSION['id_user'])) {
    header("location:login.php");
    exit;
}

$id_todo = $_GET['id_todo'];

// AMBIL DATA YANG AKAN DIEDIT
$sql = "SELECT * FROM todo WHERE id_todo='$id_todo'";
$query = mysqli_query($koneksi, $sql);
$todo = mysqli_fetch_assoc($query);

// AMBIL DATA KATEGORI
$sql_category = "SELECT * FROM category";
$query_category = mysqli_query($koneksi, $sql_category);
?>""",
        "penjelasan": {
            "title": "Mengambil Data untuk Edit",
            "points": [
                "**$_GET['id_todo']** → Mengambil parameter ID dari URL",
                "**SELECT * WHERE** → Query untuk mengambil 1 data spesifik",
                "**mysqli_fetch_assoc()** → Mengambil data dalam bentuk array",
                "**$todo[]** → Variable yang menyimpan data lama",
                "**Saat Edit** → Form diisi dengan nilai dari database"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "if (!isset($_SESSION['id_user']))",
            "header(\"location:login.php\")",
            "exit",
            "$_GET['id_todo']",
            "SELECT * FROM todo WHERE id_todo='$id_todo'",
            "mysqli_query($koneksi, $sql)",
            "mysqli_fetch_assoc($query)",
            "SELECT * FROM category",
            "mysqli_query($koneksi, $sql_category)"
        ]
    },

    "Proses Edit (UPDATE)": {
        "deskripsi": "Proses update data di database",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$id_todo = $_POST['id_todo'];
$title = $_POST['title'];
$description = $_POST['description'];
$id_category = $_POST['id_category'];

$sql = "UPDATE todo SET
        title='$title',
        description='$description',
        id_category='$id_category'
        WHERE id_todo='$id_todo'";

mysqli_query($koneksi, $sql);

header("location:index.php");
?>""",
        "penjelasan": {
            "title": "UPDATE Query Structure",
            "points": [
                "**UPDATE table SET** → Syntax untuk update data",
                "**column='value'** → Mengatur nilai baru untuk kolom",
                "**WHERE** → WAJIB untuk menentukan data mana yang diupdate",
                "**Tanpa WHERE** → Semua data akan terupdate (BAHAYA!)",
                "**$id_todo** → Identifier unik untuk data yang diupdate"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_POST['id_todo']",
            "$_POST['title']",
            "$_POST['description']",
            "$_POST['id_category']",
            "UPDATE todo SET",
            "WHERE id_todo='$id_todo'",
            "mysqli_query($koneksi, $sql)",
            "header(\"location:index.php\")"
        ]
    },

    # ---------- CRUD (DELETE) ----------
    "Proses Hapus (DELETE)": {
        "deskripsi": "Menghapus data dengan konfirmasi JavaScript",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$id_todo = $_GET['id_todo'];

$sql = "DELETE FROM todo WHERE id_todo='$id_todo'";
mysqli_query($koneksi, $sql);

header("location:index.php");
?>

<!-- JavaScript Confirm -->
<a href="hapus.php?id_todo=<?= $todo['id_todo']; ?>"
   class="btn btn-delete"
   onclick="return confirm('Yakin hapus data ini?')">
   Hapus
</a>""",
        "penjelasan": {
            "title": "DELETE dengan Keamanan",
            "points": [
                "**DELETE FROM** → Syntax untuk menghapus data",
                "**WHERE** → WAJIB agar tidak menghapus semua data",
                "**JavaScript confirm()** → Konfirmasi sebelum menghapus",
                "**return confirm()** → Jika false, link tidak diikuti",
                "**Best Practice** → Selalu gunakan konfirmasi untuk delete"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_GET['id_todo']",
            "DELETE FROM todo",
            "WHERE id_todo='$id_todo'",
            "mysqli_query($koneksi, $sql)",
            "header(\"location:index.php\")",
            "onclick=\"return confirm('Yakin hapus data ini?')\""
        ]
    },

    # ---------- NAVBAR & CSS ----------
    "Navbar CSS": {
        "deskripsi": "Navigation bar dengan styling modern",
        "tipe": "css",
        "kode": """<style>
/* NAVBAR STYLING */
.navbar{
    background: linear-gradient(90deg, #111 0%, #333 100%);
    color: white;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

/* NAVBAR LINKS */
.navbar a{
    color: white;
    text-decoration: none;
    margin-left: 20px;
    padding: 8px 16px;
    border-radius: 4px;
    transition: background 0.3s;
}
.navbar a:hover{
    background: rgba(255,255,255,0.1);
}

/* LOGOUT BUTTON */
.navbar a[href*="logout"]{
    background: #dc2626;
}
.navbar a[href*="logout"]:hover{
    background: #b91c1c;
}
</style>

<!-- HTML NAVBAR -->
<div class="navbar">
    <h3>📝 Todo App</h3>
    <div>
        <a href="index.php">🏠 Home</a>
        <a href="tambah.php">➕ Tambah</a>
        <a href="logout.php">🚪 Logout</a>
    </div>
</div>""",
        "penjelasan": {
            "title": "CSS Navbar Techniques",
            "points": [
                "**display: flex** → Untuk layout horizontal",
                "**justify-content: space-between** → Space antara logo dan menu",
                "**position: sticky** → Navbar tetap saat scroll",
                "**z-index** → Menentukan layer/tingkatan",
                "**linear-gradient()** → Background gradient",
                "**rgba()** → Warna dengan opacity",
                "**a[href*='logout']** → Selector attribute untuk styling spesifik"
            ]
        },
        "critical_parts": [
            "display: flex",
            "justify-content: space-between",
            "align-items: center",
            "position: sticky",
            "top: 0",
            "z-index: 1000",
            "box-shadow: 0 2px 10px rgba(0,0,0,0.2)",
            "background: linear-gradient(90deg, #111 0%, #333 100%)",
            "text-decoration: none",
            "transition: background 0.3s",
            ":hover",
            "a[href*=\"logout\"]"
        ]
    },

    "Button Styling": {
        "deskripsi": "Berbagai style button untuk CRUD operations",
        "tipe": "css",
        "kode": """<style>
/* BUTTON BASE */
.btn{
    display: inline-block;
    padding: 8px 16px;
    text-decoration: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
    margin: 5px;
}

/* BUTTON VARIANTS */
.btn-edit{
    background: #2563eb;
    color: white;
}
.btn-edit:hover{
    background: #1d4ed8;
    transform: translateY(-2px);
}

.btn-delete{
    background: #dc2626;
    color: white;
}
.btn-delete:hover{
    background: #b91c1c;
    transform: translateY(-2px);
}

.btn-add{
    background: #059669;
    color: white;
}
.btn-add:hover{
    background: #047857;
    transform: translateY(-2px);
}

.btn-save{
    background: #111;
    color: white;
    width: 100%;
    padding: 12px;
}
.btn-save:hover{
    background: #333;
}

/* BUTTON WITH ICON */
.btn i{
    margin-right: 6px;
}
</style>""",
        "penjelasan": {
            "title": "CSS Button Best Practices",
            "points": [
                "**transition: all 0.3s** → Smooth animation untuk semua properti",
                "**:hover** → State ketika mouse di atas button",
                "**transform: translateY()** → Efek mengangkat saat hover",
                "**Color Coding** → Warna berbeda untuk aksi berbeda",
                "**btn-edit (biru)** → Untuk update/edit",
                "**btn-delete (merah)** → Untuk delete/hapus",
                "**btn-add (hijau)** → Untuk tambah data",
                "**box-shadow** → Menambahkan depth perception"
            ]
        },
        "critical_parts": [
            "display: inline-block",
            "padding: 8px 16px",
            "text-decoration: none",
            "border-radius: 6px",
            "transition: all 0.3s",
            ":hover",
            "transform: translateY(-2px)",
            "cursor: pointer"
        ]
    }
}

# =========================
# FUNGSI UTILITY
# =========================
def calculate_similarity(text1, text2):
    """Hitung persentase kemiripan antara dua teks"""
    def clean_code(code):
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'\s+', ' ', code)
        return code.strip().lower()
    
    user_clean = clean_code(text1)
    correct_clean = clean_code(text2)
    
    similarity = SequenceMatcher(None, user_clean, correct_clean).ratio() * 100
    return round(similarity, 2)

def check_critical_parts(user_code, critical_parts):
    """Cek bagian-bagian kritis yang harus ada"""
    results = []
    user_code_lower = user_code.lower()
    
    for part in critical_parts:
        part_lower = part.lower()
        if part_lower in user_code_lower:
            results.append((part, True, "✅"))
        else:
            results.append((part, False, "❌"))
    
    return results

def analyze_code_errors(user_code, correct_code, code_type):
    """Analisis kesalahan umum dalam kode"""
    errors = []
    warnings = []
    suggestions = []
    
    user_code_lower = user_code.lower()
    
    if "php" in code_type:
        if "session_start()" not in user_code:
            errors.append("❌ **session_start()** tidak ditemukan! (WAJIB ada di baris pertama)")
        
        if "include" not in user_code_lower and "require" not in user_code_lower:
            errors.append("❌ **include/require** koneksi database tidak ditemukan!")
        
        if "header(" in user_code and "exit" not in user_code and "die" not in user_code:
            warnings.append("⚠️ **header()** digunakan tanpa **exit()** atau **die()**")
        
        if "update" in user_code_lower and "where" not in user_code_lower:
            errors.append("❌ **UPDATE** query tanpa **WHERE** clause! (SANGAT BERBAHAYA)")
        
        if "delete" in user_code_lower and "where" not in user_code_lower:
            errors.append("❌ **DELETE** query tanpa **WHERE** clause! (SANGAT BERBAHAYA)")
    
    elif "html" in code_type:
        if "<!doctype" not in user_code_lower:
            errors.append("❌ **DOCTYPE** declaration tidak ditemukan")
        
        if "<form" in user_code_lower and ("method=" not in user_code_lower or "action=" not in user_code_lower):
            warnings.append("⚠️ Form tanpa **method** atau **action** attribute")
    
    elif "css" in code_type:
        if "{" in user_code and "}" not in user_code:
            errors.append("❌ Kurung kurawal **{}** tidak ditutup")
        
        if ":" in user_code and ";" not in user_code:
            warnings.append("⚠️ Property CSS tanpa titik koma **;**")
    
    # Suggestions berdasarkan similarity
    similarity = calculate_similarity(user_code, correct_code)
    if similarity < 50:
        suggestions.append("💡 Pelajari lagi struktur dasar dari materi ini")
    elif similarity < 75:
        suggestions.append("💡 Fokus pada bagian yang masih kurang tepat")
    elif similarity < 90:
        suggestions.append("💡 Hampir sempurna! Perbaiki detail kecil")
    else:
        suggestions.append("🎉 Excellent! Kode sudah sangat mirip dengan contoh")
    
    return errors, warnings, suggestions

# =========================
# SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.title("📚 PerpusCode USK")
    
    selected_mode = option_menu(
        menu_title="Mode Belajar",
        options=["🏠 Dashboard", "📖 Belajar", "✏️ Praktek", "🎯 Simulasi", "📊 Progress", "❓ Quiz"],
        icons=['house', 'book', 'code-slash', 'clock', 'bar-chart', 'question-circle'],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "orange", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#2E86AB"},
        }
    )
    
    st.markdown("---")
    
    # Pilih materi
    materi_list = list(materi.keys())
    selected_topic = st.sidebar.selectbox(
        "📖 Pilih Materi:",
        materi_list,
        key="selected_topic"
    )
    
    # Update last viewed
    if selected_topic not in st.session_state.last_viewed:
        st.session_state.last_viewed.append(selected_topic)
        if len(st.session_state.last_viewed) > 5:
            st.session_state.last_viewed.pop(0)
    
    st.markdown("---")
    
    # Quick stats
    if selected_topic in st.session_state.practice_scores:
        latest_score = st.session_state.practice_scores[selected_topic][-1]
        st.sidebar.metric("Skor Terakhir", f"{latest_score}%")
    
    # Last viewed
    with st.sidebar.expander("📖 Riwayat Materi"):
        for item in reversed(st.session_state.last_viewed):
            st.caption(f"✓ {item}")

# =========================
# DASHBOARD MODE
# =========================
if selected_mode == "🏠 Dashboard":
    st.title("🏠 Dashboard - Persiapan USK")
    
    # Header stats
    col1, col2, col3 = st.columns(3)
    with col1:
        total_materi = len(materi)
        st.metric("Total Materi", total_materi)
    with col2:
        practiced = len(st.session_state.practice_scores)
        st.metric("Sudah Dipraktekkan", practiced)
    with col3:
        if st.session_state.practice_scores:
            all_scores = []
            for scores in st.session_state.practice_scores.values():
                all_scores.extend(scores)
            avg_score = sum(all_scores) / len(all_scores)
            st.metric("Rata-rata Skor", f"{avg_score:.1f}%")
        else:
            st.metric("Rata-rata Skor", "0%")
    
    # Study plan
    st.markdown("---")
    st.subheader("📅 Rencana Belajar 7 Hari")
    
    study_plan = [
        ("Hari 1", "Session & Login", ["Login Page (HTML)", "Proses Login (Session)"]),
        ("Hari 2", "CRUD - Read", ["Index Page (Read + Filter)"]),
        ("Hari 3", "CRUD - Create", ["Form Tambah Data (Create)", "Proses Tambah (INSERT)"]),
        ("Hari 4", "CRUD - Update", ["Form Edit Data", "Proses Edit (UPDATE)"]),
        ("Hari 5", "CRUD - Delete", ["Proses Hapus (DELETE)"]),
        ("Hari 6", "CSS Styling", ["CSS Grid Layout", "Navbar CSS", "Button Styling"]),
        ("Hari 7", "Review & Simulasi", ["Semua Materi"])
    ]
    
    for day, topic, materials in study_plan:
        with st.expander(f"{day}: {topic}", expanded=False):
            for material in materials:
                if material in materi_list:
                    status = "✅" if material in st.session_state.practice_scores else "⏳"
                    st.markdown(f"{status} {material}")
            
            day_num = int(day.split()[1])
            if not st.session_state.study_progress[f"hari_{day_num}"]:
                if st.button(f"✅ Tandai {day} Selesai", key=f"complete_{day_num}"):
                    st.session_state.study_progress[f"hari_{day_num}"] = True
                    st.rerun()
            else:
                st.success(f"{day} sudah selesai dipelajari!")
    
    # Quick actions
    st.markdown("---")
    st.subheader("🚀 Aksi Cepat")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 Lanjut Belajar", use_container_width=True):
            st.session_state.selected_mode = "📖 Belajar"
            st.rerun()
    with col2:
        if st.button("✏️ Mulai Praktek", use_container_width=True):
            st.session_state.selected_mode = "✏️ Praktek"
            st.rerun()
    with col3:
        if st.button("🎯 Simulasi USK", use_container_width=True):
            st.session_state.selected_mode = "🎯 Simulasi"
            st.rerun()

# =========================
# BELAJAR MODE
# =========================
elif selected_mode == "📖 Belajar":
    st.title("📖 Mode Belajar")
    
    topic_data = materi[selected_topic]
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"{selected_topic}")
    with col2:
        st.caption(f"Tipe: {topic_data['tipe'].upper()}")
    
    st.markdown(f"**Deskripsi:** {topic_data['deskripsi']}")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Kode Lengkap", "📚 Penjelasan", "💡 Tips"])
    
    with tab1:
        st.code(topic_data["kode"], language=topic_data["tipe"])
        
        # Critical parts
        st.markdown("### ⚠️ Bagian Kritis (WAJIB DIINGAT):")
        for part in topic_data["critical_parts"][:5]:  # Tampilkan 5 pertama
            st.markdown(f"- `{part}`")
    
    with tab2:
        penjelasan = topic_data["penjelasan"]
        st.subheader(penjelasan["title"])
        
        for point in penjelasan["points"]:
            st.markdown(f"• {point}")
        
        # Additional notes
        if "Session" in selected_topic:
            st.info("""
            **Catatan Penting Session:**
            1. `session_start()` harus dipanggil SEBELUM output apapun ke browser
            2. Session data disimpan di server, aman dari client-side manipulation
            3. Gunakan `session_destroy()` untuk logout yang aman
            """)
        elif "CSS" in selected_topic:
            st.info("""
            **Best Practice CSS:**
            1. Gunakan class selector daripada tag selector untuk reusable style
            2. Implement mobile-first design dengan media queries
            3. Gunakan CSS Grid/Flexbox untuk layout modern
            """)
    
    with tab3:
        # Tips berdasarkan jenis materi
        if "Login" in selected_topic:
            st.success("""
            **Tips Login System:**
            1. Selalu gunakan password hashing (md5, password_hash)
            2. Tambahkan limit attempt untuk prevent brute force
            3. Gunakan prepared statements untuk prevent SQL injection
            4. Always redirect setelah login/logout
            """)
        elif "INSERT" in selected_topic or "CREATE" in selected_topic:
            st.warning("""
            **Tips INSERT Data:**
            1. Validasi input di server-side (tidak hanya client-side)
            2. Gunakan prepared statements untuk keamanan
            3. Berikan feedback setelah insert (sukses/gagal)
            4. Redirect ke halaman list setelah insert
            """)
        elif "UPDATE" in selected_topic:
            st.warning("""
            **Tips UPDATE Data:**
            1. SELALU gunakan WHERE clause, jika tidak semua data akan terupdate
            2. Ambil data lama sebelum edit untuk default value
            3. Validasi bahwa user memiliki akses untuk edit data tersebut
            4. Gunakan hidden input untuk menyimpan ID data
            """)
        elif "DELETE" in selected_topic:
            st.error("""
            **Tips DELETE Data:**
            1. WAJIB gunakan WHERE dengan primary key
            2. Tambahkan konfirmasi JavaScript
            3. Pertimbangkan soft delete (tambah kolom is_deleted)
            4. Backup data penting sebelum delete operation
            """)
        elif "CSS" in selected_topic:
            st.info("""
            **Tips CSS:**
            1. Organize CSS dengan BEM methodology
            2. Use CSS variables for consistent theming
            3. Test on multiple screen sizes
            4. Use developer tools for debugging
            """)

# =========================
# PRAKTEK MODE
# =========================
elif selected_mode == "✏️ Praktek":
    st.title("✏️ Mode Praktek Menulis Kode")
    
    topic_data = materi[selected_topic]
    
    # Settings
    col1, col2 = st.columns(2)
    with col1:
        timer_minutes = st.slider("⏱️ Waktu (menit):", 5, 30, 10)
    with col2:
        show_hints = st.checkbox("💡 Tampilkan Petunjuk", value=True)
    
    # Timer
    if 'practice_start_time' not in st.session_state:
        st.session_state.practice_start_time = time.time()
    
    elapsed = time.time() - st.session_state.practice_start_time
    remaining = max(0, timer_minutes * 60 - elapsed)
    
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    
    st.markdown(f"**⏰ Waktu tersisa:** {minutes:02d}:{seconds:02d}")
    st.progress(min(1.0, elapsed/(timer_minutes*60)))
    
    if remaining <= 0:
        st.error("⏰ WAKTU HABIS! Submit jawaban kamu sekarang.")
    
    # Instructions
    st.markdown("---")
    st.markdown(f"### 📝 TUGAS: {selected_topic}")
    st.markdown(f"**Deskripsi:** {topic_data['deskripsi']}")
    
    # Hints
    if show_hints:
        with st.expander("💡 Petunjuk", expanded=True):
            st.markdown("**Bagian WAJIB ada:**")
            for part in topic_data["critical_parts"][:3]:
                st.markdown(f"• `{part}`")
    
    # Code editor
    st.markdown("### ✍️ Tulis Kode Kamu:")
    
    user_code = st.text_area(
        "Ketik kode di bawah ini:",
        height=300,
        placeholder=f"Mulai mengetik kode {topic_data['tipe'].upper()} di sini...",
        key="practice_editor"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Submit & Analisis", type="primary", use_container_width=True):
            if user_code.strip():
                # Hitung similarity
                similarity = calculate_similarity(user_code, topic_data["kode"])
                
                # Cek critical parts
                critical_results = check_critical_parts(user_code, topic_data["critical_parts"])
                
                # Analisis errors
                errors, warnings, suggestions = analyze_code_errors(
                    user_code, 
                    topic_data["kode"], 
                    topic_data["tipe"]
                )
                
                # Simpan score
                if selected_topic not in st.session_state.practice_scores:
                    st.session_state.practice_scores[selected_topic] = []
                st.session_state.practice_scores[selected_topic].append(similarity)
                
                # Tampilkan hasil
                st.session_state.show_practice_results = True
                st.session_state.last_similarity = similarity
                st.session_state.last_errors = errors
                st.session_state.last_warnings = warnings
                st.session_state.last_suggestions = suggestions
                st.session_state.critical_results = critical_results
                st.rerun()
            else:
                st.warning("⚠️ Silakan tulis kode terlebih dahulu!")
    
    with col2:
        if st.button("👁️ Lihat Contoh", use_container_width=True):
            with st.expander("📖 Kode Contoh"):
                st.code(topic_data["kode"], language=topic_data["tipe"])
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.practice_start_time = time.time()
            st.rerun()
    
    # Tampilkan hasil jika ada
    if 'show_practice_results' in st.session_state and st.session_state.show_practice_results:
        st.markdown("---")
        st.markdown("## 📊 HASIL ANALISIS")
        
        similarity = st.session_state.last_similarity
        
        # Score card
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Persentase Kemiripan", f"{similarity}%")
        with col2:
            critical_found = sum(1 for _, found, _ in st.session_state.critical_results if found)
            total_critical = len(st.session_state.critical_results)
            st.metric("Bagian Kritis", f"{critical_found}/{total_critical}")
        with col3:
            if similarity >= 90:
                grade = "A"
            elif similarity >= 80:
                grade = "B"
            elif similarity >= 70:
                grade = "C"
            else:
                grade = "D"
            st.metric("Grade", grade)
        
        # Progress bar
        st.progress(similarity/100)
        
        if similarity >= 90:
            st.success(f"🎉 EXCELLENT! Kode kamu {similarity}% mirip dengan contoh!")
        elif similarity >= 75:
            st.info(f"👍 GOOD! Kode kamu {similarity}% mirip.")
        elif similarity >= 60:
            st.warning(f"⚠️ FAIR! Kode kamu {similarity}% mirip.")
        else:
            st.error(f"❌ NEED IMPROVEMENT! Hanya {similarity}% mirip.")
        
        # Critical parts check
        st.markdown("### 📋 Hasil Cek Bagian Kritis:")
        for part, found, icon in st.session_state.critical_results[:10]:  # Tampilkan 10 pertama
            st.markdown(f"{icon} `{part}`")
        
        # Errors and warnings
        if st.session_state.last_errors:
            st.markdown("#### ❌ Kesalahan Fatal:")
            for error in st.session_state.last_errors:
                st.error(error)
        
        if st.session_state.last_warnings:
            st.markdown("#### ⚠️ Peringatan:")
            for warning in st.session_state.last_warnings:
                st.warning(warning)
        
        if st.session_state.last_suggestions:
            st.markdown("#### 💡 Saran:")
            for suggestion in st.session_state.last_suggestions:
                st.info(suggestion)
        
        # Action buttons setelah hasil
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Coba Lagi", type="primary", use_container_width=True):
                st.session_state.show_practice_results = False
                st.session_state.practice_start_time = time.time()
                st.rerun()
        with col2:
            if st.button("📚 Pelajari Materi", use_container_width=True):
                st.session_state.selected_mode = "📖 Belajar"
                st.rerun()

# =========================
# SIMULASI MODE
# =========================
elif selected_mode == "🎯 Simulasi":
    st.title("🎯 Mode Simulasi USK")
    
    # Simulation settings
    col1, col2, col3 = st.columns(3)
    with col1:
        simulation_time = st.slider("⏱️ Waktu (menit):", 30, 180, 120)
    with col2:
        question_count = st.slider("📝 Jumlah Soal:", 3, 10, 5)
    with col3:
        simulation_mode = st.selectbox("🎯 Mode:", ["Full Code", "Fill in the Blank", "Debugging"])
    
    # Start simulation
    if 'simulation_active' not in st.session_state:
        st.session_state.simulation_active = False
    
    if not st.session_state.simulation_active:
        st.markdown("### 📋 Persiapan Simulasi")
        st.warning("""
        ⚠️ **PERATURAN SIMULASI:**
        
        1. Waktu: **2 jam** (120 menit)
        2. Tidak boleh buka catatan/browser lain
        3. Kerjakan dengan sungguh-sungguh
        4. Submit sebelum waktu habis
        """)
        
        if st.button("🚀 Mulai Simulasi", type="primary"):
            st.session_state.simulation_active = True
            st.session_state.simulation_start_time = time.time()
            st.session_state.simulation_questions = random.sample(list(materi.keys()), min(question_count, len(materi)))
            st.session_state.current_question = 0
            st.session_state.simulation_answers = {}
            st.rerun()
    else:
        # Timer
        elapsed = time.time() - st.session_state.simulation_start_time
        remaining = max(0, simulation_time * 60 - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        st.markdown(f"### ⏱️ Waktu Tersisa: {minutes:02d}:{seconds:02d}")
        st.progress(min(1.0, elapsed/(simulation_time*60)))
        
        if remaining <= 0:
            st.error("⏰ WAKTU HABIS! Simulasi berakhir.")
            st.session_state.simulation_active = False
        
        # Current question
        current_q = st.session_state.current_question
        total_q = len(st.session_state.simulation_questions)
        topic = st.session_state.simulation_questions[current_q]
        topic_data = materi[topic]
        
        st.markdown(f"### 📝 Soal {current_q + 1} dari {total_q}")
        st.markdown(f"**{topic}**")
        st.markdown(f"*{topic_data['deskripsi']}*")
        
        # Question based on mode
        if simulation_mode == "Full Code":
            st.markdown("**Tugas:** Tulis kode lengkap untuk implementasi di atas.")
            answer = st.text_area(
                "Tulis kode kamu:",
                height=300,
                placeholder="Tulis kode lengkap di sini...",
                key=f"simulation_q_{current_q}"
            )
        
        elif simulation_mode == "Fill in the Blank":
            # Create fill in the blank question
            code_lines = topic_data["kode"].split('\n')
            blank_lines = random.sample(range(len(code_lines)), min(5, len(code_lines)//2))
            
            display_code = ""
            for i, line in enumerate(code_lines):
                if i in blank_lines:
                    display_code += f"_______\n"
                else:
                    display_code += f"{line}\n"
            
            st.code(display_code, language=topic_data["tipe"])
            st.markdown("**Tugas:** Isi bagian yang kosong dengan kode yang tepat.")
            answer = st.text_area(
                "Jawaban (sebutkan nomor baris dan kodenya):",
                height=150,
                placeholder="Contoh:\n1. session_start();\n3. include 'koneksi.php';",
                key=f"simulation_q_{current_q}"
            )
        
        elif simulation_mode == "Debugging":
            # Create buggy code
            original_code = topic_data["kode"]
            buggy_code = original_code
            
            # Introduce common bugs
            if "session_start()" in original_code:
                buggy_code = buggy_code.replace("session_start()", "// session_start()")
            if "WHERE" in original_code:
                buggy_code = buggy_code.replace("WHERE", "// WHERE")
            
            st.code(buggy_code, language=topic_data["tipe"])
            st.markdown("**Tugas:** Temukan dan perbaiki kesalahan dalam kode di atas.")
            answer = st.text_area(
                "Sebutkan kesalahan dan perbaikannya:",
                height=200,
                placeholder="1. Baris 2: session_start() di-comment, harus di-uncomment\n2. Baris X: WHERE hilang, harus ditambahkan",
                key=f"simulation_q_{current_q}"
            )
        
        # Save answer
        st.session_state.simulation_answers[current_q] = answer
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if current_q > 0:
                if st.button("⬅️ Sebelumnya", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if current_q < total_q - 1:
                if st.button("Berikutnya ➡️", type="primary", use_container_width=True):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("✅ Submit Semua", type="primary", use_container_width=True):
                    # Calculate score
                    total_score = 0
                    for i in range(total_q):
                        topic = st.session_state.simulation_questions[i]
                        user_answer = st.session_state.simulation_answers.get(i, "")
                        
                        if simulation_mode == "Full Code":
                            similarity = calculate_similarity(user_answer, materi[topic]["kode"])
                            total_score += similarity
                    
                    avg_score = total_score / total_q
                    
                    # Save simulation result
                    st.session_state.quiz_scores.append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "mode": simulation_mode,
                        "score": avg_score,
                        "questions": total_q
                    })
                    
                    st.session_state.simulation_active = False
                    st.session_state.show_simulation_results = True
                    st.session_state.last_simulation_score = avg_score
                    st.rerun()
        
        with col3:
            if st.button("⏹️ Akhiri Simulasi", use_container_width=True):
                st.session_state.simulation_active = False
                st.warning("Simulasi diakhiri. Hasil tidak disimpan.")
                st.rerun()
    
    # Show results if available
    if 'show_simulation_results' in st.session_state and st.session_state.show_simulation_results:
        st.markdown("---")
        st.markdown("## 📊 HASIL SIMULASI USK")
        
        score = st.session_state.last_simulation_score
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skor Akhir", f"{score:.1f}%")
        with col2:
            if score >= 85:
                grade = "A"
                color = "green"
            elif score >= 70:
                grade = "B"
                color = "blue"
            elif score >= 60:
                grade = "C"
                color = "orange"
            else:
                grade = "D"
                color = "red"
            st.metric("Grade", grade)
        with col3:
            st.metric("Mode", simulation_mode)
        
        # Feedback
        st.progress(score/100)
        
        if score >= 85:
            st.success("🎉 **LUAR BIASA!** Kamu siap menghadapi USK!")
            st.balloons()
        elif score >= 70:
            st.info("👍 **BAIK!** Perlu sedikit perbaikan lagi.")
        elif score >= 60:
            st.warning("⚠️ **CUKUP!** Perlu lebih banyak latihan.")
        else:
            st.error("❌ **PERLU BELAJAR LAGI!** Fokus pada materi dasar.")
        
        # Recommendations
        st.markdown("### 🎯 Rekomendasi:")
        if score < 70:
            st.markdown("1. **Review materi** yang masih lemah")
            st.markdown("2. **Latihan lebih banyak** di mode Praktek")
            st.markdown("3. **Fokus pada bagian kritis** yang sering keluar")
        else:
            st.markdown("1. **Pertahankan konsistensi** belajar")
            st.markdown("2. **Coba difficulty lebih tinggi**")
            st.markdown("3. **Review waktu pengerjaan** untuk efisiensi")
        
        if st.button("🔄 Coba Simulasi Lagi", type="primary"):
            st.session_state.show_simulation_results = False
            st.rerun()

# =========================
# PROGRESS MODE
# =========================
elif selected_mode == "📊 Progress":
    st.title("📊 Progress Belajar")
    
    if not st.session_state.practice_scores and not st.session_state.quiz_scores:
        st.info("📭 Belum ada data progress. Mulai latihan atau simulasi terlebih dahulu!")
    else:
        # Overall statistics
        st.markdown("### 📈 Statistik Keseluruhan")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_practices = sum(len(scores) for scores in st.session_state.practice_scores.values())
            st.metric("Total Praktek", total_practices)
        
        with col2:
            total_simulations = len(st.session_state.quiz_scores)
            st.metric("Total Simulasi", total_simulations)
        
        with col3:
            if st.session_state.practice_scores:
                all_scores = []
                for scores in st.session_state.practice_scores.values():
                    all_scores.extend(scores)
                avg_practice = sum(all_scores) / len(all_scores)
                st.metric("Rata2 Praktek", f"{avg_practice:.1f}%")
            else:
                st.metric("Rata2 Praktek", "0%")
        
        with col4:
            if st.session_state.quiz_scores:
                avg_simulation = sum(s['score'] for s in st.session_state.quiz_scores) / len(st.session_state.quiz_scores)
                st.metric("Rata2 Simulasi", f"{avg_simulation:.1f}%")
            else:
                st.metric("Rata2 Simulasi", "0%")
        
        # Practice progress per topic
        st.markdown("---")
        st.markdown("### 📊 Progress per Materi")
        
        for topic, scores in st.session_state.practice_scores.items():
            with st.expander(f"{topic} ({len(scores)}x praktek)"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_score = sum(scores) / len(scores)
                    st.metric("Rata-rata", f"{avg_score:.1f}%")
                with col2:
                    best_score = max(scores)
                    st.metric("Terbaik", f"{best_score:.1f}%")
                with col3:
                    last_score = scores[-1]
                    st.metric("Terakhir", f"{last_score:.1f}%")
                
                # Improvement
                if len(scores) > 1:
                    improvement = scores[-1] - scores[0]
                    if improvement > 0:
                        st.success(f"📈 Peningkatan: +{improvement:.1f}%")
                    elif improvement < 0:
                        st.warning(f"📉 Penurunan: {improvement:.1f}%")
                    else:
                        st.info("➡️ Stabil")
        
        # Simulation history
        if st.session_state.quiz_scores:
            st.markdown("---")
            st.markdown("### 📝 Riwayat Simulasi")
            
            for i, sim in enumerate(reversed(st.session_state.quiz_scores[-5:])):  # Tampilkan 5 terakhir
                with st.expander(f"Simulasi {len(st.session_state.quiz_scores)-i}: {sim['date']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Skor", f"{sim['score']:.1f}%")
                    with col2:
                        st.metric("Mode", sim['mode'])
                    with col3:
                        st.metric("Soal", sim['questions'])
        
        # Recommendations
        st.markdown("---")
        st.markdown("### 🎯 Rekomendasi Latihan")
        
        if st.session_state.practice_scores:
            # Find weakest topic
            topic_avgs = {}
            for topic, scores in st.session_state.practice_scores.items():
                topic_avgs[topic] = sum(scores) / len(scores)
            
            if topic_avgs:
                weakest = min(topic_avgs.items(), key=lambda x: x[1])
                st.error(f"**Perlu fokus pada:** {weakest[0]} ({weakest[1]:.1f}%)")
                st.markdown(f"**Saran:** Praktek lebih banyak dengan materi ini di mode Praktek")
        
        # Reset button
        if st.button("🔄 Reset Semua Progress", type="secondary"):
            st.session_state.practice_scores = {}
            st.session_state.quiz_scores = []
            st.success("Semua progress telah direset!")
            st.rerun()

# =========================
# QUIZ MODE
# =========================
elif selected_mode == "❓ Quiz":
    st.title("❓ Quick Quiz - Test Pemahaman")
    
    # Quiz questions database
    quiz_db = [
        {
            "question": "Di mana session_start() harus diletakkan dalam script PHP?",
            "options": [
                "Di awal script, sebelum output apapun",
                "Di akhir script, sebelum ?>",
                "Di tengah script, setelah include",
                "Di mana saja, tidak masalah"
            ],
            "answer": 0,
            "category": "PHP Session",
            "explanation": "session_start() HARUS dipanggil sebelum output apapun (termasuk spasi atau newline) ke browser."
        },
        {
            "question": "Apa yang terjadi jika UPDATE query tidak menggunakan WHERE clause?",
            "options": [
                "Hanya data pertama yang terupdate",
                "Semua data dalam tabel akan terupdate",
                "Akan terjadi error",
                "Tidak ada yang terjadi"
            ],
            "answer": 1,
            "category": "SQL",
            "explanation": "UPDATE tanpa WHERE akan mengubah SEMUA baris dalam tabel! Sangat berbahaya."
        },
        {
            "question": "Attribute apa yang WAJIB ada dalam tag <form> untuk mengirim data ke PHP?",
            "options": [
                "action dan method",
                "name dan id",
                "class dan style",
                "type dan value"
            ],
            "answer": 0,
            "category": "HTML Forms",
            "explanation": "action menentukan file tujuan, method menentukan cara pengiriman (GET/POST)."
        },
        {
            "question": "Property CSS apa yang digunakan untuk membuat grid layout?",
            "options": [
                "display: flex",
                "display: grid",
                "display: block",
                "display: inline"
            ],
            "answer": 1,
            "category": "CSS",
            "explanation": "display: grid mengaktifkan CSS Grid Layout untuk 2D layouts."
        },
        {
            "question": "Fungsi apa yang digunakan untuk mencegah SQL Injection di PHP?",
            "options": [
                "htmlspecialchars()",
                "mysqli_real_escape_string()",
                "strip_tags()",
                "trim()"
            ],
            "answer": 1,
            "category": "PHP Security",
            "explanation": "mysqli_real_escape_string() meng-escape karakter khusus dalam string untuk digunakan dalam query SQL."
        },
        {
            "question": "Apa fungsi dari md5() dalam proses login?",
            "options": [
                "Mengenkripsi password",
                "Mengkompres data",
                "Validasi format email",
                "Membersihkan input user"
            ],
            "answer": 0,
            "category": "PHP Security",
            "explanation": "md5() membuat hash dari password untuk disimpan di database (lebih baik gunakan password_hash())."
        },
        {
            "question": "Bagaimana cara mengambil data dari form dengan method POST di PHP?",
            "options": [
                "$_GET['nama_field']",
                "$_POST['nama_field']",
                "$_REQUEST['nama_field']",
                "$_FORM['nama_field']"
            ],
            "answer": 1,
            "category": "PHP Forms",
            "explanation": "$_POST adalah superglobal array yang berisi data dari form dengan method POST."
        },
        {
            "question": "Apa yang harus dilakukan setelah header('location: ...')?",
            "options": [
                "Tidak perlu apa-apa",
                "Panggil exit() atau die()",
                "Tunggu 5 detik",
                "Echo pesan sukses"
            ],
            "answer": 1,
            "category": "PHP Redirect",
            "explanation": "exit() atau die() diperlukan untuk menghentikan eksekusi script setelah redirect."
        }
    ]
    
    # Quiz settings
    col1, col2 = st.columns(2)
    with col1:
        quiz_count = st.slider("Jumlah soal:", 3, len(quiz_db), 5)
    with col2:
        selected_category = st.selectbox(
            "Kategori:",
            ["Semua"] + list(set([q["category"] for q in quiz_db]))
        )
    
    # Filter questions
    if selected_category == "Semua":
        quiz_questions = random.sample(quiz_db, min(quiz_count, len(quiz_db)))
    else:
        filtered = [q for q in quiz_db if q["category"] == selected_category]
        quiz_questions = random.sample(filtered, min(quiz_count, len(filtered)))
    
    # Initialize quiz state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    
    # Display questions
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        st.caption(f"Kategori: {q['category']}")
        
        answer_key = f"q_{i}"
        if answer_key not in st.session_state.quiz_answers:
            st.session_state.quiz_answers[answer_key] = None
        
        selected = st.radio(
            "Pilih jawaban:",
            q['options'],
            key=answer_key,
            index=st.session_state.quiz_answers[answer_key] if st.session_state.quiz_answers[answer_key] is not None else 0,
            disabled=st.session_state.quiz_submitted
        )
        
        st.session_state.quiz_answers[answer_key] = q['options'].index(selected)
        
        # Show answer if submitted
        if st.session_state.quiz_submitted:
            user_answer = st.session_state.quiz_answers[answer_key]
            if user_answer == q['answer']:
                st.success("✅ Benar!")
            else:
                st.error(f"❌ Salah! Jawaban benar: {q['options'][q['answer']]}")
                st.info(f"Penjelasan: {q['explanation']}")
        
        st.markdown("---")
    
    # Submit button
    if not st.session_state.quiz_submitted:
        if st.button("✅ Submit Jawaban", type="primary"):
            st.session_state.quiz_submitted = True
            
            # Calculate score
            correct = 0
            for i, q in enumerate(quiz_questions):
                answer_key = f"q_{i}"
                user_answer = st.session_state.quiz_answers.get(answer_key)
                if user_answer == q['answer']:
                    correct += 1
            
            score = (correct / len(quiz_questions)) * 100
            
            # Save quiz result
            st.session_state.quiz_scores.append({
                "date": datetime.now().strftime("%H:%M"),
                "score": score,
                "total": len(quiz_questions),
                "correct": correct
            })
            
            st.rerun()
    else:
        # Display results
        correct = sum(1 for i, q in enumerate(quiz_questions) 
                     if st.session_state.quiz_answers.get(f"q_{i}") == q['answer'])
        total = len(quiz_questions)
        score = (correct / total) * 100
        
        st.markdown(f"## 📊 Hasil Quiz: {score:.1f}% ({correct}/{total})")
        
        if score == 100:
            st.success("🎉 PERFECT SCORE! Kamu menguasai materi ini!")
            st.balloons()
        elif score >= 80:
            st.success("👍 EXCELLENT! Pemahaman kamu sangat baik!")
        elif score >= 60:
            st.info("💪 GOOD! Sudah cukup baik, bisa ditingkatkan lagi.")
        else:
            st.warning("📚 NEED STUDY! Pelajari lagi materinya ya.")
        
        if st.button("🔄 Coba Quiz Lagi"):
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📚 <b>PerpusCode USK - All-in-One Learning Platform</b></p>
    <p>📖 Learn • ✍️ Practice • 🎯 Simulate • 📊 Track • ❓ Quiz</p>
    <p>💪 Persiapkan USK dengan optimal menggunakan semua fitur yang tersedia!</p>
</div>
""", unsafe_allow_html=True)