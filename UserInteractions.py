def ConfirmationMessage(Message, Extra):
    s2=False

    while not s2:
        A2=input(Message.replace("{}",Extra))
        A2=A2.lower()
        
        if A2 in ["y","yes","n","not","c","cancell"]:
            s2 = True
            if A2 in ["y","yes"]:
                return "y"
            elif A2 in ["n","not"]:
                return "n"
            elif A2 in ["cancell","c"]:
                return "c"

tipos_validos = {
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "tuple": tuple,
    "set": set,
    "dict": dict
}

def ImportantQuestion(Text, Type):
    s = False
    while not s:
        Answere = input(Text+": ")
        try:
            if Type == "bool":
                Answere = Answere.lower() in ["true","1","yes","y"]
            else:
                Answere = tipos_validos[Type](Answere)
        except ValueError:
            print(Fore.RED + "⛔️ Error Transforming")
            continue
        if Type == "str" and Answere.strip() == "":
            print("⛔ El valor no puede estar vacío")
            continue
        
        if isinstance(Answere, tipos_validos[Type]):
            r = ConfirmationMessage("do you want to use this value: ({}) ❓ \n (y,n,cancell)",Answere)
            if r == "y":
                return Answere, True
            elif r == "n":
                print("↩️ Returning to question")
            elif r == "c":
                print("🚫 Cancelling Operation")
                return None, False
