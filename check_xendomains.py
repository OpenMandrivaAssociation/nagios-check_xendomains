#!/usr/bin/python2.4
#
############
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with it; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
###########
#
# check_xendomains.py by Alvaro Lopez Garcia <alvaro@perseverantia.com>
# For more info please visit http://beta.perseverantia.com/devel/
#
# $Id: check_xendomains.py 136 2007-05-28 11:19:19Z alvaro $
#
# Usage: ./check_xendomains.py --help
#
# History:
# 2007-05-28: Fixed stupid bug for debug
#             Restructured output. Code cleanup.
#	2007-05-11: Added support for more verbosity
#	2007-05-10: First version
#
###########

def fetch(host, doc, port='8000'):
  import urllib2
  url = 'http://%s:%s/%s' % (host,port,doc)
  req = urllib2.Request(url)
  req.add_header("User-Agent", "$Id: check_xendomains.py 136 2007-05-28 11:19:19Z alvaro $")
  req.add_header("Host", "%s:%s" % (host,port))
  req.add_header("Pragma", "no-cache")
  req.add_header("Accept", "*/*")
  try:
    f = urllib2.urlopen(req)
  except urllib2.URLError:
    print "CRITICAL: Could not connect to Xend http daemon on '%s'" % host
    sys.exit(2)
  return f.read()

def get_nodeinfo(host, port='8000'):
  import HTMLParser
  class ParseNodeData(HTMLParser.HTMLParser):
    def __init__(self):
      HTMLParser.HTMLParser.__init__(self)
      self.control_nodeinfo = None
      self.nodeinfo = ""

    def handle_starttag(self,tag,attrs):
      if tag == "li":
        self.control_nodeinfo = True
      elif tag == "a" and self.control_nodeinfo:
        self.control_nodeinfo = False

    def handle_data(self,data):
      if self.control_nodeinfo:
        self.nodeinfo = "%s\n%s" % (self.nodeinfo, data)

    def handle_endtag(self,tag):
      if tag == "li":
        self.control_nodeinfo=False
    def getinfo(self):
      return self.nodeinfo

  content = fetch(host, "/xend/node/", "8000")
  parser = ParseNodeData()
  parser.feed(content)
  return parser.getinfo()

def get_domains(host, port='8000'):
  import HTMLParser
  class ParseXenData(HTMLParser.HTMLParser):
    def __init__(self):
      HTMLParser.HTMLParser.__init__(self)
      self.control_vminfo = None
      self.control_vmname = None
      self.vmname = ""
      self.vminfo = ""
      self.vms = {}

    def handle_starttag(self,tag,attrs):
      if tag == "li":
        self.control_vminfo = True
        self.vminfo = ""
      elif self.control_vminfo and tag == "a":
        self.control_vmname = True
        self.vmname = ""

    def handle_data(self,data):
      if self.control_vmname:
        self.vmname = data
      elif self.control_vminfo:
        self.vminfo = data[2:-1]

    def handle_endtag(self,tag):
      if tag == "li":
        self.control_vminfo=False
        self.vms[self.vmname]=self.vminfo
      elif self.control_vminfo and tag == "a":
        self.control_vmname = False
    def get_domainsinfo(self):
      return self.vms

  content = fetch(host,'/xend/domain/','8000')
  parser = ParseXenData()
  domains= []
  parser.feed(content)
  prop_dict = {}
  for i,j in parser.get_domainsinfo().iteritems():
    properties = j.split(", ")
    prop_dict["dom"] = i.split(" ")[1]
    for l in properties:
      prop_dict[l.split(" = ")[0]] = l.split(" = ")[1]
    yield prop_dict

def help():
  print """
Usage:
  -V version (--version)
  -h help (--help)
  -t timeout (--timeout)
  -w warning threshold (--warning)
  -c critical threshold (--critical)
  -H hostname (--hostname)
  -v verbose (--verbose)
"""

def version():
  print "$Id: check_xendomains.py 136 2007-05-28 11:19:19Z alvaro $"

def main():
  import getopt
  try:
    opts, args = getopt.getopt(sys.argv[1:], "VhH:p:v")
  except getopt.GetoptError:
    help()
    return(3)

  if len(opts)<1:
    help()
    return(3)

  hostname = None
  port = 8000
  global verbose
  verbose = 0
  for o, a in opts:
    if o == "-v":
      verbose += 1
      continue
    if o == "-V":
      version()
      return(3)
    if o == "-h":
      help()
      return(3)
    if o == "-H":
      hostname = a
      continue
    if o == "-p":
      port = a
      continue

  if hostname!=None:
    if verbose > 1: print "Checking hostname '%s'." % hostname
    aux = ""
    for dom in get_domains(hostname,port):
      if verbose == 0:
        aux =  " -- ".join(["D:%s M:%s" % (dom["dom"], dom["memory"]), aux])
      elif verbose == 1:
        pass
        aux =  " -- ".join(["D:%s I:%s M:%s" % (dom["dom"], dom["id"], dom["memory"]), aux])
      elif verbose >= 2:
        aux = "\n".join([
            "",
            "-".center(50,"-"),
            "-%s-" % dom["dom"].center(48) ,
            "-".center(50,"-"),
            "",
            "\tId:%s" % dom["id"],
            "\tMemory:%s" % dom["memory"],
            "\tssidref:%s" %  dom["ssidref"],
            "\n----Node Information----",
            get_nodeinfo(hostname,port),
            aux])
    if verbose >= 3:
      aux = "\n".join([aux,
        "",
        "-".center(50,"-"),
        "-%s-" % "XEND LOG".center(48),
        "-".center(50,"-"),
        "",
        fetch(hostname,"/xend/node/dmesg/",port)])
    print aux
    return 0

if __name__ == "__main__":
  import sys
  sys.exit(main())
