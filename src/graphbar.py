import objc, re, os
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper
from rrd_to_sl import *

default_image = '/Users/seo01/Documents/Dev/graph-menu/data/graph.gif'
working_dir = '/Users/seo01/Documents/Dev/graph-menu/data'

start_time = NSDate.date()

granularities = {
  "Yearly":"1year",
  "Monthly":"1month",
  "Weekly":"1week",
  "Daily":"1day",
  "Hourly":"1hour",
  "15 minutes":"15min",
  "5 minutes":"5min"
}

class GraphConfig():

  conf = None

  def read_config(self):
    self.conf = [("Rain",["Weekly","Monthly","Yearly"]),("CPU",["5 minutes", "15 minutes","Hourly","Daily","Weekly"])]
    return self.conf

class Timer(NSObject):
  images = {}
  statusbar = None
  state = 'idle'
  granularity = None
  graph = None
  rrd_graph = RRD_Graph()#TODO pass in working_dir
  graphs = None

  def applicationDidFinishLaunching_(self, notification):
    #Read status
    gc = GraphConfig()
    self.graphs = gc.read_config()

    statusbar = NSStatusBar.systemStatusBar()
    # Create the statusbar item
    self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    status_image = NSImage.alloc().initByReferencingFile_(default_image)
    # Set initial image
    self.statusitem.setImage_(status_image)
    # Let it highlight upon clicking
    self.statusitem.setHighlightMode_(1)
    # Set a tooltip
    self.statusitem.setToolTip_('Show Graphs')

    # Build a very simple menu
    self.menu = NSMenu.alloc().init()

    for (title,granularities) in self.graphs:
      menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, 'graph:', '')
      if len(granularities) > 1:
        submenu = NSMenu.alloc().init()
        for granularity in granularities:
          submenuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(granularity, 'granularity:', '')
          submenu.addItem_(submenuitem)
        menuitem.setSubmenu_(submenu) 
      self.menu.addItem_(menuitem)

    # Default event
    menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
    self.menu.addItem_(menuitem)
    # Bind it to the status item
    self.statusitem.setMenu_(self.menu)

    # Get the timer going
    self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 5.0, self, 'tick:', None, True)
    NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
    self.timer.fire()

  def graph_(self,notification):

    self.graph = notification.title()
    if not self.granularity:
      self.granularity = dict(self.graphs)[self.graph][0]
    self.set_graph(self.graph,self.granularity)

  def set_graph(self,graph,granularity):
    if self.graph and self.granularity:
      graph_image = self.rrd_graph.generate_graph(self.graph,granularities[self.granularity])
      if graph_image:
        self.images ['graph']= NSImage.alloc().initByReferencingFile_(graph_image)
        self.statusitem.setImage_(self.images['graph'])


  def granularity_(self,notification):
    print "Do Something: %s" % notification.title()
    self.granularity = notification.title()
    self.graph_(notification.parentItem())


  def tick_(self, notification):
    #print self.state  
    self.set_graph(self.graph,self.granularity)

if __name__ == "__main__":
  app = NSApplication.sharedApplication()
  delegate = Timer.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()