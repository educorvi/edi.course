# -*- coding: utf-8 -*-
from datetime import datetime
from collective.beaker.interfaces import ISession
from pymongo import MongoClient
from bson.objectid import ObjectId
from App.config import getConfiguration
from edi.course.mongoutil import get_mongo_client
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))

mongoclient = MongoClient(mongoserver, mongoport)

def einschreiben(kurs, studentid):
    """schreibt einen Benutzer in den aktuellen Kurs ein"""

    cdb = mongoclient[kurs.id]
    cc = cdb.course_collection
    coursepost = {'studentid': studentid,
                  'date': datetime.now()}
    cc_id = cc.insert_one(coursepost).inserted_id
    uc = cdb.user_collection
    studentpost = {'studentid':studentid,
                   'lastchange':kurs.UID(),
                   'visited':[],
                   'tests':[]}
    uc_id = uc.insert_one(studentpost).inserted_id
    return (cc_id, uc_id)

def getStudentData(kurs, studentid):
    """liest die Daten des Studenten aus dem aktuellen Kurs"""

    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    studentdata = uc.find_one({"studentid": studentid})
    return studentdata

def updateVisitedData(kurs, studentid, uid, retdict):
    """aktualisiert die Daten zu den besuchten Inhalten"""

    studentdata = getStudentData(kurs, studentid)
    visited = studentdata.get('visited')
    tests = studentdata.get('tests')
    objid = studentdata.get('_id')
    if not visited:
        visited = []
    visited.append(uid)
    studentdata['visited'] = visited
    if not tests:
        tests = []
    if retdict:
        tests.append(retdict)
        studentdata['tests'] = tests
    print studentdata
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    update = uc.update_one({"_id": objid},{"$set": studentdata}, upsert=False)
    return update

def resetUserData(kurs, studentid):
    """setzt die Daten eines bestimmten Benutzers zurück."""

    studentdata = getStudentData(kurs, studentid)
    objid = studentdata.get('_id')
    studentdata['visited'] = []
    studentdata['tests'] = []
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    update = uc.update_one({"_id": objid},{"$set": studentdata}, upsert=False)
    return update
