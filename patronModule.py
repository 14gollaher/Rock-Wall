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
from globals import *
import sys
import base64
import urllib
import requests
import numpy as np
from PIL import Image

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

	patronAccount = Patron(str(request.form['patronId']), "", "", "", request.form['patronId'], "",  "", "" ,"" ,"" ,"","" ,"" , False,"" ,"", False, "", "", False, "", "", "")
	
	session['currentPatronId'] = patronAccount.id
	session['currentPatronEmail'] = patronAccount.email
	
	isValid = validateCredentials(patronAccount)
	if not isValid:
		isValid = validateEmail(patronAccount)
		session['currentPatronId'] = databaseFunctions.getPatronIdFromEmail(patronAccount)
		
	if isValid:
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

		
		if float(currentPatronId) < 0:
			currentPatronId = "Guest"

	else:
		session['messageBagPatron'] = 'ID or E-Mail does not exist!'
		return redirect('patronCheckIn')

	if currentPatronSuspensionStartDate and currentPatronSuspensionEndDate:
		startDate = datetime.strptime(currentPatronSuspensionStartDate, "%m/%d/%Y")
		endDate = datetime.strptime(currentPatronSuspensionEndDate, "%m/%d/%Y")
		today = datetime.today()
		if timeInRange(startDate, endDate, today):
			return redirect('patronSuspension')

	return render_template('patron/patronCheckIn.html', id = currentPatronId, firstName = currentPatronFirstName, lastName = currentPatronLastName, email = currentPatronEmail, phoneNumber = currentPatronPhoneNumber, address = currentPatronAddress, state = currentPatronState, city = currentPatronCity, zipCode = currentPatronZipCode, gender = currentPatronGender, isSuspended = currentPatronSuspension, pass2 = pass2)

def patronCheckInRoute2():

	patronAccount = Patron("", "", getRequestString('firstName'), getRequestString('lastName'), getRequestString('email'), getRequestString('phoneNumber'), getRequestString('gender'), getRequestString('address'),  getRequestString('city'), getRequestString('zipCode'), '', getRequestString('state'), False,"" ,"", False, "", "", False, "", "", "", "")
	patronAccount.id = databaseFunctions.getPatronIdFromEmail(patronAccount)
	databaseFunctions.editPatronAccount(patronAccount)

	myDate = datetime.now(pytz.timezone('US/Central'))
	newVisitLogItem = VisitHistoryLogItem("null", patronAccount.id, str(request.form['firstName']), str(request.form['lastName']), myDate.strftime("%m/%d/%Y"), myDate.strftime("%H:%M"))
	databaseFunctions.insertNewVisitHistoryItem(newVisitLogItem)
	return redirect('patronCheckIn')

def validateCredentials(patronAccount):

	if databaseFunctions.getPatronId(patronAccount):
		return True
	else:
		return False

def validateEmail(patronAccount):

	if databaseFunctions.getPatronEmailIfExists(patronAccount):
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

	patronAccount = Patron(str(request.form['id']), "", "", "", str(request.form['email']), "", "", "", "", "","", "", False, "", "", False, "", "", False, "", "", patronListServRequest, "")

	if databaseFunctions.getPatronId(patronAccount):
		session['messageBagPatron'] = 'Id already exists!'
		return redirect('patronSignUp')
	elif databaseFunctions.getPatronEmailIfExists(patronAccount):
		session['messageBagPatron'] = 'E-Mail already exists!'
		return redirect('patronSignUp')

	session['newPatronId'] = getRequestString('id')
	session['newPatronAccountType'] = getRequestString('accountType')
	session['newPatronFirstName'] = getRequestString('firstName')
	session['newPatronLastName'] = getRequestString('lastName')
	session['newPatronEmail'] = getRequestString('email')
	session['newPatronPhoneNumber'] = getRequestString('phoneNumber')
	session['newPatronGender'] = getRequestString('gender')
	session['newPatronAddress'] = getRequestString('address')
	session['newPatronState'] = getRequestString('state')
	session['newPatronCity'] = getRequestString('city')
	session['newPatronZipCode'] = getRequestString('zipCode')
	session['newPatronListServ'] = patronListServRequest

	session['currentPatronId'] = ""

	return redirect('signWaiver')

def signWaiver():
	if checkPreviousPage(['signWaiver']) == False:
		session['messageBagPatron'] = ""
	return render_template('patron/patronSignWaiver.html')

def patronSuspension():
	return render_template('patron/patronSuspension.html')

def signWaiverRoute():

	if session.get('currentPatronId') == "":
		file = open("sysSig.bteam", "r")
		waiverUrl = file.read()

		myDate = datetime.now(pytz.timezone('US/Central'))
		if session.get('newPatronAccountType') == "Guest":
			session['newPatronId'] = generateGuestId()
		newPatron = Patron(session.get('newPatronId'), session.get('newPatronAccountType'), session.get('newPatronFirstName'), session.get('newPatronLastName'), session.get('newPatronEmail').lower(), session.get('newPatronPhoneNumber'), session.get('newPatronGender'), session.get('newPatronAddress'), session.get('newPatronCity'), session.get('newPatronZipCode'), waiverUrl, session.get('newPatronState'), False, "", "", False, "", "", False, "", "", session.get('newPatronListServ'), myDate.strftime("%m/%d/%y"))

		databaseFunctions.insertNewPatron(newPatron)
		signPatronMinors(newPatron.id)
		file.close()
	else: 
		signPatronMinors(session.get('currentPatronId'))
	return redirect('patronCheckIn')


def signPatronMinors(patronSignId):
	patronMinorCount = 0
	while True:
		currentMinorFirstName = getRequestString("minorFirstName" + str(patronMinorCount))
		currentMinorLastName = getRequestString("minorLastName" + str(patronMinorCount))
		patronMinorCount += 1

		if currentMinorFirstName == "":
			break

		try:
			newPatronMinorId = int(float(databaseFunctions.getHighestPatronMinorId())) + 1
		except:
			newPatronMinorId = 100
		newPatronMinor = PatronMinor(newPatronMinorId, currentMinorFirstName, currentMinorLastName, patronSignId)
		databaseFunctions.insertNewPatronMinor(newPatronMinor)


def storeImage():

	url = request.form['data']
	file = open("sysSig.bteam", "w")

	filename = 'signature.jpg'

	urllib.request.urlretrieve(url, filename)

	signature = Image.open(filename)
	signature = alpha_to_color(signature)
	signatureW, signatureH = signature.size

	doc = 'document.jpg'

	unsigned = Image.open(doc)
	unsignedW, unsignedH = unsigned.size

	filename = 'signed.jpg'
	signed = Image.new('RGB', (unsignedW, (signatureH * 2) + unsignedH), 'white')

	signed.paste(signature, ((unsignedW - signatureW) // 2, unsignedH))
	signed.paste(unsigned, (0, 0))

	signed.save(filename)

	encoded = base64.b64encode(open("signed.jpg", "rb").read())

	stringEncode = str(encoded)
	stringEncode = stringEncode[2:-1]
	file.write("data:image/png;base64," + stringEncode)
	file.close()

	return redirect('signWaiver')

def alpha_to_color(image, color=(255, 255, 255)):

	x = np.array(image)
	r, g, b, a = np.rollaxis(x, axis=-1)
	r[a == 0] = color[0]
	g[a == 0] = color[1]
	b[a == 0] = color[2]
	x = np.dstack([r, g, b, a])
	return Image.fromarray(x, 'RGBA')

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

def generateGuestId():
	
	try:
		returnValue = int(float(databaseFunctions.getLowestPatronId())) - 1
	except:
		returnValue = -100

	return returnValue