import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Công cụ tính khoản vay",
    page_icon="💰",
    layout="wide"
)

# Logo
if os.path.exists("logo2.jpg.jfif"):
    st.image("logo2.jpg.jfif", width=250)

st.title("💰 Công Cụ Tính Khoản Vay")
st.subheader("Đề tài 3")

col1, col2 = st.columns(2)

with col1:

    so_tien_vay = st.number_input(
        "💵 Số tiền vay (VNĐ)",
        min_value=0,
        value=150000000,
        step=1000000,
        format="%d"
    )

    so_thang_vay = st.number_input(
        "📅 Số tháng vay",
        min_value=1,
        value=12
    )

    lai_suat_nam = st.number_input(
        "📈 Lãi suất năm (%/năm)",
        min_value=0.0,
        value=12.0,
        step=0.1
    )

with col2:

    muc_dich = st.selectbox(

        "🎯 Mục đích vay",

        [
            "-- Chọn mục đích --",

            "Mua nhà",

            "Mua xe ô tô",

            "Tiêu dùng",

            "Kinh doanh",

            "Du học",

            "Khác"

        ]

    )

    phuong_thuc_tinh = st.radio(

        "⚙️ Phương thức tính",

        [

            "Lãi theo dư nợ GỐC (cố định)",

            "Lãi theo dư nợ GIẢM DẦN"

        ]

    )

tinh = st.button(

    "🚀 Tính toán",

    use_container_width=True

)

if tinh:

    if muc_dich == "-- Chọn mục đích --":

        st.warning(

            "Vui lòng chọn mục đích vay"

        )

    else:

        lai_suat_thang = (

            lai_suat_nam / 100 / 12

        )

        goc_hang_thang = (

           
