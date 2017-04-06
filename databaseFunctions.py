from sqlalchemy import text, create_engine, MetaData
#engine = create_engine('sqlite:///SDSU-Rock-Wall/RockWall.db', convert_unicode=True)
engine = create_engine('sqlite:///RockWall.db', convert_unicode=True)
metadata = MetaData(bind=engine)


#########################################################################
###                                                                   ###
###                     Incident Report Table ###
###                                                                   ###
#########################################################################
def insertNewIncidentReport(IncidentReport):
    if IncidentReport.id == "null":
        IncidentReport.id = int(getHighestIncidentReportId()) + 1
    sqlText = text("INSERT INTO IncidentReport VALUES (:id, :time, :date, :description, :author)")
    engine.execute(sqlText, {"id": IncidentReport.id, "time": IncidentReport.time, "date": IncidentReport.date, "description": IncidentReport.description, "author": IncidentReport.author})

def getHighestIncidentReportId():
    sqlText = text("SELECT * FROM IncidentReport WHERE Id = (SELECT MAX(Id) FROM IncidentReport)")
    result = engine.execute(sqlText).fetchone()
    row = result
    return row['Id']


#########################################################################
###                                                                   ###
###                         Messages Table ###
###                                                                   ###
#########################################################################
def getTop100CalendarDescriptions():
    with engine.connect() as connection:
        sqlText = text("SELECT Description FROM Calendar ORDER by Id DESC LIMIT 100")
        result = engine.execute(sqlText)
        descriptions = []
    
        for row in result:
            descriptions.append(row[0])    

        if not descriptions:
            return None
        else:	
            return descriptions

def getTop100MessageAuthors():
    with engine.connect() as connection:
        sqlText = text("SELECT Author FROM Message ORDER by Id DESC LIMIT 100")
        result = engine.execute(sqlText)
        authors = []

        for row in result:
            authors.append(row[0])    

        if not authors:
            return None
        else:	
            return authors

def getTop100MessageTimes():
    with engine.connect() as connection:
        sqlText = text("SELECT Time FROM Message ORDER by Id DESC LIMIT 100")
        result = engine.execute(sqlText)
        times = []

        for row in result:
            times.append(row[0])    

        if not times:
            return None
        else:	
            return times

def getTop100MessageContents():
    with engine.connect() as connection:
        sqlText = text("SELECT Content FROM Message ORDER by Id DESC LIMIT 100")
        result = engine.execute(sqlText)
        contents = []

        for row in result:
            contents.append(row[0])    

        if not contents:
            return None
        else:	
            return contents

def insertNewMessage(Message):
    if Message.id == "-1Nullx0":
        Message.id = int(getHighestMessageId()) + 1
    sqlText = text("INSERT INTO Message VALUES (:id, :author, :time, :content)")
    engine.execute(sqlText, {"id": Message.id, "author": Message.author, "time": Message.time, "content": Message.content})

def getHighestMessageId():
    sqlText = text("SELECT * FROM Message WHERE Id = (SELECT MAX(Id) FROM Message)")
    result = engine.execute(sqlText).fetchone()
    row = result
    return row['Id']

#########################################################################
###                                                                   ###
###                          Patron Table ###
###                                                                   ###
#########################################################################
def insertNewPatron(Patron):
    sqlText = text("INSERT INTO Patron VALUES (:id, :firstName, :lastName, :email, :phoneNumber, :gender, :address, :city, :zipCode, :waiverFile, :state)")
    engine.execute(sqlText, {"id": Patron.id, "firstName": Patron.firstName, "lastName": Patron.lastName, "email": Patron.email, "phoneNumber": Patron.phoneNumber, "gender": Patron.gender, "address": Patron.address, "city": Patron.city, "zipCode": Patron.zipCode, "waiverFile": Patron.waiverFile, "state": Patron.state})


def getPatronId(Patron):
	sqlText = text("SELECT Id FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": Patron.id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Id']

def getAllPatronIds():
    with engine.connect() as connection:
        sqlText = text("SELECT Id FROM Patron ORDER by Id")
        result = engine.execute(sqlText)
        ids = []
    
        for row in result:
            ids.append(row[0])    

        if not ids:
            return None
        else:	
            return ids

def getAllPatronFirstNames():
    with engine.connect() as connection:
        sqlText = text("SELECT FirstName FROM Patron ORDER by FirstName")
        result = engine.execute(sqlText)
        firstNames = []
    
        for row in result:
            firstNames.append(row[0])    

        if not firstNames:
            return None
        else:	
            return firstNames

def getAllPatronLastNames():
    with engine.connect() as connection:
        sqlText = text("SELECT LastName FROM Patron ORDER by LastName")
        result = engine.execute(sqlText)
        lastNames = []
    
        for row in result:
            lastNames.append(row[0])    

        if not lastNames:
            return None
        else:	
            return lastNames

def getAllPatronEmails():
    with engine.connect() as connection:
        sqlText = text("SELECT Email FROM Patron ORDER by Email")
        result = engine.execute(sqlText)
        emails = []
    
        for row in result:
            emails.append(row[0])    

        if not emails:
            return None
        else:	
            return emails

def getAllPatronPhoneNumbers():
    with engine.connect() as connection:
        sqlText = text("SELECT PhoneNumber FROM Patron ORDER by PhoneNumber")
        result = engine.execute(sqlText)
        phoneNumbers = []
    
        for row in result:
            phoneNumbers.append(row[0])    

        if not phoneNumbers:
            return None
        else:	
            return phoneNumbers

def getAllPatronGenders():
    with engine.connect() as connection:
        sqlText = text("SELECT Gender FROM Patron ORDER by Gender")
        result = engine.execute(sqlText)
        genders = []
    
        for row in result:
            genders.append(row[0])    

        if not genders:
            return None
        else:	
            return genders

def getAllPatronAddresses():
    with engine.connect() as connection:
        sqlText = text("SELECT Address FROM Patron ORDER by Address")
        result = engine.execute(sqlText)
        addresses = []
    
        for row in result:
            addresses.append(row[0])    

        if not addresses:
            return None
        else:	
            return addresses

def getAllPatronCities():
    with engine.connect() as connection:
        sqlText = text("SELECT City FROM Patron ORDER by City")
        result = engine.execute(sqlText)
        cities = []
    
        for row in result:
            cities.append(row[0])    

        if not cities:
            return None
        else:	
            return cities

def getAllPatronZipCodes():
    with engine.connect() as connection:
        sqlText = text("SELECT Zip FROM Patron ORDER by Zip")
        result = engine.execute(sqlText)
        zips = []
    
        for row in result:
            zips.append(row[0])    

        if not zips:
            return None
        else:	
            return zips

def getAllPatronStates():
    with engine.connect() as connection:
        sqlText = text("SELECT State FROM Patron ORDER by State")
        result = engine.execute(sqlText)
        states = []
    
        for row in result:
            states.append(row[0])    

        if not states:
            return None
        else:	
            return states

def editPatronAccount(PatronItem):
    sqlText = text("UPDATE Patron SET FirstName = :firstName, LastName = :lastName, Email = :email, PhoneNumber = :phoneNumber , Gender = :gender , Address = :address , City = :city , Zip = :zipCode, State =:state  WHERE Id = :id")
    engine.execute(sqlText, {"id": PatronItem.id, "firstName": PatronItem.firstName, "lastName": PatronItem.lastName, "email": PatronItem.email, "phoneNumber": PatronItem.phoneNumber, "gender": PatronItem.gender, "address": PatronItem.address, "city": PatronItem.city, "zipCode": PatronItem.zipCode, "state": PatronItem.state})

def getCurrentPatronFirstName(id):
	sqlText = text("SELECT FirstName FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['FirstName']

def getCurrentPatronLastName(id):
	sqlText = text("SELECT LastName FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['LastName']

def getCurrentPatronEmail(id):
	sqlText = text("SELECT Email FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Email']

def getCurrentPatronPhoneNumber(id):
	sqlText = text("SELECT PhoneNumber FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['PhoneNumber']

def getCurrentPatronAddress(id):
	sqlText = text("SELECT Address FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Address']

def getCurrentPatronState(id):
    sqlText = text("SELECT State FROM Patron WHERE Id = :id")
    result = engine.execute(sqlText, {"id": id}).fetchone()
    if not result:
        return result
    else:	
        row = result
        return row['State']

def getCurrentPatronCity(id):
	sqlText = text("SELECT City FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['City']

def getCurrentPatronZipCode(id):
	sqlText = text("SELECT Zip FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Zip']

def getCurrentPatronGender(id):
	sqlText = text("SELECT Gender FROM Patron WHERE Id = :id")
	result = engine.execute(sqlText, {"id": id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Gender']

#########################################################################
###                                                                   ###
###                          Calendar Table                           ###
###                                                                   ###
#########################################################################
def insertNewCalendarItem(CalendarItem):
    if CalendarItem.id == "-1Nullx0":
        CalendarItem.id = int(getHighestCalendarId()) + 1
    sqlText = text("INSERT INTO Calendar VALUES (:id, :title, :startTime, :description, :icon, :color)")
    engine.execute(sqlText, {"id": CalendarItem.id, "title": CalendarItem.title, "startTime": CalendarItem.startTime, "description": CalendarItem.description, "icon": CalendarItem.icon, "color": CalendarItem.color})
    

def getCalendarItemId(CalendarItem):
    sqlText = text("SELECT Id FROM Calendar WHERE Id = :id")
    result = engine.execute(sqlText, {"id": CalendarItem.id}).fetchone()
    if not result:
        return result
    else:	
        row = result
    return row['Id']

def getHighestCalendarId():
    sqlText = text("SELECT * FROM Calendar WHERE Id = (SELECT MAX(Id) FROM Calendar)")
    result = engine.execute(sqlText).fetchone()
    row = result
    return row['Id']

def changeCalendarItemStartTime(CalendarItem, newStartTime):
	sqlText = text("UPDATE Calendar SET StartTime = :newStartTime WHERE Id = :id")
	engine.execute(sqlText, {"id": CalendarItem.id, "newStartTime": newStartTime})

def deleteCalendarItem(CalendarItem):
	sqlText = text("DELETE FROM Calendar WHERE Id = :id")
	engine.execute(sqlText, {"id": CalendarItem.id})

def getAllCalendarIds():
    with engine.connect() as connection:
        sqlText = text("SELECT Id FROM Calendar ORDER by Id")
        result = engine.execute(sqlText)
        ids = []
    
        for row in result:
            ids.append(row[0])    

        if not ids:
            return None
        else:	
            return ids

def getAllCalendarTitles():
    with engine.connect() as connection:
        sqlText = text("SELECT Title FROM Calendar ORDER by Id")
        result = engine.execute(sqlText)
        titles = []
    
        for row in result:
            titles.append(row[0])    

        if not titles:
            return None
        else:	
            return titles

def getAllCalendarStartTimes():
    with engine.connect() as connection:
        sqlText = text("SELECT StartTime FROM Calendar ORDER by Id")
        result = engine.execute(sqlText)
        startTimes = []
    
        for row in result:
            startTimes.append(row[0])    

        if not startTimes:
            return None
        else:	
            return startTimes

def getAllCalendarDescriptions():
    with engine.connect() as connection:
        sqlText = text("SELECT Description FROM Calendar ORDER by Id")
        result = engine.execute(sqlText)
        descriptions = []
    
        for row in result:
            descriptions.append(row[0])    

        if not descriptions:
            return None
        else:	
            return descriptions

def getAllCalendarIcons():
    with engine.connect() as connection:
        sqlText = text("SELECT Icon FROM Calendar ORDER by Id")
        result = engine.execute(sqlText)
        icons = []
    
        for row in result:
            icons.append(row[0])    

        if not icons:
            return None
        else:	
            return icons

def getAllCalendarColors():
    with engine.connect() as connection:
        sqlText = text("SELECT Color FROM Calendar ORDER by Id")
        result = engine.execute(sqlText)
        colors = []
    
        for row in result:
            colors.append(row[0])    

        if not colors:
            return None
        else:	
            return colors

#########################################################################
###                                                                   ###
###                         Inventory Table ###
###                                                                   ###
#########################################################################
def getAllInventoryIds():
    with engine.connect() as connection:
        sqlText = text("SELECT Id FROM Inventory ORDER by Id")
        result = engine.execute(sqlText)
        ids = []
    
        for row in result:
            ids.append(row[0])    

        if not ids:
            return None
        else:	
            return ids

def getAllInventoryNames():
    with engine.connect() as connection:
        sqlText = text("SELECT Name FROM Inventory ORDER by Id")
        result = engine.execute(sqlText)
        names = []
    
        for row in result:
            names.append(row[0])    

        if not names:
            return None
        else:	
            return names

def getAllInventoryDescriptions():
    with engine.connect() as connection:
        sqlText = text("SELECT Description FROM Inventory ORDER by Id")
        result = engine.execute(sqlText)
        descriptions = []
    
        for row in result:
            descriptions.append(row[0])    

        if not descriptions:
            return None
        else:	
            return descriptions

def getAllInventoryRetirementDates():
    with engine.connect() as connection:
        sqlText = text("SELECT RetirementDate FROM Inventory ORDER by Id")
        result = engine.execute(sqlText)
        retirementDates = []
    
        for row in result:
            retirementDates.append(row[0])    

        if not retirementDates:
            return None
        else:	
            return retirementDates

def getAllInventoryCheckOutStatuses():
    with engine.connect() as connection:
        sqlText = text("SELECT IsCheckOut FROM Inventory ORDER by Id")
        result = engine.execute(sqlText)
        checkOutStatuses = []
    
        for row in result:
            checkOutStatuses.append(row[0])    

        if not checkOutStatuses:
            return None
        else:	
            return checkOutStatuses

def insertNewInventoryItem(InventoryItem):
	sqlText = text("INSERT INTO Inventory VALUES (:id, :name, :description, :retirementDate, :isCheckOut)")
	engine.execute(sqlText, {"id": InventoryItem.id, "name": InventoryItem.name, "description": InventoryItem.description, "retirementDate": InventoryItem.retirementDate, "isCheckOut": "False"})

def deleteInventoryItem(InventoryItem):
	sqlText = text("DELETE FROM Inventory WHERE Id = :id")
	engine.execute(sqlText, {"id": InventoryItem.id})

def editInventoryItem(InventoryItem):
    sqlText = text("UPDATE Inventory SET Name = :name, Description = :description, RetirementDate = :retirementDate WHERE Id = :id")
    engine.execute(sqlText, {"id": InventoryItem.id, "name": InventoryItem.name, "description": InventoryItem.description, "retirementDate": InventoryItem.retirementDate})

def setInventoryCheckStatus(InventoryItem):
    sqlText = text("UPDATE Inventory SET IsCheckOut = :isCheckOut WHERE Id = :id")
    engine.execute(sqlText, {"id": InventoryItem.id, "isCheckOut": str(InventoryItem.checkOutStatus)})

def getInventoryItemId(InventoryItem):
	sqlText = text("SELECT Id FROM Inventory WHERE Id = :id")
	result = engine.execute(sqlText, {"id": InventoryItem.id}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Id']

#########################################################################
###                                                                   ###
###                           User Table ###
###                                                                   ###
#########################################################################
def getAccountEmail(User):
	sqlText = text("SELECT Email FROM User WHERE Email = :email")
	result = engine.execute(sqlText, {"email": User.email}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Email']

def getAccountPassword(User):
	sqlText = text("SELECT Password FROM User WHERE Email = :email")
	result = engine.execute(sqlText, {"email": User.email}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['Password']

def getAccountType(User):
	sqlText = text("SELECT AccountType FROM User WHERE Email = :email")
	result = engine.execute(sqlText, {"email": User.email}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['AccountType']

def getAccountFirstName(User):
	sqlText = text("SELECT FirstName FROM User WHERE Email = :email")
	result = engine.execute(sqlText, {"email": User.email}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['FirstName']

def getAccountLastName(User):
	sqlText = text("SELECT LastName FROM User WHERE Email = :email")
	result = engine.execute(sqlText, {"email": User.email}).fetchone()
	if not result:
		return result
	else:	
		row = result
		return row['LastName']

def insertNewUser(User):
	sqlText = text("INSERT INTO User VALUES (:email, :password, :accountType, :firstName, :lastName)")
	engine.execute(sqlText, {"email": User.email, "password": User.password, "accountType": User.accountType, "firstName": User.firstName, "lastName": User.lastName})

def deleteUser(User):
	sqlText = text("DELETE FROM User WHERE Email = :email")
	engine.execute(sqlText, {"email": User.email})

def changePassword(User, newPassword):
	sqlText = text("UPDATE User SET Password = :newPassword WHERE Email = :email")
	engine.execute(sqlText, {"email": User.email, "newPassword": newPassword})

def changeAccountType(User, newAccountType):
	sqlText = text("UPDATE User SET AccountType = :newAccountType WHERE Email = :email")
	engine.execute(sqlText, {"email": User.email, "newAccountType": newAccountType})

