# -*- coding: utf-8 -*-
from datetime import datetime
from collective.beaker.interfaces import ISession
from pymongo import MongoClient
from bson.objectid import ObjectId
from Products.CMFCore.interfaces import ISiteRoot
from App.config import getConfiguration
from edi.course.mongoutil import get_mongo_client
from plone import api as ploneapi
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))

mongoclient = MongoClient(mongoserver, mongoport)

def getAcquisitionChain(context):
    inner = context.aq_inner
    iter = inner
    while iter is not None:
        yield iter
        if ISiteRoot.providedBy(iter):
            break
        if not hasattr(iter, "aq_parent"):
            raise RuntimeError("Parent traversing interrupted by object: " + str(parent))
        iter = iter.aq_parent

def getCourse(context):
    """ get the CourseObject
    """
    parentobjects = getAcquisitionChain(context)
    for i in parentobjects:
        if i.portal_type == "Kurs":
            return i
    return ""

def getFinalData(context):
    """ Deliver Final Data for Final-Site
    """
    kurs = getCourse(context)
    studentid = ploneapi.user.get_current().getId()
    studentdata = getStudentData(kurs, studentid)
    return studentdata

def getResultsForQuiz(context):
    """ Hilfsfunktion fuer edi.quiz
    """
    retdict = {}
    kurs = getCourse(context)
    studentid = ploneapi.user.get_current().getId()
    quizuid = context.UID()
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    studentdata = uc.find_one({"studentid": studentid})
    if studentdata:
        tests = studentdata.get('tests')
        if tests:
            retdict = tests.get(quizuid, {})
    return retdict

def einschreiben(kurs, studentid):
    """schreibt einen Benutzer in den aktuellen Kurs ein"""

    cdb = mongoclient[kurs.id]
    cc = cdb.course_collection
    coursepost = {'studentid': studentid,
                  'date': datetime.now()}
    cc_id = cc.insert_one(coursepost).inserted_id
    uc = cdb.user_collection
    studentpost = {'studentid':studentid,
                   'lastchange':datetime.now(),
                   'visited':[],
                   'tests':{}}
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
    else:
        if not visited[-1] == uid:
            visited.append(uid)
    studentdata['visited'] = visited
    if not tests:
        tests = {}
    if retdict:
        tests[uid] = retdict
        studentdata['tests'] = tests
    studentdata['lastchange'] = datetime.now()
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
    studentdata['tests'] = {}
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    update = uc.update_one({"_id": objid},{"$set": studentdata}, upsert=False)
    return update
