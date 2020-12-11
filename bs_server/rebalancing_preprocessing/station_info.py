# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: station_info.py
@time: 2020/10/08
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""

from dataclasses import dataclass

from sqlalchemy import Column, Integer, Float, Boolean, MetaData, create_engine
from sqlalchemy.orm import registry, sessionmaker

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Station:
    __tablename__ = 'Station'

    id = Column(Integer, primary_key=True)
    demand = Column(Integer)
    max_capacity = Column(Integer)
    bike_count = Column(Integer)
    ratio = Column(Float)
    diversity = Column(Float)
    full_empty_time = Column(Float)
    warning_time = Column(Float)
    latest_time = Column(Float)
    cluster = Column(Integer)
    priority = Column(Float)
    velocity = Column(Float)
    key_distance = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    past_rent_01 = Column(Float)
    past_rent_02 = Column(Float)
    past_rent_03 = Column(Float)
    past_rent_04 = Column(Float)
    past_return_01 = Column(Float)
    past_return_02 = Column(Float)
    past_return_03 = Column(Float)
    past_return_04 = Column(Float)
    pred_rent_01 = Column(Float)
    pred_rent_02 = Column(Float)
    pred_rent_03 = Column(Float)
    pred_rent_04 = Column(Float)
    pred_return_01 = Column(Float)
    pred_return_02 = Column(Float)
    pred_return_03 = Column(Float)
    pred_return_04 = Column(Float)
    visited = Column(Boolean, default=False)

    def to_json(self):
        dicts = self.__dict__
        if "_sa_instance_state" in dicts:
            del dicts["_sa_instance_state"]
        return dicts

    def dump_to_json(self):
        return {
            'id': self.id,
            'full_empty_time': self.full_empty_time,
            'max_capacity': self.max_capacity,
            'bike_count': self.bike_count,
            'priority': self.priority,
            'diversity': self.diversity,
            'velocity': self.velocity,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'demand': self.demand
        }

metadata = MetaData()

# 初始化数据库连接:
# engine = create_engine('mysql+mysqldb://root:95930908@localhost:3306/bikeshare_docked')
# 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)

# Station.__table__.create(engine)
