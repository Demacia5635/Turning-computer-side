import threading
from networktables import NetworkTables
import csv

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.56.35.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

print("Connected!")

table = NetworkTables.getTable('SmartDashboard')


run_count = 0

while True:
    if run_count != (run_count := table.getNumber("Run Count", 0)):
        with open('runs.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([run_count,
            table.getNumber("Left Power", 0),
            table.getNumber("Right Power", 0),
            table.getNumber("L Current", 0),
            table.getNumber("R Current", 0),
            table.getNumber("L Voltage", 0),
            table.getNumber("R Voltage", 0),
            table.getNumber("L Speed", 0),
            table.getNumber("R Speed", 0)])

# Itay was here