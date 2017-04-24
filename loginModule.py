import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import itertools
from itertools import *
import re
import pytz
from passlib.hash import pbkdf2_sha256
import simplejson as json
from globals import *

def login():

    # Code Snippet to add the Master Account
    #hashedPassword = hashedPassword = pbkdf2_sha256.hash('abc123')
    #newUser = UserAccount('master@gmail.com', hashedPassword, 'Master', 'Justin', 'Parks')
    #databaseFunctions.insertNewUser(newUser) 

    try:
        if checkPreviousPage(['login']) == False:
            session['messageBag'] = ""
    except:
        session['messageBag'] = ""

    if session.get('isLoggedIn'):
        return redirect('/')
    else:
        return render_template('login/login.html')

def index():
    
    if not session.get('isLoggedIn'):
        return redirect('login')

    mT = populateMessagesTable()
    tVT = populateTodaysVisitsTable()
    tTV = sum(tVT)
    wVT = populateWeeksVisitTable()
    tWV = sum(wVT)
    mVT = populateMonthVisitTable()
    tMV = sum(mVT)

    return render_template('menu.html', currentUserFirstName = session.get('currentUserFirstName'), messageTable = mT, todaysVisitsTable = tVT, totalTodaysVisits = tTV, weeksVisitTable = wVT, totalWeekVisists = tWV, monthVisitTable = mVT, totalMonthVisits = tMV)

def populateMessagesTable ():
    
    messageTable = {}
    messageTable['author'] = databaseFunctions.getTop100MessageAuthors()
    messageTable['time'] = databaseFunctions.getTop100MessageTimes()
    messageTable['content'] = databaseFunctions.getTop100MessageContents()
    
    messageTable = [dict(author=a, time=t, content=c) for a, t, c in zip(messageTable['author'], messageTable['time'], messageTable['content'])]

    return messageTable

def populateTodaysVisitsTable ():

    allPatronVisitsDates = databaseFunctions.getAllVisitPatronVisitDates()
    allPatronsVisitsTimes = databaseFunctions.getAllVisitPatronVisitTimes()

    todaysTimes = []

    for i in range(0, len(allPatronVisitsDates)):
        dateTimeStart = allPatronVisitsDates[i]

        currentTime = datetime.now(pytz.timezone('US/Central'))
        today = date(currentTime.year, currentTime.month,currentTime.day) 

        thisVisit = datetime.strptime(dateTimeStart, "%m/%d/%Y")
        
        if thisVisit.day == today.day and thisVisit.month == today.month and thisVisit.year == today.year:
            todaysTimes.append(allPatronsVisitsTimes[i])
   
    todaysVisitsTable = [0] * 12

    for visit in todaysTimes:
        
        currentLowerBoundHourCheck = 0
        currentUpperBoundHourCheck = 2
        currentRangeIndex = 0

        for i in range (0, 12):

            if (currentUpperBoundHourCheck > 23):
                currentUpperBoundHourCheck = 23
        
            start = time(currentLowerBoundHourCheck, 0)
            end = time(currentUpperBoundHourCheck, 0)
            
            thisVisit = datetime.strptime(visit, "%H:%M")
            checkTime = time(thisVisit.hour, thisVisit.minute)

            if timeInRange(start, end, checkTime):
                todaysVisitsTable[currentRangeIndex] += 1 
                break;

            currentLowerBoundHourCheck += 2
            currentUpperBoundHourCheck += 2
            currentRangeIndex += 1
        
    return todaysVisitsTable

def populateWeeksVisitTable():

    allPatronVisitsDates = databaseFunctions.getAllVisitPatronVisitDates()
    allPatronsVisitsTimes = databaseFunctions.getAllVisitPatronVisitTimes()

    weekVisitsTable = [0] * 7
    
    for visit in allPatronVisitsDates:
    
        currentIndex = 0

        for i in range(0, 7):

            dateTimeStart = visit

            thisVisit = datetime.strptime(dateTimeStart, "%m/%d/%Y")
        
            currentTime = datetime.now(pytz.timezone('US/Central'))
            today = date(currentTime.year, currentTime.month,currentTime.day) 

            margin = timedelta(days = i)
            evaluateVisit = date(thisVisit.year, thisVisit.month, thisVisit.day)
        
            if today - margin <= evaluateVisit:
                weekVisitsTable[len(weekVisitsTable) - 1 - currentIndex] += 1
                break;
            else:
                currentIndex += 1
    
    return weekVisitsTable

def populateMonthVisitTable():

    allPatronVisitsDates = databaseFunctions.getAllVisitPatronVisitDates()
    allPatronsVisitsTimes = databaseFunctions.getAllVisitPatronVisitTimes()

    monthVisitsTable = [0] * 12

    for visit in allPatronVisitsDates:
    
        currentIndex = 0

        for i in range(0, 12):

            dateTimeStart = visit

            thisVisit = datetime.strptime(dateTimeStart, "%m/%d/%Y")
            
            currentTime = datetime.now(pytz.timezone('US/Central'))
            today = date(currentTime.year, currentTime.month,currentTime.day) 

            today = today + relativedelta(months = -i)


            start = date(today.year, today.month, 1)
            end = date.today()

            evaluateVisit = date(thisVisit.year, thisVisit.month, thisVisit.day)
        
            if timeInRange (start, end, evaluateVisit):
                monthVisitsTable[len(monthVisitsTable) - 1 - currentIndex] += 1
                break;
            else:
                currentIndex += 1
    
    return monthVisitsTable


def timeInRange(start, end, x):

    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def logout():

    session['isLoggedIn'] = False

    return redirect('login')

def loginRoute():

    userAccount = UserAccount(str(request.form['email']), str(request.form['password']), "", "", "")
    
    if validateCredentials(userAccount): 

        session['isLoggedIn'] = True
        
        if databaseFunctions.getAccountType(userAccount) == 'Employee':
            session['sessionType'] = 'Employee'
        if databaseFunctions.getAccountType(userAccount) == 'Administrator':
            session['sessionType'] = 'Administrator'
        if databaseFunctions.getAccountType(userAccount) == 'Master':
            session['sessionType'] = 'Master'
    else:
        session['messageBag'] = 'Invalid Credentials!'
        return redirect('login')
    
    session['currentUserFirstName'] = databaseFunctions.getAccountFirstName(userAccount)
    session['currentUserLastName'] = databaseFunctions.getAccountLastName(userAccount)
    session['currentUserAccountType'] = databaseFunctions.getAccountType(userAccount)
    return redirect('/')

def createAccount():
    
    if session.get('isLoggedIn'):
        return redirect('/')

    if checkPreviousPage(['createAccountRoute', 'createAccount']) == False:
            session['messageBag'] = ""
            
    
    if checkPreviousPage(['createAccountRoute', 'createAccount']):
            pass2 = []
            pass2.append('T')
            pass2 = json.dumps(pass2)
            createAccount = UserAccount("", "", session.get('newAccountType'), session.get('newAccountFirstName'), session.get('newAccountLastName'))
    else:
        createAccount = UserAccount("", "", "", "", "")
        pass2 = []
        pass2.append('F')
        pass2 = json.dumps(pass2)

    return render_template('login/createAccount.html', firstName = createAccount.firstName, lastName = createAccount.lastName, accountType = createAccount.accountType, pass2 = pass2) 

def createAccountRoute(): 
    
    if checkPreviousPage(['createAccountRoute', 'createAccount']) == False:
        session['messageBag'] = ""

    createAccount = UserAccount(str(request.form['email']), str(request.form['password']), str(request.form['accountType']), str(request.form['firstName']), str(request.form['lastName']))
    postConfirmPassword = str(request.form['confirmPassword'])

    if databaseFunctions.getAccountEmail(createAccount):
        session['messageBag'] = 'Email already exists!'
        return redirect('createAccount')        
    session['messageBag'] = ""
    session['newAccountEmail'] = createAccount.email
    session['newAccountPassword'] = createAccount.password 
    session['newAccountType'] = createAccount.accountType
    session['newAccountFirstName'] = createAccount.firstName
    session['newAccountLastName'] = createAccount.lastName

    pass2 = []
    pass2.append('T')
    pass2 = json.dumps(pass2)   

    return render_template('login/createAccount.html', firstName = createAccount.firstName, lastName = createAccount.lastName, accountType = createAccount.accountType, pass2 = pass2) 

def authenticateCreateAccount():

    validateAccount  = UserAccount(str(request.form['validateEmail']), str(request.form['validatePassword']), "", "", "")
    validateAccount.accountType = databaseFunctions.getAccountType(validateAccount)
    print (session.get('newAccountPassword'))
    hashedPassword = pbkdf2_sha256.hash(session.get('newAccountPassword'))

    createAccount = UserAccount(session.get('newAccountEmail').lower(), hashedPassword, session.get('newAccountType'), session.get('newAccountFirstName'), session.get('newAccountLastName'))
    
    if validateCredentials(validateAccount):
        if checkPermissionsPasswordChange(validateAccount, createAccount):
            databaseFunctions.insertNewUser(createAccount)
        else:
            session['messageBag'] = 'Invalid Authorization Permissions!'
            return redirect ('createAccount')
    else:
        session['messageBag'] = 'Invalid Authorization Credentials!'
        return redirect ('createAccount')

    return redirect('login')

def changePassword():
    
    if session.get('isLoggedIn'):
        return redirect('/')

    if checkPreviousPage(['changePasswordRoute', 'changePassword']) == False:
            session['messageBag'] = ""
    
    if checkPreviousPage(['changePasswordRoute']):
        pass2 = []
        pass2.append('T')
        pass2 = json.dumps(pass2)

        changePasswordAccount = UserAccount("", "", session.get('changePasswordAccountType'), session.get('changePasswordFirstName'), session.get('changePasswordLastName'))

    else:
        changePasswordAccount = UserAccount("", "", "", "", "")
        pass2 = []
        pass2.append('F')
        pass2 = json.dumps(pass2)
   
    return render_template('login/changePassword.html', firstName = changePasswordAccount.firstName, lastName = changePasswordAccount.lastName, accountType = changePasswordAccount.accountType, pass2 = pass2) 


def changePasswordRoute():

    if checkPreviousPage(['changePasswordRoute']) == False:
            session['messageBag'] = ""

    changePasswordAccount = UserAccount(str(request.form['email']), str(request.form['newPassword']), "", "", "")
    changePasswordAccount.accountType = databaseFunctions.getAccountType(changePasswordAccount)
    changePasswordAccount.firstName = databaseFunctions.getAccountFirstName(changePasswordAccount)
    changePasswordAccount.lastName = databaseFunctions.getAccountLastName(changePasswordAccount)

    postConfirmNewPassword = str(request.form['newConfirmPassword'])

    if not databaseFunctions.getAccountEmail(changePasswordAccount):
        session['messageBag'] = 'Email does not exist!'
        return redirect('changePassword')

    elif changePasswordAccount.password != postConfirmNewPassword:
        session['messageBag'] = 'Passwords do not match!'
        return redirect('changePassword')
    
    session['changePasswordEmail'] = changePasswordAccount.email
    session['changePasswordAccountType'] = changePasswordAccount.accountType
    session['changePasswordFirstName'] = changePasswordAccount.firstName
    session['changePasswordLastName'] = changePasswordAccount.lastName
    session['changePasswordNewPassword'] = postConfirmNewPassword  

    pass2 = []
    pass2.append('T')
    pass2 = json.dumps(pass2)

    return render_template('login/changePassword.html', email = changePasswordAccount.email, firstName = changePasswordAccount.firstName, lastName = changePasswordAccount.lastName, accountType = changePasswordAccount.accountType, pass2 = pass2) 


def authenticateChangePassword():

    validateAccount = UserAccount(str(request.form['validateEmail']), str(request.form['validatePassword']), "", "", "")
    validateAccount.accountType = databaseFunctions.getAccountType(validateAccount)
    passwordChangeAccount = UserAccount(session['changePasswordEmail'], session['changePasswordNewPassword'], "", "", "")
    passwordChangeAccount.accountType = databaseFunctions.getAccountType(passwordChangeAccount)
    
    if validateCredentials(validateAccount):
        if checkPermissionsPasswordChange(validateAccount, passwordChangeAccount):
            hashedPassword = pbkdf2_sha256.hash(session.get('changePasswordNewPassword'))
            databaseFunctions.changePassword(passwordChangeAccount, hashedPassword)
            
        else:
            session['messageBag'] = 'Invalid Authorization Permissions!'
            return redirect('changePassword')  
    else:
        session['messageBag'] = 'Invalid Authorization Credentials!'
        return redirect('changePassword')
    return redirect('login')

def validateCredentials(userAccount):
   
    try:
        if pbkdf2_sha256.verify(userAccount.password, databaseFunctions.getAccountPassword(userAccount)):
            return True
        else:
            return False
    except:
        return False

def checkPermissionsPasswordChange(userAccount, userChangeAccount):

    if userChangeAccount.accountType == 'Employee' and userAccount.accountType == 'Administrator':
       return True
    elif userChangeAccount.accountType == 'Employee' and userAccount.accountType == 'Master':
       return True
    elif userChangeAccount.accountType == 'Administrator' and userAccount.accountType == 'Master':
        return True
    else:
        return False

def addMessage():

    currentUserFullName = session.get('currentUserFirstName') + ' ' + session.get('currentUserLastName')
    currentTime = datetime.now(pytz.timezone('US/Central'))
    newMessage = Message('-1Nullx0', str(currentUserFullName), str(currentTime.strftime('%b-%d %I:%M %p')), str(request.form['content']))
    newMessage.content = newMessage.content
    databaseFunctions.insertNewMessage(newMessage)
    return redirect('/')

def checkPreviousPage(listGoodPages):

    checkValue = request.referrer.split('/')
    for page in listGoodPages:
        if checkValue[3] == page:
             return True
    return False
   

