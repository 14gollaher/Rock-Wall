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


def users():

    if not session.get('isLoggedIn'):
        return redirect('login')

    if session.get('currentUserAccountType') == 'employee':
        return redirect('login')
    elif session.get('currentUserAccountType') == 'administrator':
        return redirect('userViewAdmin')
    elif session.get('currentUserAccountType') == 'master':
        return redirect('userViewMaster')

def userViewAdmin():

    if not session.get('isLoggedIn'):
        return redirect('login')

    userTable = {}
    userTable['email'] = databaseFunctions.getAllUserEmails()
    userTable['firstName'] = databaseFunctions.getAllUserFirstNames()
    userTable['lastName'] = databaseFunctions.getAllUserLastNames()
    userTable['accountType'] = databaseFunctions.getAllUserAccountTypes()
    userTable = [dict(email=e, firstName=f, lastName=l, accountType = a) for e, f, l, a in zip(userTable['email'], userTable['firstName'], userTable['lastName'], userTable['accountType'])]
    
    return render_template('userViewManager.html', userTable = userTable)

def userViewMaster():

    if not session.get('isLoggedIn'):
        return redirect('login')

    userTable = {}
    userTable['email'] = databaseFunctions.getAllUserEmails()
    userTable['firstName'] = databaseFunctions.getAllUserFirstNames()
    userTable['lastName'] = databaseFunctions.getAllUserLastNames()
    userTable['accountType'] = databaseFunctions.getAllUserAccountTypes()
    userTable = [dict(email=e, firstName=f, lastName=l, accountType = a) for e, f, l, a in zip(userTable['email'], userTable['firstName'], userTable['lastName'], userTable['accountType'])]
    
    return render_template('userViewManager.html', userTable = userTable)