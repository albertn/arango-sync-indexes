from pyArango.connection import *
from pyArango.database import *
from pyArango.collection import *
from pyArango.index import *
import json

MASTER = 'http://db.plankton.master.bhinnekalocal.com:8529'
SLAVE1 = 'http://10.80.10.216:8529'
SLAVE2 = 'http://10.80.10.112:8529'
conn = Connection(arangoURL=MASTER, username='root', password='toor')
conn_slave_1 = Connection(arangoURL=SLAVE1, username='root', password='toor')
conn_slave_2 = Connection(arangoURL=SLAVE2, username='root', password='toor')

db = Database(conn, '_system')

class ArangoDBIndex:
    def __init__(self):
        self.collectionName = ''
        self.fields = []
        self.sparse = False
        self.type = ''
        self.unique = False
        self.minLength = 0

coll_list = db.collections

coll_indexes = []

for coll_name in coll_list:
    coll = db.collections[coll_name]
    if not coll.isSystem and coll.getType() != 'edge':
        for idx_list in coll.getIndexes().items():
            for idx_value in idx_list[1].values():
                arangoDBIndex = ArangoDBIndex()
                arangoDBIndex.collectionName = coll_name
                arangoDBIndex.fields = idx_value.infos['fields']
                arangoDBIndex.sparse = idx_value.infos['sparse']
                arangoDBIndex.type = idx_value.infos['type']
                arangoDBIndex.unique = idx_value.infos['unique']
                if 'minLength' in idx_value.infos.keys():
                    arangoDBIndex.minLength = idx_value.infos['minLength']
                coll_indexes.append(arangoDBIndex)


db_slave_1 = Database(conn_slave_1, '_system')
db_slave_2 = Database(conn_slave_2, '_system')

for coll_name in db_slave_1.collections:
    coll = db_slave_1.collections[coll_name]
    for idx in coll_indexes:
        if idx.collectionName == coll_name:
            if idx.type == 'hash':
                coll.ensureHashIndex(idx.fields, unique=idx.unique, sparse=idx.sparse)
            if idx.type == 'skiplist':
                coll.ensureSkiplistIndex(idx.fields, unique=idx.unique, sparse=idx.sparse)
            if idx.type == 'fulltext':
                coll.ensureFulltextIndex(idx.fields, minLength=idx.minLength)

for coll_name in db_slave_2.collections:
    coll = db_slave_2.collections[coll_name]
    for idx in coll_indexes:
        if idx.collectionName == coll_name:
            if idx.type == 'hash':
                coll.ensureHashIndex(idx.fields, unique=idx.unique, sparse=idx.sparse)
            if idx.type == 'skiplist':
                coll.ensureSkiplistIndex(idx.fields, unique=idx.unique, sparse=idx.sparse)
            if idx.type == 'fulltext':
                coll.ensureFulltextIndex(idx.fields, minLength=idx.minLength)
           