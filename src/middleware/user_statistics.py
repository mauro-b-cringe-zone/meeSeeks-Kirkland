from models.std_models.User import User
from datetime import datetime, timedelta

from utils.Environment import env


async def run(message):
    if not message.author.bot:
        # Obtenga al usuario de la base de datos y verifique si está limitado
        user, is_new_user = User.get_or_create(id=message.author.id)
        current_time = datetime.now()
        is_throttled = current_time < user.throttled_until

        if not is_throttled:
            # Agregue puntos y establezca la marca de tiempo del acelerador

            try:
                user_stats_increment: int = int(env.get('USER_STATISTICS_INCREMENT'))
            except EnvironmentError:
                user_stats_increment: int = 1

            try:
                user_stats_throttle_duration: int = int(env.get('USER_STATISTICS_THROTTLE_DURATION'))
            except EnvironmentError:
                user_stats_throttle_duration: int = 5

            user.score += user_stats_increment
            user.throttled_until = current_time + timedelta(seconds=user_stats_throttle_duration)

        user.save()

        # print("{} tiene {} puntos".format(user.id, user.score))
