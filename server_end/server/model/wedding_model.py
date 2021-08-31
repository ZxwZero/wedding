# coding=utf-8
# python3

"""
Name: wedding_model.py
Author: zhengxiangwei
Time: 2021-08-30 17:48
Desc:
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, SMALLINT, BigInteger, Table  # 定义字段
from server_end.server.common.connect import Base, session
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class BaseModel:
    id_delete = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())  # 修改时间


# 定义用户数据模型
class Users(BaseModel, Base):
    who_friend_map = {
        0: "女方",
        1: "男方",
    }
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone = Column(String(11), comment="手机号")  # 手机
    who_friend = Column(Integer, comment="谁的亲属朋友")
    relationship = Column(String(128), comment="与新郎或者新娘的关系")
    congratulation = Column(String(512), comment="送上对新人的祝福吧")

    @classmethod
    def add_user(cls, _dict):
        _dict.update({
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
        })
        _user = Users(**_dict)
        session.add(_user)
        session.commit()


# 创建表
if __name__ == "__main__":
    Base.metadata.create_all()   # 迁移到数据库

