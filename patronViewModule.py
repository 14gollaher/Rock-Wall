import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import itertools
from itertools import *
import re

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

def patrons():

    if not session.get('isLoggedIn'):
        return redirect('login')

    if session.get('currentUserAccountType') == 'Employee':
        return redirect('patronViewEmployee')
    elif session.get('currentUserAccountType') == 'Administrator':
        return redirect('patronViewAdmin')
    elif session.get('currentUserAccountType') == 'Master':
        return redirect('patronViewMaster')
    
def patronViewEmployee():

    if not session.get('isLoggedIn'):
        return redirect('login')

    patronTable = {}
    patronTable['id'] = databaseFunctions.getAllPatronIds()
    patronTable['firstName'] = databaseFunctions.getAllPatronFirstNames()
    patronTable['lastName'] = databaseFunctions.getAllPatronLastNames()
    patronTable['isBelayCertified'] = databaseFunctions.getAllPatronBelayCertifications()
    patronTable['isSoloClimbCertified'] = databaseFunctions.getAllPatronSoloClimbCertifications()
    patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
    patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
    patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()
    patronTable = [dict(id=i, firstName=f, lastName=l, isBelayCertified = b, isSoloClimbCertified = s, isSuspended = su, suspendedStartDate = st, suspendedEndDate = e) for i, f, l, b, s, su, st, e in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['isBelayCertified'], patronTable['isSoloClimbCertified'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'])]
    
    return render_template('patronViewEmployee.html', patronTable = patronTable)

def patronViewAdmin():
    if not session.get('isLoggedIn'):
        return redirect('login')

    patronTable = {}
    patronTable['id'] = databaseFunctions.getAllPatronIds()
    patronTable['firstName'] = databaseFunctions.getAllPatronFirstNames()
    patronTable['lastName'] = databaseFunctions.getAllPatronLastNames()
    patronTable['email'] = databaseFunctions.getAllPatronEmails()
    patronTable['phoneNumber'] = databaseFunctions.getAllPatronPhoneNumbers()
    patronTable['gender'] = databaseFunctions.getAllPatronGenders()
    patronTable['address'] = databaseFunctions.getAllPatronAddresses()
    patronTable['city'] = databaseFunctions.getAllPatronCities()
    patronTable['zipCode'] = databaseFunctions.getAllPatronZipCodes()
    patronTable['state'] = databaseFunctions.getAllPatronStates()
    patronTable['isBelayCertified'] = databaseFunctions.getAllPatronBelayCertifications()
    patronTable['isSoloClimbCertified'] = databaseFunctions.getAllPatronSoloClimbCertifications()
    patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
    patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
    patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()
    
    patronTable = [dict(id=i, firstName=f, lastName=l, email=e, phoneNumber=p, gender=g, address=a, city=c, zipCode=z, state=s, isBelayCertified = b, isSoloClimbCertified = sc, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se) for i, f, l, e, p, g, a, c, z, s, b, sc, su, ss, se in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['email'], patronTable['phoneNumber'], patronTable['gender'], patronTable['address'], patronTable['city'], patronTable['zipCode'], patronTable['state'], patronTable['isBelayCertified'], patronTable['isSoloClimbCertified'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'])]
    
    return render_template('patronViewManager.html', patronTable = patronTable)

def patronViewMaster():
    if not session.get('isLoggedIn'):
        return redirect('login')

    patronTable = {}
    patronTable['id'] = databaseFunctions.getAllPatronIds()
    patronTable['firstName'] = databaseFunctions.getAllPatronFirstNames()
    patronTable['lastName'] = databaseFunctions.getAllPatronLastNames()
    patronTable['email'] = databaseFunctions.getAllPatronEmails()
    patronTable['phoneNumber'] = databaseFunctions.getAllPatronPhoneNumbers()
    patronTable['gender'] = databaseFunctions.getAllPatronGenders()
    patronTable['address'] = databaseFunctions.getAllPatronAddresses()
    patronTable['city'] = databaseFunctions.getAllPatronCities()
    patronTable['zipCode'] = databaseFunctions.getAllPatronZipCodes()
    patronTable['state'] = databaseFunctions.getAllPatronStates()
    patronTable['isBelayCertified'] = databaseFunctions.getAllPatronBelayCertifications()
    patronTable['isSoloClimbCertified'] = databaseFunctions.getAllPatronSoloClimbCertifications()
    patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
    patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
    patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()
    
    patronTable = [dict(id=i, firstName=f, lastName=l, email=e, phoneNumber=p, gender=g, address=a, city=c, zipCode=z, state=s, isBelayCertified = b, isSoloClimbCertified = sc, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se) for i, f, l, e, p, g, a, c, z, s, b, sc, su, ss, se in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['email'], patronTable['phoneNumber'], patronTable['gender'], patronTable['address'], patronTable['city'], patronTable['zipCode'], patronTable['state'], patronTable['isBelayCertified'], patronTable['isSoloClimbCertified'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'])]
    
    return render_template('patronViewManager.html', patronTable = patronTable)

def patronDelete():
    if not session.get('isLoggedIn'):
        return redirect('login')

    newPatronItem = Patron(str(request.form['id']), "", "", "", "", "", "", "", "", "", "", False, False, False, "", "")
    newPatronItem.id = newPatronItem.id.strip('"')
    databaseFunctions.deletePatronItem(newPatronItem)

    return redirect('patronViewManager')

def editPatronRoute():
    if not session.get('isLoggedIn'):
        return redirect('login')

    patronUpdatedStartDate = ""
    patronUpdatedEndDate = ""
    try:
        patronUpdatedStartDate = str(request.form['updatedSuspendedStartDate'])
        patronUpdatedEndDate = str(request.form['updatedSuspendedEndDate'])
    except:
        patronUpdatedStartDate = ""
        patronUpdatedEndDate = ""
    newPatronItem = Patron(str(request.form['updatedId']), str(request.form['updatedFirstName']), str(request.form['updatedLastName']), str(request.form['updatedEmail']), str(request.form['updatedPhoneNumber']), str(request.form['updatedGender']), str(request.form['updatedAddress']), str(request.form['updatedCity']), str(request.form['updatedZipCode']), "", str(request.form['updatedState']), str(request.form['updatedBelayStatus']), str(request.form['updatedSoloClimbStatus']), str(request.form['updatedIsSuspended']), patronUpdatedStartDate, patronUpdatedEndDate)
    databaseFunctions.editPatron(newPatronItem) 
    if session.get('currentUserAccountType') == 'administrator':
        return redirect('patronViewAdmin')
    else:
        return redirect('patronViewMaster')


