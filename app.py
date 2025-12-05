import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Judul dan Konfigurasi Aplikasi (Diperbarui untuk tampilan modern) ---
st.set_page_config(
    page_title="Pusat Komando Digital: Prioritas Bencana Sumbar",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚨 Pusat Komando Digital: Prioritas Bencana Sumatra Barat")
st.markdown("### Alat Bantu Keputusan Cepat Tanggap Bencana Berbasis Data")
st.divider()

# --- Data Simulasi (Konsisten dengan Temuan Power BI) ---
data = {
    'Kabupaten_Kota': ['Lima Puluh Kota', 'Agam', 'Pesisir Selatan', 'Padang Pariaman', 'Tanah Datar', 'Kota Padang', 'Solok', 'Sawah Lunto', 'Bukittinggi', 'Mentawai'],
    'Jenis_Bencana': ['Banjir Bandang', 'Tanah Longsor', 'Banjir', 'Banjir Bandang', 'Tanah Longsor', 'Banjir', 'Banjir Bandang', 'Banjir', 'Tanah Longsor', 'Banjir'],
    'Total_Mengungsi': [6600, 5700, 5200, 4800, 3500, 3000, 2000, 1800, 1500, 1900],
    'Total_Meninggal': [18, 15, 6, 8, 4, 3, 2, 0, 1, 0],
    'Kerugian_Rupiah_Miliar': [39.0, 30.0, 30.0, 26.0, 22.0, 10.0, 5.0, 3.0, 5.0, 3.0],
    'Jembatan_Rusak': [4, 2, 1, 3, 1, 0, 1, 0, 0, 1],
    'Sekolah_Rusak': [10, 8, 5, 4, 3, 2, 1, 1, 1, 0],
    'Rumah_Rusak_Berat': [15, 12, 8, 11, 6, 3, 2, 1, 1, 0]
}
df = pd.DataFrame(data)

# --- Sidebar untuk Filter ---
st.sidebar.header("⚙️ Filter Bencana")

kabupaten_options = ['Semua'] + sorted(df['Kabupaten_Kota'].unique())
selected_kabupaten = st.sidebar.selectbox(
    "Pilih Wilayah Fokus:",
    kabupaten_options
)

bencana_options = ['Semua'] + sorted(df['Jenis_Bencana'].unique())
selected_bencana = st.sidebar.selectbox(
    "Pilih Tipe Bencana:",
    bencana_options
)

# Menerapkan Filter
df_filtered = df.copy()
if selected_kabupaten != 'Semua':
    df_filtered = df_filtered[df_filtered['Kabupaten_Kota'] == selected_kabupaten]
if selected_bencana != 'Semua':
    df_filtered = df_filtered[df_filtered['Jenis_Bencana'] == selected_bencana]

# --- Metrik Utama (Menggunakan Delta untuk Menarik Perhatian) ---
total_mengungsi = df_filtered['Total_Mengungsi'].sum()
total_kerugian = df_filtered['Kerugian_Rupiah_Miliar'].sum()
total_jembatan_rusak = df_filtered['Jembatan_Rusak'].sum()

st.header("🎯 Metrik Kritis Bencana (Skala Darurat)")
col1, col2, col3 = st.columns(3)

# Metrik Pengungsi (Status Kemanusiaan)
col1.metric(
    "Total Mengungsi (Jiwa)",
    f"{total_mengungsi:,}",
    delta=f"{total_mengungsi / 36000 * 100:.1f}% dari total pengungsi regional",
    delta_color="inverse" if total_mengungsi > 5000 else "normal"
)

# Metrik Kerugian (Status Finansial)
col2.metric(
    "Total Kerugian Finansial",
    f"Rp {total_kerugian:.1f} Miliar",
    delta=f"Rp {total_kerugian * 0.5:.1f} Miliar estimasi biaya logistik", # Simulasi dampak
    delta_color="inverse"
)

# Metrik Konektivitas (Status Akses)
col3.metric(
    "Jembatan Rusak Kritis",
    f"{total_jembatan_rusak} Unit",
    delta="Hambatan Logistik Utama",
    delta_color="inverse"
)

# --- Tabs untuk Struktur Analisis ---
tab1, tab2, tab3 = st.tabs(["🔥 HOTSPOT & PRIORITAS ZONA MERAH", "💰 ANALISIS BIAYA & KOMPOSISI", "🏗️ KERUSAKAN INFRASTRUKTUR"])

with tab1:
    st.header("Visualisasi Prioritas Tindakan (Priority Action Map)")
    st.markdown("Visualisasi ini memetakan kerentanan wilayah berdasarkan jumlah Pengungsi dan Kerugian Finansial.")

    # Visualisasi 1: Bubble Chart untuk Prioritas (Simulasi Peta Kritis)
    # Warna: Merah = Lebih banyak Pengungsi. Ukuran: Lebih besar Kerugian.
    df_hotspot = df.groupby('Kabupaten_Kota').agg({
        'Total_Mengungsi': 'sum',
        'Kerugian_Rupiah_Miliar': 'sum'
    }).reset_index()

    fig1 = px.scatter(
        df_hotspot,
        x='Kerugian_Rupiah_Miliar',
        y='Total_Mengungsi',
        size='Kerugian_Rupiah_Miliar',
        color='Total_Mengungsi',
        hover_name='Kabupaten_Kota',
        title='HOTSPOT: Korelasi Kerugian Finansial vs. Pengungsi',
        labels={
            'Kerugian_Rupiah_Miliar': 'Kerugian (Miliar Rupiah)',
            'Total_Mengungsi': 'Jumlah Pengungsi (Jiwa)'
        },
        color_continuous_scale=px.colors.sequential.Reds_r # Merah untuk kerentanan tinggi
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.warning("""
        **KESIMPULAN VISUAL ZONA MERAH:** Wilayah yang terletak di kuadran Kanan Atas (Kerugian & Pengungsi tinggi) seperti **Lima Puluh Kota** harus menjadi target intervensi utama.
    """)

with tab2:
    st.header("Analisis Sumber Biaya dan Kerugian")

    # Visualisasi 2: Komposisi Kerugian berdasarkan Jenis Bencana (Pie Chart)
    df_bencana_kerugian = df_filtered.groupby('Jenis_Bencana')['Kerugian_Rupiah_Miliar'].sum().reset_index()

    fig2 = px.pie(
        df_bencana_kerugian,
        names='Jenis_Bencana',
        values='Kerugian_Rupiah_Miliar',
        title='Distribusi Kerugian Finansial berdasarkan Jenis Bencana',
        hole=.4,
        color_discrete_sequence=px.colors.qualitative.T10
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Fokus: Banjir Bandang dan Banjir Biasa menyumbang kerugian terbesar, mengkonfirmasi perlunya mitigasi hidrologis.")

with tab3:
    st.header("Detil Kerusakan Aset Kritis (Jembatan & Sekolah)")

    # Visualisasi 3: Prioritas Rekonstruksi (Stacked Bar Chart)
    df_infrastruktur = df_filtered.groupby('Kabupaten_Kota').agg({
        'Jembatan_Rusak': 'sum',
        'Sekolah_Rusak': 'sum',
        'Rumah_Rusak_Berat': 'sum'
    }).reset_index()

    fig3 = go.Figure(data=[
        go.Bar(name='Jembatan Rusak', x=df_infrastruktur['Kabupaten_Kota'], y=df_infrastruktur['Jembatan_Rusak'], marker_color='#4C78A8'),
        go.Bar(name='Sekolah Rusak', x=df_infrastruktur['Kabupaten_Kota'], y=df_infrastruktur['Sekolah_Rusak'], marker_color='#E45756'),
        go.Bar(name='Rumah Rusak Berat', x=df_infrastruktur['Kabupaten_Kota'], y=df_infrastruktur['Rumah_Rusak_Berat'], marker_color='#F58518')
    ])
    fig3.update_layout(
        barmode='group',
        title='Perbandingan Kerusakan Aset Kritis (Akses, Pendidikan, Hunian)',
        xaxis_title="Wilayah",
        yaxis_title="Jumlah Unit Rusak"
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- Bagian Paling Penting: Call-to-Action yang Inspiratif ---
st.markdown("---")
st.header("🚀 TUJUAN APLIKASI: REKOMENDASI TINDAKAN UTAMA")

# Menentukan Rekomendasi berdasarkan filter (pilih kabupaten dengan kerugian tertinggi)
if selected_kabupaten == 'Semua':
    top_priority_kab = df_hotspot.sort_values(by='Kerugian_Rupiah_Miliar', ascending=False).iloc[0]['Kabupaten_Kota']
    rekomendasi_text = f"ANALISIS REGIONAL: Wilayah dengan dampak terparah dan prioritas intervensi adalah **{top_priority_kab}**."
else:
    rekomendasi_text = f"ANALISIS WILAYAH FOKUS: Rekomendasi tindakan difokuskan untuk **{selected_kabupaten}**."

st.success(f"## {rekomendasi_text}")

st.markdown("""
    Aplikasi ini diciptakan dengan tujuan tunggal: **Menyelamatkan Waktu dan Sumber Daya**.
    Setiap filter yang Anda gunakan menyajikan keputusan, bukan sekadar data.
""")

col_final_1, col_final_2 = st.columns(2)
col_final_1.info(
    "**TINDAKAN KEMANUSIAAN (Mengatasi 36.000 Pengungsi):** Prioritaskan pembangunan 50% hunian sementara dan sanitasi di zona merah untuk mengurangi beban pengungsi dalam 30 hari."
)
col_final_2.error(
    "**TINDAKAN REKONSTRUKSI (Mengatasi Hambatan Akses):** Segera alokasikan anggaran ke Lima Puluh Kota untuk perbaikan Jembatan Rusak. Kegagalan akses melumpuhkan distribusi bantuan."
)
