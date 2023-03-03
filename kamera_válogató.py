from tkinter import *
from datetime import datetime


RED = "#FF0000"
GREEN = "#33FF33"
YELLOW = "#FFFF00"


window = Tk()
window.title("Kamera válogatás")
window.geometry("550x350")
window.config(padx=40, pady=40)


"""keresett bárkódok beolvasása txt listából"""
with open("list_of_barcodes.txt") as file:
    list_of_barcodes = file.readlines()
stripped_bc = [bc.strip() for bc in list_of_barcodes]

"""ok darabszám beolvasása"""
with open("ok_barcodes.txt") as file:
    ok_data = file.readlines()
ok_barcodes = len(ok_data)
ok_barcodes_list = [bc[0:16:] for bc in ok_data]
print(f"OK lista: {ok_barcodes_list}")

"""nok darabszám beolvasása"""
with open("nok_barcodes.txt") as file:
    nok_data = file.readlines()
nok_barcodes = len(nok_data)
nok_barcodes_list = [bc[0:16:] for bc in nok_data]
print(f"NOK lista: {nok_barcodes_list}")


"""a már beszkennelt kódok beolvasása, összefűzése egy új listába"""
already_scanned = ok_barcodes_list + nok_barcodes_list
already_scanned_stripped = [bc.strip() for bc in already_scanned]
print(f"Már szkennelve: {already_scanned_stripped}")


def keyboard_language():
    import ctypes

    user32 = ctypes.WinDLL('user32', use_last_error=True)

    # Get the current active window handle
    handle = user32.GetForegroundWindow()

    # Get the thread id from that window handle
    threadid = user32.GetWindowThreadProcessId(handle, 0)

    # Get the keyboard layout id from the threadid
    layout_id = user32.GetKeyboardLayout(threadid)

    # Extract the keyboard language id from the keyboard layout id
    language_id = layout_id & (2 ** 16 - 1)

    # Convert the keyboard language id from decimal to hexadecimal
    language_id_hex = hex(language_id)

    if language_id_hex == "0x40e":
        print(f"A billentyűzet magyarra van állítva! {language_id_hex}")
        return "magyar"


def test_input(barcode):
    scanned_barcode = barcode
    if keyboard_language() == "magyar":
        decision_label.config(text="Magyar a billentyűzet!\n Állítsad át angolra!", width=17, bg=YELLOW, font=("bold", 19))
        entry.delete(0, "end")
        return False

    if scanned_barcode in already_scanned_stripped:
        decision_label.config(text="Már be van szkennelve", width=20, bg=YELLOW, font=("bold", 16))
        entry.delete(0, "end")
        return False

    if len(scanned_barcode) != 16:
        decision_label.config(text="Nem megfelelő karakterszám!", width=22, bg=YELLOW, font=("bold", 16))
        entry.delete(0, "end")
        return False

    return True


def get_info_from_entry(event):
    scanned_barcode = entry.get()
    print(already_scanned_stripped)

    if test_input(scanned_barcode) is False:
        return

    global ok_barcodes, nok_barcodes
    if scanned_barcode in stripped_bc:
        nok_barcodes += 1
        decision_label.config(text="NOK", width=4, bg=RED, font=("bold", 70))
        with open("nok_barcodes.txt", "a") as nok_barcode_list:
            nok_barcode_list.write(f"{scanned_barcode}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if scanned_barcode not in stripped_bc:
        ok_barcodes += 1
        decision_label.config(text="OK", width=4, bg=GREEN, font=("bold", 70))
        with open("ok_barcodes.txt", "a") as ok_barcode_list:
            ok_barcode_list.write(f"{scanned_barcode}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    already_scanned_stripped.append(scanned_barcode)
    print(f"OK: {ok_barcodes}, NOK: {nok_barcodes}")
    entry.delete(0, "end")
    nok_label.config(text=nok_barcodes)
    ok_label.config(text=ok_barcodes)


window.bind("<Return>", get_info_from_entry)


"""WIDGETS"""
nok_label = Label(text=nok_barcodes, bg=RED, width=8)
nok_label.grid(column=0, row=0)

ok_label = Label(text=ok_barcodes, bg=GREEN, width=8)
ok_label.grid(column=3, row=0)

decision_label = Label(text="?", width=4, font=("bold", 70))
decision_label.grid(column=2, row=2, pady=40)

barcode_label = Label(text="Barcode:")
barcode_label.grid(column=1, row=1, pady=30)

entry = Entry(width=40)
entry.grid(column=2, row=1, padx=15)
entry.focus()


window.mainloop()
