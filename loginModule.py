import os
from flask import Flask, flash, redirect, render_template, request, session, abort
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

class UserAccount:

    def __init__(self, email, password, accountType, firstName, lastName):
        self.email = email
        self.password = password
        self.accountType = accountType
        self.firstName = firstName
        self.lastName = lastName

class Message:

    def __init__(self, id, author, time, content):
        self.id = id
        self.author = author
        self.time = time
        self.content = content

def login():
  
    if session.get('isLoggedIn'):
        return redirect('/')
    else:
        return render_template('login/login.html', messageLogin = session.get('messageLogin'))

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
    # session.clear() # Can't use this as it'd clear the patrons sessions as well. 
                      # Need to write an individual "clear desktop site" sessions function
    return redirect('login')

def loginRoute():

    session['messageLogin'] = ""

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
        session['messageLogin'] = 'Invalid Credentials!'
        return redirect('login')
    
    session['currentUserFirstName'] = databaseFunctions.getAccountFirstName(userAccount)
    session['currentUserLastName'] = databaseFunctions.getAccountLastName(userAccount)
    session['currentUserAccountType'] = databaseFunctions.getAccountType(userAccount)
    return redirect('/')

def createAccount():

    if session.get('isLoggedIn'):
        return redirect('/')
    return render_template('login/createAccount.html', messageCreateAccount = session.get('messageCreateAccount'))

def createAccountRoute(): 

    session['messageCreateAccount'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['password']), str(request.form['accountType']), str(request.form['firstName']), str(request.form['lastName']))
    postConfirmPassword = str(request.form['confirmPassword'])

    isCreateAccountSuccess = True

    if databaseFunctions.getAccountEmail(userAccount):
        session['messageCreateAccount'] = 'Email already exists!'
        isCreateAccountSuccess = False

    elif userAccount.password != postConfirmPassword:
        isCreateAccountSuccess = False  

    if isCreateAccountSuccess == False: 
        return redirect('createAccount')

    session['newAccountEmail'] = userAccount.email
    session['newAccountPassword'] = userAccount.password 
    session['newAccountType'] = userAccount.accountType
    session['newFirstName'] = userAccount.firstName
    session['newLastName'] = userAccount.lastName
    newAccountType = userAccount.accountType
   
    return render_template('login/authenticateCreateAccount.html', accountType = session.get('newAccountType'))

def authenticateCreateAccount():

    session['messageCreateAccount'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['password']), "", "", "")
    userAccount.accountType = databaseFunctions.getAccountType(userAccount)

    hashedPassword = pbkdf2_sha256.hash(session.get('newAccountPassword'))

    newUser = UserAccount(session.get('newAccountEmail'), hashedPassword, session.get('newAccountType'), session.get('newFirstName'), session.get('newLastName'))
    
    if validateCredentials(userAccount):
        if checkPermissionsPasswordChange(userAccount, newUser):
            databaseFunctions.insertNewUser(newUser)
        else:
            session['messageCreateAccount'] = 'Invalid Permissions!'
            return render_template('login/authenticateCreateAccount.html', messageCreateAccount = session.get('messageCreateAccount'))  
    else:
        session['messageCreateAccount'] = 'Invalid credentials!'
        return render_template('login/authenticateCreateAccount.html', messageCreateAccount = session.get('messageCreateAccount'))  

    session['isLoggedIn'] = False
    return redirect('login')

def changePassword():

    if session.get('isLoggedIn'):
        return redirect('/')
    return render_template('login/changePassword.html', messageChangePassword = session.get('messageChangePassword')) 

def changePasswordRoute():

    session['messageChangePassword'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['newPassword']), "", "", "")
    userAccount.accountType = databaseFunctions.getAccountType(userAccount)
    postConfirmNewPassword = str(request.form['newConfirmPassword'])

    isChangePasswordSuccess = True
    
    if not databaseFunctions.getAccountEmail(userAccount):
        session['messageChangePassword'] = 'Email does not exist!'
        isChangePasswordSuccess = False

    elif userAccount.password != postConfirmNewPassword:
        isChangePasswordSuccess = False

    if isChangePasswordSuccess == False: 
        return redirect('changePassword')

    session['changePasswordEmail'] = userAccount.email
    session['changePasswordNewPassword'] = userAccount.password
    session['changePasswordAccountType'] = databaseFunctions.getAccountType(userAccount)

    return render_template('login/authenticateChangePassword.html', accountType = session.get('changePasswordAccountType')) 


def authenticateChangePassword():
    session['messageChangePassword'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['password']), "", "", "")
    userAccount.accountType = databaseFunctions.getAccountType(userAccount)
    passwordChangeAccount = UserAccount(session['changePasswordEmail'], session['changePasswordNewPassword'], session['changePasswordAccountType'], "", "")

    if validateCredentials(userAccount):
        if checkPermissionsPasswordChange(userAccount, passwordChangeAccount):
            databaseFunctions.changePassword(passwordChangeAccount, session.get('changePasswordNewPassword'))
        else:
            session['messageChangePassword'] = 'Invalid Permissions!'
            return render_template('authenticateChangePassword.html', messageChangePassword = session.get('messageChangePassword'))  
    else:
        session['messageChangePassword'] = 'Invalid credentials!'
        return render_template('login/authenticateChangePassword.html', messageChangePassword = session.get('messageChangePassword'))  

    session['isLoggedIn'] = False
    return redirect('login')

def validateCredentials(userAccount):

    # Code Snippet to add the Master Account
    #hashedPassword = hashedPassword = pbkdf2_sha256.hash('abc123')
    #newUser = UserAccount('master@gmail.com', hashedPassword, 'Master', 'Justin', 'Parks')
    #databaseFunctions.insertNewUser(newUser)    

    if pbkdf2_sha256.verify(userAccount.password, databaseFunctions.getAccountPassword(userAccount)):
        return True
    else:
        return False

def checkPermissionsPasswordChange(userAccount, userChangeAccount):
    if userChangeAccount.accountType == 'Employee' and databaseFunctions.getAccountType(userAccount) == 'Administrator':
       return True
    elif userChangeAccount.accountType == 'Employee' and databaseFunctions.getAccountType(userAccount) == 'Master':
       return True
    elif userChangeAccount.accountType == 'Administrator' and databaseFunctions.getAccountType(userAccount) == 'Master':
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