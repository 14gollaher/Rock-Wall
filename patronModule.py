import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import make_response
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import simplejson as json
import time
import pytz

class Patron:

    def __init__(self, id, firstName, lastName, email, phoneNumber, gender, address, city, zipCode, waiverFile, state, isBelayCertified, isSoloClimbCertified, isSuspended, suspendedStartDate, suspendedEndDate):
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
        self.isSoloClimbCertified = isSoloClimbCertified
        self.isSuspended = isSuspended
        self.suspendedStartDate = suspendedStartDate
        self.suspendedEndDate = suspendedEndDate

class VisitHistoryLogItem:

    def __init__(self, id, patronId, patronFirstName, patronLastName, patronVisitDate, patronVisitTime):

        self.id = id    
        self.patronId = patronId
        self.patronFirstName = patronFirstName
        self.patronLastName = patronLastName
        self.patronVisitDate = patronVisitDate
        self.patronVisitTime = patronVisitTime

def patronSignUp():

    return render_template('patron/patronSignUp.html')

def patronCheckIn():
    
    pass2 = []
    pass2.append('F')
    pass2 = json.dumps(pass2)

    return render_template('patron/patronCheckIn.html', pass2 = pass2)

def patronCheckInRoute():
    
    pass2 = []
    pass2.append('F')
    pass2 = json.dumps(pass2)
    patronAccount = Patron(str(request.form['patronId']), "", "", "", "" ,"" ,"" ,"" ,"" ,"" ,"", False, False, False, "", "")
    session['currentPatronId'] = patronAccount.id

    if validateCredentials(patronAccount): 
        session['isCheckedIn'] = True
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
        pass2 = []
        pass2.append('T')
        pass2 = json.dumps(pass2)

    else:
        session['messageCheckIn'] = 'Account does not exist!'
        return redirect('patronCheckIn')

    return render_template('patron/patronCheckIn.html', id = currentPatronId, firstName = currentPatronFirstName, lastName = currentPatronLastName, email = currentPatronEmail, phoneNumber = currentPatronPhoneNumber, address = currentPatronAddress, state = currentPatronState, city = currentPatronCity, zipCode = currentPatronZipCode, gender = currentPatronGender, pass2 = pass2)


def patronCheckInRoute2():

    patronAccount = Patron(str(request.form['patronId2']), str(request.form['firstName']), str(request.form['lastName']), str(request.form['email']), str(request.form['phoneNumber']), str(request.form['gender']), str(request.form['address']),  str(request.form['city']), str(request.form['zipCode']), '', str(request.form['state']), False, False, False, "", "")
    databaseFunctions.editPatronAccount(patronAccount)

    my_date = datetime.datetime.now(pytz.timezone('US/Central'))
    newVisitLogItem = VisitHistoryLogItem("null", str(request.form['patronId2']), str(request.form['firstName']), str(request.form['lastName']), my_date.strftime("%m/%d/%Y"), my_date.strftime("%H:%M"))
    databaseFunctions.insertNewVisitHistoryItem(newVisitLogItem)
    return redirect('patronCheckIn')

def validateCredentials(patronAccount):

    if databaseFunctions.getPatronId(patronAccount):
        return True
    else:
        return False

def patronSignUpRoute(): 

    session['messagePatronSignUp'] = ""

    patronAccount = Patron(str(request.form['id']), "", "", "", "" ,"" ,"" ,"" ,"" ,"" ,"", False, False, False, "", "")

    if databaseFunctions.getPatronId(patronAccount):
        session['messagePatronSignUp'] = 'Id already exists!'
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

    return redirect('signWaiver')

def signWaiver():
    return render_template('patron/signWaiver.html')
    
def createPatronAccountRoute():
    
    file = open("sysSig.bteam", "r")
    waiverUrl = file.read()
    newPatron = Patron(session.get('newPatronId'), session.get('newPatronFirstName'), session.get('newPatronLastName'), session.get('newPatronEmail'), session.get('newPatronPhoneNumber'), session.get('newPatronGender'), session.get('newPatronAddress'), session.get('newPatronCity'), session.get('newPatronZipCode'), waiverUrl, session.get('newPatronState'), False, False, False, "", "")
    databaseFunctions.insertNewPatron(newPatron)
    file.close()

    return redirect('patronCheckIn')

def storeImage():

    data = request.form['data']
    
    file = open("sysSig.bteam", "w")
    file.write(data)
    file.close() 

    return redirect('signWaiver')