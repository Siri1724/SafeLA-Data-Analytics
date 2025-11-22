

import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="LA Crime Dashboard (Dark Mode)", layout="wide")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv(r"E:\final project\clean_crime_data_3.csv")
    df['Incident_Date'] = pd.to_datetime(df['Incident_Date'], errors='coerce')
    df['year'] = df['Incident_Date'].dt.year
    df['month'] = df['Incident_Date'].dt.month_name()
    df['day_of_week'] = df['Incident_Date'].dt.day_name()
    df.columns = [c.strip() for c in df.columns]
    return df

df = load_data()

# 🎨 الألوان الأساسية (أزرق غامق)
PRIMARY_COLOR = "#007BFF"   # أزرق داكن قوي
ACCENT_COLOR = "#D9534F"    # أحمر خطر
CARD_BG = "#1E1E1E"
BACKGROUND_COLOR = "#121212"

# 🌙 CSS للتصميم الداكن والبطاقات والفلاتر
st.markdown(f"""
    <style>
    body {{
        background-color: {BACKGROUND_COLOR};
        color: #E0E0E0;
    }}
    .block-container {{
        background-color: {BACKGROUND_COLOR};
    }}
    h1, h2, h3, h4 {{
        color: {PRIMARY_COLOR};
    }}
    div[data-baseweb="tag"] {{
        background-color: {PRIMARY_COLOR} !important;
        color: white !important;
    }}
    .metric-card {{
        border-left: 5px solid {PRIMARY_COLOR};
        background-color: {CARD_BG};
        border-radius: 20px;
        padding: 20px;
        transition: all 0.3s ease;
    }}
    .metric-card:hover {{
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(0,123,255,0.3);
    }}
    </style>
""", unsafe_allow_html=True)

# العنوان
st.markdown(f"<h1 style='text-align:center; color:{PRIMARY_COLOR};'>📊  Los Angeles Crime Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- الفلاتر --------------------
st.sidebar.markdown(f"""
    <div style='background-color:{CARD_BG}; padding:15px; border-radius:10px;'>
    <h3 style='color:{PRIMARY_COLOR};'>🎯 Filters</h3>
    </div>
""", unsafe_allow_html=True)

area_filter = st.sidebar.multiselect("Select Area", sorted(df['Area_Name'].dropna().unique()), default=[])
gender_filter = st.sidebar.multiselect("Select Gender", sorted(df['Victim_Gender'].dropna().unique()), default=[])
year_filter = st.sidebar.multiselect("Select Year", sorted(df['year'].dropna().unique()), default=[])

filtered_df = df.copy()
if area_filter:
    filtered_df = filtered_df[filtered_df['Area_Name'].isin(area_filter)]
if gender_filter:
    filtered_df = filtered_df[filtered_df['Victim_Gender'].isin(gender_filter)]
if year_filter:
    filtered_df = filtered_df[filtered_df['year'].isin(year_filter)]

# -------------------- البطاقات --------------------
total_crimes = len(filtered_df)
top_area = filtered_df['Area_Name'].value_counts().idxmax() if not filtered_df.empty else "N/A"
avg_age = int(round(filtered_df['Victim_Age'].dropna().astype(float).mean(), 0)) if filtered_df['Victim_Age'].notna().any() else "N/A"

c1, c2, c3 = st.columns(3)
card_html = lambda title, value: f"""
<div class='metric-card'>
<h4 style='color:#A0A0A0; text-align:center;'>{title}</h4>
<p style='color:{PRIMARY_COLOR}; font-size:30px; font-weight:bold; text-align:center;'>{value}</p>
</div>
"""
c1.markdown(card_html("Total Crimes", f"{total_crimes:,}"), unsafe_allow_html=True)
c2.markdown(card_html("Top Area", top_area), unsafe_allow_html=True)
c3.markdown(card_html("Average Victim Age", avg_age), unsafe_allow_html=True)

st.markdown("---")

# -------------------- الصف الأول --------------------
col1, col2, col3 = st.columns(3)

# 📈 Crimes Over Years
with col1:
    st.subheader("📅 Crimes Over Years")
    year_df = filtered_df.groupby('year').size().reset_index(name='Crimes')
    if not year_df.empty:
        fig_line = px.line(year_df, x='year', y='Crimes', markers=True, line_shape='spline',
                           color_discrete_sequence=[PRIMARY_COLOR])
        fig_line.update_layout(template='plotly_dark', plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
                               font_color='#E0E0E0', showlegend=False)
        st.plotly_chart(fig_line, use_container_width=True)

# 🧍 Crimes by Gender
with col2:
    st.subheader("🧍 Crimes by Gender")
    gender_counts = filtered_df['Victim_Gender'].fillna("Unknown").value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    if not gender_counts.empty:
        fig_pie = px.pie(gender_counts, names='Gender', values='Count', hole=0.45,
                         color_discrete_sequence=['#007BFF', '#0056B3', '#4DA3FF'])
        fig_pie.update_traces(textinfo='label+percent')
        fig_pie.update_layout(template='plotly_dark', plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG)
        st.plotly_chart(fig_pie, use_container_width=True)

# 🔝 Top 10 Crimes
with col3:
    st.subheader("🔝 Top 10 Crime Types")
    top_crimes = filtered_df['Crime_Type'].value_counts().head(10).reset_index()
    top_crimes.columns = ['Crime Type', 'Count']
    top_crimes = top_crimes.sort_values('Count', ascending=True)
    colors = ['#D9534F' if c == 'VEHICLE - STOLEN' else '#2B2BFF' for c in top_crimes['Crime Type']]
    fig_bar = px.bar(top_crimes, x='Count', y='Crime Type', orientation='h',
                     color='Count', color_continuous_scale=[(0, '#2B2BFF'), (1, '#D9534F')])
    fig_bar.update_layout(template='plotly_dark', plot_bgcolor=CARD_BG,
                          paper_bgcolor=CARD_BG, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# -------------------- الصف الثاني --------------------
col4, col5 = st.columns([1.6, 0.9])

# 🗺️ Crime Map
with col4:
    st.subheader("🗺️ Crime Map")
    if {'Latitude', 'Longitude'}.issubset(filtered_df.columns):
        pts = filtered_df.dropna(subset=['Latitude', 'Longitude']).copy()
        agg = pts.groupby(['Latitude', 'Longitude']).size().reset_index(name='Crimes')

        # 🔹 عرض فقط النقاط التي عدد الجرائم فيها > 300
        agg = agg[agg['Crimes'] > 300]

        # 🔹 تدرج لوني من الأزرق الفاتح للغامق وشفافية بسيطة
        fig_map = px.scatter_mapbox(
            agg,
            lat='Latitude',
            lon='Longitude',
            size='Crimes',
            color='Crimes',
            color_continuous_scale=[(0, '#66B2FF'), (0.5, '#007BFF'), (1, '#00264D')],
            size_max=40,
            zoom=9,
            mapbox_style='carto-darkmatter',
            opacity=0.6
        )
        fig_map.update_layout(height=560, margin={"r":0,"t":30,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)


# 📅 Crimes by Day of Week
with col5:
    st.subheader("📅 Crimes by Day of Week")

    # 🔹 توحيد شكل أسماء الأيام (أول حرف كابتل)
    filtered_df['day_of_week'] = filtered_df['day_of_week'].str.capitalize()

    # 🔹 ترتيب الأيام: يبدأ من السبت وينتهي بالجمعة
    ordered_days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    filtered_df['day_of_week'] = pd.Categorical(
        filtered_df['day_of_week'], 
        categories=ordered_days, 
        ordered=True
    )

    # 🔹 حساب عدد الجرائم لكل يوم وترتيبها حسب الأسبوع
    day_counts = (
        filtered_df['day_of_week']
        .value_counts()
        .sort_index()
        .reset_index()
    )
    day_counts.columns = ['Day', 'Count']

    # 🔹 تحديد اليوم الأعلى في عدد الجرائم
    max_day = day_counts.loc[day_counts['Count'].idxmax(), 'Day']

    # 🔹 ألوان الأعمدة (اليوم الأعلى غامق)
    colors = ['#004C99' if d == max_day else '#3399FF' for d in day_counts['Day']]

    # 🔹 رسم العمود البياني
    fig_day = px.bar(
        day_counts,
        x='Day',
        y='Count',
        text='Count',
        color=colors
    )

    fig_day.update_traces(textposition='outside')
    fig_day.update_layout(
        template='plotly_dark',
        plot_bgcolor=CARD_BG,
        paper_bgcolor=CARD_BG,
        showlegend=False,
        height=560,
        xaxis_title='Day of Week',
        yaxis_title='Number of Crimes',
    )

    st.plotly_chart(fig_day, use_container_width=True)



st.caption("📊 Data: Los Angeles | All respect and appreciation to Instructor Ammar Mustafa ")
