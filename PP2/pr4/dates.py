# import datetime

# x = datetime.datetime.now()
# print(x)
# print(x.year)
# print(x.strftime("%A")) #%A- format
# y = datetime.datetime(2020, 5, 17)
# print(y)    
# %a	Weekday, short version
# %A	Weekday, full version
# %b	Month name, short version  
# %B	Month name, full version

import datetime

today=datetime.date.today()
result=today-datetime.timedelta(days=5)
print(result)

yesterday=today-datetime.timedelta(days=1)
tommorow=today+datetime.timedelta(days=1)
print( yesterday)
print(tommorow)

now=datetime.datetime.now()
new=now.replace(microsecond=0)
print(new)

fd=datetime.datetime(2020, 5, 17)
sd=datetime.datetime(2021, 6, 18)
diff=sd-fd
print(diff)