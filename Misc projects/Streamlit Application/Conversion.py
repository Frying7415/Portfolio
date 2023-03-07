# =============================================================================
# Conversion report visualization using StreamLit
# =============================================================================

import pandas as pd
import requests
import streamlit as st
import plotly_express as px


st.set_page_config(
    page_title='Total Conversion report',
    page_icon=":part_alternation_mark:",
    layout="wide"
)
# ============================= DATAFRAMES ====================================
# Без указания хэдера для библиотеки requests сервер OneDrive'a периодически разрывает соединение
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}


def get_one_data():
    url_one = "url"
    one = requests.get(
        url_one,
        headers=headers
    ).content
    df_one = pd.read_excel(one)
    cols_one = df_one.columns
    df_one.drop(columns=cols_one[24:], inplace=True)
    
    # Находим первую пустую ячейку в столбце, получаем индекс строки, удаляем все лишние строки ниже
    for i in reversed(range(0, len(df_one))):
        if i > 0 and str(df_one.at[i-1, "6"]) == 'nan':
            a = i-1

    df_one.drop(
        df_one.index[a:],
        axis=0,
        inplace=True
    )

    df_one['Date'] = pd.to_datetime(
        df_one['Date'],
        infer_datetime_format=True
    )
    df_one = df_one.astype(
        {
            '1': float,
            '2': float,
            '3': float,
            '4': float,
            '5': float,
            '6': int,
            '7': int,
            '8': int,
            '9': int,
            '10': int,
            '11': int,
            '12': float,
            '13': float,
            '14': int,
            '15': float,
            '16': int,
            '17': int,
            '18': float,
            '19': float,
            '20': float
        }
    )
    df_one["Conf"] = df_one["5"] * 100
    df_one["12"] = df_one["12"] * 100
    df_one["Year"] = pd.DatetimeIndex(df_one["Date"]).year
    df_one["Month"] = pd.DatetimeIndex(df_one["Date"]).month
    df_one["MonthName"] = pd.DatetimeIndex(df_one["Date"]).month_name()
    df_one["Un7"] = df_one["6"] - df_one["7"]
    return df_one

# =============================================================================

# =============================== SIDEBAR ===================================== 


st.sidebar.header("Фильтры")

year_one = st.sidebar.multiselect(
    "Выберите год для one:",
    options=get_one_data()["Year"].unique(),
    default=get_one_data()["Year"].unique()
)
df_selection_one = get_one_data().query(
    "Year == @year_one"
)

# =============================================================================

# ============================== PAGE CONTAINERS ==============================
one_header = st.container()
one_dataset = st.container()
whitespace1 = st.container()
# =============================================================================

# =================================== one ====================================
with one_header:
    st.image("url", width=100, output_format='JPEG')

with one_dataset:
    st.header("Показатели конверсии в динамике по проекту one:")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.area(
            df_selection_one,
            x="Date",
            y="11",
            color_discrete_sequence=["#AAFA9E"],
            title="title",
            markers=True
        )

        fig1.update_layout(yaxis_title=None, xaxis_title=None)
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.area(
            df_selection_one,
            x="Date",
            y="12",
            color_discrete_sequence=["#AAFA9E"],
            title="title",
            markers=True
        )
        
        fig2.update_layout(yaxis_title=None, xaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)
        
        fig3 = px.area(
            df_selection_one,
            x="Date",
            y="17",
            color_discrete_sequence=["#AAFA9E"],
            title="title",
            markers=True
        )
        
        fig3.update_layout(yaxis_title=None, xaxis_title=None)
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        fig4 = px.area(
            df_selection_one,
            x="Date",
            y="Conf",
            color_discrete_sequence=["#AAFA9E"],
            title="title",
            markers=True
        )
        
        fig4.update_layout(yaxis_title=None, xaxis_title=None)
        st.plotly_chart(fig4, use_container_width=True)
        
        fig5 = px.area(
            df_selection_one,
            x="Date",
            y="16",
            color_discrete_sequence=["#AAFA9E"],
            title="title",
            markers=True
        )
        fig5.update_layout(yaxis_title=None, xaxis_title=None)
        st.plotly_chart(fig5, use_container_width=True)
        
        fig6 = px.area(
            df_selection_one,
            x="Date",
            y="2",
            color_discrete_sequence=["#AAFA9E"],
            title="title",
            markers=True,
            hover_data=["19"]
        )
        fig6.update_layout(yaxis_title=None, xaxis_title=None)
        st.plotly_chart(fig6, use_container_width=True)
    st.header("Дополнительная аналитика:")
    
    fig = px.bar(
        df_selection_one,
        x="Date",
        y=["7", "Un7"],
        barmode="group",
        title="title",
        hover_data=["Conf"],
        height=650
    )
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
    
    scat = px.scatter(
        df_selection_one,
        x="4",
        y="1",
        size="14",
        color=get_one_data().index,
        size_max=30,
        height=650,
        hover_data=["Date"],
        title="title"
    )
    st.plotly_chart(scat, use_container_width=True)
    
    scat1 = px.scatter(
        df_selection_one,
        x="1",
        y="Conf",
        size="14",
        color=get_one_data().index,
        size_max=30,
        height=650,
        hover_data=["Date"],
        title="title"
    )
    st.plotly_chart(scat1, use_container_width=True)
    st.write("Исходные данные:")
    st.dataframe(get_one_data(), height=450)

with whitespace1:
    st.markdown("<br></br>", unsafe_allow_html=True)
# =============================================================================
# ---- FOOTER ----
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #003D4D;
        color: black;
        text-align: right;
        height: 35px;
        line-height: 35px;
        font-size: 16px
    }
</style>
<div class="footer">
    <p style="color: #FEFF00; text-align: right;">Developed by Elijah Adamovich 2022  </p>
</div>
"""
st.markdown(
    footer,
    unsafe_allow_html=True
)
