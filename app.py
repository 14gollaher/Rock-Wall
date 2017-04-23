import os
from os import environ
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, make_response, jsonify
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
import pytz

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
    logMessage('index')
    return loginModule.index()

@app.route('/employeeMenu')
def employeeMenu():
    logMessage('employeeMenu')
    return loginModule.employeeMenu()

@app.route('/userAddMessage', methods=['POST'])
def addMessage():
    logMessage('userAddMessage')
    return loginModule.addMessage()

@app.route('/administratorMenu')
def administratorMenu():
    logMessage('administratorMenu')
    return loginModule.administratorMenu()

@app.route('/masterMenu')
def masterMenu():
    logMessage('masterMenu')
    return loginModule.masterMenu()

@app.route('/logout')
def logout():
    logMessage('logout')
    return loginModule.logout()

@app.route('/login')
def login():
    logMessage('login')
    return loginModule.login()

@app.route('/loginRoute', methods=['POST'])
def loginRoute():
    logMessage('loginRoute')
    return loginModule.loginRoute()
 
@app.route('/createAccount')
def createAccount():
    logMessage('createAccount')
    return loginModule.createAccount()

@app.route('/createAccountRoute', methods=['POST'])
def createAccountRoute():
    logMessage('createAccountRoute')
    return loginModule.createAccountRoute()
    
@app.route('/authenticateCreateAccount', methods=['POST'])
def authenticateCreateAccount():
    logMessage('authenticateCreateAccount')
    return loginModule.authenticateCreateAccount()

@app.route('/changePassword')
def changePassword():
    logMessage('changePassword')
    return loginModule.changePassword()

@app.route('/changePasswordRoute', methods=['POST'])
def changePasswordRoute():
    logMessage('changePasswordRoute')
    return loginModule.changePasswordRoute()

@app.route('/authenticateChangePassword', methods=['POST'])
def authenticateChangePassword():
    logMessage('authenticateChangePassword')
    return loginModule.authenticateChangePassword()

#########################################################################
###                                                                   ###
###                        Inventory                                  ###
###                                                                   ###
######################################################################### 

@app.route('/inventory')
def inventory():
    logMessage('inventory')
    return inventoryModule.inventory()

@app.route('/addInventoryRoute', methods=['POST'])
def addInventoryRoute():
    logMessage('addInventoryRoute')
    return inventoryModule.addInventoryRoute()

@app.route('/editInventoryRoute', methods=['POST'])
def editInventoryRoute():
    logMessage('editInventoryRoute')
    return inventoryModule.editInventoryRoute()

@app.route('/inventoryDelete', methods=['POST'])
def inventoryDelete():
    logMessage('inventoryDelete')
    return inventoryModule.inventoryDelete()

@app.route('/inventoryMessageClear', methods=['POST'])
def inventoryMessageClear():
    logMessage('inventoryMessageClear')
    return inventoryModule.inventoryMessageClear()

@app.route('/inventoryUpdate', methods=['POST'])
def inventoryUpdate():
    logMessage('inventoryUpdate')
    return inventoryModule.inventoryToggleCheckStatus()

@app.route('/inventoryEdit', methods=['POST'])
def inventoryEdit():
    logMessage('inventoryEdit')
    return inventoryModule.inventoryEdit()

#########################################################################
###                                                                   ###
###                         Calendar                                  ###
###                                                                   ###
######################################################################### 

@app.route('/calendar')
def calendar():
    logMessage('calendar')
    return calendarModule.calendar() 

@app.route('/calendarUpdate', methods=['POST'])
def calendarUpdate():
    logMessage('calendarUpdate')
    return calendarModule.calendarUpdate()

@app.route('/calendarDelete', methods=['POST'])
def calendarDelete():
    logMessage('calendarDelete')
    return calendarModule.calendarDelete()

@app.route('/calendarInsert', methods=['POST'])
def calendarInsert():
    logMessage('calendarInsert')
    return calendarModule.calendarInsert()


#########################################################################
###                                                                   ###
###                            Patron                                 ###
###                                                                   ###
######################################################################### 

@app.route('/patronSignUp')
def patronSignUp():
    logMessage('patronSignUp')
    return patronModule.patronSignUp()

@app.route('/patronSignUpRoute', methods=['POST'])
def patronSignUpRoute():
    logMessage('patronSignUpRoute')
    return patronModule.patronSignUpRoute()

@app.route('/patronCheckIn')
def patronCheckIn():
    logMessage('patronCheckIn')
    return patronModule.patronCheckIn()

@app.route('/patronCheckInRoute', methods=['POST'])
def patronCheckInRoute():
    logMessage('patronCheckInRoute')
    return patronModule.patronCheckInRoute()

@app.route('/patronCheckInRoute2', methods=['POST'])
def patronCheckInRoute2():
    logMessage('patronCheckInRoute2')
    return patronModule.patronCheckInRoute2()

@app.route('/patronConfirmation')
def patronConfirmation():
    logMessage('patronConfirmation')
    return patronModule.patronConfirmation()

@app.route('/signWaiver')
def signWaiver():
    logMessage('signWaiver')
    return patronModule.signWaiver()

@app.route('/patronSuspension')
def patronSuspension():
    logMessage('patronSuspension')
    return patronModule.patronSuspension()

@app.route('/signWaiverRoute', methods=['POST'])
def signWaiverRoute():
    logMessage('signWaiverRoute')
    return patronModule.signWaiverRoute()

@app.route('/createPatronAccountRoute', methods=['POST'])
def createPatronAccountRoute():
    logMessage('createPatronAccountRoute')
    return patronModule.createPatronAccountRoute()

@app.route('/storeImage', methods=['POST'])
def storeImage():
    logMessage('storeImage')
    return patronModule.storeImage()

#########################################################################
###                                                                   ###
###                          Reporting                                ###
###                                                                   ###
######################################################################### 

@app.route('/reporting')
def reporting():
    logMessage('reporting')
    return reportingModule.reporting()

@app.route('/reportingEmployee')
def reportingEmployee():
    logMessage('reportingEmployee')
    return reportingModule.reportingEmployee()

@app.route('/reportingAdmin')
def reportingAdmin():
    logMessage('reportingAdmin')
    return reportingModule.reportingAdmin()

@app.route('/reportingMaster')
def reportingMaster():
    logMessage('reportingMaster')
    return reportingModule.reportingMaster()

@app.route('/addIncidentRoute', methods=['POST'])
def addIncidentRoute():
    logMessage('addIncidentRoute')
    return reportingModule.addIncidentRoute()

@app.route('/toggleReportReviewStatus', methods=['POST'])
def toggleReportReviewStatus():
    logMessage('toggleReportReviewStatus')
    return reportingModule.toggleReportReviewStatus()

@app.route('/editPatronSuspensionRoute', methods=['POST'])
def editPatronSuspensionRoute():
    logMessage('editPatronSuspensionRoute')
    return reportingModule.editPatronSuspensionRoute()


#########################################################################
###                                                                   ###
###                        Patron View                                ###
###                                                                   ###
######################################################################### 

@app.route('/patrons')
def patron():
    logMessage('patrons')
    return patronViewModule.patrons()

@app.route('/patronViewEmployee')
def patronViewEmployee():
    logMessage('patronViewEmployee')
    return patronViewModule.patronViewEmployee()

@app.route('/patronViewAdmin')
def patronViewAdmin():
    logMessage('patronViewAdmin')
    return patronViewModule.patronViewAdmin()

@app.route('/patronViewMaster')
def patronViewMaster():
    logMessage('patronViewMaster')
    return patronViewModule.patronViewMaster()

@app.route('/editPatronRoute', methods=['POST'])
def editPatronRoute():
    logMessage('editPatronRoute')
    return patronViewModule.editPatronRoute()

@app.route('/editPatronCertificationRoute', methods=['POST'])
def editPatronCertificationRoute():
    logMessage('editPatronCertificationRoute')
    return patronViewModule.editPatronCertificationRoute()

@app.route('/patronDelete', methods=['POST'])
def patronDelete():
    logMessage('patronDelete')
    return patronViewModule.patronDelete()

#########################################################################
###                                                                   ###
###                          User View                                ###
###                                                                   ###
######################################################################### 

@app.route('/users')
def users():
    logMessage('users')
    return userViewModule.users()

@app.route('/userViewAdmin')
def userViewAdmin():
    logMessage('userViewAdmin')
    return userViewModule.userViewAdmin()

@app.route('/userViewMaster')
def userViewMaster():
    logMessage('userViewMaster')
    return userViewModule.userViewMaster()

@app.route('/editUserRoute', methods=['POST'])
def editUserRoute():
    logMessage('editUserRoute')
    return userViewModule.editUserRoute()

@app.route('/userDelete', methods=['POST'])
def userDelete():
    logMessage('userDelete')
    return userViewModule.userDelete()


#########################################################################
###                                                                   ###
###                             Others                                ###
###                                                                   ###
#########################################################################

def logMessage(log):
    currentTime = datetime.now(pytz.timezone('US/Central'))

    with open("debugLog.txt", "a") as logFile:
        print(str(request.environ['REMOTE_ADDR']) + '- {:%Y-%m-%d %H:%M:%S}'.format(datetime.now(pytz.timezone('US/Central'))) + ': ' + str(log) + '\n')
        logFile.write(str(request.environ['REMOTE_ADDR']) + '- {:%Y-%m-%d %H:%M:%S}'.format(datetime.now(pytz.timezone('US/Central'))) + ': ' + str(log) + '\n')

#if __name__ == '__main__':
#     HOST = environ.get('SERVER_HOST', 'localhost')
#     try:
#         PORT = int(environ.get('SERVER_PORT', '5555'))
#     except ValueError:
#         PORT = 5555
#     app.run(HOST, PORT,debug=True)

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=4000)