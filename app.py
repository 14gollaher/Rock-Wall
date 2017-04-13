import os
from os import environ
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, make_response
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import loginModule
import inventoryModule
import calendarModule
import patronModule
import reportingModule
import patronViewModule
import userViewModule

app = Flask(__name__)
app.secret_key = os.urandom(12)

#########################################################################
###                                                                   ###
###                         Login                                     ###
###                                                                   ###
######################################################################### 

@app.route('/')
@app.route('/index')
@app.route('/menu')
@app.route('/home')

def index():
    return loginModule.index()

@app.route('/employeeMenu')
def employeeMenu():
    return loginModule.employeeMenu()

@app.route('/userAddMessage', methods=['POST'])
def addMessage():
    return loginModule.addMessage()

@app.route('/administratorMenu')
def administratorMenu():
    return loginModule.administratorMenu()

@app.route('/masterMenu')
def masterMenu():
    return loginModule.masterMenu()

@app.route('/logout')
def logout():
    return loginModule.logout()

@app.route('/login')
def login():
    return loginModule.login()

@app.route('/loginRoute', methods=['POST'])
def loginRoute():
    return loginModule.loginRoute()
 
@app.route('/createAccount')
def createAccount():
    return loginModule.createAccount()

@app.route('/createAccountRoute', methods=['POST'])
def createAccountRoute(): 
    return loginModule.createAccountRoute()
    
@app.route('/authenticateCreateAccount', methods=['POST'])
def authenticateCreateAccount():
    return loginModule.authenticateCreateAccount()

@app.route('/changePassword')
def changePassword():
    return loginModule.changePassword()

@app.route('/changePasswordRoute', methods=['POST'])
def changePasswordRoute():
    return loginModule.changePasswordRoute()

@app.route('/authenticateChangePassword', methods=['POST'])
def authenticateChangePassword():
    return loginModule.authenticateChangePassword()

#########################################################################
###                                                                   ###
###                        Inventory                                  ###
###                                                                   ###
######################################################################### 

@app.route('/inventory')
def inventory():
    return inventoryModule.inventory()

@app.route('/addInventoryRoute', methods=['POST'])
def addInventoryRoute():
    return inventoryModule.addInventoryRoute()

@app.route('/editInventoryRoute', methods=['POST'])
def editInventoryRoute():
    return inventoryModule.editInventoryRoute()

@app.route('/inventoryDelete', methods=['POST'])
def inventoryDelete():
    return inventoryModule.inventoryDelete()

@app.route('/inventoryUpdate', methods=['POST'])
def inventoryUpdate():
    return inventoryModule.inventoryToggleCheckStatus()

@app.route('/inventoryEdit', methods=['POST'])
def inventoryEdit():
    return inventoryModule.inventoryEdit()

#########################################################################
###                                                                   ###
###                         Calendar                                  ###
###                                                                   ###
######################################################################### 

@app.route('/calendar')
def calendar():
    return calendarModule.calendar() 

@app.route('/calendarUpdate', methods=['POST'])
def calendarUpdate():
    return calendarModule.calendarUpdate()

@app.route('/calendarDelete', methods=['POST'])
def calendarDelete():
    return calendarModule.calendarDelete()

@app.route('/calendarInsert', methods=['POST'])
def calendarInsert():
    return calendarModule.calendarInsert()


#########################################################################
###                                                                   ###
###                            Patron                                 ###
###                                                                   ###
######################################################################### 

@app.route('/patronSignUp')
def patronSignUp():
    return patronModule.patronSignUp()

@app.route('/patronSignUpRoute', methods=['POST'])
def patronSignUpRoute():
    return patronModule.patronSignUpRoute()

@app.route('/patronCheckIn')
def patronCheckIn():
    return patronModule.patronCheckIn()

@app.route('/patronCheckInRoute', methods=['POST'])
def patronCheckInRoute():
    return patronModule.patronCheckInRoute()

@app.route('/patronCheckInRoute2', methods=['POST'])
def patronCheckInRoute2():
    return patronModule.patronCheckInRoute2()

@app.route('/patronConfirmation')
def patronConfirmation():
    return patronModule.patronConfirmation()

@app.route('/signWaiver')
def signWaiver():
    return patronModule.signWaiver()

@app.route('/patronSuspension')
def patronSuspension():
    return patronModule.patronSuspension()

@app.route('/signWaiverRoute', methods=['POST'])
def signWaiverRoute():
    return patronModule.signWaiverRoute()

@app.route('/createPatronAccountRoute', methods=['POST'])
def createPatronAccountRoute():
    return patronModule.createPatronAccountRoute()

@app.route('/storeImage', methods=['POST'])
def storeImage():
    return patronModule.storeImage()

#########################################################################
###                                                                   ###
###                          Reporting                                ###
###                                                                   ###
######################################################################### 

@app.route('/reporting')
def reporting():
    return reportingModule.reporting()

@app.route('/reportingEmployee')
def reportingEmployee():
    return reportingModule.reportingEmployee()

@app.route('/reportingAdmin')
def reportingAdmin():
    return reportingModule.reportingAdmin()

@app.route('/reportingMaster')
def reportingMaster():
    return reportingModule.reportingMaster()

@app.route('/addIncidentRoute', methods=['POST'])
def addIncidentRoute():
    return reportingModule.addIncidentRoute()

@app.route('/toggleReportReviewStatus', methods=['POST'])
def toggleReportReviewStatus():
    return reportingModule.toggleReportReviewStatus()

@app.route('/editPatronSuspensionRoute', methods=['POST'])
def editPatronSuspensionRoute():
    return reportingModule.editPatronSuspensionRoute()


#########################################################################
###                                                                   ###
###                        Patron View                                ###
###                                                                   ###
######################################################################### 

@app.route('/patrons')
def patron():
    return patronViewModule.patrons()

@app.route('/patronViewEmployee')
def patronViewEmployee():
    return patronViewModule.patronViewEmployee()

@app.route('/patronViewAdmin')
def patronViewAdmin():
    return patronViewModule.patronViewAdmin()

@app.route('/patronViewMaster')
def patronViewMaster():
    return patronViewModule.patronViewMaster()

@app.route('/editPatronRoute', methods=['POST'])
def editPatronRoute():
    return patronViewModule.editPatronRoute()


@app.route('/patronDelete', methods=['POST'])
def patronDelete():
    return patronViewModule.patronDelete()

#########################################################################
###                                                                   ###
###                          User View                                ###
###                                                                   ###
######################################################################### 

@app.route('/users')
def users():
    return userViewModule.users()

@app.route('/userViewAdmin')
def userViewAdmin():
    return userViewModule.userViewAdmin()

@app.route('/userViewMaster')
def userViewMaster():
    return userViewModule.userViewMaster()

if __name__ == '__main__':
     HOST = environ.get('SERVER_HOST', 'localhost')
     try:
         PORT = int(environ.get('SERVER_PORT', '5555'))
     except ValueError:
         PORT = 5555
     app.run(HOST, PORT,debug=True)

#if __name__ == "__main__":
#    app.run(debug=False,host='0.0.0.0', port=4000)