#! /home/wangdy/miniconda3/bin/python
# -*- coding: UTF-8 -*-

# FileName     : config
# Author       : EastsunW eastsunw@foxmail.com
# Create at    : 2022-04-22 17:49
# Last Modified: 2022-04-22 17:49
# Modified By  : EastsunW
# -------------
# Description  : 用来创建flask的设置
# -------------
from .development import DevelopmentConfig
from .production import ProductionConfig

current_config = {
    'development': DevelopmentConfig,
    'production' : ProductionConfig,
    'default'    : ProductionConfig
}
