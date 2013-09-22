import time
import psutil
import rrdtool

RRD_CPU_FILE = "/Users/seo01/Documents/Dev/graph-menu/data/cpu.rrd"

#while(True):
#    cpu_usage = psutil.cpu_percent(interval=0)
#    cur_time = int(time.mktime(time.gmtime()))
#    rrdtool.update(RRD_CPU_FILE,"%s:%s" %(cur_time,cpu_usage))
#    print cpu_usage
#    time.sleep(1)

def update_rrd(reader):
	while(True):
		next_value = reader.next()
		cur_time = int(time.mktime(time.gmtime()))
		print "%s"%next_value
		rrdtool.update(RRD_CPU_FILE,"%s:%s" %(cur_time,next_value))

class CpuReader():
	def get_next_value(self):
		firstRead = True
		while(True):
			if not firstRead:
				time.sleep(1)
			else:
				firstRead = False
			yield psutil.cpu_percent(interval=0)

update_rrd(CpuReader().get_next_value())