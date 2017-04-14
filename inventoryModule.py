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

    def __init__(self, id, name, description, purchaseDate, retirementDate, checkOutStatus):
        self.id = id
        self.name = name
        self.description = description
        self.purchaseDate = purchaseDate
        self.retirementDate = retirementDate
        self.checkOutStatus = checkOutStatus

def inventory():

    if not session.get('isLoggedIn'):
        return redirect('login');

    inventoryTable = {}
    inventoryTable['id'] = databaseFunctions.getAllInventoryIds()
    inventoryTable['name'] = databaseFunctions.getAllInventoryNames()
    inventoryTable['description'] = databaseFunctions.getAllInventoryDescriptions()
    inventoryTable['purchaseDate'] = databaseFunctions.getAllInventoryPurchaseDates()
    inventoryTable['retirementDate'] = databaseFunctions.getAllInventoryRetirementDates()
    inventoryTable['checkOutStatus'] = databaseFunctions.getAllInventoryCheckOutStatuses()
    inventoryTable = [dict(id=i, name=n, description=d, purchaseDate=p, retirementDate=r, checkOutStatus=s) for i, n, d, p, r, s in zip(inventoryTable['id'], inventoryTable['name'], inventoryTable['description'], inventoryTable['purchaseDate'], inventoryTable['retirementDate'], inventoryTable['checkOutStatus'])]
    
    return render_template('inventory.html', inventoryTable = inventoryTable)

def addInventoryRoute():

    if not session.get('isLoggedIn'):
        return redirect('login')

    newInventoryItem = InventoryItem(str(request.form['newId']), str(request.form['newName']), str(request.form['newDescription']), str(request.form['newPurchaseDate']), str(request.form['newRetirementDate']), False)
    if not databaseFunctions.getInventoryItemId(newInventoryItem):
        databaseFunctions.insertNewInventoryItem(newInventoryItem)
    else: 
        session['addInventoryMessage'] = 'Item Id already exists!'

    return redirect('inventory')

def editInventoryRoute():

    if not session.get('isLoggedIn'):
        return redirect('login')

    if str(request.form['updatedCheckOutStatus']) == 'Yes':
        newInventoryItem = InventoryItem(str(request.form['updatedId']), str(request.form['updatedName']), str(request.form['updatedDescription']), str(request.form['updatedPurchaseDate']), str(request.form['updatedRetirementDate']), True)
    else:
        newInventoryItem = InventoryItem(str(request.form['updatedId']), str(request.form['updatedName']), str(request.form['updatedDescription']), str(request.form['updatedPurchaseDate']), str(request.form['updatedRetirementDate']), False)

    databaseFunctions.editInventoryItem(newInventoryItem)
    return redirect('inventory')

def inventoryToggleCheckStatus():

    if not session.get('isLoggedIn'):
        return redirect('login')

    if str(request.form['isCheckOut']) == 'Yes':
        newInventoryItem = InventoryItem(str(request.form['id']), "", "", "", "", False)
    else:
        newInventoryItem = InventoryItem(str(request.form['id']), "", "", "", "", True)

    databaseFunctions.setInventoryCheckStatus(newInventoryItem)
    return redirect('inventory')

def inventoryDelete():

    if not session.get('isLoggedIn'):
        return redirect('login')

    newInventoryItem = InventoryItem(str(request.form['id']), "", "", "", "", False)
    newInventoryItem.id = newInventoryItem.id.strip('"')
    databaseFunctions.deleteInventoryItem(newInventoryItem)

    return redirect('inventory')

