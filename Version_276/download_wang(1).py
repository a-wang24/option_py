
from getChain import getChain
from datetime import datetime
 
def download(filenamesour = 'source_data.txt', filenamedest = 'opt_data'):
    datestr = str(datetime.now().strftime("%Y-%m-%d"))
    filenamedest = filenamedest + '_' + str(datetime.now().strftime("%Y%m%d")) + '.txt'
    #fp = open(filenamedest,'w+')
    #fp.close()
    data = {}

    fin = open(filenamesour) #filename should be a string type: e.g filename = 'file.txt'

    for element in fin:
            #print (i)
            t = datetime.now()  
            sym = element.strip()
            print sym.ljust(6) , str(datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
            #fail = 1
            #  Run a loop if the data download fails (which occasionally happens)
            #while fail == 1:    
            #        try:
            
            #opts = []
            puts, calls = getChain(sym,filenamedest,datestr)
            #opts.append(puts)
            #opts.append(calls)
            #fp.write(" ".join([sym,str(t),str(puts),str(calls),'\n']))
            #for i in puts:
            #    fp.write(i)
 

    #fp.close()
                     
if __name__ == '__main__':
 
    download(filenamesour = 'source_data.txt', filenamedest = 'opt_data')
