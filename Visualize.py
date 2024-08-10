import streamlit as st
import pandas as pd
from pandas.api.types import is_numeric_dtype
import seaborn as sns
import re
import numpy as np

st.set_page_config(layout="wide")
col = st.columns((100, 40), gap="large")

graph = st.sidebar.selectbox(
    "Choose a plot",
    ("Line", "Bar", "Histogram", "Pie")
)


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

        # numeric_columns = data.select_dtypes(include=np.number).columns

        global attr
        attr = st.sidebar.selectbox(
            "Choose a column:",
            data.columns,
        )

        with col[1]:
            if csv:
                togg = st.toggle("Show Attribute")
                if togg:
                    st.write(data[attr])

        range_ = st.sidebar.slider(
            "Enter range",
            10, data[attr].size, 10
        )

        # clean_attr = st.sidebar.selectbox(
        #     "Choose a column to clean:",
        #     tuple(data.columns),
        #     index=None,
        #     placeholder="Select a Column",
        # )

        if is_numeric_dtype(data[attr]):

            if graph == "Line":
                st.line_chart(data[attr].head(range_))

            if graph == "Bar":
                st.bar_chart(data[attr].head(range_))

            if graph == "Histogram":
                auto = st.sidebar.toggle("Auto bins?")

                if auto:
                    hist = sns.histplot(data=data[attr], bins = auto, kde=True)
                else:
                    bins_ = st.sidebar.slider("Bins", 0, 100, 10)
                    hist = sns.histplot(data=data[attr], bins = bins_, kde=True)

                st.pyplot(hist.get_figure())

        if "df" not in st.session_state:
            st.session_state["df"] = data
        st.write(data)
