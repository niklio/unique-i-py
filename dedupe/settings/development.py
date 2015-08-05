import os

def get_env_setting(setting):
    try:
        return os.environ[setting]
    except KeyError:
        print "Set the %s env variable" % setting

db_user = get_env_setting("DB_USER")
db_passwd = get_env_setting("DB_PASSWD")