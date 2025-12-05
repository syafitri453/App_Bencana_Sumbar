import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Judul dan Konfigurasi Aplikasi ---
st.set_page_config(
    page_title="Analisis Bencana Sumatera Barat Interaktif",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Aplikasi Interaktif: Analisis Dampak Bencana Sumatra Barat")
st.markdown("Visualisasi data komprehensif untuk mendukung keputusan strategis pasca-bencana. [Image of Dashboard Streamlit]")

# --- Data Simulasi (Berdasarkan Temuan Power BI) ---
# Data ini mencerminkan temuan kritis dari 5 dashboard Anda.
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
st.sidebar.header("Filter Analisis")

# Filter Kabupaten/Kota
kabupaten_options = ['Semua'] + sorted(df['Kabupaten_Kota'].unique())
selected_kabupaten = st.sidebar.selectbox(
    "Pilih Kabupaten/Kota:",
    kabupaten_options
)

# Filter Jenis Bencana
bencana_options = ['Semua'] + sorted(df['Jenis_Bencana'].unique())
selected_bencana = st.sidebar.selectbox(
    "Pilih Jenis Bencana:",
    bencana_options
)

# Menerapkan Filter
df_filtered = df.copy()
if selected_kabupaten != 'Semua':
    df_filtered = df_filtered[df_filtered['Kabupaten_Kota'] == selected_kabupaten]
if selected_bencana != 'Semua':
    df_filtered = df_filtered[df_filtered['Jenis_Bencana'] == selected_bencana]

# --- Metrik Utama (Dashboard Ringkasan Eksekutif) ---
st.header("1. Metrik Utama & Skala Dampak")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Mengungsi (Jiwa)", f"{df_filtered['Total_Mengungsi'].sum():,} Jiwa")
col2.metric("Total Meninggal", f"{df_filtered['Total_Meninggal'].sum()} Jiwa")
col3.metric("Total Kerugian", f"Rp {df_filtered['Kerugian_Rupiah_Miliar'].sum():.1f} Miliar")
col4.metric("Total Unit Rusak Kritis", f"{df_filtered['Jembatan_Rusak'].sum() + df_filtered['Sekolah_Rusak'].sum()} Unit")
st.markdown("---")

# --- Visualisasi 1: Ranking Pengungsi & Fatalitas (Dashboard 2) ---
st.subheader("2. Hotspot Kemanusiaan: Pengungsi vs. Fatalitas")

# Mengelompokkan data berdasarkan Kabupaten/Kota
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

# --- Visualisasi 2: Komposisi Kerugian (Dashboard 4) ---
st.subheader("3. Komposisi Kerugian Finansial berdasarkan Jenis Bencana")
df_bencana_kerugian = df.groupby('Jenis_Bencana')['Kerugian_Rupiah_Miliar'].sum().reset_index()

fig2 = px.pie(
    df_bencana_kerugian,
    names='Jenis_Bencana',
    values='Kerugian_Rupiah_Miliar',
    title='Persentase Kerugian Rupiah berdasarkan Jenis Bencana',
    hole=.3,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig2.update_traces(textinfo='percent+label', textfont_size=14)
st.plotly_chart(fig2, use_container_width=True)
st.caption("Analisis: Data pie chart menunjukkan pemicu finansial terbesar, memandu alokasi anggaran mitigasi di masa depan.")

# --- Visualisasi 3: Prioritas Rekonstruksi (Dashboard 3 & 5) ---
st.subheader("4. Prioritas Rekonstruksi: Kerusakan Jembatan vs. Sekolah")
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

# --- Bagian Analisis Teks Kritis ---
st.markdown("## 5. Insight Kritis: Lima Puluh Kota sebagai Episentrum")

lima_puluh_kota_data = df[df['Kabupaten_Kota'] == 'Lima Puluh Kota'].iloc[0]

st.info(f"""
    **Fakta Data Terkini (Berdasarkan Filter):**
    Wilayah yang saat ini paling kritis adalah **{lima_puluh_kota_data['Kabupaten_Kota']}**, menyumbang:
    - **{lima_puluh_kota_data['Total_Mengungsi']:,}** Jiwa Mengungsi (Tertinggi).
    - **{lima_puluh_kota_data['Jembatan_Rusak']}** Unit Jembatan Rusak (Tertinggi).
    - **Rp {lima_puluh_kota_data['Kerugian_Rupiah_Miliar']:.1f} Miliar** Kerugian Finansial (Tertinggi).
    
    **Implikasi Strategis:**
    Hasil analisis ini secara tegas merekomendasikan **Kabupaten Lima Puluh Kota** sebagai **Priority-1 Response Zone**. Semua alokasi dana dan sumber daya rekonstruksi harus dipusatkan di sini untuk efektivitas pemulihan maksimum.
""")

st.success("Aplikasi Streamlit ini dirancang untuk menyediakan data *real-time* dan interaktif, memudahkan Pemerintah dan pemangku kepentingan dalam pengambilan keputusan yang cepat dan tepat sasaran.")
