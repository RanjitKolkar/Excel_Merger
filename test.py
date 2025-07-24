import streamlit as st
import pandas as pd
import io

# Set page config
st.set_page_config(page_title="Excel Merger", layout="wide")

# App title
st.markdown("<h1 style='color:#2E8B57;'>📊 Excel Merger & Visualizer (Cloud-Ready)</h1>", unsafe_allow_html=True)

# Upload multiple Excel files
uploaded_files = st.file_uploader(
    "📤 Upload one or more Excel files (.xlsx or .xls):",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Uploaded {len(uploaded_files)} Excel file(s).")

    # Display uploaded file names
    st.markdown("### 🗂 Uploaded Files")
    for file in uploaded_files:
        st.markdown(f"- `{file.name}`")

    if st.button("🔗 Merge Files"):
        merged_dataframes = []

        for file in uploaded_files:
            try:
                df = pd.read_excel(file)
                df["Source File"] = file.name  # Track the source file
                merged_dataframes.append(df)
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")

        if merged_dataframes:
            merged_df = pd.concat(merged_dataframes, ignore_index=True)
            st.success("✅ Files merged successfully!")

            # Show merged data
            st.markdown("### 📋 Merged Data Preview")
            st.dataframe(merged_df, use_container_width=True)

            # Download merged Excel
            buffer = io.BytesIO()
            merged_df.to_excel(buffer, index=False)
            st.download_button(
                label="💾 Download Merged Excel",
                data=buffer.getvalue(),
                file_name="merged_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Visualization
            st.markdown("### 📈 Visualize Numeric Column")
            numeric_cols = merged_df.select_dtypes(include='number').columns.tolist()
            if numeric_cols:
                selected_col = st.selectbox("Choose a column to visualize:", numeric_cols)
                st.bar_chart(merged_df[selected_col])
            else:
                st.info("No numeric columns found for visualization.")
        else:
            st.warning("⚠️ No valid data found in uploaded files.")
else:
    st.info("👈 Upload some Excel files to begin.")
