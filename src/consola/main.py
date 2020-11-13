import os, time, sys
from termcolor import cprint


class CrearEnv():
    def __init__(self, directorio):
        self.directorio = directorio

    def checkearPlataforma(self):
        if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  
            return "win"
        else:
            return "lin"

    def inizializar(self):
        if self.checkearPlataforma == "win":
            os.system("py -m pip install --user virtualenv")
            os.system("py -m venv env") 
        elif self.checkearPlataforma == "lin":
            os.system("python3 -m pip install --user virtualenv")
            os.system("python3 -m venv env ")
        cprint("\nAhora pon en la consola verdadera \"source env/bin/activate\" ara activarlo SI ESTAS EN LINUX", "green")
        cprint("Ahora pon en la consola verdadera \".\env\Scripts\activate\" ara activarlo SI NO ESTAS EN LINUX", "green")
        cprint("\nPuedes poner 'deactivate' para quitar el virtual env\n", "green")

class Consola():
    def __init__(self, comando):
        self.comando = comando.lower()
        self.comandos = [["empezar", "run"], ["cls", "clear"], "pip", ["exit", "salir", "exit()"], "instalar", "python", ["help", "ayuda"], "instrucciones", "env"]

    def pip(self, pack):
        if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  
            os.system(f"pip install {pack}")
        else:
            os.system(f"pip3 install {pack}")

    def python(self):
        if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  
            os.system(f"python")
        else:
            os.system(f"python3")

    def instrucciones(self, dir):
        cprint(f"\nTutorial de como usar Maubot\n\n1. Ve ha 'https://asciinema.org/a/P8nJyagpVvdjVmj1nPnKHCyHy' y sigue las instrucciones\n2. Rellena todo lo que necesites en {dir}.example.env rellenalo y camviale el nombre a .env\n3. ve ha {dir}\launcher.py \n4. Pon en la consola python launcher.py y despues pon 'run' \n", "green")

    def procesar_comandos(self, directorio):
        if self.comando == "":
            return True
        
        elif self.comando == self.comandos[0][0] or self.comando == self.comandos[0][1]:
            cprint("\nCTRL + C para parar el programa e iniciar la consola\n", "red")
            time.sleep(1)
            return "preparacion"
        
        elif self.comando == self.comandos[1][0] or self.comando == self.comandos[1][1]:
            if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  
                os.system("cls")
            else:
                os.system("clear")
        
        elif self.comando.startswith("pip"):
            mod = self.comando.split("pip")
            if len(mod) <= 1.0:
                return cprint("\nAñade un argumento\n", "red")
            self.pip(mod[1])
        
        elif self.comando == self.comandos[3][0] or self.comando == self.comandos[3][1]:
            cprint("\nSi quieres salir del programa deverias de poner \"exit()\"\n", "yellow")

        elif self.comando == self.comandos[4]:
            if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  
                os.system(f"pip install -r requirements.txt")
            else:
                os.system(f"pip3 install -r requirements.txt")
            cprint(f"\n\n1. AHORA VE HA '{directorio}\.example.env' \n2. RELLENA TODO LO NECESARIO Y YA DE PASO CAMBIA EL '{directorio}\.example.env' A '{directorio}\.env' \n\n", "green")
        
        elif self.comando == self.comandos[5]:
            self.python()
        
        elif self.comando == self.comandos[3][2]:
            sys.exit(0)

        elif self.comando == self.comandos[7]:
            self.instrucciones(directorio)

        elif self.comando == self.comandos[6][1] or self.comando == self.comandos[6][0]:
            cprint("\nAyuda:\n-> exit() - Se sale del programa\n-> pip <modulo> - Instalar un modulo con pip\n-> cls (clear) - Limpiar la consola\n-> run (empezar) - Correr maubot\n-> instalar - Instalar lo necesario para maubot (RECOMENDABLE SI ES LA PRIMERA VEZ QUE USAS MAUBOT)\n-> help (ayuda) - Enseña este mensage\n-> instrucciones - Te esñara como utilizar maubot\n-> env - Empezar el 'virtual enviroment'\n", "green")
        
        elif self.comando == self.comandos[8]:
            CrearEnv(directorio).inizializar()

        else:
            cprint(f"\n{self.comando} no existe:\n-> Prueva a poner \"ayuda\" o \"help\"\n", "red")
