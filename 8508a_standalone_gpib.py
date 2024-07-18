import pyvisa,time,csv
from datetime import datetime

rm = pyvisa.ResourceManager()
my_instrument=rm.open_resource("TCPIP::192.168.0.88::GPIB0,9")
my_instrument.timeout = 20000
my_instrument.write('*RST')
my_instrument.write('*CLS')
time.sleep(3)
print(my_instrument.query('*IDN?'))
my_instrument.write("DCV 10,FILT_OFF,RESL8,FAST_ON,TWO_WR")
my_instrument.write("ZERO?")

timestr = time.strftime("%Y%m%d-%H%M%S_")
with open('csv/'+timestr+'F_8508A_short_10V_FAST_ON.csv', mode='w') as csv_file:
    fieldnames = ['time', '8508a_volt']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    clock=datetime.now()
    while True:
        val = float(my_instrument.query("*TRG;GET;RDG?"))
        writer.writerow({'time':time.time(), '8508a_volt': val})
        print(val)
        print( "Effective reading output rate: "+str(1/(datetime.now()-clock).total_seconds()))
        clock=datetime.now()