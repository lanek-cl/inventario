# -*- coding: utf-8 -*-
"""
@file     : CSV Handler
@brief   : Handles CSV and TXT file conversion and plotting.
@date    : 2022/08/12
@version : 1.0.0
@author  : Lucas Cortés.
@contact : lucas.cortes@lanek.cl
@bug     : None.
"""

from PIL import Image
import streamlit as st
from config.config import Config
import functions as fn
import os
import json
import gspread
import Requests as rq
import threading
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


def select_component(inout, product):
    categorias = ["Componentes", "Insumos"]
    categoria = st.selectbox("Seleccione categoría", categorias)
    familia = (
        Config.familia_insumos if categoria == "Insumos" else Config.familia_componentes
    )
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    miembro = st.selectbox("Seleccione familia de insumo", familia.keys())

    banana = st.selectbox("Seleccione producto", familia[miembro])

    cantidad = st.number_input(f"Ingrese la cantidad de {miembro}", 0, 1000000, 1)
    
    if st.button("Enviar"):
        Entry_key = "17H_Z_kJcqJBX4A0LKizI4A450V_y0nI3Qu4tq9UP4n8"
        Stock_key = "1Qqxaof92dIeP--Vy3B62l3pEnL_FG42SdzEV9Kxy0fI"
        Outs_key = "1sZK9-F7PN4xCzU2q2fMNbR7U1CGnMUbAlUhAKVAJJ2c"

        creds = {
            "type": st.secrets["type"],
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"],
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        }
        #st.write(creds)

        gc = gspread.service_account_from_dict(creds) #gspread.service_account(filename="credentials.json")
        Entry_sheet = gc.open_by_key(Entry_key)
        Outs_sheet = gc.open_by_key(Outs_key)
        Stock_sheet = gc.open_by_key(Stock_key)

        Ent_sheet = Entry_sheet.worksheet("Entradas")
        Out_sheet = Outs_sheet.worksheet("Salidas")
        Inv_sheet = Stock_sheet.worksheet("Inventario")

        sheet = Ent_sheet if inout == "Entrada" else Out_sheet
        id = fn.create_ID(sheet, categoria, miembro, banana)
        st.write(f"{inout} de {cantidad} {miembro} de {banana}, ID: {id}")
        cant = -cantidad if inout == "Salida" else cantidad
        
        if inout == "Entrada":
            if categoria == "Componentes":
                data = [id, fecha, categoria, miembro, banana, cantidad]
                fn.Add_Comp(Inv_sheet, id, categoria, miembro, banana, cant)

            if categoria == "Insumos":
                data = [id, fecha, categoria, "", "", "", miembro, banana, cantidad]
                fn.Add_Insu(Inv_sheet, id, categoria, miembro, banana, cant)

        if inout == "Salida":
            if categoria == "Componentes":
                data = [fecha, product, categoria, miembro, banana, cantidad]
                fn.Add_Comp(Inv_sheet, id, categoria, miembro, banana, cant)

            if categoria == "Insumos":
                data = [fecha, product, categoria, "", "", "", miembro, banana, cantidad]
                fn.Add_Insu(Inv_sheet, id, categoria, miembro, banana, cant)

        try:
            sheet.append_row(data)
            st.balloons()

        except Exception as e:
            # Print the error message
            st.write("An error occurred:", str(e))


def main():
    im = Image.open("assets/logos/favicon.png")

    st.set_page_config(
        page_title="Agrosuper",
        page_icon=im,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Sistema de inventario :blue[Lanek] :poop:")

    inout = ["Entrada", "Salida"]
    operacion = st.selectbox("Seleccione operación a realizar", inout)

    if operacion == "Entrada":
        select_component(operacion, None)

    if operacion == "Salida":
        productos = ["AVM", "ABMA"]
        producto = st.selectbox("Seleccione producto", productos)
        select_component(operacion, producto)


if __name__ == "__main__":
    main()
