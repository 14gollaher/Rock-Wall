class CalendarItem:

    def __init__(self, id, title, startTime, description, icon, color):

        self.id = id
        self.title = title
        self.startTime = startTime
        self.description = description
        self.icon = icon
        self.color = color

class InventoryItem:

    def __init__(self, id, name, description, purchaseDate, retirementDate, checkOutStatus):
        self.id = id
        self.name = name
        self.description = description
        self.purchaseDate = purchaseDate
        self.retirementDate = retirementDate
        self.checkOutStatus = checkOutStatus

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

class Patron:

 def __init__(self, id, firstName, lastName, email, phoneNumber, gender, address, city, zipCode, waiverFile, state, isBelayCertified, belayStartDate, belayEndDate, isLeadClimbCertified, leadClimbStartDate, leadClimbEndDate, isSuspended, suspendedStartDate, suspendedEndDate, listServ):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.gender = gender
        self.address = address
        self.city = city
        self.zipCode = zipCode
        self.waiverFile = waiverFile
        self.state = state
        self.isBelayCertified = isBelayCertified
        self.belayStartDate = belayStartDate
        self.belayEndDate = belayEndDate
        self.isLeadClimbCertified = isLeadClimbCertified
        self.leadClimbStartDate = leadClimbStartDate
        self.leadClimbEndDate = leadClimbEndDate
        self.isSuspended = isSuspended
        self.suspendedStartDate = suspendedStartDate
        self.suspendedEndDate = suspendedEndDate
        self.listServ = listServ

class VisitHistoryLogItem:

    def __init__(self, id, patronId, patronFirstName, patronLastName, patronVisitDate, patronVisitTime):

        self.id = id    
        self.patronId = patronId
        self.patronFirstName = patronFirstName
        self.patronLastName = patronLastName
        self.patronVisitDate = patronVisitDate
        self.patronVisitTime = patronVisitTime