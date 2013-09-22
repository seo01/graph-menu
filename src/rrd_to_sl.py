from my_sparkplot import *
import rrdtool
import time
import os
RRD_CPU_FILE = "/Users/seo01/Documents/Dev/graph-menu/data/cpu.rrd"

seconds = {
  "1year":'2903040',
  "1month":'241920',
  "1week":'60480',
  "1day":'8640',
  "1hour":'360',
  "15min":'90',
  "5min":'30'
}

class RRD_Graph():

	working_dir = '/Users/seo01/Documents/Dev/graph-menu/data'
	
	graphs = {}
	cur_graph = None

	def fetch_data(self,graph,granularity):
		print "Fetching data %s %s" % (graph,granularity)
		data = rrdtool.fetch(RRD_CPU_FILE,'AVERAGE', '-r', '30', '-s', 'end-%s'%granularity)
		end = data[0][1]
		points = [p[0] for p in data[2]]
		#strip nulls
		while len(points) and not points[0]:
			points = points[1:]
		while len(points) and not points[-1]:
			points = points[:-1]
		points = [p if p else 0 for p in points] #should interpolate not nil
		points = points[-25:]
		print data
		print end
		print points
		return points,end

	def build_graph(self,file_name,data):
		print "Building graph"
		try:
			os.remove(file_name)
		except OSError:
			pass
		sparkplot = Sparkplot(plot_first=False, verbose=1, label_max=True)
		sparkplot.data = data
		sparkplot.output_file = file_name
		sparkplot.plot_sparkline()

	def generate_graph(self, graph_name, granularity):
		#return None is graph has not changed otherwise return new graph object
		#Read data from an RRD file
		#Create a spark line
		print "Generate Graph"
		key = "%s_%s" % (graph_name,granularity)
		file_name = '/Users/seo01/Documents/Dev/graph-menu/data/%s.png' % key
		points,end = self.fetch_data(graph_name,granularity)
		if self.graphs.get(key) != end:
			self.build_graph(file_name,points)
			self.graphs[key] = end
		return file_name

if __name__ == "__main__":
	rrd_graph = RRD_Graph()
	data,end = rrd_graph.fetch_data()
	data = [float(p) for p in data]
	print data
	rrd_graph.build_graph('/Users/seo01/Documents/Dev/graph-menu/data/cpu_now.png',data)
	print rrd_graph.generate_graph('CPU','Secondly')