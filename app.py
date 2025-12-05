import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Konfigurasi dan Setup Halaman ---
st.set_page_config(
    page_title="Pusat Komando 5-D: Prioritas Bencana Sumbar",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 PUSAT KOMANDO 5-D: PRIORITAS BENCANA SUMBAR")
st.markdown("### DATA DIMENSI: Transformasi Data Harian menjadi Keputusan Cepat Tanggap")
st.divider()

# --- Data Simulasi LENGKAP (Menggabungkan Data Harian dari Power BI) ---
# Data Dasar
data_base = {
    'Kabupaten_Kota': ['Lima Puluh Kota', 'Agam', 'Pesisir Selatan', 'Padang Pariaman', 'Tanah Datar', 'Kota Padang', 'Solok', 'Sawah Lunto', 'Bukittinggi', 'Mentawai'],
    'Jenis_Bencana': ['Banjir Bandang', 'Tanah Longsor', 'Banjir', 'Banjir Bandang', 'Tanah Longsor', 'Banjir', 'Banjir Bandang', 'Banjir', 'Tanah Longsor', 'Banjir'],
    'Total_Mengungsi': [6600, 5700, 5200, 4800, 3500, 3000, 2000, 1800, 1500, 1900],
    'Total_Meninggal': [18, 15, 6, 8, 4, 3, 2, 0, 1, 0],
    'Kerugian_Rupiah_Miliar': [39.0, 30.0, 30.0, 26.0, 22.0, 10.0, 5.0, 3.0, 5.0, 3.0],
    'Jembatan_Rusak': [4, 2, 1, 3, 1, 0, 1, 0, 0, 1],
    'Sekolah_Rusak': [10, 8, 5, 4, 3, 2, 1, 1, 1, 0],
    'Rumah_Rusak_Berat': [15, 12, 8, 11, 6, 3, 2, 1, 1, 0]
}
df_base = pd.DataFrame(data_base)

# Data Harian (Dibuat berdasarkan visualisasi Power BI Day 25-30)
data_harian = {
    'Day': list(range(25, 31)),
    'Total_Kerugian_Day': [23.0, 36.5, 32.0, 35.0, 37.5, 31.5], # Miliar
    'Total_Mengungsi_Day': [12000, 15000, 18000, 25000, 30000, 36000], # Simulasi kumulatif
    'Total_Meninggal_Day': [10, 15, 25, 35, 45, 57] # Simulasi kumulatif
}
df_harian = pd.DataFrame(data_harian)


# --- Sidebar untuk Filter ---
st.sidebar.header("⚙️ Filter Fokus Data")

# Filter Tanggal (Simulasi Waktu Kritis)
selected_day = st.sidebar.select_slider(
    "Simulasi Waktu Kritis (Hari ke-)",
    options=df_harian['Day'].unique(),
    value=30, # Default hari terakhir
    help="Geser untuk melihat metrik pada hari tertentu (misal: Hari 30 adalah data akhir)."
)

# Filter Kabupaten/Kota dan Bencana
kabupaten_options = ['Semua Wilayah'] + sorted(df_base['Kabupaten_Kota'].unique())
selected_kabupaten = st.sidebar.selectbox(
    "Pilih Wilayah Fokus:",
    kabupaten_options
)

bencana_options = ['Semua Jenis Bencana'] + sorted(df_base['Jenis_Bencana'].unique())
selected_bencana = st.sidebar.selectbox(
    "Pilih Tipe Bencana:",
    bencana_options
)

# Menerapkan Filter (Hanya filter non-harian yang diterapkan pada data base)
df_filtered = df_base.copy()
if selected_kabupaten != 'Semua Wilayah':
    df_filtered = df_filtered[df_filtered['Kabupaten_Kota'] == selected_kabupaten]
if selected_bencana != 'Semua Jenis Bencana':
    df_filtered = df_filtered[df_filtered['Jenis_Bencana'] == selected_bencana]

# --- Metrik Utama Harian (Disajikan sebagai ringkasan) ---
day_data = df_harian[df_harian['Day'] == selected_day].iloc[0]
kerugian_harian = day_data['Total_Kerugian_Day']
mengungsi_harian = day_data['Total_Mengungsi_Day']
meninggal_harian = day_data['Total_Meninggal_Day']

st.header(f"🎯 Metrik Kritis Hari ke-{selected_day} (Pembaruan Real-Time)")
col1, col2, col3 = st.columns(3)

# Metrik Pengungsi (Status Kemanusiaan)
col1.metric(
    "Total Pengungsi Kumulatif",
    f"{mengungsi_harian:,} Jiwa",
    delta=f"Hari ini: +{(df_harian[df_harian['Day'] == selected_day]['Total_Mengungsi_Day'].values[0] - df_harian[df_harian['Day'] == selected_day - 1]['Total_Mengungsi_Day'].values[0] if selected_day > 25 else mengungsi_harian):,} Jiwa",
    delta_color="inverse"
)

# Metrik Kerugian (Status Finansial)
col2.metric(
    "Total Kerugian Kumulatif",
    f"Rp {kerugian_harian:.1f} Miliar",
    delta=f"Peningkatan Kerugian: Rp {kerugian_harian / 30 * 10:.1f} Juta/Jam (Est.)", # Simulasi dampak
    delta_color="inverse"
)

# Metrik Korban Jiwa
col3.metric(
    "Total Korban Meninggal",
    f"{meninggal_harian} Jiwa",
    delta=f"Sejak Hari ke-{selected_day-1}: +{(df_harian[df_harian['Day'] == selected_day]['Total_Meninggal_Day'].values[0] - df_harian[df_harian['Day'] == selected_day - 1]['Total_Meninggal_Day'].values[0] if selected_day > 25 else meninggal_harian)} Jiwa",
    delta_color="inverse"
)

# --- 5 Tabs Logis (Sesuai Fase Analisis) ---
tab_r, tab_k, tab_kr, tab_i, tab_p = st.tabs(
    ["1. RINGKASAN EKSEKUTIF", "2. DAMPAK KORBAN JIWA", "3. ANALISIS KERUGIAN", "4. KERUSAKAN INFRASTRUKTUR", "5. PRIORITAS & REKOMENDASI"]
)

with tab_r:
    st.header("Ringkasan Situasi Kritis")
    st.info("🎯 **ANALISIS CEPAT:** Metrik menunjukkan eskalasi dampak yang cepat. Fokus harus pada Lima Puluh Kota, yang dominan dalam semua kategori kerugian.")
    
    # Visual 1.1: Grafik Garis Kerugian Harian (Diambil dari Power BI)
    st.subheader("Tren Kerugian Harian (Rp Miliar)")
    fig_r1 = px.area(
        df_harian,
        x='Day',
        y='Total_Kerugian_Day',
        title='Perkembangan Kerugian Finansial per Hari (Day 25-30)',
        labels={'Day': 'Hari ke-', 'Total_Kerugian_Day': 'Kerugian (Miliar Rupiah)'},
        line_shape='spline',
        color_discrete_sequence=['#E45756']
    )
    fig_r1.add_vline(x=selected_day, line_width=2, line_dash="dash", line_color="orange", annotation_text=f"Hari ke-{selected_day}")
    st.plotly_chart(fig_r1, use_container_width=True)

    # Visual 1.2: Total Kerusakan Unit (Diambil dari Power BI)
    st.subheader("Proporsi Kerusakan Rumah Berdasarkan Tingkat Keparahan")
    
    # Data proporsi dari Power BI: Rusak Berat 78.29%, Sedang 4.65%, Ringan 17.06%
    df_rusak = pd.DataFrame({
        'Kategori': ['Rusak Berat', 'Rusak Ringan', 'Rusak Sedang'],
        'Persentase': [78.29, 17.06, 4.65]
    })

    fig_r2 = px.pie(
        df_rusak,
        names='Kategori',
        values='Persentase',
        title='Persentase Kerusakan Rumah (Fokus pada Kebutuhan Hunian Darurat)',
        hole=.4,
        color='Kategori',
        color_discrete_map={'Rusak Berat': '#E45756', 'Rusak Ringan': '#F58518', 'Rusak Sedang': '#4C78A8'}
    )
    st.plotly_chart(fig_r2, use_container_width=True)


with tab_k:
    st.header("Analisis Dampak Korban Jiwa (Kemanusiaan)")
    st.info("🎯 **ANALISIS CEPAT:** Banjir Bandang dan Banjir menelan korban jiwa terbesar. Prioritaskan evakuasi dan pencarian di wilayah yang terdampak tipe bencana ini (Lima Puluh Kota dan Agam).")

    # Visual 2.1: Total Meninggal berdasarkan Jenis Bencana dan Kabupaten (Stacked Bar dari Power BI)
    st.subheader("Dampak Kematian Berdasarkan Jenis Bencana dan Wilayah")
    
    # Menghitung Total Meninggal per Jenis Bencana
    df_korban = df_filtered.groupby(['Jenis_Bencana', 'Kabupaten_Kota'])['Total_Meninggal'].sum().reset_index()

    fig_k1 = px.bar(
        df_korban,
        x='Jenis_Bencana',
        y='Total_Meninggal',
        color='Kabupaten_Kota',
        title='Total Korban Meninggal Berdasarkan Jenis Bencana',
        labels={'Total_Meninggal': 'Jumlah Korban Meninggal', 'Jenis_Bencana': 'Tipe Bencana'},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_k1, use_container_width=True)
    
    # Visual 2.2: Gap Pemulihan Korban Jiwa (Waterfall Chart dari Power BI)
    st.subheader("Target Pemulihan: Mengatasi Kesenjangan Pengungsi (Korban Jiwa)")

    # Data Gap Pemulihan (Simulasi dari Power BI, 35.5K)
    df_gap = pd.DataFrame(data={
        "Jenis_Bencana": ["Banjir Bandang", "Banjir", "Tanah Longsor", "Total"],
        "Mengungsi": [13.7, 12.9, 8.9, 35.5], # Disederhanakan dari K (ribu)
    })
    
    fig_k2 = go.Figure(go.Waterfall(
        name = "Gap Pemulihan", 
        orientation = "v",
        measure = ["relative"] * 3 + ["total"],
        x = df_gap['Jenis_Bencana'],
        textposition = "outside",
        text = [f"{m}K" for m in df_gap['Mengungsi']],
        y = df_gap['Mengungsi'],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        increasing = {"marker":{"color":"#17B855"}}, # Hijau untuk peningkatan (relatif)
        totals = {"marker":{"color":"#4C78A8"}} # Biru untuk total
    ))

    fig_k2.update_layout(
        title = "Kontribusi Jenis Bencana Terhadap Total Pengungsi (35.500 Jiwa)",
        showlegend = False
    )
    st.plotly_chart(fig_k2, use_container_width=True)


with tab_kr:
    st.header("Analisis Kerugian Finansial (Rp Miliar)")
    st.info("🎯 **ANALISIS CEPAT:** Total kerugian didominasi oleh Banjir Bandang dan Banjir. Lima Puluh Kota adalah sumber kerugian finansial terbesar. Segera lakukan audit di sana.")

    # Visual 3.1: Perbandingan Kerugian Berdasarkan Tipe Bencana (Bar Chart dari Power BI)
    st.subheader("Total Kerugian Berdasarkan Jenis Bencana")
    df_kerugian_type = df_filtered.groupby('Jenis_Bencana')['Kerugian_Rupiah_Miliar'].sum().reset_index()

    fig_kr1 = px.bar(
        df_kerugian_type,
        x='Jenis_Bencana',
        y='Kerugian_Rupiah_Miliar',
        title='Kerugian Terdorong oleh Faktor Hidrologis (Banjir)',
        labels={'Kerugian_Rupiah_Miliar': 'Kerugian (Miliar Rupiah)', 'Jenis_Bencana': 'Tipe Bencana'},
        color='Kerugian_Rupiah_Miliar',
        color_continuous_scale=px.colors.sequential.Purples_r
    )
    st.plotly_chart(fig_kr1, use_container_width=True)

    # Visual 3.2: Scatter Plot Kerugian vs Mengungsi (Diambil dari Power BI)
    st.subheader("Korelasi Kerugian Finansial vs. Jumlah Pengungsi")

    df_kerugian_scatter = df_filtered.groupby('Kabupaten_Kota').agg({
        'Total_Mengungsi': 'sum',
        'Kerugian_Rupiah_Miliar': 'sum'
    }).reset_index()

    fig_kr2 = px.scatter(
        df_kerugian_scatter,
        x='Total_Mengungsi',
        y='Kerugian_Rupiah_Miliar',
        size='Kerugian_Rupiah_Miliar',
        color='Kabupaten_Kota',
        hover_name='Kabupaten_Kota',
        title='Wilayah Zona Merah (High Cost, High Human Impact)',
        labels={'Kerugian_Rupiah_Miliar': 'Kerugian (Miliar Rupiah)', 'Total_Mengungsi': 'Jumlah Pengungsi (Jiwa)'}
    )
    st.plotly_chart(fig_kr2, use_container_width=True)


with tab_i:
    st.header("Analisis Kerusakan Aset Kritis (Infrastruktur)")
    st.info("🎯 **ANALISIS CEPAT:** Jembatan (Akses Logistik) dan Sekolah (Masa Depan Generasi) adalah aset yang paling banyak rusak. Lima Puluh Kota memimpin dalam kedua kategori ini, membutuhkan alokasi dana rekonstruksi segera.")

    # Visual 4.1: Total Jembatan Rusak dan Rumah Rusak Berat (Bar Grouped dari Power BI)
    st.subheader("Fokus: Jembatan (Akses) vs. Rumah Rusak Berat (Hunian)")
    
    df_infrastruktur_1 = df_filtered.groupby('Kabupaten_Kota').agg({
        'Jembatan_Rusak': 'sum',
        'Rumah_Rusak_Berat': 'sum'
    }).reset_index().sort_values(by='Jembatan_Rusak', ascending=False).head(10)

    fig_i1 = go.Figure(data=[
        go.Bar(name='Jembatan Rusak', x=df_infrastruktur_1['Kabupaten_Kota'], y=df_infrastruktur_1['Jembatan_Rusak'], marker_color='#4C78A8'),
        go.Bar(name='Rumah Rusak Berat', x=df_infrastruktur_1['Kabupaten_Kota'], y=df_infrastruktur_1['Rumah_Rusak_Berat'], marker_color='#E45756')
    ])
    fig_i1.update_layout(
        barmode='group',
        title='Aset Paling Vital yang Rusak (Dampak Jangka Panjang)',
        xaxis_title="Wilayah",
        yaxis_title="Jumlah Unit Rusak"
    )
    st.plotly_chart(fig_i1, use_container_width=True)

    # Visual 4.2: Proporsi Sekolah vs Fasilitas Kesehatan (Stacked Bar dari Power BI)
    st.subheader("Proporsi Kerusakan Sekolah dan Fasilitas Kesehatan")

    # Data Proporsi dari Power BI (Simulasi Proporsi)
    df_infrastruktur_2 = df_filtered.groupby('Kabupaten_Kota').agg({
        'Sekolah_Rusak': 'sum',
        # Asumsikan Fasilitas Kesehatan Rusak adalah 28% dari Total Sekolah Rusak untuk simulasi data
        'Fasilitas_Kesehatan_Rusak': lambda x: (x.sum() * 0.28).astype(int) 
    }).reset_index()

    fig_i2 = px.bar(
        df_infrastruktur_2.melt(id_vars='Kabupaten_Kota', var_name='Tipe_Fasilitas', value_name='Jumlah_Rusak'),
        x='Kabupaten_Kota',
        y='Jumlah_Rusak',
        color='Tipe_Fasilitas',
        title='Kerusakan Fasilitas Umum (Pendidikan vs. Kesehatan)',
        labels={'Jumlah_Rusak': 'Jumlah Unit Rusak'},
        color_discrete_sequence=['#F58518', '#A0CBE8']
    )
    st.plotly_chart(fig_i2, use_container_width=True)


with tab_p:
    st.header("Prioritas Utama & Rekomendasi Tindakan (The Action)")
    st.info("🎯 **TUJUAN:** Menentukan Wilayah dan Sektor yang paling membutuhkan intervensi berdasarkan analisis 4 tab sebelumnya.")

    # Menentukan Rekomendasi berdasarkan kerugian gabungan
    df_rank = df_base.groupby('Kabupaten_Kota').agg({
        'Kerugian_Rupiah_Miliar': 'sum',
        'Total_Mengungsi': 'sum'
    }).mean(axis=1).sort_values(ascending=False).index[0] # Ambil rata-rata skor kerugian dan korban

    st.success(f"## 🏆 PRIORITAS INTERVENSI UTAMA: {df_rank.upper()}")
    st.caption("Wilayah ini memiliki skor gabungan tertinggi antara dampak kemanusiaan (korban) dan kerugian finansial.")

    st.markdown("---")
    
    st.subheader("Rekomendasi Tindakan Berdasarkan Sektor")
    col_p1, col_p2, col_p3 = st.columns(3)

    col_p1.metric(
        "Sektor #1: KEMANUSIAAN (Korban)",
        "Fokus Pengungsi & Rumah Rusak Berat",
        delta="Target: 78% rumah rusak berat harus ditangani dalam 90 hari.",
        delta_color="off"
    )
    col_p1.warning(
        f"""
        **TINDAKAN:** Kirim bantuan non-makanan (tenda, selimut, obat-obatan) ke **{df_rank}** dan **Agam**. Prioritaskan pendataan Rumah Rusak Berat untuk alokasi dana perbaikan darurat.
        """
    )
    
    col_p2.metric(
        "Sektor #2: LOGISTIK (Akses)",
        "Fokus Jembatan Rusak",
        delta="Target: Perbaikan 50% Jembatan vital dalam 60 hari.",
        delta_color="off"
    )
    col_p2.error(
        f"""
        **TINDAKAN:** Alokasikan tim dan dana tercepat untuk perbaikan **Jembatan Rusak** di **Lima Puluh Kota** (4 unit) dan **Padang Pariaman** (3 unit). Akses adalah kunci distribusi.
        """
    )

    col_p3.metric(
        "Sektor #3: MITIGASI (Pencegahan)",
        "Fokus Jenis Bencana",
        delta="Target: Mengurangi dampak Banjir Bandang dan Tanah Longsor.",
        delta_color="off"
    )
    col_p3.info(
        """
        **TINDAKAN:** Investasikan pada sistem peringatan dini (EWS) untuk **Banjir Bandang** di hulu sungai. Lakukan reboisasi di wilayah rawan **Tanah Longsor** (Agam).
        """
    )
