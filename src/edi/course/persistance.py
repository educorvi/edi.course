# -*- coding: utf-8 -*-
from datetime import datetime
from collective.beaker.interfaces import ISession
from bson.objectid import ObjectId
from Products.CMFCore.interfaces import ISiteRoot
from App.config import getConfiguration
from edi.course.mongoutil import get_mongo_client
from zope.component import getUtility
from plone import api as ploneapi

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
    mongoclient = get_mongo_client()
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
    mongoclient = get_mongo_client()
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
    mongoclient = get_mongo_client()
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    studentdata = uc.find_one({"studentid": studentid})
    return studentdata

def getCourseData(kurs, studentid):
    """liest die Daten des Kurses aus dem aktuellen Kurs"""
    mongoclient = get_mongo_client()
    cdb = mongoclient[kurs.id]
    cc = cdb.course_collection
    coursedata = cc.find_one({"studentid": studentid})
    return coursedata

def updateVisitedData(kurs, studentid, uid, retdict, finished):
    """aktualisiert die Daten zu den besuchten Inhalten"""
    mongoclient = get_mongo_client()
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    cc = cdb.course_collection

    if finished:
        coursedata = getCourseData(kurs, studentid)
        objid = coursedata.get('_id')
        if not 'finished' in coursedata:
            coursedata['finished'] = datetime.now()
            courseupdate = cc.update_one({"_id": objid},{"$set": coursedata}, upsert=False)
        
    studentdata = getStudentData(kurs, studentid)
    if not studentdata:
        #Autoren und Redakteure arbeiten am Kurs
        return
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
    update = uc.update_one({"_id": objid},{"$set": studentdata}, upsert=False)
    return update

def getGlobalStats(kurs):
    """sucht alle Dokumente eingetragener Studenten aus der Datenbank
    """
    mongoclient = get_mongo_client()
    cdb = mongoclient[kurs.id]
    cc = cdb.course_collection
    alldocs = []
    for doc in cc.find():
        entry = {}
        studentid = doc.get('studentid')
        if studentid:
            user = ploneapi.user.get(userid = studentid)
            entry['studentid'] = studentid
            entry['fullname'] = user.getProperty('fullname')
            entry['email'] = user.getProperty('email')
            entry['in'] = doc.get('date').strftime('%d.%m.%Y %H:%M')
            entry['fin'] = ''
            if doc.get('finished'):
                entry['fin'] = doc.get('finished').strftime('%d.%m.%Y %H:%M')
            alldocs.append(entry)
    return alldocs    

def resetUserData(kurs, studentid):
    """setzt die Daten eines bestimmten Benutzers zurück."""

    studentdata = getStudentData(kurs, studentid)
    objid = studentdata.get('_id')
    studentdata['visited'] = []
    studentdata['tests'] = {}
    mongoclient = get_mongo_client()
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    update = uc.update_one({"_id": objid},{"$set": studentdata}, upsert=False)
    return update

def resetComplete(kurs, studentid):
    """setzt alle Daten eines Benutzers komplett zurück"""

    mongoclient = get_mongo_client()
    cdb = mongoclient[kurs.id]
    cc = cdb.course_collection
    myquery = {'studentid': studentid}
    ret = cc.delete_one(myquery)
    studentdata = getStudentData(kurs, studentid)
    objid = studentdata.get('_id')
    cdb = mongoclient[kurs.id]
    uc = cdb.user_collection
    ret = uc.delete_one({"_id": objid})
    return True 
