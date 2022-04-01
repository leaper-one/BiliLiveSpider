from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, text
from sqlalchemy.orm import sessionmaker, relationship
import time

engine = create_engine(r'sqlite:///D:\\Workspace\\sqlite\\db.sqlite3')

Base = declarative_base()

max = int(10E8)
min = int(0)
add = int(10E6)
uid_ranked = []
uid_rank = []
# 定义Naomi对象:
class Naomi(Base):
    # 表的名字:
    __tablename__ = 'model_naomi'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    uid = Column(String(100))
    qn = Column(Integer, default=0)
    ts = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))

class Rank(Base):
    __tablename__ = 'model_rank'

    id = Column(Integer, primary_key=True)
    uid = Column(String(100))
    rank = Column(Integer, default=0)
    qn = Column(Integer, default=0)
    ts = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))

# 更新rank表
def rank(uid, qn):
    Session = sessionmaker(bind=engine)
    session = Session()

    search = session.query(Rank).filter(Rank.uid == uid).first()
    if search:
        if search.qn != qn:
            updateFunc(uid, qn)
    else:
        createFunc(uid, qn)

def updateFunc(uid, qn):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Rank).filter(Rank.uid == uid).delete()
    session.commit()

    createFunc(uid, qn)


def createFunc(uid, qn):
    Session = sessionmaker(bind=engine)
    session = Session()

    search = session.query(Rank).order_by(Rank.rank.desc()).all()
    rank = 0
    if search:
        # for i in range(len(search)):
        #     if qn > search[0].qn:
        #         rank = search[0].qn + add
        #         break
        #     elif qn <= search[i].qn and qn >= search[i+1].qn:
        #         rank = (search[i].qn + search[i+1].qn)/2
        #         break
        #     elif qn < search[-1].qn:
        #         rank = search[-1].qn - add
        #         break
        #     else:
        #         pass
        if qn > search[0].qn:
            rank = search[0].rank + add
        elif qn < search[-1].qn:
            rank = search[-1].rank - add
        elif len(search) == 1:
            if qn >= search[0].qn:
                rank = search[0].rank + add
            else:
                rank = search[0].rank - add
        else:
            for i in range(len(search)):
                if qn <= search[i].qn and qn >= search[i + 1].qn:
                    rank = (search[i].rank + search[i+1].rank)/2
                    break
        session.add(Rank(uid=uid, rank=int(rank), qn=qn))
        session.commit()
    else:
        rank = (max - min)/2
        session.add(Rank(uid=uid, rank=rank, qn=qn))
        session.commit()

# 更新Naomi表
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

def main(ts):
    Session = sessionmaker(bind=engine)
    session = Session()
    ts = ''
    # results = session.query(Naomi).order_by(Naomi.qn.desc()).all()
    results = session.query(Naomi).all()
    for r in results:
        print(r.uid, r.qn)
        uid_rank.append([r.uid, r.qn])
        rank(r.uid, r.qn)
        ts = r.ts
    return ts

if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    #
    # results = session.query(Naomi).order_by(Naomi.qn.desc()).all()
    results = session.query(Naomi).all()
    for r in results:
        print(r.uid, r.qn)
        uid_rank.append([r.uid, r.qn])
        rank(r.uid, r.qn)

    # results_ranked = session.query(Rank).order_by(Rank.rank.desc()).all()
    # for r in results_ranked:
    #     # print(r.uid, r.qn)
    #     uid_ranked.append([r.uid, r.qn])
    #     rank(r.uid, r.qn)
    #
    # print(uid_rank)
    # print(uid_ranked)
    # if uid_ranked == uid_rank:
    #     pass
    #     # return 0
    # else:
    #     for i in range(0, len(uid_rank)):
    #         if i < len(uid_ranked):
    #             if uid_rank[i] != uid_ranked[i]:
    #                 uid_ranked.insert(i, 0)
    #         else:
    #             uid_ranked.append(0)
    #
    # print(uid_rank)
    # print(uid_ranked)

