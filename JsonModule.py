import json
import os
import time
import subprocess

from colorama import init, Fore, Back, Style

def CreateJson(Rute,PreData):
    print("Creando un nuevo archivo...")
    if os.path.isfile(Rute):
        s = ConfirmationMessage(Fore.RED + "⚠  El archivo [{}] ya existe, deseas eliminar el actual?", Rute)
        if not (s in ["y","yes"]):
            raise FileExistsError("⛔ Revise Meticulosamente el .json en busqueda de caracteres que no deban ir ahi.")
        else:
            try:
                os.remove(Rute)
                print(f"\n✅️ Success File Removed: {Rute}")
            except OSError as e:
                print(f"No se pudo eliminar el archivo: {e.strerror}")
    try:
        with open(Rute,"w") as f:
            json.dump(PreData,f,indent=4,ensure_ascii=True)
            print(f"\n✅️ Success Data File Created: {Rute}")
            return True
    except OSError as e:
        raise OSError(Fore.RED + f"⛔️ Error al escribir el archivo JSON: {e}")

def WaitForDisk(Rute,PD,Ty,Data):
    Datos = None
    unidad = Rute[:3]
    s = False
    print("📥 Inserta USB 📥")
    while not s:
        if os.path.exists(unidad):    #"D:\\"):
            s = True
            print("Si")
            time.sleep(0.1)
            if not os.path.isfile(Rute):
                print(Fore.RED + f"⛔  No se encontró el archivo: {Rute}")
                s = CreateJson(Rute,PD)
                if s:
                    if Ty=="r":
                        Datos = PD
                else:
                    raise FileNotFoundError()
            try:
                with open(Rute,Ty) as f:
                    if Ty=="r":
                        Datos =json.load(f)
                    elif Ty=="w":
                        json.dump(Data,f,indent=4, ensure_ascii=False)
            except json.JSONDecodeError as e:
                print(Fore.RED+f"El archivo no contiene JSON válido: {e}\n\n")
                s = CreateJson(Rute,PD)
            except FileNotFoundError:
                print(Fore.RED + f"⛔  No se encontró el archivo: {Rute}")
            except PermissionError or OSError:
                print(Fore.RED + f"⛔  No se puede acceder al archivo: {Rute}")
            time.sleep(0.1)


            unidad_eject =unidad.rstrip("\\")
            subprocess.run([
                "powershell",
                "-Command",
                f"(New-Object -comObject Shell.Application).Namespace(17).ParseName('{unidad_eject}').InvokeVerb('Eject')"
            ])
            time.sleep(0.5)
            print("puedes retirar la USB")
            if Ty=="r" and Datos:
                return Datos, True
            elif Ty=="w":
                return None,True
            else:
                return None,False
                print("No Valid Type")
        else:
            time.sleep(0.25)

def LoadJson(Rute,PD):
    SuccessData = False
    if not isinstance(Rute, str):
        raise TypeError(Fore.RED + "  La ruta debe ser una cadena de texto.")

    if not os.path.isfile(Rute):
        print(Fore.RED + f"⛔  No se encontró el archivo: {Rute}")
        print(f"{Rute[:1]}:\\")
        if Rute.startswith(r"C:\Users\igoli\Documents\Documentos") or os.path.isfile(f"{Rute[:1]}:\\"):
            s = CreateJson(Rute,PD)
            if s:
                return LoadJson(Rute,PD)
            else:
                raise FileNotFoundError()
        else:
            print(Fore.RED + f"⛔  el archivo pertenece a una ubicacion externa: {Rute}")
            return(None,False)
    try:
        with open(Rute) as f:
            return(json.load(f),True)
    except json.JSONDecodeError as e:
        print(Fore.RED+f"El archivo no contiene JSON válido: {e}\n\n")
        s = CreateJson(Rute,PD)
        if s:
            return LoadJson(Rute,PD)
        else:
            raise ValueError("El Error Persiste: {e}")

def SaveData(data, FileRute):
    if not isinstance(data, (dict, list)):
        raise TypeError(Fore.RED + "⛔️ Solo se pueden guardar diccionarios o listas en JSON.")

    try:
        with open(FileRute, "w") as f:
             json.dump(data,f,indent=4, ensure_ascii=True)
    except OSError as e:
        print(Fore.RED + f"⛔️ Error al escribir el archivo JSON: {e}")
        return False
    return True
