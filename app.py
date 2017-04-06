import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, make_response
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import loginModule
import inventoryModule
import calendarModule
import messageModule
import patronModule
import reportingModule
import patronViewModule


app = Flask(__name__)

engine = create_engine('sqlite:///RockWall.db', echo=True)

#########################################################################
###                                                                   ###
###                         Login                                     ###
###                                                                   ###
######################################################################### 

@app.route('/')
def index():
    return loginModule.index()

@app.route('/employeeMenu')
def employeeMenu():
    return loginModule.employeeMenu()

@app.route('/employeeAddMessage', methods=['GET', 'POST'])
def addMessage():
    return messageModule.addMessage()

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
    return loginModule.authenticateChangePassword

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

@app.route('/inventoryDelete', methods=['GET', 'POST'])
def inventoryDelete():
    return inventoryModule.inventoryDelete()

@app.route('/inventoryUpdate', methods=['GET', 'POST'])
def inventoryUpdate():
    return inventoryModule.inventoryToggleCheckStatus()

@app.route('/inventoryEdit', methods=['GET', 'POST'])
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

@app.route('/calendarUpdate', methods=['GET', 'POST'])
def calendarUpdate():
    return calendarModule.calendarUpdate()

@app.route('/calendarDelete', methods=['GET', 'POST'])
def calendarDelete():
    return calendarModule.calendarDelete()

@app.route('/calendarInsert', methods=['GET', 'POST'])
def calendarInsert():
    return calendarModule.calendarInsert()

#########################################################################
###                                                                   ###
###                           Message                                 ###
###                                                                   ###
######################################################################### 

#@app.route('/message')
#def message():
#    return messageModule.message()

#@app.route('/addMessage', methods=['GET', 'POST'])
#def addMessage():
#    return messageModule.addMessage()

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

@app.route('/signWaiverRoute', methods=['POST'])
def signWaiverRoute():
    return patronModule.signWaiverRoute()

@app.route('/createPatronAccountRoute', methods=['GET', 'POST'])
def createPatronAccountRoute():
    return patronModule.createPatronAccountRoute()

@app.route('/storeImage', methods=['GET', 'POST'])
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

@app.route('/addIncidentRoute', methods=['POST'])
def addIncidentRoute():
    return reportingModule.addIncidentRoute()

#########################################################################
###                                                                   ###
###                        Patron View                                ###
###                                                                   ###
######################################################################### 
@app.route('/patronViewEmployee')
def patronViewEmployee():
    return patronViewModule.patronViewEmployee()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False,host='0.0.0.0', port=4000)