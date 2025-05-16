import streamlit as st # for creating UI for the application
import fitz  # PyMuPDF #Extration of the data from pdf
import json
import os

def extract_text_and_tables(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    extracted_data = {}
    list_items = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split("\n")

        for line in lines:
            if "  " in line:  # crude table detector using multiple spaces
                list_items.append(line.strip())
            else:
                key = " ".join(line.strip().split(" ")[:3]).replace(":", "")
                if key:
                    if key in extracted_data:
                        extracted_data[key] += " " + line.strip()
                    else:
                        extracted_data[key] = line.strip()

    return {
        "Headers": extracted_data,
        "List_items": list_items
    }

def save_json(data, file_path):
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Streamlit UI ---
st.title("📄 PDF Text & Table Extractor")

pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    st.info("Extracting text and table-like data from your PDF...")

    extracted = extract_text_and_tables(pdf_file)

    st.subheader("🔹 Headers")
    st.json(extracted["Headers"])

    st.subheader("🔸 List_items (Detected Tables)")
    st.write(extracted["List_items"])

    if st.button("💾 Download JSON"):
        save_json(extracted, "extracted_data.json")
        with open("extracted_data.json", "rb") as f:
            st.download_button(label="Download Extracted JSON", data=f, file_name="extracted_data.json", mime="application/json")
