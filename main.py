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

Entry_key = st.secrets["Entry_key"]
Stock_key = st.secrets["Stock_key"]
Outs_key = st.secrets["Outs_key"]

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

gc = gspread.service_account_from_dict(
    creds
)  # gspread.service_account(filename="credentials.json")
Entry_sheet = gc.open_by_key(Entry_key)
Outs_sheet = gc.open_by_key(Outs_key)
Stock_sheet = gc.open_by_key(Stock_key)

Ent_sheet = Entry_sheet.worksheet("Entradas")
Out_sheet = Outs_sheet.worksheet("Salidas")
Inv_sheet = Stock_sheet.worksheet("Inventario")


# @st.cache_data(ttl=60)
def show_inventory():
    inventory = Inv_sheet.get_all_records()
    return inventory


def update_inventory(inout, product, categoria, miembro, banana, cantidad):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sheet = Ent_sheet if inout == "Entrada" else Out_sheet
    id = fn.create_ID(sheet, categoria, miembro, banana)
    # st.write(f"{inout} de {cantidad} {miembro} de {banana}, ID: {id}")
    cant = -cantidad if inout == "Salida" else cantidad
    done = False
    if inout == "Entrada":
        if categoria == "Componentes":
            data = [id, fecha, categoria, miembro, banana, cantidad]
            done = fn.Add_Comp(Inv_sheet, id, categoria, miembro, banana, cant)

        if categoria == "Insumos":
            data = [id, fecha, categoria, "", "", "", miembro, banana, cantidad]
            done = fn.Add_Insu(Inv_sheet, id, categoria, miembro, banana, cant)

    if inout == "Salida":
        if categoria == "Componentes":
            data = [fecha, product, categoria, miembro, banana, cantidad]
            done = fn.Add_Comp(Inv_sheet, id, categoria, miembro, banana, cant)
            if not done:
                st.error(
                    f"No existen suficientes componentes para realizar la operación!",
                    icon="🚨",
                )

        if categoria == "Insumos":
            data = [fecha, product, categoria, "", "", "", miembro, banana, cantidad]
            done = fn.Add_Insu(Inv_sheet, id, categoria, miembro, banana, cant)
            if not done:
                st.error(
                    f"No existen suficientes insumos para realizar la operación!",
                    icon="🚨",
                )

    try:
        sheet.append_row(data)
        inventory = show_inventory()
        if done:
            st.success("Operación realizada correctamente!", icon="✅")
        # st.balloons()
        return inventory

    except Exception as e:
        # Print the error message
        st.error(f"Error {e}", icon="🚨")


def select_component(inout, product, inventory):
    categorias = ["Componentes", "Insumos"]
    categoria = st.selectbox("Seleccione categoría", categorias)
    familia = (
        Config.familia_insumos if categoria == "Insumos" else Config.familia_componentes
    )

    miembro = st.selectbox("Seleccione familia de insumo", familia.keys())
    banana = st.selectbox("Seleccione producto", familia[miembro])
    cantidad = st.number_input(f"Ingrese la cantidad de {miembro}", 0, 1000000, 1)

    return inout, product, categoria, miembro, banana, cantidad, inventory


def main():
    im = Image.open("assets/logos/favicon.png")

    st.set_page_config(
        page_title="Inventario",
        page_icon=im,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Sistema de Inventario :blue[Lanek] :package:")

    inventory = show_inventory()

    inout = ["Entrada", "Salida"]
    operacion = st.selectbox("Seleccione operación a realizar", inout)

    if operacion == "Entrada":
        (
            inout,
            product,
            categoria,
            miembro,
            banana,
            cantidad,
            inventory,
        ) = select_component(operacion, None, inventory)

    if operacion == "Salida":
        productos = ["AVM", "ABMA"]
        producto = st.selectbox("Seleccione producto", productos)
        (
            inout,
            product,
            categoria,
            miembro,
            banana,
            cantidad,
            inventory,
        ) = select_component(operacion, producto, inventory)

    if st.button("Enviar Inventario"):
        inventory = update_inventory(
            inout, product, categoria, miembro, banana, cantidad
        )

    if st.button("Actualizar Inventario"):
        inventory = show_inventory()

    st.dataframe(inventory)


if __name__ == "__main__":
    main()
