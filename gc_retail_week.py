from datetime import datetime, date, timedelta
import math

MonthWeekDic = {'January':1,'February':5,'March':10,'April':14,'May':18,'June':23,'July':27,'August':31,'September':36,'October':40,'November':44,'December':49}

class GCWeek(object):
    '''
    Returns the a calendar representing the Gear Coop implementation
    of the 4-5-4 retail calendar.
    *Running Sunday through Saturday
    '''
    def __init__(self, d=date.today()):
        self.date = d
        self.gc_week = get_gc_week(d)
        self.weeks_in_year = get_weeks_in_year(d)
        self.week = get_gc_week_only(d)
        self.year_week = gc_week_string(get_gc_week(d))
        self.following_saturday = get_following_saturday(d)
        self.previous_sunday = get_previous_sunday(d)       

    def lw(self):
        '''
        Return the last week as an int %Y%m
        '''
        d = self.date - timedelta(weeks=1)
        return get_gc_week(d)

    def lylw(self):
        '''
        Return the last week of last year as an int %Y%m
        '''
        d = self.date - timedelta(weeks=53)
        return get_gc_week(d)

    def l4w(self):
        '''
        Return the last 4 weeks as a tuple of ints %Y%m
        '''
        d1 = self.date - timedelta(weeks=4)
        d2 = self.date - timedelta(weeks=1)
        return get_weeks_between_dates_inclusive(d1, d2)

    def n4w(self):
        '''
        Return the next 4 weeks as a tuple of ints %Y%m
        '''
        d = self.date + timedelta(weeks=3)
        return get_weeks_between_dates_inclusive(self.date, d)

    def ytd(self):
        '''
        Return each week year to date as a tuple of ints %Y%m
        '''
        d1 = get_fiscal_year_start_date(self.date)
        # d2 = self.date - timedelta(weeks=1)
        d2 = self.date
        return get_weeks_between_dates_inclusive(d1, d2)

    def lyytd(self):
        '''
        Return each week of last year to date as a tuple of ints %Y%m
        '''
        # d1 = get_fiscal_year_start_date(self.date - timedelta(weeks=52))
        # d2 = self.date - timedelta(weeks=52)
        ty_wks = self.weeks_in_year
        # ly_wks = get_weeks_in_year(self.date - timedelta(weeks=self.weeks_in_year))
        d1 = get_fiscal_year_start_date(self.date - timedelta(weeks=ty_wks + 1))
        d2 = self.date - timedelta(weeks=ty_wks)
        # if ty_wks == ly_wks:
        #     d1 = get_fiscal_year_start_date(self.date - timedelta(weeks=ty_wks + 1))
        #     d2 = self.date - timedelta(weeks=ty_wks)
        # else:
        #     d1 = get_fiscal_year_start_date(self.date - timedelta(weeks=ty_wks + 1))
        #     d2 = self.date - timedelta(weeks=ty_wks)
        return get_weeks_between_dates_inclusive(d1, d2)
    def lytd(self):
        '''
        Return the same day last year as a date %Y%m%d
        '''
        
        lytd = self.date - timedelta(weeks=self.weeks_in_year)
        if self.week != get_gc_week_only(lytd):
            lytd -= timedelta(weeks=1)
        tdiso = self.date.isoweekday()
        lyiso = lytd.isoweekday()
        if lyiso != tdiso:
            sat = get_following_saturday(lytd)
            if tdiso < 6:
                return (sat - timedelta(days=tdiso))
            return (sat + timedelta(days=1))
        else:
            return lytd
    def retail_month_name(self):
        cw = int(gc_week_string(self.gc_week).split('-')[1])
        # print(cw)
        keys = list(MonthWeekDic.keys())
        vals = MonthWeekDic.values()
        c = 0
        if cw >= 49:
            return keys[len(keys)-1]
        for v in vals:
            if cw == v:
                return keys[c]
            if cw > v:
                c += 1   
                continue
            return keys[c-1]
    def retail_month(self):
        cw = int(gc_week_string(self.gc_week).split('-')[1])
        print(cw)
        vals = MonthWeekDic.values()
        prev = 1
        if cw >= 49:
            return 49
        for v in vals:
            if cw == v:
                return cw
            if cw > v:
                prev = v
                continue
            return prev
    def mtd(self):
        '''
        returns a list of ints for the current GC Week month to date
        '''
        year = get_fiscal_year(self.date)
        rm = self.retail_month()
        cw = int(gc_week_string(self.gc_week).split('-')[1])
        l = []
        if cw == rm:
            return list(str(year)+str(cw))
        else:
            w = cw - rm
            for i in range(w + 1):
                wk = str(cw-i)
                if len(wk) == 1:
                    wk = '0'+wk
                l.append((str(year)+wk))
        l.sort()
        return l
    def daysinyear(self):
        start = get_fiscal_year_start_date(self.date)
        end = get_fiscal_year_start_date(date(year=get_fiscal_year(start)+1,month=2,day=1)) - timedelta(days=1)
        # first = date(year=self.date.year,month=1,day=1)
        # if start == first:
        return abs(end - start).days + 1
        # d = abs((end - start)).days
        
        # return d
    def three_month_rolling(self,poptw=False):
        '''
        Return a list of the last 3 retail months as ints
        poptw is a boolean for removing this weeks data from the list
        '''
        rmstart = self.retail_month()
        l3m = list(get_weeks_between_dates_inclusive(self.date-timedelta(weeks=12),self.date))
        print(l3m)
        startcheck = int(gc_week_string(l3m[-1]).split('-')[1])
        print(startcheck)
        if startcheck - rmstart > 0:
            delta = startcheck - rmstart + 1 
            l3m = list(get_weeks_between_dates_inclusive(self.date-timedelta(weeks=12 + delta),self.date))
        print('length of list {}'.format(len(l3m)))
        if poptw:
            l3m.pop()
            print('length of list after pop {}'.format(len(l3m)))
        return l3m
    def three_month_rolling_tostring(self,poptw=False):
        '''
        Return a list of the last 3 retail months as strings
        poptw is a boolean for removing this weeks data from the list
        '''
        if poptw:
            l = self.three_month_rolling(poptw=True)
        else:
            l = self.three_month_rolling(poptw=False)
        s = []
        for v in l:
            s.append(gc_week_string(v))
        return s
    
    def thirteen_month_rolling(self,poptw=False):
        '''
        Return a list of the last 13 retail months as ints
        poptw is a boolean for removing this weeks data from the list
        '''
        rmstart = self.retail_month()
        l13m = list(get_weeks_between_dates_inclusive(self.date-timedelta(weeks=53),self.date))
        startcheck = int(gc_week_string(l13m[0]).split('-')[1])
        if startcheck - rmstart > 0:
            delta = startcheck - rmstart
            l13m = list(get_weeks_between_dates_inclusive(self.date-timedelta(weeks=53 + delta),self.date))
        print('length of list {}'.format(len(l13m)))
        if poptw:
            l13m.pop()
            print('length of list after pop {}'.format(len(l13m)))
        return l13m
    def thirteen_month_rolling_tostring(self,poptw=False):
        '''
        Return a list of the last 13 retail months as strings
        poptw is a boolean for removing this weeks data from the list
        '''
        if poptw:
            l = self.thirteen_month_rolling(poptw=True)
        else:
            l = self.thirteen_month_rolling()
        s = []
        for v in l:
            s.append(gc_week_string(v))
        return s
    def month_year(self):
        y = str(get_fiscal_year(self.date))
        m = self.retail_month_name()
        return m + '-' + y
def get_following_saturday(date_obj):
    '''
    Returns the Saturday immediately following the date passed in.
    If the date passed in is a Saturday it should return itself.
    '''
    # print('function get_following_saturday()')
    # In Python isoweekday Monday is 1 and Sunday is 7
    weekday = date_obj.isoweekday()
    # print('weekday {}'.format(weekday))
    # if weekday > 6:
    #     distance_from_sat = 7 - abs(6 - weekday)
    # else:
    #     distance_from_sat = abs(6 - weekday)
    if weekday == 7:
        distance_from_sat = 6
    else:
        distance_from_sat = abs(6 - weekday)
    # print('distance from saturday {}'.format(distance_from_sat))
    return date_obj + timedelta(days=distance_from_sat)

def get_previous_sunday(date_obj):
    '''
    Returns the Sunday prior to the date passed in.
    If the date passed in is a Sunday it should return itself.
    '''
    # print('function get_previous_sunday()')
    # In Python isoweekday Monday is 1 and Sunday is 7
    weekday = date_obj.isoweekday()
    # if weekday < 7:
    #     distance_from_sun = 7 - abs(7 - weekday)
    # else:
    #     distance_from_sun = abs(7 - weekday)
    if weekday < 7:
        distance_from_sun = weekday
    else:
        distance_from_sun = 0
    # print('distance from sunday {}'.format(distance_from_sun))
    return date_obj - timedelta(days=distance_from_sun)

def get_fiscal_year_start_date(date_obj):
    '''
    Returns the start date of the fiscal year of the date passed in.
    ** GC fiscal calendar follows a 4-5-4 weeks pattern where every 6 years the year has 53 weeks instead of 52    
    ** GC Weeks start on Sunday and end on Saturday
    '''
    # print('function get_fiscal_year_start_date({})'.format(date_obj))
    # Find the next Saturday that follows the given date
    following_saturday = get_following_saturday(date_obj)
    # Determine weeks in year
    week_53 = False
    if get_weeks_in_year(date_obj) == 53:
        week_53 = True
    # Determine GC fiscal year
    
    # if (date_obj.month == 1) & (following_saturday.month != 1):
    #     fiscal_year = date_obj.year - 1
    if week_53 & (date_obj.month == 12) & (following_saturday.month == 1):
        fiscal_year = date_obj.year
    elif (date_obj.month == 12) & (following_saturday.month == 1):
        fiscal_year = date_obj.year + 1
    else:
        fiscal_year = date_obj.year
    # print('fiscal year {}'.format(fiscal_year))
    # Find the first Saturday in January of the fiscal year we just found
    jan_1 = date(fiscal_year, 1, 1)
    # print('jan_1 {}'.format(jan_1))
    first_jan_sat = get_following_saturday(jan_1)
    # print('first_jan_sat {}'.format(first_jan_sat))
    # Get the first day of the GC Week that ends on the first Saturday we just found
    fiscal_year_start_date = first_jan_sat - timedelta(days=6)#days=6
    # print('fiscal_year_start_date {}'.format(fiscal_year_start_date))
    return fiscal_year_start_date

def get_fiscal_year(date_obj):
    '''
    Returns the fiscal year of the date passed in.
    ** GC fiscal calendar follows a 4-5-4 weeks pattern where every 6 years the year has 53 weeks instead of 52    
    ** GC Weeks start on Sunday and end on Saturday
    '''
    # print('function get_fiscal_year_start_date({})'.format(date_obj))
    # Find the next Saturday that follows the given date
    following_saturday = get_following_saturday(date_obj)
    # Determine weeks in year
    week_53 = False
    if get_weeks_in_year(date_obj) == 53:
        week_53 = True
    # Determine GC fiscal year
    
    # if (date_obj.month == 1) & (following_saturday.month != 1): #& (date_obj.day < 10):
    #     fiscal_year = date_obj.year - 1
    if week_53 & (date_obj.month == 12) & (following_saturday.month == 1):
        fiscal_year = date_obj.year
    elif (date_obj.month == 12) & (following_saturday.month == 1):
        fiscal_year = date_obj.year + 1
    else:
        fiscal_year = date_obj.year
    # print('fiscal year {}'.format(fiscal_year))
    return fiscal_year
def get_gc_week(d):
    '''
    Returns the GC Week for the date passed into the method.
    If no date is passed in, the methods defaults to today.
    '''
    # print('function get_gc_week(d) d={}'.format(d))
    fiscal_year_start_date = get_fiscal_year_start_date(d)
    # print('fiscal_year_start_date {}'.format(fiscal_year_start_date))
    # Get the day of GC fiscal year
    # day_of_gc_year = (d - fiscal_year_start_date).days + 1
    day_of_gc_year = abs(d - fiscal_year_start_date).days + 1
    if day_of_gc_year > 366:
        day_of_gc_year = abs(day_of_gc_year - 364)
    # print('day_of_gc_year {}'.format(day_of_gc_year))
    # Get week number by dividing day number by 7 and rounding up
    gc_week_nbr = math.ceil(day_of_gc_year/7)
    weekcheck = False
    if gc_week_nbr == 53:
        if gc_week_nbr != get_weeks_in_year(d):
            gc_week_nbr = 1
            weekcheck = True
    # print('gc_week_nbr {}'.format(gc_week_nbr))
    
    if fiscal_year_start_date.day != 1:
        fiscal_year = fiscal_year_start_date.year + 1
    else:
        fiscal_year = fiscal_year_start_date.year
    if weekcheck == True:
        fiscal_year += 1
    # print('fiscal_year {}'.format(fiscal_year))

    # Return GC Week as an int
    # print('returning {}'.format((fiscal_year * 100) + gc_week_nbr))
    return (fiscal_year * 100) + gc_week_nbr
def get_gc_week_only(d):
    '''
    Returns the GC Week excluding the year for the date passed into the method.
    If no date is passed in, the methods defaults to today.
    '''
    # print('function get_gc_week(d) d={}'.format(d))
    fiscal_year_start_date = get_fiscal_year_start_date(d)
    # print('fiscal_year_start_date {}'.format(fiscal_year_start_date))
    # Get the day of GC fiscal year
    # day_of_gc_year = (d - fiscal_year_start_date).days + 1
    day_of_gc_year = abs(d - fiscal_year_start_date).days + 1
    # print('day_of_gc_year {}'.format(day_of_gc_year))
    # Get week number by dividing day number by 7 and rounding up
    gc_week_nbr = math.ceil(day_of_gc_year/7)
    if gc_week_nbr == 53:
        if gc_week_nbr != get_weeks_in_year(d):
            gc_week_nbr = 1
    return gc_week_nbr

def get_weeks_between_dates_inclusive(start_date, end_date):
    '''
    Returns tuple of the GC Weeks between the two days passed to the method,
    including the weeks that the dates are in.
    '''
    # print('function get_weeks_between_dates_inclusive(start_date, end_date) start={} end={}'.format(start_date,end_date))
    weeks = []
    weeks_start = get_previous_sunday(start_date)
    # print('weeks_start {}'.format(weeks_start))
    weeks_end = get_following_saturday(end_date)
    # print('weeks_end {}'.format(weeks_end))
    nbr_of_weeks = math.ceil(((weeks_end - weeks_start).days + 1) / 7)
    # print('nbr_of_weeks {}'.format(nbr_of_weeks))
    for i in range(nbr_of_weeks):
      d = start_date + timedelta(weeks=i)
      weeks.append(get_gc_week(d))
    return tuple(weeks)#sorted(tuple(weeks))
def gc_week_todate(gcw):
    '''
    Deprecated. Not yet functional
    '''
    if len(str(gcw)) == 6:
        gc_str = gc_week_string(gcw)
        print(gc_str)
        mon = datetime.strptime(gc_str,'%Y-%U')# + '-1'
        print('monday: {}'.format(mon))
        return [get_previous_sunday(mon),get_following_saturday(mon)]
    # weeksinyear = (lambda x: 52 if x % 6 == 0 else 53)
    # winy = weeksinyear(y)
    # rm = get_retail_month()
    # if rm != winy:
    #     winy - rm
    # y = int(gc_str.split('-')[0])
    # w = int(gc_str.split('-')[1])
    # d = y+"-W"+w
def get_retail_month_start(cw):
        vals = MonthWeekDic.values()        
        for v in vals:
            if cw == v:
                return cw
            if cw < v:
                continue
            return v
def get_weeks_in_year(d):
    if (d.year % 6) != 0:
        return 52
    else:
        return 53
def gc_week_string(gcw):
    if gcw is None:
        return ''
    # elif len(str(gcw)) != 6:
    #     return ''
    split = list(str(gcw))
    yw = ''
    for s in split:
        if len(yw) != 3:
            yw = yw+s
        else:
            yw = yw+s+'-' 
    return yw

