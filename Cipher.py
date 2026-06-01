import random
from colorama import init, Fore,Style
init(autoreset=True)

Base = 72

def Encripter(String):
    Seed = Base
    BitStr = []

    for l in String:
        BitStr.append(ord(l))

    for Leve in range(255):
        for index,byte in enumerate(BitStr):
            byte^=Seed
            Seed = (Seed*3 + byte*3 + index*3) % 256
            BitStr[index] = byte
    Txt=""
    for index,_Num in enumerate(BitStr):
        Txt+=f"{BitStr[index]:08b}"
    Txt+=f"{Seed:08b}"
    return(Txt)

def Decripter(Bits):

    if len(Bits) % 8 != 0:
        raise ValueError("Longitud inválida")

    BitStr = []


    TotalBytes = len(Bits)//8
    
    for Build in range(TotalBytes):
        
        Byte = Bits[Build*8:(Build+1)*8]

        if Build < TotalBytes - 1:
            BitStr.append(int(Byte,2))
        else:
            Seed = int(Byte,2)

    for Leve in range(255):
        for index2,byte in enumerate(reversed(BitStr)):
            index = len(BitStr) - 1 - index2
            
            Seed =((Seed - 3*byte - 3*index) * 171) % 256
            byte^=Seed
            BitStr[index] = byte

    Texto = ""

    for byte in BitStr:
        Texto += chr(byte)

    return Texto,Seed

#AutoTest:
class CipherError(Exception):
    pass
class CipherHandlingError(Exception):
    pass

def SelfTest():
    txt=""
    TestSuccess=True
    t5 = "a" * 1000

    tests = [
        "áéíóú",
        "",
        " ",
        "Hello World",
        "Python-12345678",
        "A",
        t5,
        str(random.random())
    ]

    for t in tests:

        enc = Encripter(t)
        dec,c = Decripter(enc)

        if t != dec or c!=Base:
            TestSuccess=False
            if t!=dec:
                raise CipherError(
                    f"Cipher Error\n"
                    f"Original: {repr(t)}\n"
                    f"Decoded : {repr(dec)}"
                )
            elif c!=Base:
                raise CipherHandlingError(
                    "El Archivo Original Fue manipulado"
                )
        if t==dec and c==Base:
            txt+="[s]"
    print(Style.DIM+Fore.BLACK+txt+str(TestSuccess))
            
if __name__ == "__main__":
    SelfTest()

print(Style.DIM+Fore.BLACK+" The library has been successfully loaded: Cypher encryption by Cirsev")
