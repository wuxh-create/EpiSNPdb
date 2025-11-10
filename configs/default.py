#! /home/wangdy/miniconda3/bin/python
# -*- coding: UTF-8 -*-

# FileName     : default
# Author       : EastsunW eastsunw@foxmail.com
# Create at    : 2022-04-23 00:40
# Last Modified: 2022-04-23 00:40
# Modified By  : EastsunW
# -------------
# Description  :
# -------------

class Config:
    ENV          = "default"
    RESTFUL_JSON = dict(ensure_ascii=False)
    @staticmethod
    def init_app(app):
        pass
