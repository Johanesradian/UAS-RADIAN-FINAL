import pandas as pd
import streamlit as st
import plotly.express as px
import json
from PIL import Image

st.set_page_config(page_title='Survey Minyak Mentah',
                   page_icon=":fuelpump:",
                   layout="wide")

title_container = st.container()
col1,col2 = st.columns([10,1])
image = Image.open('gambar1.png')
st.title ("Johanes Radian Saputra/1220134")
with title_container:
    with col1:
        st.markdown('<h2>Data Produksi Minyak Mentah dari Berbagai Negara</h2>',
                    unsafe_allow_html=True)
    with col2:
        st.image(image,width=64)
        

csv_file = 'produksi_minyak_mentah.csv'
sheet_name = 'produksi_minyak_mentah'

df = pd.read_csv(csv_file,
                 sep=',',
                 header=0,
                 )
st.subheader('Produksi Minyak Mentah per Tahun')

negara_info = pd.read_json("kode_negara_lengkap.json")
negara_info = negara_info[["name","alpha-3"]]
negara_info_singkatan = negara_info.set_index('alpha-3').to_dict()['name']


# --- no.1
negara=df['kode_negara'].map(negara_info_singkatan).unique().tolist()
tahun = df['tahun'].unique().tolist()

tahun_selection = st.slider('Tahun:',
                            min_value= min(tahun),
                            max_value= max(tahun),
                            value=(min(tahun),max(tahun)))

negara_selection = st.multiselect('Negara:',
                                  negara)

mask = (df['tahun'].between(*tahun_selection) & df['kode_negara'].map(negara_info_singkatan).isin(negara_selection))

df_grouped = df[mask].groupby(by=['tahun']).sum()[["produksi"]]


fig_produksinegarapertahun = px.bar(
    df_grouped,
    x=df_grouped.index,
    y="produksi",
    title="<b>Grafik Produksi Minyak Mentah Setiap Negara per Tahunnya</b>"
    )

st.plotly_chart(fig_produksinegarapertahun)

if st.checkbox("Tampilkan Data Produksi Minyak Mentah"):
    st.subheader('Data Produksi Minyak Mentah')
    st.dataframe(df[mask])

# --- no.2
st.subheader("Negara dengan Jumlah Produksi Terbesar per Tahunnya")
jumlah_negara_B = int(st.text_input("Besar Negara:",10))
nama_negara = df['kode_negara'].map(negara_info_singkatan)
tahun = df['tahun'].unique().tolist()

tahun_selection = st.multiselect('Tahun:',
                            tahun,
                                 )
mask = df['tahun'].isin(tahun_selection)
df_grouped = df[mask].groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'],ascending=False)
selected_df=df_grouped.head(jumlah_negara_B)



fig_besarnegarapadatahun = px.bar(
    selected_df,
    x=selected_df.index,
    y='produksi',
    title="<b>Grafik Negara dengan Jumlah Produksi Terbesar</b>",
    labels={
        "kode_negara": "Nama Negara",
        "produksi": "Produksi"
        },
    width=1260
    )

st.plotly_chart(fig_besarnegarapadatahun)
if st.checkbox("Tampilkan Data Negara sesuai Besar Negara dengan Jumlah Produksi Terbesar"):
    st.subheader('Data Negara dengan Jumlah Produksi Terbesar')
    st.dataframe(selected_df)

# --- no.3
st.subheader("Negara dengan Jumlah Produksi Terbesar dalam Kumulatif Keseluruhan Tahun")
jumlah_negara_A = int(st.text_input("Besar Negara Kumulatif:",10))
nama_negara = df['kode_negara'].map(negara_info_singkatan)

df_grouped = df.groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'],ascending=False)
selected_df=df_grouped.head(jumlah_negara_A)


fig_besarnegarakeseluruhan = px.bar(
    selected_df,
    x=selected_df.index,
    y='produksi',
    title="<b>Grafik Negara dengan Jumlah Produksi Terbesar secara Keseluruhan Tahun</b>",
    labels={
        "kode_negara": "Nama Negara",
        "produksi": "Produksi"
        },
    color="produksi",
    color_discrete_sequence=["blue", "red", "orange", "goldenrod", "pink","yellow","green"],
    width=1260,
    height=600
    )

st.plotly_chart(fig_besarnegarakeseluruhan)
if st.checkbox("Tampilkan Data Negara sesuai Besar Negara dengan Jumlah Produksi Terbesar Kumulatif"):
    st.subheader('Data Negara dengan Jumlah Produksi Terbesar Kumulatif Keseluruhan Tahun')
    st.dataframe(selected_df)


# --- no.4
st.subheader("Negara dengan Jumlah Produksi Terbesar, Terkecil, dan Tidak Memproduksi Minyak Mentah")
st.markdown("<h5><u>Pada Tahun</u></h5>",unsafe_allow_html=True)
tahun4 = df['tahun'].unique().tolist()

tahun_selection4 = st.multiselect('Pilih Tahun:',
                            tahun4,
                                 )
nama_negara = df['kode_negara'].map(negara_info_singkatan)
mask = df['tahun'].isin(tahun_selection4)
#seleksi tahun dan negara terbesar
st.markdown("**Negara dengan Jumlah Produksi Terbesar** :arrow_up:")
df_selected = df[mask].groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'],ascending=False)
selected_df = df_selected.head(1)
negara_info = pd.read_json("kode_negara_lengkap.json")
negara_info = negara_info[["name","alpha-3","region","sub-region"]]
for row in selected_df.index:
        st.write(row,"merupakan negara dengan dengan jumlah produksi terbesar.")
        mask = negara_info['name'].isin(selected_df.index)
        st.markdown("Informasi Mengenai Negara")
        st.dataframe(negara_info[mask])

#seleksi tahun dan negara terkecil
st.markdown("**Negara dengan Jumlah Produksi Terkecil** :arrow_down:")
mask = (df['tahun'].isin(tahun_selection4) & (df['produksi']>0)==True)
df_selected = df[mask].groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'])
selected_df = df_selected.head(1)
negara_info = pd.read_json("kode_negara_lengkap.json")
negara_info = negara_info[["name","alpha-3","region","sub-region"]]
for row in selected_df.index:
        st.write(row,"merupakan negara dengan dengan jumlah produksi terkecil (bukan 0).")
        mask = negara_info['name'].isin(selected_df.index)
        st.markdown("Informasi Mengenai Negara")
        st.dataframe(negara_info[mask])

#seleksi tahun dan negara sama dengan nol
st.markdown("**Negara dengan Jumlah Produksi sama dengan Nol** :zero:")
mask = (df['tahun'].isin(tahun_selection4) & (df['produksi']==0)==True)
df_selected = df[mask].groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'])
selected_df = df_selected
negara_info = pd.read_json("kode_negara_lengkap.json")
negara_info = negara_info[["name","alpha-3","region","sub-region"]]
if tahun_selection4:
    mask = negara_info['name'].isin(selected_df.index)
    st.dataframe(negara_info[mask])
    
#kumulatif
st.markdown("<br>",unsafe_allow_html=True)    
st.markdown("<h5><u>Keseluruhan Tahun</u></h5>",unsafe_allow_html=True)        
            
#kumulatif negara terbesar
nama_negara = df['kode_negara'].map(negara_info_singkatan)
st.markdown("**Negara dengan Jumlah Produksi Terbesar** :arrow_up:")
df_selected = df.groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'],ascending=False)
selected_df = df_selected.head(1)
negara_info = pd.read_json("kode_negara_lengkap.json")
negara_info = negara_info[["name","alpha-3","region","sub-region"]]
for row in selected_df.index:
        st.write(row,"merupakan negara dengan dengan jumlah produksi terbesar.")
        mask = negara_info['name'].isin(selected_df.index)
        st.markdown("Informasi Mengenai Negara")
        st.dataframe(negara_info[mask])

#kumulatif negara terkecil
st.markdown("**Negara dengan Jumlah Produksi Terkecil** :arrow_down:")
mask = (df['produksi']>0)==True
df_selected = df[mask].groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'])
selected_df = df_selected.head(1)
negara_info = pd.read_json("kode_negara_lengkap.json")
negara_info = negara_info[["name","alpha-3","region","sub-region"]]
for row in selected_df.index:
        st.write(row,"merupakan negara dengan dengan jumlah produksi terkecil (bukan 0).")
        mask = negara_info['name'].isin(selected_df.index)
        st.markdown("Informasi Mengenai Negara")
        st.dataframe(negara_info[mask])

#kumulatif negara sama dengan 0
st.markdown("**Negara dengan Jumlah Produksi sama dengan Nol** :zero:")
mask = (df['produksi']==0)==True
df_selected = df[mask].groupby(by=nama_negara).sum()[['produksi']].sort_values(by=['produksi'])
selected_df = df_selected
negara_info = pd.read_json("kode_negara_lengkap.json")
negara_info = negara_info[["name","alpha-3","region","sub-region"]]
mask = negara_info['name'].isin(selected_df.index)
st.dataframe(negara_info[mask])
