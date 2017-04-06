import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions

class UserAccount:
    def __init__(self, email, password, accountType, firstName, lastName):
        self.email = email
        self.password = password
        self.accountType = accountType
        self.firstName = firstName
        self.lastName = lastName

def login():
    if session.get('isLoggedIn'):
        return redirect('/')
    else:
        return render_template('login/login.html', messageLogin = session.get('messageLogin'))

def index():
    logMessage('Begin Menu')
    if session.get('isLoggedIn'):
        if session.get('sessionType') == 'employee':
            return redirect('employeeMenu')
        elif session.get('sessionType') == 'administrator':
            return redirect('administratorMenu')
        elif session.get('sessionType') == 'master':
            return redirect('masterMenu')
        else: 
            logMessage('Unhandled Expection @ index()')
            return redirect('login')
    else:
        return redirect('login')

def employeeMenu():
    messageTable = {}
    messageTable['author'] = databaseFunctions.getTop100MessageAuthors()
    messageTable['time'] = databaseFunctions.getTop100MessageTimes()
    messageTable['content'] = databaseFunctions.getTop100MessageContents()
    messageTable = [dict(author=a, time=t, content=c) for a, t, c in zip(messageTable['author'], messageTable['time'], messageTable['content'])]

    if session.get('isLoggedIn'):
        if session.get('sessionType') == 'employee':
            return render_template('employeeMenu.html', currentUserFirstName = session.get('currentUserFirstName'), messageTable = messageTable)
        elif session.get('sessionType') == 'administrator':
            return redirect('administratorMenu')
        elif session.get('sessionType') == 'master':
            return redirect('masterMenu')
        else: 
            logMessage('Unhandled Expection @ employeeMenu()')
            return redirect('login')
    else:
        return redirect('login')

def administratorMenu():
    if session.get('isLoggedIn'):
        if session.get('sessionType') == 'employee':
            return redirect('employeeMenu')
        elif session.get('sessionType') == 'administrator':
            return render_template('adminMenu.html')
        #"Hello Administrator!  <a href='/logout'>Logout</a>"
        elif session.get('sessionType') == 'master':
            return redirect('masterMenu')
        else: 
            logMessage('Unhandled Expection @ administratorMenu()')
            return redirect('login')
    else:
        return redirect('login')

def masterMenu():
    if session.get('isLoggedIn'):
        if session.get('sessionType') == 'employee':
            return redirect('employeeMenu')
        elif session.get('sessionType') == 'administrator':
            return redirect('administratorMenu')
        elif session.get('sessionType') == 'master':
            return "Hello Master!  <a href='/logout'>Logout</a>"
        else: 
            logMessage('Unhandled Expection @ masterMenu()')
            return redirect('login')
    else:
        return redirect('login')

def logout():
    logMessage('Begin logout')
    session['isLoggedIn'] = False
    session['sessionType'] = ""
    return redirect('login')

def loginRoute():
    logMessage('Begin login')
    session['messageLogin'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['password']), "", "", "")
    
    if validateCredentials(userAccount): 
        session['isLoggedIn'] = True
        
        if databaseFunctions.getAccountType(userAccount) == 'employee':
            session['sessionType'] = 'employee'
        if databaseFunctions.getAccountType(userAccount) == 'administrator':
            session['sessionType'] = 'administrator'
        if databaseFunctions.getAccountType(userAccount) == 'master':
            session['sessionType'] = 'master'
    else:
        session['messageLogin'] = 'Invalid Credentials!'
        return redirect('login')
    
    session['currentUserFirstName'] = databaseFunctions.getAccountFirstName(userAccount)
    session['currentUserLastName'] = databaseFunctions.getAccountLastName(userAccount)
    return redirect('/')

def createAccount():
    logMessage('Begin createAccount')
    if session.get('isLoggedIn'):
        return redirect('/')
    return render_template('login/createAccount.html', messageCreateAccount = session.get('messageCreateAccount'))

def createAccountRoute(): 
    logMessage('Begin createAccountRoute')
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
    logMessage("Begin authenticateCreateAccount")
    session['messageCreateAccount'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['password']), "")
    userAccount.accountType = databaseFunctions.getAccountType(userAccount)
    newUser = UserAccount(session.get('newAccountEmail'), session.get('newAccountPassword'), session.get('newAccountType'), session.get('newFirstName'), session.get('newLastName'))
    
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
    logMessage('Begin changePassword')
    if session.get('isLoggedIn'):
        return redirect('/')
    return render_template('login/changePassword.html', messageChangePassword = session.get('messageChangePassword')) 

def changePasswordRoute():
    logMessage('Begin changePasswordRoute')
    session['messageChangePassword'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['newPassword']), "")
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
    logMessage("Begin authenticateChangePassword")
    session['messageChangePassword'] = ""

    userAccount = UserAccount(str(request.form['email']), str(request.form['password']), "")
    userAccount.accountType = databaseFunctions.getAccountType(userAccount)
    passwordChangeAccount = UserAccount(session['changePasswordEmail'], session['changePasswordNewPassword'], session['changePasswordAccountType'])

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
    if databaseFunctions.getAccountEmail(userAccount) and (databaseFunctions.getAccountPassword(userAccount) == userAccount.password):
        return True
    else:
        return False

def checkPermissionsPasswordChange(userAccount, userChangeAccount):
    if userChangeAccount.accountType == 'employee' and databaseFunctions.getAccountType(userAccount) == 'administrator':
       return True
    elif userChangeAccount.accountType == 'employee' and databaseFunctions.getAccountType(userAccount) == 'master':
       return True
    elif userChangeAccount.accountType == 'administrator' and databaseFunctions.getAccountType(userAccount) == 'master':
        return True
    else:
        return False

def logMessage(log):
    with open("debugLog.txt", "a") as logFile:
        print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ': ' + str(log) + '\n')
        logFile.write('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ': ' + str(log) + '\n')
