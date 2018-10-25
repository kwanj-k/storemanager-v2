"""
A utilities file
A place for reuseable code
"""
#standard library import
from datetime import datetime


d1 = datetime.now()
d = d1.strftime('%H:%M%P %A %d %B %Y')
def myconverter(o):
    return o.__str__()
dt = myconverter(d)
