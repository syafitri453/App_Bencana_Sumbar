import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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
# Data Dasar (Disesuaikan agar lebih realistis dan sesuai visual Power BI)
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

# Data Harian (Day 25-30)
data_harian = {
    'Day': list(range(25, 31)),
    'Total_Kerugian_Day': [23.0, 36.5, 32.0, 35.0, 37.5, 39.0], # Disesuaikan agar total max = 39 Miliar
    'Total_Mengungsi_Day': [12000, 15000, 18000, 25000, 30000, 36000], 
    'Total_Meninggal_Day': [10, 15, 25, 35, 45, 57],
    'Total_Unit_Rusak_Harian': [190, 295, 245, 305, 303, 230] # Dari visual Power BI
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

# Menerapkan Filter pada data dasar
df_filtered = df_base.copy()
if selected_kabupaten != 'Semua Wilayah':
    df_filtered = df_filtered[df_filtered['Kabupaten_Kota'] == selected_kabupaten]
if selected_bencana != 'Semua Jenis Bencana':
    df_filtered = df_filtered[df_filtered['Jenis_Bencana'] == selected_bencana]

# LOGIKA METRIK BERDASARKAN FILTER TANGGAL
if selected_day == "Semua Hari (Total Kumulatif)":
    display_day_title = "Total Kumulatif Bencana"
    mengungsi_val = df_harian['Total_Mengungsi_Day'].max()
    meninggal_val = df_harian['Total_Meninggal_Day'].max()
    # Delta disesuaikan untuk mode total
    delta_mengungsi_text = f"Tren Harian Terakhir: +{(df_harian.iloc[-1]['Total_Mengungsi_Day'] - df_harian.iloc[-2]['Total_Mengungsi_Day']):,} Jiwa"
    delta_meninggal_text = f"Tren Harian Terakhir: +{(df_harian.iloc[-1]['Total_Meninggal_Day'] - df_harian.iloc[-2]['Total_Meninggal_Day'])} Jiwa"
    
else:
    # Jika Hari spesifik dipilih (Snapshot Harian)
    selected_day_int = int(selected_day)
    day_data = df_harian[df_harian['Day'] == selected_day_int].iloc[0]

st.header(f"🎯 Metrik Kritis Hari ke-{selected_day} (Pembaruan Real-Time)")
col1, col2, col3 = st.columns(3)

# Perhitungan Delta untuk visualisasi dramatis
prev_mengungsi = df_harian[df_harian['Day'] == selected_day - 1]['Total_Mengungsi_Day'].values[0] if selected_day > 25 else 0
delta_mengungsi = mengungsi_harian - prev_mengungsi

prev_meninggal = df_harian[df_harian['Day'] == selected_day - 1]['Total_Meninggal_Day'].values[0] if selected_day > 25 else 0
delta_meninggal = meninggal_harian - prev_meninggal


col1.metric(
    "Total Pengungsi Kumulatif",
    f"{mengungsi_harian:,} Jiwa",
    delta=f"Hari ini: +{delta_mengungsi:,} Jiwa",
    delta_color="inverse"
)

col2.metric(
    "Total Kerugian Kumulatif",
    f"Rp {df_base['Kerugian_Rupiah_Miliar'].sum():.1f} Miliar", # Mengambil total akhir
    delta=f"Update Harian: Rp {kerugian_harian:.1f} Miliar",
    delta_color="inverse"
)

col3.metric(
    "Total Korban Meninggal",
    f"{meninggal_harian} Jiwa",
    delta=f"Sejak Hari ke-{selected_day-1}: +{delta_meninggal} Jiwa",
    delta_color="inverse"
)

# --- 5 Tabs Logis (Sesuai Fase Analisis) ---
tab_r, tab_k, tab_kr, tab_i, tab_p = st.tabs(
    ["1. RINGKASAN EKSEKUTIF", "2. DAMPAK KORBAN JIWA", "3. ANALISIS KERUGIAN", "4. KERUSAKAN INFRASTRUKTUR", "5. PRIORITAS & REKOMENDASI"]
)

with tab_r:
    st.header("Ringkasan Situasi Kritis")
    st.info("🎯 **ANALISIS CEPAT:** Metrik menunjukkan eskalasi dampak yang cepat. Fokus harus pada Lima Puluh Kota, yang dominan dalam semua kategori kerugian.")
    
    # Visual 1.1: Grafik Garis Kerugian Harian
    st.subheader("Tren Kerugian Harian (Rp Miliar)")
    
    # Gabungkan 2 visual: Kerugian Harian dan Total Unit Rusak Harian
    fig_r1 = go.Figure()
    
    # Total Kerugian Harian
    fig_r1.add_trace(go.Scatter(
        x=df_harian['Day'],
        y=df_harian['Total_Kerugian_Day'],
        mode='lines+markers',
        name='Kerugian (Miliar Rp)',
        yaxis='y1',
        line=dict(color='#E45756')
    ))

    # Total Unit Rusak Harian (Visual yang ada di Power BI Anda)
    fig_r1.add_trace(go.Scatter(
        x=df_harian['Day'],
        y=df_harian['Total_Unit_Rusak_Harian'],
        mode='lines+markers',
        name='Total Unit Rusak',
        yaxis='y2',
        line=dict(color='#4C78A8', dash='dot')
    ))
    
    fig_r1.update_layout(
        title='Perkembangan Kerugian (Rp Miliar) vs. Total Unit Rusak Harian',
        xaxis_title="Hari ke-",
        yaxis=dict(title='Kerugian (Miliar Rp)', color='#E45756'),
        yaxis2=dict(title='Total Unit Rusak', overlaying='y', side='right', color='#4C78A8'),
        legend=dict(x=0.01, y=0.99)
    )

    st.plotly_chart(fig_r1, use_container_width=True)

    # Visual 1.2: Proporsi Kerusakan Rumah
    st.subheader("Proporsi Kerusakan Rumah Berdasarkan Tingkat Keparahan")
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
    st.info("🎯 **ANALISIS CEPAT:** Banjir Bandang dan Tanah Longsor adalah penyumbang korban jiwa terbesar. Prioritaskan evakuasi dan pencarian di wilayah yang terdampak tipe bencana ini.")

    # Visual 2.1: Total Meninggal berdasarkan Jenis Bencana dan Kabupaten
    st.subheader("Dampak Kematian Berdasarkan Jenis Bencana dan Wilayah")
    
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
    
    # Visual 2.2: Gap Pemulihan Korban Jiwa (Waterfall Chart)
    st.subheader("Target Pemulihan: Kontribusi Jenis Bencana Terhadap Total Pengungsi")

    df_gap = pd.DataFrame(data={
        "Jenis_Bencana": ["Banjir Bandang", "Banjir", "Tanah Longsor", "Total"],
        "Mengungsi_K": [13.7, 12.9, 8.9, 35.5], 
    })
    
    fig_k2 = go.Figure(go.Waterfall(
        name = "Gap Pemulihan", 
        orientation = "v",
        measure = ["relative"] * 3 + ["total"],
        x = df_gap['Jenis_Bencana'],
        textposition = "outside",
        text = [f"{m}K" for m in df_gap['Mengungsi_K']],
        y = df_gap['Mengungsi_K'],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        increasing = {"marker":{"color":"#17B855"}}, 
        totals = {"marker":{"color":"#4C78A8"}} 
    ))

    fig_k2.update_layout(
        title = "Kontribusi Jenis Bencana Terhadap Total Pengungsi (35.500 Jiwa)",
        showlegend = False
    )
    st.plotly_chart(fig_k2, use_container_width=True)


with tab_kr:
    st.header("Analisis Kerugian Finansial (Rp Miliar)")
    st.info("🎯 **ANALISIS CEPAT:** Total kerugian didominasi oleh Banjir Bandang (78 Miliar) dan Banjir (73 Miliar). Ini mengkonfirmasi prioritas mitigasi bencana hidrologis.")

    # Visual 3.1: Perbandingan Kerugian Berdasarkan Tipe Bencana (Bar Chart dari Power BI)
    st.subheader("Perbandingan Kerugian Berdasarkan Tipe Bencana")
    df_kerugian_type = pd.DataFrame({
        'Jenis_Bencana': ['Banjir Bandang', 'Banjir', 'Tanah Longsor'],
        'Total_Kerugian': [78.0, 73.0, 49.0]
    })

    fig_kr1 = px.bar(
        df_kerugian_type,
        x='Jenis_Bencana',
        y='Total_Kerugian',
        title='Kerugian Terdorong oleh Faktor Hidrologis',
        labels={'Total_Kerugian': 'Kerugian (Miliar Rupiah)', 'Jenis_Bencana': 'Tipe Bencana'},
        color='Total_Kerugian',
        color_continuous_scale=px.colors.sequential.Sunsetdark,
        text_auto='.1f'
    )
    st.plotly_chart(fig_kr1, use_container_width=True)

    # Visual 3.2: Ranking Total Kerugian by Kabupaten Kota (Mirip Peta Panas/Heatmap)
    st.subheader("Ranking Wilayah Berdasarkan Total Kerugian")
    
    df_ranking_kerugian = df_filtered.groupby('Kabupaten_Kota')['Kerugian_Rupiah_Miliar'].sum().reset_index().sort_values(by='Kerugian_Rupiah_Miliar', ascending=False)

    fig_kr2 = px.bar(
        df_ranking_kerugian,
        y='Kabupaten_Kota',
        x='Kerugian_Rupiah_Miliar',
        orientation='h',
        title='Wilayah Zona Merah (High Cost) - Total Kerugian Kumulatif',
        labels={'Kerugian_Rupiah_Miliar': 'Kerugian (Miliar Rupiah)', 'Kabupaten_Kota': 'Wilayah'},
        color='Kerugian_Rupiah_Miliar',
        color_continuous_scale=px.colors.sequential.Reds_r,
        text_auto='.1f'
    )
    fig_kr2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_kr2, use_container_width=True)


with tab_i:
    st.header("Analisis Kerusakan Aset Kritis (Infrastruktur)")
    st.info("🎯 **ANALISIS CEPAT:** Fokus pada infrastruktur. Terdapat 13 Jembatan dan 35 Sekolah rusak. Lima Puluh Kota (4 Jembatan, 10 Sekolah) adalah fokus utama untuk rekonstruksi.")

    # Visual 4.1: Total Jembatan Rusak dan Rumah Rusak Berat (Bar Grouped dari Power BI)
    st.subheader("Fokus: Jembatan (Akses) vs. Rumah Rusak Berat (Hunian)")
    
    df_infrastruktur_1 = df_filtered.groupby('Kabupaten_Kota').agg({
        'Jembatan_Rusak': 'sum',
        'Rumah_Rusak_Berat': 'sum'
    }).reset_index().sort_values(by='Jembatan_Rusak', ascending=False)

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

    # Data Proporsi - Dibuat terpisah agar tidak error
    df_proporsi_rusak = df_filtered.groupby('Kabupaten_Kota')['Sekolah_Rusak'].sum().reset_index()
    df_proporsi_rusak['Fasilitas_Kesehatan_Rusak'] = (df_proporsi_rusak['Sekolah_Rusak'] * 0.28).astype(int) # Simulasi Aman
    
    df_proporsi_rusak_melt = df_proporsi_rusak.melt(id_vars='Kabupaten_Kota', var_name='Tipe_Fasilitas', value_name='Jumlah_Rusak')

    fig_i2 = px.bar(
        df_proporsi_rusak_melt,
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
    st.info("🎯 **TUJUAN:** Menentukan Wilayah dan Sektor yang paling membutuhkan intervensi berdasarkan analisis data, didukung oleh visualisasi Gap Pemulihan.")

    # Menentukan Rekomendasi berdasarkan kerugian gabungan
    df_base['Prioritas_Skor'] = df_base['Kerugian_Rupiah_Miliar'] + (df_base['Total_Mengungsi'] / 1000)
    top_priority_kab = df_base.sort_values(by='Prioritas_Skor', ascending=False).iloc[0]['Kabupaten_Kota']

    st.success(f"## 🏆 PRIORITAS INTERVENSI UTAMA: {top_priority_kab.upper()}")
    st.caption("Wilayah ini memiliki skor gabungan tertinggi antara dampak kemanusiaan (korban) dan kerugian finansial.")

    st.markdown("---")
    
    st.subheader("Rekomendasi Tindakan Berdasarkan Sektor")
    col_p1, col_p2, col_p3 = st.columns(3)

    col_p1.metric(
        "Sektor #1: KEMANUSIAAN (Korban)",
        "Fokus Pengungsi & Rumah Rusak Berat",
        delta="Target: Penanganan 78% rumah rusak berat harus ditangani dalam 90 hari.",
        delta_color="off"
    )
    col_p1.warning(
        f"""
        **TINDAKAN:** Kirim bantuan non-makanan (tenda, selimut, obat-obatan) ke **{top_priority_kab}** dan **Agam**. Prioritaskan pendataan Rumah Rusak Berat untuk alokasi dana perbaikan darurat.
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
        **TINDAKAN:** Alokasikan tim dan dana tercepat untuk perbaikan **Jembatan Rusak** di **{top_priority_kab}** (4 unit) dan **Padang Pariaman** (3 unit). Akses adalah kunci distribusi.
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
        **TINDAKAN:** Investasikan pada sistem peringatan dini (EWS) untuk **Banjir Bandang** di hulu sungai. Lakukan reboisasi di wilayah rawan **Tanah Longsor** (Agam dan Pesisir Selatan).
        """
    )
