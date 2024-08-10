import streamlit as st
import pandas as pd
import re
import numpy as np
from pandas.api.types import is_numeric_dtype


st.set_page_config(layout="wide")
col = st.columns((100, 40), gap="large")

with col[0]:
    csv = st.file_uploader(
        "Drop your CSV file here",
        type="csv"
    )

    if csv:
        global data
        data = pd.read_csv(csv)

        clean_cols = {
            col: re.sub(r'[^a-zA-Z0-9]', "", col) for col in data.columns
        }

        data.rename(columns = clean_cols, inplace = True)

        if "df" not in st.session_state:
            st.session_state["df"] = data

        st.write(st.session_state.df)

        attr = st.sidebar.selectbox("Choose an attribute", st.session_state.df.columns)

        with col[1]:
            st.write(st.session_state.df[attr])
            find_replace = st.text_input(
                "Find Replace",
            ).split()



            if find_replace:
                st.session_state.df[attr] = st.session_state.df[attr].str.replace(
                    find_replace[0],
                    find_replace[1]
                ) if is_numeric_dtype(attr) else st.session_state.df[attr].replace(
                    int(find_replace[0]),
                    int(find_replace[1])
                )

                if st.button("Replace"):
                    st.rerun()

            if st.button("Delete"):
                st.session_state.df.drop(columns=[attr], axis=1, inplace=True)
