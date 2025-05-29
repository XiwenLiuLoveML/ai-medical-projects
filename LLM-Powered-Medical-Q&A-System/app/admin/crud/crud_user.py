# 📁 app/admin/crud/crud_user.py
# 📝 本文件为医疗 LLM Q&A 系统公开版本，演示最小化的用户管理 CRUD 功能
# 用于演示登录注册流程中的数据操作部分（配合 schema.user, model.sys_user 使用）

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from app.admin.model import User
from app.admin.schema.user import RegisterUserParam
from common.security.jwt import get_hash_password


class CRUDUser(CRUDPlus[User]):
    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        return await self.select_model_by_column(db, username=username)

    async def create(self, db: AsyncSession, obj: RegisterUserParam) -> None:
        salt = bcrypt.gensalt()
        obj.password = get_hash_password(f'{obj.password}', salt)
        dict_obj = obj.model_dump()
        dict_obj.update({'salt': salt, 'is_staff': True})
        db.add(self.model(**dict_obj))


# 注册为 DAO 实例
user_dao: CRUDUser = CRUDUser(User)
