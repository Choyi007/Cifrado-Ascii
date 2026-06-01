    import json
    import Levenshtein
    import os
    import time
    import subprocess
    import pyperclip

    import ctypes

    ctypes.windll.kernel32.SetConsoleTitleW(
        "DataVault v1.0 - Secure Data Manager"
    )

    ErrorCode = {
        200:"ok",
        201:"Manipulado",
        404:"No existe",
        405:"Error de Formato"
        }

    #Internal Library
    from Cipher import Encripter, Decripter
    from Cipher import SelfTest as CipherST
    from UserInteractions import ConfirmationMessage, ImportantQuestion
    from JsonModule import CreateJson,WaitForDisk,LoadJson,SaveData
    from TimeStapModule import safe_ctime

    #External Library
    from colorama import init, Fore, Back, Style

    CipherST()

    init(autoreset=True,strip=True)

    CompleteDR =r"C:\Users\igoli\Documents\Documentos\Datos_OlivoVazquezIsaíasGuillermo.json"
    CompleteLR = r"C:\Users\igoli\Documents\Documentos\Logs_Data.json"
    DataRute = r"Datos_OlivoVazquezIsaíasGuillermo.json"
    LogsRute = r"Logs_Data.json"
    USBdRute = r"D:\DataVault\config.json"



Data, Success = LoadJson(DataRute, {})
if not Success:
    Data = {}

Logs, Success2 = LoadJson(LogsRute, [])
if not Success2:
    Logs = []

DcrD, Success3 = WaitForDisk(USBdRute, {}, "r", None)
if not Success3:
    DcrD = {}

#print(Data)

def AdvancedSearch(Key1):
    mk = None
    mv = float("inf")

    for Key2 in Data:

        if Key1.lower() == Key2.lower():
            return Key2

        ld = Levenshtein.distance(
            Key1.lower(),
            Key2.lower()
        )

        if ld < mv:
            mk = Key2
            mv = ld

    if mv < 10:
        return mk

    return None

def GetKV(Key):
    try:
        DData,s = Decripter(Data[Key])
        if s!=72:
            return DData, 201
        return DData, 200
    except KeyError:
        return None,404
    except ValueError:
        return None,405
    
def PrintKV(Key):

    DData, response = GetKV(Key)

    if response >=400 and response <500:
        return response

    print(
        "╔═══════════════════════\n"
        f"║ 🔑 {Key}:\n"
        f"║     🪪 {DData}\n"
        "╚═══════════════════════"
    )
    pyperclip.copy(DData)
    print("📋 Dato copiado al portapapeles")

    return response

def Open(Key):
    s2 = PrintKV(AdvancedSearch(DataN))
    if s2==404:
        print(Fore.RED + "⛔️ Not Exist")
    elif s2==405:
        print(Fore.RED + "⛔️ the data is illegible")
    elif s2==201:
        print(Fore.YELLOW+"⚠ Warning, possible data manipulation")


Logs.append(f"{safe_ctime()} | System Init")
SaveData(Logs,LogsRute)

print(Style.DIM+"Type ? or Help to open Guide")

while True:
    CMD = input(">>>")
    Logs.append(f"{safe_ctime()} | {CMD}")
    SaveData(Logs,LogsRute)
    
    if CMD.lower().startswith("open"):
        
        DataN = CMD[4:].strip(" :")
        Open(DataN)
        
    elif CMD.lower()=="add":
        Success1 = False
        while not Success1:
            Key, Success1 = ImportantQuestion("🔑 Key","str")
            if Key in Data:
                Success1 = False
                print(Fore.YELLOW + "⚠ la llave actual ya esa en uso")
                r = ConfirmationMessage("Deseas Remplazar el valor de la llave?","")
                if r in ["y","yes"]:
                    Success1 = True
        if Success1:
            Val, Success2 = ImportantQuestion("🪪 Data","str")
            if Success2:
                Data[Key]=Encripter(Val)
                SS = SaveData(Data,DataRute)
                if SS:
                    print(Fore.GREEN+"✅ Adicion Guardada con Exito")
                else:
                    print(Fore.RED + "❌ Error al Guardar la llave")
    elif CMD.lower()=="delete":
        s = False
        while not s:
            DataN = input("🔑 Key: ")
            try:
                Data[DataN]
                s = True
                ItemS,response=GetKV(DataN)
                if not ItemS:
                    ItemS = ErrorCode[response]
                if response == 201:
                    print(Fore.YELLOW+"⚠ Warning, possible data manipulation")
                a = ConfirmationMessage("\n⚠️  Are you sure you want to delete this item: \n{}\n\n» ",str(ItemS))
                if a == "y":
                    a2 = input("\n🔐  Confirm by typing 1234:\n\n» ")
                    if a2 == "1234":
                        print("\n🗑️Deleting Item...")
                        del Data[DataN]
                        print(Fore.GREEN+"✅  Data Deleted")
                        SaveData(Data,DataRute)
                    else:
                        print("🚫  Canceling Operation")
                else:
                    print("🚫  Canceling Operation")
            except KeyError:
                print(Fore.RED+"⛔ Not Exist")
    elif "?" in CMD or CMD == "Help":
        print("≡ to see a piece of data, insert its key as follows: [Open: Key]")
        print("≡ to add a piece of data, type the command [Add] and follow the instructions")
        print("≡ to delete a piece of data, type the [Delete] command and follow the instructions")
    else:
        print(Fore.RED+"❓ Comando desconocido. Escribe ? o Help")
        
