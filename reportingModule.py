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

class IncidentReport:
	def __init__(self, id, time, date, description, author, isReviewed):
		self.id = id
		self.time = time
		self.date = date
		self.description = description
		self.author = author
		self.isReviewed = isReviewed

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

def reporting():

	if not session.get('isLoggedIn'):
		return redirect('login')

	if session.get('currentUserAccountType') == 'Employee':
		return redirect('reportingEmployee')
	elif session.get('currentUserAccountType') == 'Administrator':
		return redirect('reportingAdmin')
	elif session.get('currentUserAccountType') == 'Master':
		return redirect('reportingMaster')
	
def reportingEmployee():

	if not session.get('isLoggedIn'):
		return redirect('login')

	return render_template('reporting.html')

def reportingAdmin():

	if not session.get('isLoggedIn'):
		return redirect('login')

	try:
		reportTable = {}
		reportTable['id'] = databaseFunctions.getAllIncidentReportIds()
		reportTable['time'] = databaseFunctions.getAllIncidentReportTimes()
		reportTable['date'] = databaseFunctions.getAllIncidentReportDates()
		reportTable['description'] = databaseFunctions.getAllIncidentReportDescriptions()
		reportTable['author'] = databaseFunctions.getAllIncidentReportAuthors()
		reportTable['isReviewed'] = databaseFunctions.getAllIncidentReportIsRevieweds()

		reportTable = [dict(id=i, time=t, date=d, description=de, author=a, isReviewed=ir) for i, t, d, de, a, ir in zip(reportTable['id'], reportTable['time'], reportTable['date'], reportTable['description'], reportTable['author'], reportTable['isReviewed'])]
	except:
		reportTable = {}

	try:
		patronTable = {}
		patronTable = {}
		patronTable['id'] = databaseFunctions.getAllPatronIds()
		patronTable['firstName'] = databaseFunctions.getAllPatronFirstNames()
		patronTable['lastName'] = databaseFunctions.getAllPatronLastNames()
		patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
		patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
		patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()

		for i in range (len(patronTable['id'])):
			if float(patronTable['id'][i]) < 0:
			   patronTable['id'][i] = "Guest"
		patronTable = [dict(id=i, firstName=f, lastName=l, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se) for i, f, l, su, ss, se in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'])]
	except:
		patronTable = {}
	
	return render_template('reportingManager.html', reportTable = reportTable, patronTable = patronTable)


def reportingMaster():
	
	if not session.get('isLoggedIn'):
		return redirect('login')

	try:
		reportTable = {}
		reportTable['id'] = databaseFunctions.getAllIncidentReportIds()
		reportTable['time'] = databaseFunctions.getAllIncidentReportTimes()
		reportTable['date'] = databaseFunctions.getAllIncidentReportDates()
		reportTable['description'] = databaseFunctions.getAllIncidentReportDescriptions()
		reportTable['author'] = databaseFunctions.getAllIncidentReportAuthors()
		reportTable['isReviewed'] = databaseFunctions.getAllIncidentReportIsRevieweds()

		reportTable = [dict(id=i, time=t, date=d, description=de, author=a, isReviewed=ir) for i, t, d, de, a, ir in zip(reportTable['id'], reportTable['time'], reportTable['date'], reportTable['description'], reportTable['author'], reportTable['isReviewed'])]
	except:
		reportTable = {}

	try:
		patronTable = {}
		patronTable['id'] = databaseFunctions.getAllPatronIds()
		patronTable['firstName'] = databaseFunctions.getAllPatronFirstNames()
		patronTable['lastName'] = databaseFunctions.getAllPatronLastNames()
		patronTable['isSuspended'] = databaseFunctions.getAllPatronSuspensions()
		patronTable['suspendedStartDate'] = databaseFunctions.getAllPatronSuspensionStartDates()
		patronTable['suspendedEndDate'] = databaseFunctions.getAllPatronSuspensionEndDates()

		for i in range (len(patronTable['id'])):
			if float(patronTable['id'][i]) < 0:
			   patronTable['id'][i] = "Guest"

		patronTable = [dict(id=i, firstName=f, lastName=l, isSuspended = su, suspendedStartDate = ss, suspendedEndDate = se) for i, f, l, su, ss, se in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['isSuspended'], patronTable['suspendedStartDate'], patronTable['suspendedEndDate'])]
	except:
		patronTable = {}

	return render_template('reportingManager.html', reportTable = reportTable, patronTable = patronTable)


def addIncidentRoute():

	if not session.get('isLoggedIn'):
		return redirect('login')

	currentUserFullName = session.get('currentUserFirstName') + ' ' + session.get('currentUserLastName')
	newIncidentReport = IncidentReport("null", str(request.form['incidentTime']), str(request.form['incidentDate']), str(request.form['incidentDescription']), currentUserFullName, "No")
	databaseFunctions.insertNewIncidentReport(newIncidentReport)
	return redirect('reporting')


def toggleReportReviewStatus():

	if not session.get('isLoggedIn'):
		return redirect('login')

	if str(request.form['isReviewed']) == 'Yes':
		incidentReport = IncidentReport(str(request.form['id']), "", "", "", "", "No" )
	else:
		incidentReport = IncidentReport(str(request.form['id']), "", "", "", "", "Yes" )
	databaseFunctions.toggleIncidentReportIsReviewed(incidentReport)

	return redirect('reporting')

def editPatronSuspensionRoute():
	if not session.get('isLoggedIn'):
	   return redirect('login')

	patronUpdatedStartDate = ""
	patronUpdatedEndDate = ""
	try:
		patronUpdatedStartDate = str(request.form['updatedPatronSuspensionStartDate'])
		patronUpdatedEndDate = str(request.form['updatedPatronSuspensionEndDate'])
	except:
		patronUpdatedStartDate = ""
		patronUpdatedEndDate = ""
	newPatronItem = Patron(str(request.form['updatedPatronId']), "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", str(request.form['updatedPatronSuspensionStatus']),  patronUpdatedStartDate, patronUpdatedEndDate, "")
	databaseFunctions.editPatronSuspensions(newPatronItem)
	if session.get('currentUserAccountType') == 'administrator':
		return redirect('reportingAdmin')
	else:
		return redirect('reportingMaster')
