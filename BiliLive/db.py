# 导入:
from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker, relationship
from faker import Faker
from sqlalchemy import Column, TIMESTAMP, text
import time

# 创建对象的基类:
engine = create_engine(r'sqlite:///db.sqlite3')
Base = declarative_base()
# 定义Naomi对象:
class Naomi(Base):
    # 表的名字:
    __tablename__ = 'model_naomi'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    uid = Column(String(100))
    qn = Column(Integer, default=0)
    ts = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))


# class Rank(Base):
#     __tablename__ = 'model_rank'
#
#     id = Column(Integer, primary_key=True)
#     uid = Column(String(100))
#     rank = Column(Integer, default=0)

# 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
#
# # 创建session对象:
# session = DBSession()
# # 创建新User对象:
# new_user = Naomi(id='1', uid='34899368', qn='1')
# # 添加到session:
# session.add(new_user)
# # 提交即保存到数据库:
# session.commit()
# # 关闭session:
# session.close()

def update(uid, add_qn=0, table=Naomi):
    Session = sessionmaker(bind=engine)
    session = Session()

    search = session.query(table).filter(table.uid == uid).first()
    if search:
        cock = int(search.qn) + add_qn
        search.qn = cock
        session.commit()
    else:
        session.add(table(uid = uid, qn = add_qn))
        session.commit()
def compare(list1, list2):
    error = []
    error_index = []
    if len(list1) == len(list2):
        for i in range(0, len(list1)):
        #两个列表对应元素相同，则直接过
            if list1[i] == list2[i]:
                pass
            else:#两个列表对应元素不同，则输出对应的索引
                error.append(abs(list1[i]-list2[i]))
                # print(i)
                error_index.append(i)
    print(error)
    print(error_index)
if __name__ == '__main__':
    # Base.metadata.create_all(engine)

    # # fake = Faker()
    Session = sessionmaker(bind=engine)
    session = Session()
    #
    # faker_naomi = Naomi(uid = '755408')
    #
    # session.add(faker_naomi)
    # session.commit()
    # update(Naomi, '524050', add_qn=1)
    # Session = sessionmaker(bind=engine)
    # update(Naomi, '2351782673489', 4735)
    # session = Session()
    #
    # se = session.query(Naomi).filter(Naomi.uid == '524050').first()
    # if se:
    #     cock = int(se.qn) + 10
    #     print(cock)
    #     se.qn = cock
    #     session.commit()
    # r = session.query(Naomi).all()
    # for i in r:
    # #     print(i.id, i.uid, i.qn)
    # list1 = [1,2,3,4]
    # list2 = [4,2,3,1]
    #
    # compare(list1,list2)
    r = session.query(Naomi).all()
    timestr = str(r[0].ts)
    print(int(time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))))
