import streamlit as st
import os
import streamlit as st
from PIL import Image
import numpy as np
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from streamlit_lottie import st_lottie
import json
import requests
from io import BytesIO, StringIO
import csv
import base64

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)
beauty = load_lottiefile("D://Development//Meet//Python_Dev//Projects69//Python101//beauty.json")
st.title("Welcome to Nail Vali")
st_lottie(beauty,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=None,
            width=None)
client_name = st.text_input("Enter Client Name")
contact_number = st.text_input("Enter Client Contact")
service = st.text_input("Enter service name")
amount = st.text_input("Enter Amount")
appointment_date = st.date_input("Enter appointment Date")
apppointment_details = {}
os.environ["INVOICE_LANG"] = "en"
client = Client(client_name)
provider = Provider('Nail Vali', bank_account='2600420569', bank_code='2010')
creator = Creator('Nail Vali')
show_file = st.empty()



if st.button("Book Appointment"):
    fields = ["appointment_date", "client_name", "contact_number", "service", "amount"]
    appointment_details = {"client_name": client_name,"contact_number": contact_number,"service": service,"amount": amount,"appointment_date": appointment_date}
    st.write(appointment_details)
    with open('Clients.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
    #  writer.writerow(["appointment_date", "client_name", "contact_number", "service", "amount"])
    #  writer.writerow([appointment_date,client_name ,contact_number,service,amount])
         
        writer.writerow(appointment_details)



if st.button("Generate Invoice"):
    # fields = ["appointment_date", "client_name", "contact_number", "service", "amount"]
    invoice = Invoice(client, provider, creator)
    invoice.currency_locale = 'en_US.UTF-8'
    invoice.add_item(Item(1, 1599, description=service))
    invoice.currency = "₹"
    invoice.number = "001"
    docu = SimpleInvoice(invoice)
    docu.gen(f"{client_name}.pdf", generate_qr_code=True)
    
    with open(f"{client_name}.pdf","rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
            

if st.button("Upload Nail Art"):
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", f"{client_name}")
        st.write(bytes_data)

