#import

import streamlit as st
import pandas as pd
import os
from io import BytesIO


#set up our app

st.set_page_config(page_title="Data Swepper", layout="wide")
st.title("Data sweeper")
st.write("transform your files between csv and excel format with build-in data cleaning and visualization")

uploaded_files = st.file_uploader("Upload your files (CSV or EXCEL):", type=["csv", "xlsx"], accept_multiple_files = True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file, encoding='latin1')
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsopprted file type: {file_ext}")    
            continue

        #display info about the files
        st.write(f"**file Name:** {file.name}")
        st.write(f"**file Size:** {file.size/1024}")

        #show 5 rows of our df
        st.write("preview the head of the Dataframe")
        st.dataframe(df.head())

        #option for data cleaning
        st.subheader("Data Cleaning Option")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Removed duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("duplicates Removed!")

            with col2:
                if st.button(f"fill missing value for {file.name}"):
                    numeric_cols = df.select_dtypes(include = ["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Value have been Filled")

            #choose specific columns to keeps or convert
            st.subheader("select culomns to convert")
            columns = st.multiselect(f"choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            #create som visualization
            st.subheader("data visualization")
            if st.checkbox(f"show visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include = "number").iloc[:,:2])

            
            #convert the file CSV to -> Excel    
            st.subheader("Conversion Options")
            conversion_type = st.radio(f"convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"convert{file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index = False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel" :
                    df.to_excel(buffer, index = False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)




                #download Button
                st.download_button(
                    label= f"Download {file.name} as {conversion_type}",
                    data = buffer,
                    file_name = file_name,
                    mime = mime_type
                )


                st.success("all files are Processed!")

