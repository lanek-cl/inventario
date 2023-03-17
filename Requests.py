import functions as func

# Ent_sheet = sh.worksheet('Entradas')
# Inv_sheet = sh.worksheet('Inventario')


# last_entry = Ent_sheet.col_values(1)[-1]
# last_entry_qty = Ent_sheet.col_values(7)[-1]

# print(str(len(Ent_sheet.col_values(1)))+" "+last_entry+" "+last_entry_qty)
# print(last_row)
# Inv_sheet.append_row([100, 'holamundo', 3, 4, 5])


def New_entry(Ent, Inv):
    # 1: ID, 2: TimeStamp, 3: Cat, 4: Comp_Fam, 5: Comp_Desc, 6: Comp_Cant
    # 7: Insu_Fam, 8: Insu_Desc, 9: Insu_Cant
    last_entry_cat = Ent.col_values(3)[-1]
    # last_entry_pro = Ent.col_values(4)[-1]
    Last_row = len(Ent.col_values(2))

    if last_entry_cat == "Componente":
        last_entry_fam = Ent.col_values(4)[-1]
        last_entry_des = Ent.col_values(5)[-1]
        last_entry_qty = Ent.col_values(6)[-1]

        id = func.create_ID(Ent, last_entry_cat, last_entry_fam, last_entry_des)

        Ent.update_cell(Last_row, 1, id)

        func.Add_Comp(
            Inv, id, last_entry_cat, last_entry_fam, last_entry_des, int(last_entry_qty)
        )

    elif last_entry_cat == "Insumo":
        last_entry_fam = Ent.col_values(7)[-1]
        last_entry_des = Ent.col_values(8)[-1]
        last_entry_qty = Ent.col_values(9)[-1]

        id = func.create_ID(Ent, last_entry_cat, last_entry_fam, last_entry_des)

        Ent.update_cell(Last_row, 1, id)

        func.Add_Insu(
            Inv, id, last_entry_cat, last_entry_fam, last_entry_des, int(last_entry_qty)
        )

    # print(str(len(Ent_sheet.col_values(1)))+" "+last_entry+" "+last_entry_qty)
    with open("entries.txt", "a") as file:
        file.write(id + "\n")

    return True


def New_out(Out, Inv):
    # 1: TimeStamp, 2: Prod, 32: Cat, 4: Comp_Fam, 5: Comp_Desc, 6: Comp_Cant
    # 7: Insu_Fam, 8: Insu_Desc, 9: Insu_Cant
    last_out_cat = Out.col_values(3)[-1]
    # last_entry_pro = Ent.col_values(4)[-1]
    Last_row = len(Out.col_values(1))

    if last_out_cat == "Componente":
        last_out_fam = Out.col_values(4)[-1]
        last_out_des = Out.col_values(5)[-1]
        last_out_qty = Out.col_values(6)[-1]

        id = func.create_ID(Out, last_out_cat, last_out_fam, last_out_des)

        # print('Componente '+id+' out')

        func.Add_Comp(
            Inv, id, last_out_cat, last_out_fam, last_out_des, -int(last_out_qty)
        )

    elif last_out_cat == "Insumo":
        last_out_fam = Out.col_values(7)[-1]
        last_out_des = Out.col_values(8)[-1]
        last_out_qty = Out.col_values(9)[-1]

        id = func.create_ID(Out, last_out_cat, last_out_fam, last_out_des)

        # print('Insumo '+id+' out')

        func.Add_Insu(
            Inv, id, last_out_cat, last_out_fam, last_out_des, -int(last_out_qty)
        )

    with open("outs.txt", "a") as file:
        file.write(id + "\n")

    # print(str(len(Ent_sheet.col_values(1)))+" "+last_entry+" "+last_entry_qty)
    return True
