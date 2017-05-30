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
	
	try:
		patronTable = {}
		patronTable['id'] = databaseFunctions.getAllPatronIds()
		patronTable['accountType'] = databaseFunctions.getAllPatronAccountTypes()
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

		for i in range (len(patronTable['id'])):
			if float(patronTable['id'][i]) < 0:
			   patronTable['id'][i] = "Guest"

		patronTable = [dict(id=i, accountType=aT, firstName=f, lastName=l, isBelayCertified=b, belayStartDate=bsd, belayEndDate=bed, isLeadClimbCertified = lcc, leadClimbStartDate = lcsd, leadClimbEndDate = lced, isSuspended = su, suspendedStartDate = st, suspendedEndDate = e, listServ = ls) for i, aT, f, l, b, bsd, bed, lcc, lcsd, lced, su, st, e, ls in zip(patronTable['id'], patronTable['accountType'], patronTable['firstName'], patronTable['lastName'], patronTable['isBelayCertified'], patronTable['belayStartDate'], patronTable['belayEndDate'], patronTable['isLeadClimbCertified'], patronTable['leadClimbStartDate'], patronTable['leadClimbEndDate'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'], patronTable['listServ'])]
	except:
		patronTable = {}

	return render_template('viewPatronEmployee.html', patronTable = patronTable)

def patronViewAdmin():
	if not session.get('isLoggedIn'):
		return redirect('login')
	try:
		patronTable = {}
		patronTable['id'] = databaseFunctions.getAllPatronIds()
		patronTable['accountType'] = databaseFunctions.getAllPatronAccountTypes()
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
		patronTable['belayStartDate'] = databaseFunctions.getAllPatronBelayStartDates()
		patronTable['belayEndDate'] = databaseFunctions.getAllPatronBelayEndDates()
		patronTable['isLeadClimbCertified'] = databaseFunctions.getAllPatronLeadClimbCertifications()
		patronTable['leadClimbStartDate'] = databaseFunctions.getAllPatronLeadClimbStartDates()
		patronTable['leadClimbEndDate'] = databaseFunctions.getAllPatronLeadClimbEndDates()
		patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
		patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
		patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()
		patronTable['listServ'] = databaseFunctions.getAllPatronListServ()

		for i in range (len(patronTable['id'])):
			if float(patronTable['id'][i]) < 0:
			   patronTable['id'][i] = "Guest"
	
		patronTable = [dict(id=i, accountType=aT, firstName=f, lastName=l, email=e, phoneNumber=p, gender=g, address=a, city=c, zipCode=z, state=s, isBelayCertified = b, belayStartDate =bsd, belayEndDate =bed, isLeadClimbCertified = lcc, leadClimbStartDate = lcsd, leadClimbEndDate = lced, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se, listServ = ls) for i, aT, f, l, e, p, g, a, c, z, s, b, bsd, bed, lcc, lcsd, lced, su, ss, se, ls in zip(patronTable['id'], patronTable['accountType'], patronTable['firstName'], patronTable['lastName'], patronTable['email'], patronTable['phoneNumber'], patronTable['gender'], patronTable['address'], patronTable['city'], patronTable['zipCode'], patronTable['state'], patronTable['isBelayCertified'], patronTable['belayStartDate'], patronTable['belayEndDate'], patronTable['isLeadClimbCertified'], patronTable['leadClimbStartDate'], patronTable['leadClimbEndDate'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'], patronTable['listServ'])]
	except:
		patronTable = {}

	try:
		visitTable = {}
		visitTable['Id'] = databaseFunctions.getAllVisitIds()
		visitTable['PatronId'] = databaseFunctions.getAllVisitPatronIds()
		visitTable['PatronFirstName'] = databaseFunctions.getAllVisitPatronFirstNames()
		visitTable['PatronLastName'] = databaseFunctions.getAllVisitPatronLastNames()
		visitTable['PatronVisitDate'] = databaseFunctions.getAllVisitPatronVisitDates()
		visitTable['PatronVisitTime'] = databaseFunctions.getAllVisitPatronVisitTimes()

		visitTable = [dict(id=i, patronId=pI, patronFirstName=f, patronLastName=l, patronVistDate=d, patronVisitTime=t) for i, pI, f, l, d, t in zip(visitTable['Id'], visitTable['PatronId'], visitTable['PatronFirstName'], visitTable['PatronLastName'], visitTable['PatronVisitDate'], visitTable['PatronVisitTime'])]
	except:
		visitTable = {}

	return render_template('viewPatronManager.html', patronTable = patronTable, visitTable = visitTable)

def patronViewMaster():
	if not session.get('isLoggedIn'):
		return redirect('login')
	
	try:
		patronTable = {}
		patronTable['id'] = databaseFunctions.getAllPatronIds()
		patronTable['accountType'] = databaseFunctions.getAllPatronAccountTypes()
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
		patronTable['waiverSignDate'] = databaseFunctions.getAllPatronWaiverSignDate()

		for i in range (len(patronTable['id'])):
			if float(patronTable['id'][i]) < 0:
			   patronTable['id'][i] = "G" + str(patronTable['id'][i])
	
		patronTable = [dict(id=i, accountType=aT, firstName=f, lastName=l, email=e, phoneNumber=p, gender=g, address=a, city=c, zipCode=z, state=s, waiver=w, isBelayCertified = b, belayStartDate =bsd, belayEndDate =bed, isLeadClimbCertified = lcc, leadClimbStartDate = lcsd, leadClimbEndDate = lced, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se, listServ = ls, waiverSignDate = wS) for i, aT, f, l, e, p, g, a, c, z, s, w, b, bsd, bed, lcc, lcsd, lced, su, ss, se, ls, wS in zip(patronTable['id'], patronTable['accountType'], patronTable['firstName'], patronTable['lastName'], patronTable['email'], patronTable['phoneNumber'], patronTable['gender'], patronTable['address'], patronTable['city'], patronTable['zipCode'], patronTable['state'], patronTable['waiver'], patronTable['isBelayCertified'], patronTable['belayStartDate'], patronTable['belayEndDate'], patronTable['isLeadClimbCertified'], patronTable['leadClimbStartDate'], patronTable['leadClimbEndDate'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'], patronTable['listServ'], patronTable['waiverSignDate'])]
	except:
		patronTable = {}

	try:
		visitTable = {}
		visitTable['Id'] = databaseFunctions.getAllVisitIds()
		visitTable['PatronId'] = databaseFunctions.getAllVisitPatronIds()
		visitTable['PatronFirstName'] = databaseFunctions.getAllVisitPatronFirstNames()
		visitTable['PatronLastName'] = databaseFunctions.getAllVisitPatronLastNames()
		visitTable['PatronVisitDate'] = databaseFunctions.getAllVisitPatronVisitDates()
		visitTable['PatronVisitTime'] = databaseFunctions.getAllVisitPatronVisitTimes()

		
		for i in range (len(visitTable['PatronId'])):
			if float(visitTable['PatronId'][i]) < 0:
			   visitTable['PatronId'][i] = "G" + str(visitTable['PatronId'][i])

		visitTable = [dict(id=i, patronId=pI, patronFirstName=f, patronLastName=l, patronVistDate=d, patronVisitTime=t) for i, pI, f, l, d, t in zip(visitTable['Id'], visitTable['PatronId'], visitTable['PatronFirstName'], visitTable['PatronLastName'], visitTable['PatronVisitDate'], visitTable['PatronVisitTime'])]
	except:
		visitTable = {}


	try:
		patronMinorTable = {}
		patronMinorTable['FirstName'] = databaseFunctions.getAllPatronMinorFirstNames()
		patronMinorTable['LastName'] = databaseFunctions.getAllPatronMinorLastNames()
		patronMinorTable['PatronId'] = databaseFunctions.getAllPatronMinorPatronIds()


		for i in range (len(patronMinorTable['PatronId'])):
			if float(patronMinorTable['PatronId'][i]) < 0:
			   patronMinorTable['PatronId'][i] = "G" + str(patronMinorTable['PatronId'][i])

		patronMinorTable = [dict(firstName=f, lastName=l, patronId=p) for f, l, p in zip(patronMinorTable['FirstName'], patronMinorTable['LastName'], patronMinorTable['PatronId'])]
	except:	
		patronMinorTable = {}

	return render_template('viewPatronManager.html', patronTable = patronTable, visitTable = visitTable, patronMinorTable = patronMinorTable)

def patronDelete():
	if not session.get('isLoggedIn'):
		return redirect('login')

	patronToDelete = Patron(str(request.form['id']), "", "", "", "", "", "", "", "", "","", "", False, "", "", False, "", "", False, "", "", False, "")
	patronToDelete.id = patronToDelete.id.strip('"')
	databaseFunctions.deletePatronItem(patronToDelete)

	return redirect('patronViewManager')

def patronDeleteAll():
	if not session.get('isLoggedIn'):
		return redirect('login')
	
	databaseFunctions.deleteAllPatrons()
	return redirect('patronViewManager')

def editPatronRoute():
	if not session.get('isLoggedIn'):
		return redirect('login')

	newPatronItem = Patron(getRequestString('updatedId'), getRequestString('updatedAccountType'), getRequestString('updatedFirstName'), getRequestString('updatedLastName'), getRequestString('updatedEmail').lower(), getRequestString('updatedPhoneNumber'), getRequestString('updatedGender'), getRequestString('updatedAddress'), getRequestString('updatedCity'), getRequestString('updatedZipCode'), "", getRequestString('updatedState'), "", "", "", "", "", "", "" , "", "", getRequestString("updatedListServ"), "")
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
	
	certificatePatronItem = Patron(str(request.form['certificateId']), "", "", "", "", "", "", "", "", "", "", "", str(request.form['certificateBelayStatus']), patronUpdatedBelayStartDate, patronUpdatedBelayEndDate, str(request.form['certificateLeadClimbStatus']), patronUpdatedLeadClimbStartDate, patronUpdatedLeadClimbEndDate, "", "", "", "", "")
	databaseFunctions.editPatronCertifications(certificatePatronItem) 

	if session.get('currentUserAccountType') == 'administrator':
		return redirect('patronViewAdmin')
	else:
		return redirect('patronViewMaster')
