
from lunar_python import Lunar,EightChar
from lunar_python.util import HolidayUtil
from datetime import datetime 
lunar = Lunar.fromDate(datetime.now())
d = lunar.getEightChar()
print(d)