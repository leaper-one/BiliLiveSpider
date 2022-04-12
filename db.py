from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from sqlalchemy.orm import sessionmaker

__all__ = (
    'SQLControl',
)

engine = create_engine(r'sqlite:///db.sqlite3')

Base = declarative_base()


# 定义Rank表
class modelRank(Base):
    __tablename__ = 'model_rank'
    # 表结构
    id = Column(Integer, primary_key=True)
    uid = Column(String(100))
    room_id = Column(String(100))
    rank = Column(Integer, default=0)
    qn = Column(Integer, default=0)
    ts = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))


class SQLControl:

    def __init__(self):
        # 定义Rank表中rank字段的范围
        self.max = int(10E8)
        self.min = int(0)
        self.add = int(10E6)

        # 连接数据库
        self.__Session = sessionmaker(bind=engine)
        self.__session = self.__Session()

    # 通过room_id来删除数据，用于直播结束时
    def del_by_room_id(self, room_id: str):
        search = self.__session.query(modelRank).filter(modelRank.room_id == room_id)
        if search:
            search.delete()
            self.__session.commit()

    # 排名主要方法，请传入参数直播间room_id、用户的uid以及增加的qn值（注意不是增加后的qn值
    def rank(self, room_id: str, uid: str, qn: int):
        search = self.__session.query(modelRank).filter(modelRank.uid == uid and modelRank.room_id == room_id).first()
        if search:
            self.__update_func(room_id, uid, qn)
        else:
            self.__create_func(room_id, uid, qn)

    def __update_func(self, room_id: str, uid: str, qn: int):
        _qn = self.__session.query(modelRank).filter(modelRank.uid == uid and modelRank.room_id == room_id).first().qn
        self.__session.query(modelRank).filter(modelRank.uid == uid).delete()
        self.__session.commit()
        self.__create_func(room_id, uid, qn=qn + _qn)  # 将原qn值添加后传入creat_func处理

    def __create_func(self, room_id: str, uid: str, qn: int):
        rank = 0
        search = self.__session.query(modelRank).order_by(modelRank.rank.desc() and modelRank.room_id == room_id).all()
        if search:
            if qn > search[0].qn:
                rank = search[0].rank + self.add
            elif qn < search[-1].qn:
                rank = search[-1].rank - self.add
            elif len(search) == 1:
                if qn >= search[0].qn:
                    rank = search[0].rank + self.add
                else:
                    rank = search[0].rank - self.add
            else:
                for i in range(len(search)):
                    if search[i].qn >= qn >= search[i + 1].qn:
                        rank = (search[i].rank + search[i + 1].rank) / 2
                        break
            self.__session.add(modelRank(room_id=room_id, uid=uid, rank=int(rank), qn=qn))
            self.__session.commit()
        else:
            rank = (max - min) / 2
            self.__session.add(modelRank(room_id=room_id, uid=uid, rank=rank, qn=qn))
            self.__session.commit()


# 直接运行该文件将会创建表
if __name__ == '__main__':
    Base.metadata.create_all(engine)
