from environs import Env


def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    return {'Token': env.str('Token'),
            'host': env.str('host'),
            'user': env.str('user'),
            'password': env.str('password'),
            'db_name': env.str('db_name')}
