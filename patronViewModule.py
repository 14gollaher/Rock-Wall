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
from globals import *

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
    patronTable['belayStartDate'] = databaseFunctions.getAllPatronBelayStartDates()
    patronTable['belayEndDate'] = databaseFunctions.getAllPatronBelayEndDates()
    patronTable['isLeadClimbCertified'] = databaseFunctions.getAllPatronLeadClimbCertifications()
    patronTable['leadClimbStartDate'] = databaseFunctions.getAllPatronLeadClimbStartDates()
    patronTable['leadClimbEndDate'] = databaseFunctions.getAllPatronLeadClimbEndDates()
    patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
    patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
    patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()
    patronTable['listServ'] = databaseFunctions.getAllPatronListServ()
    patronTable = [dict(id=i, firstName=f, lastName=l, isBelayCertified = b, belayStartDate =bsd, belayEndDate =bed, isLeadClimbCertified = lcc, leadClimbStartDate = lcsd, leadClimbEndDate = lced, isSuspended = su, suspendedStartDate = st, suspendedEndDate = e, listServ = ls) for i, f, l, b, bsd, bed, lcc, lcsd, lced, su, st, e, ls in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['isBelayCertified'], patronTable['belayStartDate'], patronTable['belayEndDate'], patronTable['isLeadClimbCertified'], patronTable['leadClimbStartDate'], patronTable['leadClimbEndDate'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'], patronTable['listServ'])]
    
    return render_template('viewPatronEmployee.html', patronTable = patronTable)

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
    patronTable['waiver'] = databaseFunctions.getAllPatronWaivers()
    patronTable['isBelayCertified'] = databaseFunctions.getAllPatronBelayCertifications()
    patronTable['belayStartDate'] = databaseFunctions.getAllPatronBelayStartDates()
    patronTable['belayEndDate'] = databaseFunctions.getAllPatronBelayEndDates()
    patronTable['isLeadClimbCertified'] = databaseFunctions.getAllPatronLeadClimbCertifications()
    patronTable['leadClimbStartDate'] = databaseFunctions.getAllPatronLeadClimbStartDates()
    patronTable['leadClimbEndDate'] = databaseFunctions.getAllPatronLeadClimbEndDates()
    patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
    patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
    patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()
    patronTable['listServ'] = databaseFunctions.getAllPatronListServ()
    
    patronTable = [dict(id=i, firstName=f, lastName=l, email=e, phoneNumber=p, gender=g, address=a, city=c, zipCode=z, state=s, waiver=w, isBelayCertified = b, belayStartDate =bsd, belayEndDate =bed, isLeadClimbCertified = lcc, leadClimbStartDate = lcsd, leadClimbEndDate = lced, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se, listServ = ls) for i, f, l, e, p, g, a, c, z, s, w, b, bsd, bed, lcc, lcsd, lced, su, ss, se, ls in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['email'], patronTable['phoneNumber'], patronTable['gender'], patronTable['address'], patronTable['city'], patronTable['zipCode'], patronTable['state'], patronTable['waiver'], patronTable['isBelayCertified'], patronTable['belayStartDate'], patronTable['belayEndDate'], patronTable['isLeadClimbCertified'], patronTable['leadClimbStartDate'], patronTable['leadClimbEndDate'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'], patronTable['listServ'])]
    
    visitTable = {}
    visitTable['Id'] = databaseFunctions.getAllVisitIds()
    visitTable['PatronId'] = databaseFunctions.getAllVisitPatronIds()
    visitTable['PatronFirstName'] = databaseFunctions.getAllVisitPatronFirstNames()
    visitTable['PatronLastName'] = databaseFunctions.getAllVisitPatronLastNames()
    visitTable['PatronVisitDate'] = databaseFunctions.getAllVisitPatronVisitDates()
    visitTable['PatronVisitTime'] = databaseFunctions.getAllVisitPatronVisitTimes()

    visitTable = [dict(id=i, patronId=pI, patronFirstName=f, patronLastName=l, patronVistDate=d, patronVisitTime=t) for i, pI, f, l, d, t in zip(visitTable['Id'], visitTable['PatronId'], visitTable['PatronFirstName'], visitTable['PatronLastName'], visitTable['PatronVisitDate'], visitTable['PatronVisitTime'])]
        
    return render_template('viewPatronManager.html', patronTable = patronTable, visitTable = visitTable)

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
    patronTable['waiver'] = databaseFunctions.getAllPatronWaivers()
    patronTable['isBelayCertified'] = databaseFunctions.getAllPatronBelayCertifications()
    patronTable['belayStartDate'] = databaseFunctions.getAllPatronBelayStartDates()
    patronTable['belayEndDate'] = databaseFunctions.getAllPatronBelayEndDates()
    patronTable['isLeadClimbCertified'] = databaseFunctions.getAllPatronLeadClimbCertifications()
    patronTable['leadClimbStartDate'] = databaseFunctions.getAllPatronLeadClimbStartDates()
    patronTable['leadClimbEndDate'] = databaseFunctions.getAllPatronLeadClimbEndDates()
    patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
    patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
    patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()
    patronTable['listServ'] = databaseFunctions.getAllPatronListServ()
    
    patronTable = [dict(id=i, firstName=f, lastName=l, email=e, phoneNumber=p, gender=g, address=a, city=c, zipCode=z, state=s, waiver=w, isBelayCertified = b, belayStartDate =bsd, belayEndDate =bed, isLeadClimbCertified = lcc, leadClimbStartDate = lcsd, leadClimbEndDate = lced, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se, listServ = ls) for i, f, l, e, p, g, a, c, z, s, w, b, bsd, bed, lcc, lcsd, lced, su, ss, se, ls in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['email'], patronTable['phoneNumber'], patronTable['gender'], patronTable['address'], patronTable['city'], patronTable['zipCode'], patronTable['state'], patronTable['waiver'], patronTable['isBelayCertified'], patronTable['belayStartDate'], patronTable['belayEndDate'], patronTable['isLeadClimbCertified'], patronTable['leadClimbStartDate'], patronTable['leadClimbEndDate'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'], patronTable['listServ'])]
    
    visitTable = {}
    visitTable['Id'] = databaseFunctions.getAllVisitIds()
    visitTable['PatronId'] = databaseFunctions.getAllVisitPatronIds()
    visitTable['PatronFirstName'] = databaseFunctions.getAllVisitPatronFirstNames()
    visitTable['PatronLastName'] = databaseFunctions.getAllVisitPatronLastNames()
    visitTable['PatronVisitDate'] = databaseFunctions.getAllVisitPatronVisitDates()
    visitTable['PatronVisitTime'] = databaseFunctions.getAllVisitPatronVisitTimes()

    visitTable = [dict(id=i, patronId=pI, patronFirstName=f, patronLastName=l, patronVistDate=d, patronVisitTime=t) for i, pI, f, l, d, t in zip(visitTable['Id'], visitTable['PatronId'], visitTable['PatronFirstName'], visitTable['PatronLastName'], visitTable['PatronVisitDate'], visitTable['PatronVisitTime'])]
        
    return render_template('viewPatronManager.html', patronTable = patronTable, visitTable = visitTable)

def patronDelete():

    if not session.get('isLoggedIn'):
        return redirect('login')

    patronToDelete = Patron(str(request.form['id']), "", "", "", "", "", "", "", "","", "", False, "", "", False, "", "", False, "", "", False)
    patronToDelete.id = patronToDelete.id.strip('"')
    databaseFunctions.deletePatronItem(patronToDelete)

    return redirect('patronViewManager')

def editPatronRoute():

    if not session.get('isLoggedIn'):
        return redirect('login')

    patronUpdatedSuspendedStartDate = ""
    patronUpdatedSuspendedEndDate = ""

    patronUpdatedBelayStartDate = ""
    patronUpdatedBelayEndDate = ""

    patronUpdatedLeadClimbStartDate = ""
    patronUpdatedLeadClimbEndDate = ""

    try:
        patronUpdatedSuspendedStartDate = str(request.form['updatedSuspendedStartDate'])
        patronUpdatedSuspendedEndDate = str(request.form['updatedSuspendedEndDate'])
    except:
        patronUpdatedSuspendedStartDate = ""
        patronUpdatedSuspendedEndDate = ""

    try:
        patronUpdatedBelayStartDate = str(request.form['updatedBelayStartDate'])
        patronUpdatedBelayEndDate = str(request.form['updatedBelayEndDate'])
    except:
        patronUpdatedBelayStartDate = ""
        patronUpdatedBelayEndDate = ""

    try:
        patronUpdatedLeadClimbStartDate = str(request.form['updatedLeadClimbStartDate'])
        patronUpdatedLeadClimbEndDate = str(request.form['updatedLeadClimbEndDate'])
    except:
        patronUpdatedLeadClimbStartDate = ""
        patronUpdatedLeadClimbEndDate = ""


    newPatronItem = Patron(str(request.form['updatedId']), str(request.form['updatedFirstName']), str(request.form['updatedLastName']), str(request.form['updatedEmail']).lower(), str(request.form['updatedPhoneNumber']), str(request.form['updatedGender']), str(request.form['updatedAddress']), str(request.form['updatedCity']), str(request.form['updatedZipCode']), "", str(request.form['updatedState']), str(request.form['updatedBelayStatus']), patronUpdatedBelayStartDate, patronUpdatedBelayEndDate, str(request.form['updatedLeadClimbStatus']), patronUpdatedLeadClimbStartDate, patronUpdatedLeadClimbEndDate, str(request.form['updatedIsSuspended']), patronUpdatedSuspendedStartDate, patronUpdatedSuspendedEndDate, str(request.form['updatedListServ']))
    databaseFunctions.editPatron(newPatronItem) 
    if session.get('currentUserAccountType') == 'administrator':
        return redirect('patronViewAdmin')
    else:
        return redirect('patronViewMaster')

def editPatronCertificationRoute():

    if not session.get('isLoggedIn'):
        return redirect('login')

    patronUpdatedBelayStartDate = ""
    patronUpdatedBelayEndDate = ""

    patronUpdatedLeadClimbStartDate = ""
    patronUpdatedLeadClimbEndDate = ""

    try:
        patronUpdatedBelayStartDate = str(request.form['certificateBelayStartDate'])
        patronUpdatedBelayEndDate = str(request.form['certificateBelayEndDate'])
    except:
        patronUpdatedBelayStartDate = ""
        patronUpdatedBelayEndDate = ""

    try:
        patronUpdatedLeadClimbStartDate = str(request.form['certificateLeadClimbStartDate'])
        patronUpdatedLeadClimbEndDate = str(request.form['certificateLeadClimbEndDate'])
    except:
        patronUpdatedLeadClimbStartDate = ""
        patronUpdatedLeadClimbEndDate = ""
    
    certificatePatronItem = Patron(str(request.form['certificateId']), "", "", "", "", "", "", "", "", "", "", str(request.form['certificateBelayStatus']), patronUpdatedBelayStartDate, patronUpdatedBelayEndDate, str(request.form['certificateLeadClimbStatus']), patronUpdatedLeadClimbStartDate, patronUpdatedLeadClimbEndDate, "", "", "", "")
    databaseFunctions.editPatronCertifications(certificatePatronItem) 

    if session.get('currentUserAccountType') == 'administrator':
        return redirect('patronViewAdmin')
    else:
        return redirect('patronViewMaster')

