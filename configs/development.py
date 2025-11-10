#! /home/wangdy/miniconda3/bin/python
# -*- coding: UTF-8 -*-

# FileName     : development
# Author       : EastsunW eastsunw@foxmail.com
# Create at    : 2022-04-23 00:37
# Last Modified: 2022-04-23 00:37
# Modified By  : EastsunW
# -------------
# Description  :
# -------------
from configs.default import Config
from urllib.parse import quote

class DevelopmentConfig(Config):
    DEBUG     = True
    ENV       = "development"
    # mongodb
    username = quote('wuxh')
    password = quote('GlKj5t3NToQIevggauyt')

    MONGO_URI      = 'mongodb://{}:{}@mongodb:27017/wuxh_database'.format(username, password)


