import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import make_response
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import date
from datetime import datetime
from datetime import timedelta
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import simplejson as json
import time
import pytz
import ctypes

class Patron:

    def __init__(self, id, firstName, lastName, email, phoneNumber, gender, address, city, zipCode, waiverFile, state, isBelayCertified, belayStartDate, belayEndDate, isLeadClimbCertified, leadClimbStartDate, leadClimbEndDate, isSuspended, suspendedStartDate, suspendedEndDate, listServ):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.gender = gender
        self.address = address
        self.city = city
        self.zipCode = zipCode
        self.waiverFile = waiverFile
        self.state = state
        self.isBelayCertified = isBelayCertified
        self.belayStartDate = belayStartDate
        self.belayEndDate = belayEndDate
        self.isLeadClimbCertified = isLeadClimbCertified
        self.leadClimbStartDate = leadClimbStartDate
        self.leadClimbEndDate = leadClimbEndDate
        self.isSuspended = isSuspended
        self.suspendedStartDate = suspendedStartDate
        self.suspendedEndDate = suspendedEndDate
        self.listServ = listServ

class VisitHistoryLogItem:

    def __init__(self, id, patronId, patronFirstName, patronLastName, patronVisitDate, patronVisitTime):

        self.id = id    
        self.patronId = patronId
        self.patronFirstName = patronFirstName
        self.patronLastName = patronLastName
        self.patronVisitDate = patronVisitDate
        self.patronVisitTime = patronVisitTime

def patronCheckIn():
    
    try:
        if checkPreviousPage(['patronCheckIn', 'patronCheckInRoute']) == False:
            session['messageBagPatron'] = ""    
    except:
        session['messageBagPatron'] = ""    


    pass2 = []
    pass2.append('F')
    pass2 = json.dumps(pass2)

    return render_template('patron/patronCheckIn.html', pass2 = pass2)

def patronCheckInRoute():

    if checkPreviousPage(['patronCheckIn', 'patronCheckInRoute']) == False:
        session['messageBagPatron'] = ""  

    patronAccount = Patron(str(request.form['patronId']), "", "", "", "", "" ,"" ,"" ,"","" ,"" , False,"" ,"", False, "", "", False, "", "", "")
    session['currentPatronId'] = patronAccount.id

    if validateCredentials(patronAccount): 
        session['messageBagPatron'] = ""  
        currentPatronId = session.get('currentPatronId')
        currentPatronFirstName = databaseFunctions.getCurrentPatronFirstName(currentPatronId)
        currentPatronLastName = databaseFunctions.getCurrentPatronLastName(currentPatronId)
        currentPatronEmail = databaseFunctions.getCurrentPatronEmail(currentPatronId)
        currentPatronPhoneNumber = databaseFunctions.getCurrentPatronPhoneNumber(currentPatronId)
        currentPatronAddress = databaseFunctions.getCurrentPatronAddress(currentPatronId)
        currentPatronState = databaseFunctions.getCurrentPatronState(currentPatronId)
        currentPatronCity = databaseFunctions.getCurrentPatronCity(currentPatronId)
        currentPatronZipCode = databaseFunctions.getCurrentPatronZipCode(currentPatronId)
        currentPatronGender = databaseFunctions.getCurrentPatronGender(currentPatronId)
        currentPatronSuspension = databaseFunctions.getCurrentPatronSuspension(currentPatronId)
        currentPatronSuspensionStartDate = databaseFunctions.getCurrentPatronSuspensionStartDate(currentPatronId)
        currentPatronSuspensionEndDate = databaseFunctions.getCurrentPatronSuspensionEndDate(currentPatronId)
        pass2 = []
        pass2.append('T')
        pass2 = json.dumps(pass2)

    else:
        session['messageBagPatron'] = 'ID does not exist!'
        return redirect('patronCheckIn')

    if currentPatronSuspensionStartDate and currentPatronSuspensionEndDate:
        startDate = datetime.strptime(currentPatronSuspensionStartDate, "%m/%d/%Y")
        endDate = datetime.strptime(currentPatronSuspensionEndDate, "%m/%d/%Y")
        today = datetime.today()
        if timeInRange(startDate, endDate, today):
            return redirect('patronSuspension')
   
    return render_template('patron/patronCheckIn.html', id = currentPatronId, firstName = currentPatronFirstName, lastName = currentPatronLastName, email = currentPatronEmail, phoneNumber = currentPatronPhoneNumber, address = currentPatronAddress, state = currentPatronState, city = currentPatronCity, zipCode = currentPatronZipCode, gender = currentPatronGender, isSuspended = currentPatronSuspension, pass2 = pass2)

def patronCheckInRoute2():

    patronAccount = Patron(str(request.form['patronId2']), str(request.form['firstName']), str(request.form['lastName']), str(request.form['email']), str(request.form['phoneNumber']), str(request.form['gender']), str(request.form['address']),  str(request.form['city']), str(request.form['zipCode']), '', str(request.form['state']), False,"" ,"", False, "", "", False, "", "", "")
    databaseFunctions.editPatronAccount(patronAccount)

    my_date = datetime.now(pytz.timezone('US/Central'))
    newVisitLogItem = VisitHistoryLogItem("null", str(request.form['patronId2']), str(request.form['firstName']), str(request.form['lastName']), my_date.strftime("%m/%d/%Y"), my_date.strftime("%H:%M"))
    databaseFunctions.insertNewVisitHistoryItem(newVisitLogItem)
    return redirect('patronCheckIn')

def validateCredentials(patronAccount):

    if databaseFunctions.getPatronId(patronAccount):
        return True
    else:
        return False

def patronSignUp():
    
    if checkPreviousPage(['patronSignUp', 'patronSignUpRoute']) == False:
        session['messageBagPatron'] = ""    

    return render_template('patron/patronSignUp.html')

def patronSignUpRoute(): 

    if checkPreviousPage(['patronSignUp', 'patronSignUpRoute']) == False:
        session['messageBagPatron'] = ""    

    try: 
        str(request.form['listServ'])
        patronListServRequest = "True"
    except:
        patronListServRequest = "False"

    patronAccount = Patron(str(request.form['id']),"", "", str(request.form['email']), "", "", "", "", "","", "", False, "", "", False, "", "", False, "", "", patronListServRequest)

    if databaseFunctions.getPatronId(patronAccount):
        session['messageBagPatron'] = 'Id already exists!'
        return redirect('patronSignUp')
    elif databaseFunctions.getPatronEmailIfExists(patronAccount):
        session['messageBagPatron'] = 'E-Mail already exists!'
        return redirect('patronSignUp')

    session['newPatronId'] = str(request.form['id'])
    session['newPatronFirstName'] = str(request.form['firstName'])
    session['newPatronLastName'] = str(request.form['lastName'])
    session['newPatronEmail'] = str(request.form['email'])
    session['newPatronPhoneNumber'] = str(request.form['phoneNumber'])
    session['newPatronGender'] = str(request.form['gender'])
    session['newPatronAddress'] = str(request.form['address'])
    session['newPatronState'] = str(request.form['state'])
    session['newPatronCity'] = str(request.form['city'])
    session['newPatronZipCode'] = str(request.form['zipCode'])
    session['newPatronListServ'] = patronListServRequest
    
    return redirect('signWaiver')

def signWaiver():
    
    if checkPreviousPage(['signWaiver']) == False:
        session['messageBagPatron'] = ""    

    return render_template('patron/patronSignWaiver.html')
    
def patronSuspension():
    return render_template('patron/patronSuspension.html')

def createPatronAccountRoute():
    
    file = open("sysSig.bteam", "r")
    waiverUrl = file.read()

    newPatron = Patron(session.get('newPatronId'), session.get('newPatronFirstName'), session.get('newPatronLastName'), session.get('newPatronEmail'), session.get('newPatronPhoneNumber'), session.get('newPatronGender'), session.get('newPatronAddress'), session.get('newPatronCity'), session.get('newPatronZipCode'), waiverUrl, session.get('newPatronState'), False, "", "", False, "", "", False, "", "", session.get('newPatronListServ'))
   
    databaseFunctions.insertNewPatron(newPatron)
    file.close()

    return redirect('patronCheckIn')

def storeImage():

    data = request.form['data']
    
    file = open("sysSig.bteam", "w")
    file.write(data)
    file.close() 

    return redirect('signWaiver')

def checkPreviousPage(listGoodPages):
    
    checkValue = request.referrer.split('/')
    
    for page in listGoodPages:
        if checkValue[3] == page:
             return True
    return False
   
def timeInRange(start, end, x):

    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end