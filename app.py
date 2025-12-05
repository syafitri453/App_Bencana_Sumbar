import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Judul dan Konfigurasi Aplikasi ---
st.set_page_config(
    page_title="Pusat Komando 5-D: Analisis Bencana Sumbar Interaktif",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 PUSAT KOMANDO 5-D: ANALISIS DAMPAK BENCANA SUMATRA BARAT")
st.markdown("Visualisasi data komprehensif untuk mendukung keputusan strategis pasca-bencana.")
st.divider()

# --- Data Simulasi (Berdasarkan Temuan Power BI) ---
# Data Dasar (Agregat Wilayah)
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

# Data Harian (Untuk Metrik Dinamis dan Tren)
df_harian = pd.DataFrame({
    'Day': list(range(25, 31)),
    'Total_Kerugian_Day': [23.0, 36.5, 32.0, 35.0, 37.5, 39.0], 
    'Total_Mengungsi_Day': [12000, 15000, 18000, 25000, 30000, 36000], 
    'Total_Meninggal_Day': [10, 15, 25, 35, 45, 57],
    'Total_Unit_Rusak_Harian': [190, 295, 245, 305, 303, 230] 
})

# --- Sidebar untuk Filter ---
st.sidebar.header("⚙️ Filter Analisis")

# Filter Tanggal BARU: Menambahkan opsi "Semua Hari"
day_options = ["Semua Hari (Total Kumulatif)"] + sorted(df_harian['Day'].astype(str).tolist())
selected_day = st.sidebar.selectbox(
    "Fokus Waktu Kritis:",
    options=day_options,
    index=len(day_options) - 1, # Default ke Hari 30 (snapshot terakhir)
    help="Pilih 'Semua Hari' untuk melihat data total keseluruhan, atau pilih Hari ke-XX untuk melihat snapshot data harian."
)

# Filter Kabupaten/Kota
kabupaten_options = ['Semua'] + sorted(df_base['Kabupaten_Kota'].unique())
selected_kabupaten = st.sidebar.selectbox(
    "Pilih Kabupaten/Kota:",
    kabupaten_options
)

# Filter Jenis Bencana
bencana_options = ['Semua'] + sorted(df_base['Jenis_Bencana'].unique())
selected_bencana = st.sidebar.selectbox(
    "Pilih Jenis Bencana:",
    bencana_options
)

# Menerapkan Filter pada data agregat (df_base)
df_filtered = df_base.copy()
if selected_kabupaten != 'Semua':
    df_filtered = df_filtered[df_filtered['Kabupaten_Kota'] == selected_kabupaten]
if selected_bencana != 'Semua':
    df_filtered = df_filtered[df_filtered['Jenis_Bencana'] == selected_bencana]

# --- Metrik Utama DINAMIS (Dashboard Ringkasan Eksekutif) ---

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
    
    display_day_title = f"Snapshot Hari ke-{selected_day_int}"
    mengungsi_val = day_data['Total_Mengungsi_Day']
    meninggal_val = day_data['Total_Meninggal_Day']

    if selected_day_int > df_harian['Day'].min():
        prev_mengungsi = df_harian[df_harian['Day'] == selected_day_int - 1]['Total_Mengungsi_Day'].values[0]
        delta_mengungsi_text = f"Sejak Hari ke-{selected_day_int-1}: +{(mengungsi_val - prev_mengungsi):,} Jiwa"
        
        prev_meninggal = df_harian[df_harian['Day'] == selected_day_int - 1]['Total_Meninggal_Day'].values[0]
        delta_meninggal_text = f"Sejak Hari ke-{selected_day_int-1}: +{(meninggal_val - prev_meninggal)} Jiwa"
    else:
        delta_mengungsi_text = "Data Hari Awal"
        delta_meninggal_text = "Data Hari Awal"


st.header(f"1. Metrik Utama & Skala Dampak ({display_day_title})")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Mengungsi (Jiwa)", 
    f"{mengungsi_val:,} Jiwa",
    delta=delta_mengungsi_text,
    delta_color="inverse"
)
col2.metric("Total Meninggal", f"{meninggal_val} Jiwa", delta=delta_meninggal_text, delta_color="inverse")
col3.metric("Total Kerugian", f"Rp {df_filtered['Kerugian_Rupiah_Miliar'].sum():.1f} Miliar", help="Kerugian Finansial adalah nilai agregat (tidak berubah per hari).")
col4.metric("Total Unit Rusak Kritis", f"{df_filtered['Jembatan_Rusak'].sum() + df_filtered['Sekolah_Rusak'].sum()} Unit", help="Unit Rusak adalah nilai agregat (tidak berubah per hari).")
st.markdown("---")


# --- 5 Tabs Logis (Sesuai Struktur Awal) ---
tab_r, tab_k, tab_kr, tab_i, tab_p = st.tabs(
    ["2. RINGKASAN & TREN", "3. DAMPAK KORBAN JIWA", "4. ANALISIS KERUGIAN", "5. KERUSAKAN INFRASTRUKTUR", "6. PRIORITAS & REKOMENDASI"]
)

with tab_r:
    st.header("Ringkasan Situasi Kritis dan Tren Harian")
    st.info("🎯 **ANALISIS:** Metrik menunjukkan eskalasi dampak yang cepat. Bagian ini fokus pada tren harian dan ringkasan kerusakan utama.")
    
    # --- Visual 2.1: Grafik Garis Kerugian Harian (Vital untuk Tren) ---
    st.subheader("Tren Kerugian (Rp Miliar) dan Unit Rusak Harian")
    
    fig_r1 = go.Figure()
    
    fig_r1.add_trace(go.Scatter(
        x=df_harian['Day'],
        y=df_harian['Total_Kerugian_Day'],
        mode='lines+markers',
        name='Kerugian (Miliar Rp)',
        yaxis='y1',
        line=dict(color='#E45756')
    ))

    fig_r1.add_trace(go.Scatter(
        x=df_harian['Day'],
        y=df_harian['Total_Unit_Rusak_Harian'],
        mode='lines+markers',
        name='Total Unit Rusak Harian',
        yaxis='y2',
        line=dict(color='#4C78A8', dash='dot')
    ))
    
    fig_r1.update_layout(
        title='Perkembangan Kerugian vs. Total Unit Rusak Harian',
        xaxis_title="Hari ke-",
        yaxis=dict(title='Kerugian (Miliar Rp)', color='#E45756'),
        yaxis2=dict(title='Total Unit Rusak Harian', overlaying='y', side='right', color='#4C78A8'),
        legend=dict(x=0.01, y=0.99)
    )

    st.plotly_chart(fig_r1, use_container_width=True)

with tab_k:
    st.header("Hotspot Kemanusiaan: Pengungsi vs. Fatalitas")
    st.info("🎯 **ANALISIS CEPAT:** Fokus evakuasi dan pencarian di wilayah yang terdampak Banjir Bandang dan Tanah Longsor, yang merupakan penyumbang korban jiwa terbesar.")
    
    # --- Visual 2.2 (Dari Visualisasi 1 Sebelumnya): Ranking Pengungsi & Fatalitas ---
    df_group = df_filtered.groupby('Kabupaten_Kota').agg({
        'Total_Mengungsi': 'sum',
        'Total_Meninggal': 'sum'
    }).reset_index().sort_values(by='Total_Mengungsi', ascending=False)

    fig1 = px.bar(
        df_group,
        x='Kabupaten_Kota',
        y='Total_Mengungsi',
        title='Ranking Total Mengungsi Berdasarkan Kabupaten/Kota',
        labels={'Total_Mengungsi': 'Jumlah Pengungsi (Jiwa)', 'Kabupaten_Kota': 'Wilayah'},
        color='Total_Meninggal',
        color_continuous_scale=px.colors.sequential.Reds
    )
    fig1.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Analisis: Kabupaten dengan Pengungsi tertinggi (diwakili oleh ketinggian bar) sekaligus memiliki Fatalitas tinggi (diwakili oleh warna merah gelap) adalah Hotspot Ganda.")


with tab_kr:
    st.header("Komposisi Kerugian Finansial (Rp Miliar)")
    st.info("🎯 **ANALISIS CEPAT:** Total kerugian didominasi oleh Banjir Bandang dan Banjir. Ini mengkonfirmasi prioritas mitigasi bencana hidrologis.")

    # --- Visual 3.1 (Dari Visualisasi 2 Sebelumnya): Komposisi Kerugian ---
    # Menggunakan df_base agar persentase total tidak berubah saat filter kabupaten diterapkan
    df_bencana_kerugian = df_base.groupby('Jenis_Bencana')['Kerugian_Rupiah_Miliar'].sum().reset_index()

    fig2 = px.pie(
        df_bencana_kerugian,
        names='Jenis_Bencana',
        values='Kerugian_Rupiah_Miliar',
        title='Persentase Kerugian Rupiah berdasarkan Jenis Bencana (Total Sumbar)',
        hole=.3,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_traces(textinfo='percent+label', textfont_size=14)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Analisis: Data pie chart menunjukkan pemicu finansial terbesar, memandu alokasi anggaran mitigasi di masa depan.")


with tab_i:
    st.header("Prioritas Rekonstruksi: Kerusakan Infrastruktur Kritis")
    st.info("🎯 **ANALISIS CEPAT:** Fokus pada infrastruktur. Terdapat 13 Jembatan dan 35 Sekolah rusak. Lima Puluh Kota (4 Jembatan, 10 Sekolah) adalah fokus utama untuk rekonstruksi.")

    # --- Visual 4.1 (Dari Visualisasi 3 Sebelumnya): Jembatan vs. Sekolah ---
    df_infrastruktur = df_filtered.groupby('Kabupaten_Kota').agg({
        'Jembatan_Rusak': 'sum',
        'Sekolah_Rusak': 'sum'
    }).reset_index()

    fig3 = go.Figure(data=[
        go.Bar(
            name='Jembatan Rusak (Unit)',
            x=df_infrastruktur['Kabupaten_Kota'],
            y=df_infrastruktur['Jembatan_Rusak'],
            marker_color='rgb(31, 119, 180)'
        ),
        go.Bar(
            name='Sekolah Rusak (Unit)',
            x=df_infrastruktur['Kabupaten_Kota'],
            y=df_infrastruktur['Sekolah_Rusak'],
            marker_color='rgb(255, 127, 14)'
        )
    ])
    fig3.update_layout(
        barmode='group',
        title='Kerusakan Infrastruktur Kritis per Kabupaten/Kota',
        xaxis_title="Wilayah",
        yaxis_title="Jumlah Unit Rusak"
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Analisis: Visualisasi ini membandingkan dua aset kritis. Kerusakan Jembatan memutus konektivitas, sementara kerusakan Sekolah mengancam kelanjutan pendidikan.")


with tab_p:
    st.header("Insight Kritis dan Rekomendasi Tindakan")
    st.info("🎯 **TUJUAN:** Menentukan Wilayah dan Sektor yang paling membutuhkan intervensi berdasarkan skor prioritas gabungan.")

    # Menentukan prioritas gabungan berdasarkan data yang TIDAK DIFILTER oleh tanggal (agar rekomendasi selalu stabil)
    df_base['Prioritas_Skor'] = df_base['Kerugian_Rupiah_Miliar'] * 2 + (df_base['Total_Mengungsi'] / 1000)
    lima_puluh_kota_data = df_base[df_base['Kabupaten_Kota'] == 'Lima Puluh Kota'].iloc[0]

    st.success(f"""
        ## 🏆 PRIORITAS INTERVENSI UTAMA: {lima_puluh_kota_data['Kabupaten_Kota'].upper()}
        
        **Fakta Data Terkini (Fokus Tetap):**
        Wilayah ini secara konsisten menyumbang angka tertinggi dalam metrik:
        - **{lima_puluh_kota_data['Total_Mengungsi']:,}** Jiwa Mengungsi.
        - **{lima_puluh_kota_data['Jembatan_Rusak']}** Unit Jembatan Rusak.
        - **Rp {lima_puluh_kota_data['Kerugian_Rupiah_Miliar']:.1f} Miliar** Kerugian Finansial.
        
        **Implikasi Strategis:**
        Hasil analisis ini secara tegas merekomendasikan **Kabupaten Lima Puluh Kota** sebagai **Priority-1 Response Zone**. Semua alokasi dana dan sumber daya rekonstruksi harus dipusatkan di sini untuk efektivitas pemulihan maksimum.
    """)
    
    st.markdown("---")
    
    st.subheader("Rekomendasi Tindakan Berdasarkan Sektor")
    col_p1, col_p2, col_p3 = st.columns(3)

    col_p1.metric(
        "Sektor KEMANUSIAAN",
        "Penanganan Pengungsi & Rumah Rusak Berat",
        delta="Target: Penanganan 78% rumah rusak berat harus ditangani dalam 90 hari.",
        delta_color="off"
    )
    col_p1.warning(
        f"""
        **TINDAKAN:** Kirim bantuan non-makanan (tenda, selimut, obat-obatan) ke **{lima_puluh_kota_data['Kabupaten_Kota']}** dan Agam. Prioritaskan pendataan Rumah Rusak Berat.
        """
    )
    
    col_p2.metric(
        "Sektor LOGISTIK",
        "Rekonstruksi Jembatan Vital",
        delta="Target: Perbaikan 50% Jembatan vital dalam 60 hari.",
        delta_color="off"
    )
    col_p2.error(
        f"""
        **TINDAKAN:** Alokasikan tim dan dana tercepat untuk perbaikan **Jembatan Rusak** di **{lima_puluh_kota_data['Kabupaten_Kota']}** (4 unit) dan Padang Pariaman (3 unit).
        """
    )

    col_p3.metric(
        "Sektor MITIGASI",
        "Pencegahan Bencana Hidrologis",
        delta="Target: Mengurangi dampak Banjir Bandang dan Tanah Longsor.",
        delta_color="off"
    )
    col_p3.info(
        """
        **TINDAKAN:** Investasikan pada sistem peringatan dini (EWS) untuk **Banjir Bandang** di hulu sungai. Lakukan reboisasi di wilayah rawan **Tanah Longsor**.
        """
    )


st.success("Aplikasi Streamlit ini dirancang untuk menyediakan data *real-time* dan interaktif, memudahkan Pemerintah dan pemangku kepentingan dalam pengambilan keputusan yang cepat dan tepat sasaran.")
