#! /home/wangdy/miniconda3/bin/python
# -*- coding: UTF-8 -*-

# FileName     : production
# Author       : EastsunW eastsunw@foxmail.com
# Create at    : 2022-04-23 00:37
# Last Modified: 2022-04-23 00:37
# Modified By  : EastsunW
# -------------
# Description  :
# -------------
from configs.default import Config

class ProductionConfig(Config):
    DEBUG     = False
    ENV       = "production"
    MONGO_URI = "mongodb://wuxh:GlKj5t3NToQIevggauyt@localhost:30000/wuxh_database"
