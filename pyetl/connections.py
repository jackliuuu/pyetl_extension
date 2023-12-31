# -*- coding: utf-8 -*-
"""
@time: 2020/6/4 11:04 下午
@desc:
"""
from pydbclib import connect, Database
from sqlalchemy import engine
from confluent_kafka import Consumer
from pyetl.es import Client


class DatabaseConnection(object):

    def __init__(self, db):
        if isinstance(db, Database):
            self.db = db
        elif isinstance(db, engine.base.Engine) or hasattr(db, "cursor"):
            self.db = connect(driver=db)
        elif isinstance(db, dict):
            self.db = connect(**db)
        elif isinstance(db, str):
            self.db = connect(db)
        else:
            raise ValueError("db 参数类型错误")


class ElasticsearchConnection(object):
    _client = None

    def __init__(self, es_params=None):
        if es_params is None:
            es_params = {}
        self.es_params = es_params

    @property
    def client(self):
        if self._client is None:
            self._client = Client(**self.es_params)
        return self._client
    
    
class KafkaConnection(object):
    def __init__(self, consumer_config):
        self.consumer_instance = None
        self.consumer_config = consumer_config
    def get_consumer(self):
        if self.consumer_instance is None:
            # 创建 Kafka Consumer 连接
            self.consumer_instance = Consumer(self.consumer_config)
        return self.consumer_instance