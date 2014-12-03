#!/usr/bin/python
#
# Memcache monitoring plugin for server density 
# http://www.serverdensity.com/
#
# Depends on python-memcached
# http://www.tummy.com/Community/software/python-memcached/
# easy_install python-memcached
#
 
import re, telnetlib, sys
import statsd
import time
import json
import socket
import os

class MemcachedStats:

    _client = None
    _key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(ur'STAT items:(.*):number')
    _stat_regex = re.compile(ur"STAT (.*) (.*)\r")

    def __init__(self, host='localhost', port='11211'):
        self._host = host
        self._port = port

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write("%s\n" % cmd)
        return self.client.read_until('END')

    def key_details(self, sort=True, limit=100):
        ' Return a list of tuples containing keys and details '
        cmd = 'stats cachedump %s %s'
        keys = [key for id in self.slab_ids()
            for key in self._key_regex.findall(self.command(cmd % (id, limit)))]
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True, limit=100):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort, limit=limit)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))

def getHostInfo():
    hostInfo = {}
    assetPath='/home/dspeak/yyms/hostinfo'
    fh = open(assetPath,'r')
    try:
        rawHostInfo = fh.read( )
    finally:
        fh.close( )
    hostInfo = json.loads(rawHostInfo)
    return hostInfo

def alarm(msg):
    fid=12026
    sid=77502
    os.system('/home/dspeak/yyms/yymp/yymp_report_script/yymp_report_alarm.py ' + str(fid) + ' ' + str(sid) + ' 0 ' + msg)

def main(argv=None):
    hostInfo = getHostInfo()
    mem_host = '0.0.0.0'
    mem_port=11211
    key_prefix='sysop.yuntu.memcache.idc_id>%s.server_id>%s.mem_port>%s' % ( hostInfo['idc_id'] , hostInfo['server_id'] , mem_port ) 
 
    statsClient = statsd.StatsClient('apm.sysop.duowan.com', 8125, prefix=key_prefix)

    m = MemcachedStats(mem_host , mem_port)
    try:
        metrics = m.stats()
    except socket.error:
        alarm('memcache host %s , port: %s cannot connect' % ( mem_host , mem_port ))
        return

    for key,value in metrics.items():
        if key == 'version':			
            continue
        statsClient.gauge(key,value)  

if __name__ == '__main__':
    main()
