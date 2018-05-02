import os
import logging

import yaml



def load_config(file_path):
    with open(file_path, 'r') as conf_file:
        config = yaml.load(conf_file)
    return config


def get_config():
    log = logging.getLogger()
    config = {}
    try:
        config = load_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.yaml'))
    except FileNotFoundError:
        pass
    except yaml.YAMLError:
        log.error('Failed to load config, incorrect format. Trying to load from ENV variables')

    config.update(_load_from_env(['DB_NAME', 'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'GIF_URL', 'HOST',
                                  'UPLOAD_FOLDER', 'UPLOAD_URL', 'RESOURCES_DIR', 'SECRET_KEY',
                                  'VERSION', 'SECURE', 'FONT_UPLOAD_FOLDER', 'GIF_FOLDER', 'PROD', 'CACHE_LIFETIME']))
    return config


def _load_from_env(keys):
    env_config = {}

    for key in keys:
        env_value = os.environ.get(key)

        if env_value:
            env_config[key] = env_value

    return env_config


def get_test_config():
    config = get_config()
    config['DB_NAME'] = 'test_database'
    config['FONT_UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), './../fonts')
    config['GIF_FOLDER'] = '/tmp'
    config['PROD'] = False
    config['HOST'] = None
    config['RESOURCES_DIR'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), './../tests/functional/')
    return config