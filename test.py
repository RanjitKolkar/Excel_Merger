import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel Merger", layout="wide")

st.markdown("<h1 style='color:#1f77b4;'>📁 Excel Merger & Visualizer</h1>", unsafe_allow_html=True)

# File uploader (accepts multiple Excel files)
uploaded_files = st.file_uploader(
    "📤 Upload multiple Excel files (.xlsx or .xls):",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

    # Show list of uploaded files
    st.markdown("### Files Uploaded:")
    for f in uploaded_files:
        st.markdown(f"- 🗂️ `{f.name}`")

    if st.button("🔗 Merge and Show Data"):
        merged_df = pd.DataFrame()
        dataframes = []

        for file in uploaded_files:
            try:
                df = pd.read_excel(file)
                df['Source File'] = file.name  # Track file source
                dataframes.append(df)
            except Exception as e:
                st.error(f"❌ Error reading `{file.name}`: {e}")

        if dataframes:
            merged_df = pd.concat(dataframes, ignore_index=True)
            st.success("✅ Merge successful!")

            # Show preview
            st.markdown("### 🧾 Merged Data Preview")
            st.dataframe(merged_df, use_container_width=True)

            # Download as Excel
            output = io.BytesIO()
            merged_df.to_excel(output, index=False)
            st.download_button(
                label="💾 Download Merged Excel File",
                data=output.getvalue(),
                file_name="merged_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Visualization section
            st.markdown("### 📊 Visualize a Column")
            numeric_cols = merged_df.select_dtypes(include="number").columns.tolist()

            if numeric_cols:
                col_to_plot = st.selectbox("Select a numeric column to visualize:", numeric_cols)
                st.bar_chart(merged_df[col_to_plot])
            else:
                st.info("No numeric columns found for charting.")
        else:
            st.warning("⚠️ No valid Excel data to merge.")
else:
    st.info("👈 Upload some Excel files to get started.")
