from peewee import Model, CharField, IntegerField, TimestampField

from utils.DataStore import db


class User(Model):
    id = CharField(null=False, unique=True, primary_key=True)
    # La puntuación del usuario.
    score = IntegerField(default=0)
    # Cuando el usuario envía un mensaje y recibe puntos, será estrangulado hasta que vuelva a recibir puntos
    throttled_until = TimestampField(null=True)

    class Meta:
        database = db
