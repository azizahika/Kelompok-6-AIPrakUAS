import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Data penyakit dan gejala
penyakit_gejala = {
    'autisme': [
        'kesulitan berkomunikasi', 
        'gangguan interaksi sosial', 
        'perilaku repetitif', 
        'persepsi sensorik yang tidak biasa', 
        'kesulitan beradaptasi dengan perubahan rutinitas'
    ],
    'asperger': [
        'kesulitan dalam interaksi sosial', 
        'perilaku repetitif', 
        'minat yang terbatas atau obsesif', 
        'kesulitan dalam komunikasi nonverbal', 
        'keterampilan motorik yang terlambat'
    ],
    'pdd-nos': [
        'keterlambatan bahasa', 
        'interaksi sosial yang aneh atau tidak pantas', 
        'perilaku repetitif atau stereotip', 
        'masalah dalam perubahan rutinitas', 
        'keterlambatan perkembangan'
    ],
    'rett': [
        'kehilangan keterampilan motorik', 
        'masalah koordinasi', 
        'kehilangan kemampuan bahasa', 
        'masalah pernapasan', 
        'keterlambatan pertumbuhan kepala'
    ],
    'cdd': [
        'kehilangan kemampuan bahasa', 
        'kehilangan keterampilan sosial', 
        'kehilangan kontrol kandung kemih atau usus', 
        'kehilangan keterampilan bermain', 
        'perilaku stereotip'
    ],
    'spd': [
        'hipersensitivitas terhadap rangsangan sensorik', 
        'hipo-sensitivitas terhadap rangsangan sensorik', 
        'kesulitan mengkoordinasikan gerakan', 
        'masalah dalam fokus dan perhatian', 
        'perilaku pencari sensasi'
    ]
}

# Pertanyaan dasar
pertanyaan_list_tambahan = [
    ("Apakah anak Anda pernah mengalami kesulitan dalam bergaul dengan teman sebayanya?", 'kesulitan dalam bergaul dengan teman sebayanya'),
    ("Apakah anak Anda sering terlihat cemas atau khawatir berlebihan?", 'sering cemas atau khawatir berlebihan'),
    ("Apakah anak Anda memiliki kesulitan dalam berkonsentrasi atau menyelesaikan tugas?", 'kesulitan berkonsentrasi atau menyelesaikan tugas'),
    ("Apakah anak Anda sering merasa sedih atau murung tanpa alasan yang jelas?", 'sering merasa sedih atau murung tanpa alasan yang jelas'),
    ("Apakah anak Anda pernah mengalami perubahan besar dalam pola makan atau tidur?", 'perubahan besar dalam pola makan atau tidur'),
    ("Apakah anak Anda sering menunjukkan perilaku yang impulsif atau sulit dikendalikan?", 'perilaku impulsif atau sulit dikendalikan'),
    ("Apakah anak Anda pernah berbicara tentang atau mencoba melukai dirinya sendiri?", 'berbicara tentang atau mencoba melukai dirinya sendiri'),
    ("Apakah anak Anda pernah mengalami trauma atau peristiwa yang sangat menakutkan?", 'mengalami trauma atau peristiwa menakutkan'),
    ("Apakah anak Anda merasa sulit untuk mengikuti aturan atau instruksi di rumah atau sekolah?", 'merasa sulit mengikuti aturan atau instruksi'),
    ("Apakah anak Anda sering menunjukkan perilaku agresif terhadap orang lain?", 'perilaku agresif terhadap orang lain'),
    ("Apakah anak Anda tampak sangat terganggu oleh perubahan rutinitas atau lingkungan?", 'terganggu oleh perubahan rutinitas atau lingkungan'),
    ("Apakah anak Anda sering mengeluh tentang masalah fisik (seperti sakit kepala atau sakit perut) tanpa penyebab medis yang jelas?", 'mengeluh tentang masalah fisik tanpa penyebab medis yang jelas'),
    ("Apakah anak Anda pernah mengalami masalah dengan penggunaan alkohol atau narkoba?", 'mengalami masalah dengan penggunaan alkohol atau narkoba'),
    ("Apakah anak Anda menunjukkan ketidakmampuan dalam memahami atau mengekspresikan emosi dengan tepat?", 'ketidakmampuan dalam memahami atau mengekspresikan emosi dengan tepat'),
    ("Apakah anak Anda sering menarik diri dari kegiatan yang sebelumnya dinikmati?", 'menarik diri dari kegiatan yang sebelumnya dinikmati'),
]

# Pertanyaan lanjutan
pertanyaan_list = [
    ("Apakah anak Anda memiliki kesulitan berkomunikasi?", 'kesulitan berkomunikasi'),
    ("Apakah anak Anda mengalami gangguan interaksi sosial?", 'gangguan interaksi sosial'),
    ("Apakah anak Anda menunjukkan perilaku repetitif?", 'perilaku repetitif'),
    ("Apakah anak Anda memiliki persepsi sensorik yang tidak biasa?", 'persepsi sensorik yang tidak biasa'),
    ("Apakah anak Anda kesulitan beradaptasi dengan perubahan rutinitas?", 'kesulitan beradaptasi dengan perubahan rutinitas'),
    ("Apakah anak Anda mengalami kesulitan dalam interaksi sosial?", 'kesulitan dalam interaksi sosial'),
    ("Apakah anak Anda memiliki minat yang terbatas atau obsesif?", 'minat yang terbatas atau obsesif'),
    ("Apakah anak Anda mengalami kesulitan dalam komunikasi nonverbal?", 'kesulitan dalam komunikasi nonverbal'),
    ("Apakah anak Anda mengalami keterlambatan keterampilan motorik?", 'keterampilan motorik yang terlambat'),
    ("Apakah anak Anda mengalami keterlambatan bahasa?", 'keterlambatan bahasa'),
    ("Apakah anak Anda menunjukkan interaksi sosial yang aneh atau tidak pantas?", 'interaksi sosial yang aneh atau tidak pantas'),
    ("Apakah anak Anda mengalami perilaku repetitif atau stereotip?", 'perilaku repetitif atau stereotip'),
    ("Apakah anak Anda mengalami masalah dalam perubahan rutinitas?", 'masalah dalam perubahan rutinitas'),
    ("Apakah anak Anda mengalami keterlambatan perkembangan?", 'keterlambatan perkembangan'),
    ("Apakah anak Anda mengalami kehilangan keterampilan motorik?", 'kehilangan keterampilan motorik'),
    ("Apakah anak Anda mengalami masalah koordinasi?", 'masalah koordinasi'),
    ("Apakah anak Anda mengalami kehilangan kemampuan bahasa?", 'kehilangan kemampuan bahasa'),
    ("Apakah anak Anda mengalami masalah pernapasan?", 'masalah pernapasan'),
    ("Apakah anak Anda mengalami keterlambatan pertumbuhan kepala?", 'keterlambatan pertumbuhan kepala'),
    ("Apakah anak Anda mengalami kehilangan keterampilan sosial?", 'kehilangan keterampilan sosial'),
    ("Apakah anak Anda mengalami kehilangan kontrol kandung kemih atau usus?", 'kehilangan kontrol kandung kemih atau usus'),
    ("Apakah anak Anda mengalami kehilangan keterampilan bermain?", 'kehilangan keterampilan bermain'),
    ("Apakah anak Anda menunjukkan perilaku stereotip?", 'perilaku stereotip'),
    ("Apakah anak Anda mengalami hipersensitivitas terhadap rangsangan sensorik?", 'hipersensitivitas terhadap rangsangan sensorik'),
    ("Apakah anak Anda mengalami hipo-sensitivitas terhadap rangsangan sensorik?", 'hipo-sensitivitas terhadap rangsangan sensorik'),
    ("Apakah anak Anda mengalami kesulitan mengkoordinasikan gerakan?", 'kesulitan mengkoordinasikan gerakan'),
    ("Apakah anak Anda mengalami masalah dalam fokus dan perhatian?", 'masalah dalam fokus dan perhatian'),
    ("Apakah anak Anda menunjukkan perilaku pencari sensasi?", 'perilaku pencari sensasi')
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pertanyaan_dasar')
def pertanyaan_dasar():
    return render_template('dasar.html', pertanyaan_list=pertanyaan_list_tambahan, enumerate=enumerate)

@app.route('/hasil2', methods=['POST'])
def hasil2():
    total_pertanyaan = len(pertanyaan_list_tambahan)
    jumlah_ya = 0
    for i in range(total_pertanyaan):
        jawaban = request.form.get(f'jawaban{i}')
        if jawaban == 'ya':
            jumlah_ya += 1

    presentase_ya = (jumlah_ya / total_pertanyaan) * 100

    if presentase_ya > 70:
        return redirect(url_for('pemeriksaan_lanjutan'))
    else:
        hasil_diagnosa = "Berdasarkan hasil jawaban yang Anda berikan:"
        if presentase_ya > 50:
            hasil_diagnosa += " Kecenderungan ada beberapa indikasi untuk mempertimbangkan konsultasi lebih lanjut."
        else:
            hasil_diagnosa += " Tidak terlihat ada indikasi yang signifikan untuk konsultasi saat ini."
        
        return render_template('hasil2.html', presentase_ya=presentase_ya, hasil_diagnosa=hasil_diagnosa)

@app.route('/pemeriksaan_lanjutan')
def pemeriksaan_lanjutan():
    return render_template('lanjutan.html', pertanyaan_list=pertanyaan_list, enumerate=enumerate)

@app.route('/hasil', methods=['POST'])
def hasil():
    jawaban = {}
    for i in range(len(pertanyaan_list)):
        jawab = request.form.get(f'jawaban{i}')
        gejala_name = pertanyaan_list[i][1]
        jawaban[gejala_name] = jawab == 'super yakin'

    # Diagnosa berdasarkan gejala
    diagnosa_result = []
    for penyakit, gejala_list in penyakit_gejala.items():
        if any(jawaban.get(gejala) for gejala in gejala_list):
            diagnosa_result.append(penyakit)

    hasil_diagnosa = "Berdasarkan jawaban yang Anda berikan, anak Anda memiliki kemungkinan mengalami beberapa gangguan berikut:\n"
    if diagnosa_result:
        hasil_diagnosa += ", ".join(set(diagnosa_result))
    else:
        hasil_diagnosa += "tidak ada gangguan yang terdeteksi dengan gejala yang diberikan."

    # Generate bar chart
    labels = ['Autisme', 'Asperger', 'PDD-NOS', 'Rett', 'CDD']
    sizes = [0] * 5
    for i, (penyakit, gejala_list) in enumerate(penyakit_gejala.items()):
        if i < 5:  # Hanya proses lima penyakit pertama
            if penyakit in diagnosa_result:
                presentase = (len([gejala for gejala in gejala_list if jawaban.get(gejala)]) / len(gejala_list)) * 100
                labels[i] = f'Gejala {penyakit.capitalize()}'
                sizes[i] = presentase
    
    fig, ax = plt.subplots()
    ax.bar(labels, sizes, color=['gold', 'lightcoral', 'lightblue', 'lightgreen', 'lightskyblue'])
    ax.set_ylabel('Presentase (%)')
    ax.set_title('Presentase Gejala Terdeteksi')

    # Save it to a temporary buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    # Embed the result in the html output
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return render_template('hasil.html', hasil_diagnosa=hasil_diagnosa, chart=uri)

if __name__ == '__main__':
    app.run(debug=True)
