import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import itertools
from itertools import *
import re

class InventoryItem:

    def __init__(self, id, name, description, retirementDate, checkOutStatus):
        self.id = id
        self.name = name
        self.description = description
        self.retirementDate = retirementDate
        self.checkOutStatus = checkOutStatus

def inventory():
    if not session.get('isLoggedIn'):
        return redirect('login');

    inventoryTable = {}
    inventoryTable['id'] = databaseFunctions.getAllInventoryIds()
    inventoryTable['name'] = databaseFunctions.getAllInventoryNames()
    inventoryTable['description'] = databaseFunctions.getAllInventoryDescriptions()
    inventoryTable['retirementDate'] = databaseFunctions.getAllInventoryRetirementDates()
    inventoryTable['checkOutStatus'] = databaseFunctions.getAllInventoryCheckOutStatuses()
    inventoryTable = [dict(id=i, name=n, description=d, retirementDate=r, checkOutStatus=s) for i, n, d, r, s in zip(inventoryTable['id'], inventoryTable['name'], inventoryTable['description'], inventoryTable['retirementDate'], inventoryTable['checkOutStatus'])]
    
    return render_template('inventory.html', inventoryTable = inventoryTable)

def addInventoryRoute():
    newInventoryItem = InventoryItem(str(request.form['newId']), str(request.form['newName']), str(request.form['newDescription']), str(request.form['newRetirementDate']), False)
    if not databaseFunctions.getInventoryItemId(newInventoryItem):
        databaseFunctions.insertNewInventoryItem(newInventoryItem)
    else: 
        session['addInventoryMessage'] = 'Item Id already exists!'

    return redirect('inventory')

def editInventoryRoute():
    if request.method == 'POST':
        print (str(request.form['updatedId']))
        print (str(request.form['updatedName']))
        print (str(request.form['updatedDescription']))
        print (str(request.form['updatedRetirementDate']))
        newInventoryItem = InventoryItem(str(request.form['updatedId']), str(request.form['updatedName']), str(request.form['updatedDescription']), str(request.form['updatedRetirementDate']), False)
        databaseFunctions.editInventoryItem(newInventoryItem)
    return redirect('inventory')

def inventoryToggleCheckStatus():
    if request.method == 'POST':
        if str(request.form['isCheckOut']) == 'Yes':
            newInventoryItem = InventoryItem(str(request.form['id']), "", "", "", False)
        else:
            newInventoryItem = InventoryItem(str(request.form['id']), "", "", "", True)

        databaseFunctions.setInventoryCheckStatus(newInventoryItem)
    return redirect('inventory')

def inventoryDelete():
    if request.method == 'POST':
        newInventoryItem = InventoryItem(str(request.form['id']), "", "", "", False)
        newInventoryItem.id = newInventoryItem.id.strip('"')
        databaseFunctions.deleteInventoryItem(newInventoryItem)
    return redirect('inventory')

