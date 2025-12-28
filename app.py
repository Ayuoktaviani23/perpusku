import streamlit as st
import pandas as pd
import joblib
import time

# Load model & scaler
model = joblib.load("model_pony.joblib")
scaler = joblib.load("scaler_pony.joblib")

# Konfigurasi halaman
st.set_page_config(page_title="Pony Character Prediction", layout="centered")

# CSS custom + animasi modern
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(-45deg, #ffdde1, #ee9ca7, #fad0c4, #ffd1ff);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .result-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .pony-name {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .pony-desc {
        font-size: 18px;
        margin-top: 5px;
    }

    .rainbow { color: #ff5722; text-shadow: 0 0 10px #ff9800; }
    .twilight { color: #6a1b9a; text-shadow: 0 0 10px #ab47bc; }
    .pinkie { color: #e91e63; text-shadow: 0 0 10px #f48fb1; }
    .rarity { color: #3f51b5; text-shadow: 0 0 10px #7986cb; }
    .fluttershy { color: #ffb300; text-shadow: 0 0 10px #ffd54f; }
    .applejack { color: #795548; text-shadow: 0 0 10px #a1887f; }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul
st.markdown("<h1 style='text-align: center; color: purple;'>🦄 Personality Quiz - My Little Pony</h1>", unsafe_allow_html=True)
st.write("✨ Jawab pertanyaan di bawah ini untuk tahu kamu mirip dengan pony siapa! ✨")

# Pertanyaan (slider)
st.subheader("📋 Pertanyaan Kepribadian")

membaca = st.slider("📚 Seberapa sering kamu suka membaca buku?", 0, 10, 5)
bercanda = st.slider("😂 Apakah kamu suka bercanda / humor?", 0, 10, 5)
olahraga = st.slider("🏃 Seberapa aktif kamu dalam olahraga?", 0, 10, 5)
berpenampilan = st.slider("👗 Seberapa peduli kamu dengan penampilan / fashion?", 0, 10, 5)
jujur = st.slider("🤝 Seberapa jujur kamu dalam kehidupan sehari-hari?", 0, 10, 5)
baik_hati = st.slider("💖 Apakah kamu orang yang baik hati?", 0, 10, 5)
kreatif = st.slider("🎨 Seberapa kreatif kamu dalam ide / karya?", 0, 10, 5)
petualang = st.slider("🌍 Apakah kamu suka tantangan dan petualangan?", 0, 10, 5)
pendiam = st.slider("😶 Seberapa pendiam / introvert kamu?", 0, 10, 5)
loyal = st.slider("🛡️ Seberapa loyal / setia kamu terhadap teman?", 0, 10, 5)
memimpin = st.slider("👑 Apakah kamu lebih suka menjadi pemimpin?", 0, 10, 5)
kerjasama = st.slider("🤗 Seberapa baik kamu bekerja dalam tim / kerjasama?", 0, 10, 5)

# Prediksi
if st.button("🔮 Lihat Hasil"):
    data_baru = pd.DataFrame([[membaca, bercanda, olahraga, berpenampilan, jujur,
                               baik_hati, kreatif, petualang, pendiam, loyal,
                               memimpin, kerjasama]],
                             columns=["membaca","bercanda","olahraga","berpenampilan","jujur",
                                      "baik_hati","kreatif","petualang","pendiam","loyal",
                                      "memimpin","kerjasama"])
    data_baru_scaled = scaler.transform(data_baru)

    # Prediksi
    prediksi = model.predict(data_baru_scaled)[0]
    presentase = max(model.predict_proba(data_baru_scaled)[0])

    # Loading animasi
    with st.spinner("🔮 Meramal kepribadianmu..."):
        time.sleep(2)

    # Card hasil
    pony_class = "rarity"
    desc = "✨ Kamu unik, seperti pony spesial lainnya! ✨"

    if "Rainbow" in prediksi:
        pony_class = "rainbow"
        desc = "🌈 Penuh energi & berani seperti Rainbow Dash! 🚀"
    elif "Twilight" in prediksi:
        pony_class = "twilight"
        desc = "📖 Pintar, bijak, dan suka belajar seperti Twilight Sparkle ✨"
    elif "Pinkie" in prediksi:
        pony_class = "pinkie"
        desc = "🎉 Fun, ceria, dan suka pesta kayak Pinkie Pie! 🎂"
    elif "Rarity" in prediksi:
        pony_class = "rarity"
        desc = "💎 Elegan, stylish, dan penuh kreativitas seperti Rarity 👗"
    elif "Fluttershy" in prediksi:
        pony_class = "fluttershy"
        desc = "🌸 Lembut, penyayang, dan penuh empati seperti Fluttershy 🦋"
    elif "Applejack" in prediksi:
        pony_class = "applejack"
        desc = "🍎 Jujur, pekerja keras, dan sederhana seperti Applejack 🤠"

    st.markdown(
        f"""
        <div class="result-card">
            <div class="pony-name {pony_class}">{prediksi}</div>
            <div class="pony-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Progress bar + tingkat keyakinan
    st.progress(presentase)
    st.success(f"Tingkat keyakinan: {presentase*100:.2f}%")

    # Efek tambahan
    st.snow()
    st.balloons()

# Sidebar
st.sidebar.title("Tentang Quiz")
st.sidebar.info("Quiz ini dibuat untuk seru-seruan ✨. Jawabanmu akan dibandingkan dengan kepribadian karakter di My Little Pony 🦄.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:14px;'>🌸 Dibuat dengan ❤️ oleh Aydes 🌸</p>", unsafe_allow_html=True)
