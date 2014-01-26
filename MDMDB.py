__author__ = 'sonto'
import sqlite3
import binascii

from plistlib import *


class MDMDB:
    __conn__=None
    __db    = None

    def __init__(self, db=''):
        self.__db = db

    def __table_exists(self, tablename=''):
        c = self.__conn__.cursor()
        sql = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s'"%(tablename)
        #print "[SQL] %s"%sql
        c.execute(sql)
        if c.fetchone()[0] == 1:
            c.close()
            #print "Table exists"
            return True
        c.close()
        #print "Table dose not exist"
        return False

    def __device_exists(self, UDID=''):
        c = self.__conn__.cursor()
        sql = "SELECT UDID FROM mdm_device WHERE UDID='%s'"%UDID
        c.execute(sql)
        if c.fetchone():
            c.close()
            return True
        c.close()
        return False

    def open(self, name=None):
        if not name:
            name = self.__db
        if name:
            self.__conn__ = sqlite3.connect(name)
            if not self.__conn__:
                return None
            c = self.__conn__.cursor()

            if not self.__table_exists(tablename='mdm_device'):
                sql="CREATE TABLE mdm_device (UDID text," \
                    "deviceToken text, " \
                    "untoken blob," \
                    "pushMagic text," \
                    "topic text)"
                c.execute(sql)

            if not self.__table_exists(tablename='mdm_cmd_queue'):
                sql="CREATE TABLE mdm_cmd_queue (UDID text, command text, arguments text, status integer)"
                c.execute(sql)
            self.__conn__.commit()
            c.close()

    def addNewDevice(self, UDID='', token=None, untoken=None, magic='', topic=''):
        if not self.__conn__:
            if not self.open(self.__db):
                return False
        if self.__device_exists(UDID=UDID):
            return False
        c = self.__conn__.cursor()
        sql = "INSERT INTO mdm_device (UDID, deviceToken, untoken, pushMagic, topic) VALUES(?,?,?,?,?)"
        print sql
        c.execute(sql,[UDID, token, sqlite3.Binary(untoken), magic, topic])
        self.__conn__.commit()
        c.close()
        return True

    def addNewCommandToWaitQueue(self,UDID='', command='', args=''):
        if not self.__conn__:
            if not self.open(self.__db):
                return False
        c = self.__conn__.cursor()
        sql = "INSERT INTO mdm_cmd_queue VALUES('%s','%s','%s',0)"%(UDID, command, args)
        print sql
        c.execute(sql)
        self.__conn__.commit()
        c.close()
        return True

    def getDeviceInfo(self,UDID=''):
        if not self.__conn__:
            if not self.open(self.__db):
                return False

        c = self.__conn__.cursor()
        sql = "SELECT * FROM mdm_device WHERE UDID='%s'"%(UDID)
        c.execute(sql)
        #try:
        device=c.fetchone()
        devinfo = {
                "UDID":device[0],
                "Token": device[1],
                "UnToken":device[2],
                "PushMagic":device[3],
                "Topic":device[4],
        }
        c.close()
        return devinfo

    def getCommandInfo(self,UDID=''):
        if not self.__conn__:
            if not self.open(self.__db):
                return False

        c = self.__conn__.cursor()
        sql = "SELECT * FROM mdm_cmd_queue WHERE UDID='%s'"%(UDID)
        c.execute(sql)
        try:
            cmd_row=c.fetchone()
            cmdinfo = {
                "UDID":str(cmd_row[0]),
                "Command":cmd_row[1],
                "Arguments":cmd_row[2],
                "Status":cmd_row[3]
            }
        except:
            c.close()
            return None

        c.close()
        return cmdinfo

    def setCommandStatus(self, UDID='', status=0):
        if not self.__conn__:
            if not self.open(self.__db):
                return False
        c = self.__conn__.cursor()
        sql = "UPDATE mdm_cmd_queue SET status=%d WHERE UDID='%s'"%(status, UDID)
        c.execute(sql)
        self.__conn__.commit()
        c.close()
        return True

    def removeCommand(self, UDID=''):
        if not self.__conn__:
            if not self.open(self.__db):
                return False
        c = self.__conn__.cursor()
        sql = "DELETE FROM mdm_cmd_queue WHERE UDID='%s'"%UDID
        try:
            c.execute(sql)
        except:
            return False
        c.close()
        return True
    def cleanTable(self,table=''):
        if not self.__conn__:
            if not self.open(self.__db):
                return False
        c = self.__conn__.cursor()
        sql = "DELETE FROM %s"%table
        c.execute(sql)
        self.__conn__.commit()
        c.close()
        return True

    def close(self):
        self.__conn__.close()
        self.__conn__ = None
#if __name__ == "__main__":
#    db = MDMDB('./mdm.db')

#    db.addNewCommandToWaitQueue(UDID='12345',command='DeviceLock')
#    print db.getCommandInfo(UDID='12345')
#    db.removeCommand(UDID='12345')
#    print db.getCommandInfo(UDID='12345')



