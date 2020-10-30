import colorama
from colorama import Style

class Logger:
    """
    Helper Class for logging.
    """

    __separador = '--------------------------------------------------------------------------------------------------'

    @staticmethod
    def separador(color: str = colorama.Fore.RESET):
        print(f'{color}{Logger.__separador}')

    @staticmethod
    def error(mensage: str, separador: bool = False, newline: bool = True):
        """
        Imprime el mensaje dado en la consola. Colorea el texto en rojo.
        :mensaje param: Mensaje para imprimir.
        :param separador: alternar separador.
        :param nueva línea: alternar nueva línea.
        :return:
        """
        Logger.print("❌   "+mensage, colorama.Fore.RED, separador, newline)

    @staticmethod
    def success(mensage: str, separador: bool = False, newline: bool = True):
        """
        Imprime el mensaje dado en la consola. Colorea el texto en verde.
        : mensaje param: Mensaje para imprimir.
        : param separador: alternar separador.
        : param nueva línea: alternar nueva línea.
        :return:
        """
        Logger.print(mensage, colorama.Fore.GREEN, separador, newline)

    @staticmethod
    def info(mensage: str, separador: bool = False, newline: bool = True):
        """
        Imprime el mensaje dado en la consola.
        : mensaje param: Mensaje para imprimir.
        : param separador: alternar separador.
        : param nueva línea: alternar nueva línea.
        :return:
        """
        Logger.print("🛈   INFO: "+mensage, colorama.Fore.RESET, separador, newline)

    @staticmethod
    def warning(mensage: str, separador: bool = False, newline: bool = True):
        """
        Imprime el mensaje dado en la consola. Colorea el texto de amarillo.
        : mensaje param: Mensaje para imprimir.
        : param separador: alternar separador.
        : param nueva línea: alternar nueva línea.
        :return:
        """
        Logger.print("⚠️   WARNICION: " + mensage, colorama.Fore.YELLOW, separador, newline)

    @staticmethod
    def print(mensage: str, color: str, separador: bool = False, newline: bool = True):
        """
        Imprime el mensaje dado en la consola con el color dado.
        : mensaje param: Mensaje para imprimir.
        : param color: Color en el que se imprimirá el mensaje.
        : param separador: alternar separador.
        : param nueva línea: alternar nueva línea.
        :return:
        """
        mensage = f'{color}{Logger.__get_separated_message(mensage) if separador else mensage}{Style.RESET_ALL}'
        if newline:
            print(mensage)
        else:
            print(mensage, end='')

    @staticmethod
    def __get_separated_message(mensage: str):
        """
        Agrega separador al mensaje dado.
        : param mensage: mensage para poner entre medio.
        : retorno: mensaje separado.
        """
        return f'{Logger.__separador}\n{mensage}\n{Logger.__separador}'
