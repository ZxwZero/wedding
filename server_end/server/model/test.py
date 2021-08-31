# coding=utf-8
# python3

"""
Name: test.py
Author: zhengxiangwei
Time: 2021-08-30 17:46
Desc:
"""

# coding=utf-8
# python3

"""
Name: model_role_login.py
Author: zhengxiangwei
Time: 2021-08-26 10:40
Desc:
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, SMALLINT, BigInteger, Table  # 定义字段
from server_end.server.common.connect import Base, session
from sqlalchemy.orm import relationship


# Create your models here.
class BaseModel:
    id_delete = Column(Boolean, default=False)
    createdAt = Column(DateTime, nullable=False)  # 创建时间
    updatedAt = Column(DateTime, nullable=False, onupdate=True)  # 修改时间


# 用户to角色表(多对多中间表)
UserRoles = Table(
    'users_roles',
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id"))
    )


# 角色to权限表(多对多中间表)
RolePermission = Table(
    "roles_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id"))
    )


# 定义用户数据模型
class Users(BaseModel, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)  # 昵称
    pwd = Column(String(255), nullable=False)  # 密码
    email = Column(String(100), nullable=False, unique=True)  # 邮箱
    phone = Column(String(11), nullable=False, unique=True)  # 手机
    face = Column(String(100), nullable=True)  # 头像
    info = Column(String(600), nullable=True)  # 个性签名
    roles = relationship("Roles", secondary="users_roles", backref="users")
    desc = Column(String(128))

    @classmethod
    def create_user(cls, user_dict):
        person = Users(**user_dict)
        session.add(person)
        session.commit()


# 定义角色模型
class Roles(BaseModel, Base):
    RoleSymbolMap = {
        0: "visitor",  # 访客
        1: "editor",  # 维护人员
        2: "administrator",  # 管理员
        3: "root",  # 超级管理员
    }

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    role_symbol = Column(Integer, default=0)
    permissions = relationship("Permissions", secondary="roles_permission", backref="roles")
    desc = Column(String(128))


# 定义权限模型
class Permissions(BaseModel, Base):
    PermissionSymbolMap = {
        0: "find",  # 查看
        1: "edit",  # 编辑
        2: "delete",  # 删除
    }

    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    desc = Column(String(128))


# 创建表
if __name__ == "__main__":
    Base.metadata.create_all()  # 去数据库里面创建所有的表

