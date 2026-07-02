import streamlit as st
import pandas as pd
st.image("logo2.jpg.jfif")

st.subheader("💰 Công Cụ Tính Khoản Vay_Đề tài 3")

# --- PHẦN NHẬP LIỆU (ĐÃ BỔ SUNG MỤC ĐÍCH VAY) ---
col1, col2 = st.columns(2)

with col1:
    so_tien_vay = st.number_input("💵 Số tiền vay (VNĐ)", min_value=0, value=150000000, step=1000000)
    so_thang_vay = st.number_input("📅 Số tháng vay", min_value=1, value=12, step=1)
    # LƯU Ý: NHẬP 12.0 (dấu chấm) thay vì 12,00 để tránh lỗi
    lai_suat_nam = st.number_input("📈 Lãi suất năm (%/năm)", min_value=0.0, value=12.0, step=0.1)

with col2:
    # 1. BỔ SUNG: Dropdown chọn mục đích vay
    muc_dich = st.selectbox(
        "🎯 Mục đích vay / Sản phẩm cho vay",
        ["-- Chọn mục đích --", "Mua nhà", "Mua xe ô tô", "Tiêu dùng (Mua sắm)", 
         "Kinh doanh (Bổ sung vốn lưu động)", "Du học", "Khác"]
    )
    
    # 2. BỔ SUNG: Lựa chọn cách tính lãi
    phuong_thuc_tinh = st.radio(
        "⚙️ Phương thức tính lãi suất",
        ["Lãi theo dư nợ GỐC (cố định)", "Lãi theo dư nợ GIẢM DẦN"]
    )

# Nút bấm
tinh_toan = st.button("🚀 Tính toán ngay", use_container_width=True)

# --- PHẦN XỬ LÝ KẾT QUẢ ---
if tinh_toan:
    # Kiểm tra đã chọn mục đích chưa
    if muc_dich == "-- Chọn mục đích --":
        st.warning("⚠️ Vui lòng chọn mục đích vay trước khi tính toán!")
    else:
        # Tính toán tham số chung
        lai_suat_thang = lai_suat_nam / 100 / 12
        goc_hang_thang = so_tien_vay / so_thang_vay
        
        st.divider()
        st.subheader("📋 KẾT QUẢ PHÂN TÍCH KHOẢN VAY")
        st.caption(f"📌 Mục đích: **{muc_dich}**")
        
        # ---------------- XỬ LÝ TRƯỜNG HỢP 1: DƯ NỢ GỐC ----------------
        if phuong_thuc_tinh == "Lãi theo dư nợ GỐC (cố định)":
            lai_hang_thang = so_tien_vay * lai_suat_thang
            tong_hang_thang = goc_hang_thang + lai_hang_thang
            tong_tra = tong_hang_thang * so_thang_vay
            tong_lai = tong_tra - so_tien_vay

            # Thông tin tóm tắt
            col_a, col_b = st.columns(2)
            col_a.metric("💰 Gốc + Lãi mỗi tháng", f"{tong_hang_thang:,.0f} VNĐ")
            col_b.metric("🏦 Tổng lãi phải trả", f"{tong_lai:,.0f} VNĐ")
            
            # Tạo bảng chi tiết (Dư nợ gốc nên gốc và lãi đều cố định)
            du_no_cuoi = so_tien_vay
            data = []
            for thang in range(1, so_thang_vay + 1):
                du_no_cuoi -= goc_hang_thang
                data.append({
                    "Tháng": thang,
                    "Gốc trả (VNĐ)": goc_hang_thang,
                    "Lãi trả (VNĐ)": lai_hang_thang,
                    "Tổng trả (VNĐ)": tong_hang_thang,
                    "Dư nợ còn lại (VNĐ)": max(du_no_cuoi, 0) # max để tránh số âm do làm tròn
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)

        # ---------------- XỬ LÝ TRƯỜNG HỢP 2: DƯ NỢ GIẢM DẦN ----------------
        else:
            du_no = so_tien_vay
            tong_lai = 0
            data = []
            
            for thang in range(1, so_thang_vay + 1):
                lai_thang = du_no * lai_suat_thang
                tong_thang = goc_hang_thang + lai_thang
                tong_lai += lai_thang
                du_no -= goc_hang_thang
                
                data.append({
                    "Tháng": thang,
                    "Gốc trả (VNĐ)": goc_hang_thang,
                    "Lãi trả (VNĐ)": lai_thang,
                    "Tổng trả (VNĐ)": tong_thang,
                    "Dư nợ còn lại (VNĐ)": max(du_no, 0)
                })
            
            # Tổng số tiền phải trả cuối cùng
            tong_tra = so_tien_vay + tong_lai
            tong_trung_binh_thang = tong_tra / so_thang_vay

            # Thông tin tóm tắt
            col_a, col_b = st.columns(2)
            col_a.metric("💰 Trung bình Gốc+Lãi mỗi tháng", f"{tong_trung_binh_thang:,.0f} VNĐ")
            col_b.metric("🏦 Tổng lãi phải trả", f"{tong_lai:,.0f} VNĐ")

            st.caption("📉 *Lưu ý: Số tiền trả tháng đầu cao nhất và giảm dần về cuối kỳ.*")
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        # Dòng tổng kết cuối cùng
        st.success(f"✅ Tổng số tiền phải trả sau {so_thang_vay} tháng: **{tong_tra:,.0f} VNĐ**")
