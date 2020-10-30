from models.Models import Models
from models.std_models.User import User


class StdModels(Models):
    def get(self):
        """
        :return: Todos los modelos a utilizar.
        """
        return [User]
