import time
  
t = time.time()
  
from xml.etree.ElementTree import ElementTree
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
#, urllib2
import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
import datetime as dt
from datetime import date
  
class YQL(object):
    url = 'http://query.yahooapis.com/v1/public/yql'
    env = 'store://datatables.org/alltableswithkeys'
    format = 'xml'
  
    @classmethod
    def query(cls, string):
        q = urllib.parse.quote(string)
        url = cls.url + '&'.join(('?q=%s' % q, 'env=%s' % cls.env,
                                   'format=%s' % cls.format))
        #print url                           
        resp = urlopen(url)
        return ElementTree(file=resp).getroot().find('results')[:]
  
  
def getchain(sym,filename,today_date):
  
    xml_dates = YQL.query('select * from yahoo.finance.option_contracts where ' + 'symbol="%s"' %sym)[0]
    
    xml_contracts = YQL.query('select * from yahoo.finance.options where ' + 'symbol="%s"' %sym  )
    
    #today_date = dt.datetime.now().strftime("%d-%b-%Y")
    if today_date == '2000-01-01':
       today_date = str(dt.datetime.now().strftime("%Y_%m_%d") )
    dates = []
    
    fp = open(filename,'a')
    for attr in xml_dates:
         #print attr.tag, attr.text
         dates.append(attr.text)
  
    #optionChain = []
  
    puts = []; calls = []
    for expiration in dates:
            xml_contracts = YQL.query('select * from yahoo.finance.options where ' + 'symbol="%s" AND expiration="' %sym + expiration +'"'  )
  
  
            expiration=rrule.rrule(rrule.MONTHLY, byweekday=(relativedelta.FR(3)), dtstart=date(int(expiration.split("-")[0]), int(expiration.split("-")[1]), 1))[0]
            expiration = str(expiration).split(" ")[0]
  
            for option in xml_contracts[0]:
                # Get actual expiration date, usually Exp Date + 1 on Saturdays instead of Friday
                l_symbol = str(option.attrib['symbol'])
                l_end =  l_symbol.rfind('C') ; 

                if l_end < 6 :
                   l_end =  l_symbol.rfind('P') ; 
                
                #print l_end;
                new_exp = '20' +  l_symbol[l_end-6:l_end-4] + '-' +  l_symbol[l_end-4:l_end-2] + '-' +  l_symbol[l_end-2:l_end]
                
                if (option.attrib['type']=='P'):
                   #print ('Put: strike=' + option.findtext('strikePrice') + ', ask=' + option.findtext('ask') +  ', vol=' + option.findtext('vol') +', date='+ expiration + ', close=' + option.findtext('lastPrice')) 
                   
                   if (str(option.findtext('ask')) not in ('NaN','None')  and str(option.findtext('bid')) not in ('NaN','None')  and str(option.findtext('vol'))  not in ('NaN','None') ) :
                       puts.append([today_date,'P',sym,option.attrib['symbol'],expiration,option.findtext('strikePrice'),option.findtext('lastPrice'),option.findtext('change'),option.findtext('ask'),option.findtext('bid'),option.findtext('vol'),option.findtext('openInt')])
                       fp.write(today_date+','+'P'+','+str(sym)+','+l_symbol+','+new_exp+','+str(option.findtext('strikePrice'))+','+str(option.findtext('lastPrice'))+','+str(option.findtext('change'))+','+str(option.findtext('ask'))+','+str(option.findtext('bid'))+','+str(option.findtext('vol'))+','+str(option.findtext('openInt'))+'\n')
                   #fp.write(today_date+','+'p'+','+sym+','+option.attrib['symbol']+','+expiration+','+option.findtext('strikePrice')+','+option.findtext('lastPrice')+','+option.findtext('change')+','+option.findtext('ask')+','+option.findtext('buy')+','+option.findtext('vol')+','+option.findtext('openInt'))

                if (option.attrib['type']=='C'):
                   #print ('Call: strike=' + option.findtext('strikePrice') + ', ask=' + option.findtext('ask') +  ', vol=' + option.findtext('vol') +', date='+ expiration + ', close=' + option.findtext('lastPrice'))
                   if (str(option.findtext('ask')) not in ('NaN','None')  and str(option.findtext('bid')) not in ('NaN','None')  and str(option.findtext('vol'))  not in ('NaN','None') ) :
                       calls.append([today_date,'C',sym,option.attrib['symbol'],expiration,option.findtext('strikePrice'),option.findtext('lastPrice'),option.findtext('change'),option.findtext('ask'),option.findtext('bid'),option.findtext('vol'),option.findtext('openInt')])
                       fp.write(today_date+','+'C'+','+str(sym)+','+l_symbol+','+new_exp+','+str(option.findtext('strikePrice'))+','+str(option.findtext('lastPrice'))+','+str(option.findtext('change'))+','+str(option.findtext('ask'))+','+str(option.findtext('bid'))+','+str(option.findtext('vol'))+','+str(option.findtext('openInt'))+'\n')
                   #fp.write(today_date+','+'c'+','+sym+','+option.attrib['symbol']+','+expiration+','+option.findtext('strikePrice')+','+option.findtext('lastPrice')+','+option.findtext('change')+','+option.findtext('ask')+','+option.findtext('buy')+','+option.findtext('vol')+','+option.findtext('openInt'))
   
    fp.close()
    return puts, calls
  
  
if __name__ == '__main__':
  getchain('HRB','opt_data_20000101.txt','2000-01-01')

  
