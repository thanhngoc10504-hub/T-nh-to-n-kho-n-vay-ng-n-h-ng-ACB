import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ======================
# CẤU HÌNH TRANG
# ======================

st.set_page_config(
    page_title="Công cụ tính khoản vay",
    page_icon="💰",
    layout="wide"
)

# ======================
# LOGO
# ======================

if os.path.exists("logo2.jpg.jfif"):
    st.image("logo2.jpg.jfif", width=180)

st.title("💰 Công Cụ Tính Khoản Vay")
st.subheader("Đề tài 3")

st.divider()

# ======================
# NHẬP THÔNG TIN
# ======================

col1, col2 = st.columns(2)

with col1:

    so_tien_vay = st.number_input(
        "💵 Số tiền vay (VNĐ)",
        min_value=1,
        value=150_000_000,
        step=1_000_000,
        format="%d"
    )

    so_thang_vay = st.number_input(
        "📅 Thời hạn vay (tháng)",
        min_value=1,
        value=12
    )

    lai_suat_nam = st.number_input(
        "📈 Lãi suất (%/năm)",
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

    phuong_thuc = st.radio(

        "⚙️ Phương thức tính lãi",

        [

            "Lãi theo dư nợ GỐC (cố định)",

            "Lãi theo dư nợ GIẢM DẦN"

        ]

    )

# ======================
# NÚT TÍNH TOÁN
# ======================

if st.button("🚀 Tính toán", use_container_width=True):

    if muc_dich == "-- Chọn mục đích --":

        st.warning("⚠️ Vui lòng chọn mục đích vay.")

    else:

        lai_suat_thang = lai_suat_nam / 100 / 12

        goc_hang_thang = so_tien_vay / so_thang_vay

        tong_lai = 0

        data = []

        # ======================
        # DƯ NỢ GỐC
        # ======================

        if phuong_thuc == "Lãi theo dư nợ GỐC (cố định)":

            lai_co_dinh = so_tien_vay * lai_suat_thang

            du_no = so_tien_vay

            for thang in range(1, so_thang_vay + 1):

                tong_thang = (

                    goc_hang_thang +

                    lai_co_dinh

                )

                tong_lai += lai_co_dinh

                du_no -= goc_hang_thang

                data.append({

                    "Tháng": thang,

                    "Gốc trả (VNĐ)": round(goc_hang_thang),

                    "Lãi trả (VNĐ)": round(lai_co_dinh),

                    "Tổng trả (VNĐ)": round(tong_thang),

                    "Dư nợ còn lại (VNĐ)": round(max(du_no, 0))

                })

        # ======================
        # DƯ NỢ GIẢM DẦN
        # ======================

        else:

            du_no = so_tien_vay

            for thang in range(1, so_thang_vay + 1):

                lai_thang = du_no * lai_suat_thang

                tong_thang = (

                    goc_hang_thang +

                    lai_thang

                )

                tong_lai += lai_thang

                du_no -= goc_hang_thang

                data.append({

                    "Tháng": thang,

                    "Gốc trả (VNĐ)": round(goc_hang_thang),

                    "Lãi trả (VNĐ)": round(lai_thang),

                    "Tổng trả (VNĐ)": round(tong_thang),

                    "Dư nợ còn lại (VNĐ)": round(max(du_no, 0))

                })

        tong_tra = so_tien_vay + tong_lai

        df = pd.DataFrame(data)

        # ======================
        # KPI
        # ======================

        st.subheader("📋 Kết quả")

        k1, k2, k3 = st.columns(3)

        k1.metric(

            "💵 Tổng khoản vay",

            f"{so_tien_vay:,.0f}"

        )

        k2.metric(

            "🏦 Tổng lãi",

            f"{tong_lai:,.0f}"

        )

        k3.metric(

            "💰 Tổng thanh toán",

            f"{tong_tra:,.0f}"

        )

        st.markdown(

            f"**🎯 Mục đích vay:** {muc_dich}"

        )

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True

        )

        # ======================
        # BIỂU ĐỒ
        # ======================

        fig, ax = plt.subplots()

        ax.plot(

            df["Tháng"],

            df["Tổng trả (VNĐ)"],

            marker='o'

        )

        ax.set_xlabel("Tháng")

        ax.set_ylabel("VNĐ")

        ax.grid(True)

        st.pyplot(fig)

        # ======================
        # DOWNLOAD CSV
        # ======================

        csv = df.to_csv(index=False)

        st.download_button(

            "📥 Tải lịch trả nợ",

            csv,

            file_name="lich_tra_no.csv",

            mime="text/csv"

        )

        st.success(

            f"✅ Tổng số tiền phải trả: {tong_tra:,.0f} VNĐ"

        )
