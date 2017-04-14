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

class UserAccount:

    def __init__(self, email, password, accountType, firstName, lastName):
        self.email = email
        self.password = password
        self.accountType = accountType
        self.firstName = firstName
        self.lastName = lastName

def users():

    if not session.get('isLoggedIn'):
        return redirect('login')

    if session.get('currentUserAccountType') == 'Employee':
        return redirect('login')
    elif session.get('currentUserAccountType') == 'Administrator':
        return redirect('userViewAdmin')
    elif session.get('currentUserAccountType') == 'Master':
        return redirect('userViewMaster')

def userViewAdmin():

    if not session.get('isLoggedIn'):
        return redirect('login')

    userTable = {}
    userTable['email'] = databaseFunctions.getAllEmployeeUserEmails()
    userTable['firstName'] = databaseFunctions.getAllEmployeeUserFirstNames()
    userTable['lastName'] = databaseFunctions.getAllEmployeeUserLastNames()
    userTable['accountType'] = databaseFunctions.getAllEmployeeUserAccountTypes()

    userTable = [dict(email=e, firstName=f, lastName=l, accountType = a) for e, f, l, a in zip(userTable['email'], userTable['firstName'], userTable['lastName'], userTable['accountType'])]
    
    return render_template('userViewManager.html', userTable = userTable)

def userViewMaster():

    if not session.get('isLoggedIn'):
        return redirect('login')

    userTable = {}
    userTable['email'] = databaseFunctions.getAllEmployeeAdminUserEmails()
    userTable['firstName'] = databaseFunctions.getAllEmployeeAdminUserFirstNames()
    userTable['lastName'] = databaseFunctions.getAllEmployeeAdminUserLastNames()
    userTable['accountType'] = databaseFunctions.getAllEmployeeAdminUserAccountTypes()
    userTable = [dict(email=e, firstName=f, lastName=l, accountType = a) for e, f, l, a in zip(userTable['email'], userTable['firstName'], userTable['lastName'], userTable['accountType'])]
    
    return render_template('userViewManager.html', userTable = userTable)

def editUserRoute():

    if not session.get('isLoggedIn'):
        return redirect('login')

    newUserItem = UserAccount(str(request.form['updatedEmail']), "", str(request.form['updatedAccountType']), str(request.form['updatedFirstName']), str(request.form['updatedLastName']))
    databaseFunctions.editUser(newUserItem) 
    if session.get('currentUserAccountType') == 'administrator':
        return redirect('userViewAdmin')
    else:
        return redirect('userViewMaster')

def userDelete():
    if not session.get('isLoggedIn'):
        return redirect('login')

    newUserItem = UserAccount(str(request.form['email']), "", "", "", "")
    newUserItem.email = newUserItem.email.strip('"')
    databaseFunctions.deleteUser(newUserItem)

    if session.get('currentUserAccountType') == 'administrator':
        return redirect('userViewAdmin')
    else:
        return redirect('userViewMaster')