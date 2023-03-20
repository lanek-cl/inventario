def create_ID(sheet, Cat, Fam, Des):
    try:
        id = Cat[:4] + "-" + Fam[:3] + "-" + Des
        id = "".join(id.split())
        # sheet.update_cell(row, 1, id)
        print(f"ID: {id}")
        return id
    except Exception as e:
        # Print the error message
        print("An error occurred:", str(e))
        return False


def Add_Comp(sheet, id, cat, fam, des, qty):
    try:
        cell = sheet.find(id)
        row = cell.row
        current_qty = sheet.cell(row, 6).value  # col 7 is the qty data
        if int(current_qty) + qty >= 0:
            sheet.update_cell(row, 6, int(current_qty) + qty)
            return True
        else:
            return False
    except Exception as e:
        # Handle the exception
        print(e)
        print(f"The value '{id}' was not found in the sheet. Adding...")
        sheet.append_row([id, cat, fam, des, "", qty])
        return None


def Add_Insu(sheet, id, cat, fam, des, qty):
    try:
        cell = sheet.find(id)
        row = cell.row
        current_qty = sheet.cell(row, 6).value  # col 7 is the qty data
        if int(current_qty) + qty >= 0:
            sheet.update_cell(row, 6, int(current_qty) + qty)
            return True
        else:
            return False
    except Exception as e:
        # Handle the exception
        print(e)
        print(f"The value '{id}' was not found in the sheet. Adding...")
        sheet.append_row([id, cat, fam, des, "", qty])
        return None
