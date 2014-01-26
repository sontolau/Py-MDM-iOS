__author__ = 'sonto'

import web, os, json, uuid
from web.wsgiserver import CherryPyWSGIServer
from MDMCommand import *
from MDMConfig  import *
from subprocess import *
import SocketServer
from binascii import *
import threading,thread
from MDMDB import *

MDM_SERV_CONFIG="./mdm.cfg"

g_command = MDMCommand()
g_config  = MDMConfig(MDM_SERV_CONFIG)

# Setting the followings to configure Database
urls = (
    '/', 'homePage',
    '/getCA', 'getCA',
    '/server',  'server',
    '/checkIn', "checkIn",
    '/enrollment', "enroll",
    '/checkOut', 'checkOut',
    '/getMobileConfig', 'getMobileConfig',
)

def getUDIDWithIdentity(identity=''):
    return ''


def initMDM():
    global g_config
    #change working directory.
    os.chdir(g_config.base_dir)

    #set certificate and private key for Https connection.
    if not ( os.path.exists(g_config.https_certificate)
             and os.path.exists(g_config.https_private_key)):
        print "The certificate for https connection not found"
        return False

    print "Https:%s -- %s"%(g_config.https_certificate, g_config.https_private_key)
    CherryPyWSGIServer.ssl_certificate=g_config.https_certificate
    CherryPyWSGIServer.ssl_private_key=g_config.https_private_key

    cmd_queue=MDMDB("./mdm.db")
    cmd_queue.open()
    cmd_queue.cleanTable('mdm_cmd_queue')
    cmd_queue.close()
    return True
def authUserAndPass(user,password):
    #TODO: Add code here to authenticate user.
    return True


def responseWith(errcode=0, identity='', command=''):
    resplist = dict (
        Command = command,
        Identity= identity,
        Errcode = errcode,
    )

    return writePlistToString(resplist)

def saveIdentityConfig(identity='', config=None):
    global g_config
    id_path = '%s/%s/%s.data'%(g_config.identity_dir, identity, identity)
    writePlist(config, id_path)


class CoreRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global g_config
        global g_command

        g_cmd_queue = MDMDB("./mdm.db")
        g_cmd_queue.open("./mdm.db")
        data = self.request.recv(g_config.max_packet_size)
        plist = readPlistFromString(data)
        udid = plist.get('UDID')
        command = plist.get('Command')
        args    = plist.get("Arguments")
        #print "Command request arrived"

        devinfo = g_cmd_queue.getDeviceInfo(UDID=udid)
        if not devinfo:
            return
        push_magic=devinfo["PushMagic"]

        print  push_magic
        g_command.wakeUpDevice(topic=str(devinfo["Topic"]),
                               token=devinfo["Token"],
                               magic=str(devinfo['PushMagic']),
                               cert="./mdm-APNS.pem")
        try:
            g_cmd_queue.addNewCommandToWaitQueue (UDID=udid,command=command, args=args)
            g_cmd_queue.setCommandStatus(UDID=udid,status=0)
        except:
            print ("Connected to server failed.")
            pass
        g_cmd_queue.close()


def createInternalServer():
    global g_internal_server
    server = SocketServer.ThreadingTCPServer(server_address=g_config.internal_server,RequestHandlerClass=CoreRequestHandler)
    g_internal_server = threading.Thread (target=server.serve_forever())
    g_internal_server.daemon = True
    g_internal_server.start()

#The portal of MDM.
class homePage:
    def GET(self):
        home_page = './Pages/home_page.html'
        if os.path.exists(home_page):
            return open(home_page, "rb")
        else:
            raise web.notfound

#The CA of Aotain Inc
class getCA:
    def GET(self):
        if os.path.exists(g_config.ca):
            web.header('Content-Type', 'application/x-x509-ca-cert')
            return open(g_config.ca, "rb").read()
        else:
            raise web.notfound

class getMobileConfig:
    def GET(self):
        if not os.path.exists(g_config.mobile_config):
            return web.notfound
        else:
            web.header('Content-Type', 'application/x-apple-aspen-config')
            return open(g_config.mobile_config,'r').read()

class enroll:
    def POST(self):
        ca_config='./Pages/reqCAAndConfig.html'
        username=web.input().username
        password=web.input().password

        if (authUserAndPass(username,password)):
            if os.path.exists(ca_config):
                return open(ca_config,"r").read()
            else:
                return web.notfound
        else:
            return web.unauthorized

class checkOut:
    def PUT(self):
        return web.ok

class checkIn:
    def PUT(self):
        g_cmd_queue = MDMDB("./mdm.db")
        identity = 'sonto'
        request = readPlistFromString(web.data())
        msgType = request.get('MessageType')
        status  = request.get('Status')

        #print "MessageType = %s"%msgType
        if msgType == "Authenticate":
            gTopic = request.get('Topic')
            UDID   = request.get('UDID')
            return web.ok
        elif msgType == "TokenUpdate":
            UDID   = request.get('UDID')
            push_magic=request['PushMagic']
            topic  = request['Topic']
            token  = request['Token'].data
            unlock_token = request['UnlockToken'].data

            g_cmd_queue.open("./mdm.db")
            g_cmd_queue.addNewDevice(UDID=UDID,
                                     topic=topic,
                                     token=binascii.hexlify(token),
                                     untoken=unlock_token,
                                     magic=push_magic)
            print g_cmd_queue.getDeviceInfo(UDID=UDID)
            g_cmd_queue.close()

            return web.ok
def getCommandPlist(command='', args=''):
    global g_command
    arg_arry={}
    if args:
        for arg in args.split(","):
            key,value = arg.split(":")
            arg_arry[key] = value

    if command=="DeviceLock":
        return g_command.deviceLock(pin=arg_arry["PIN"],
                                    msg=arg_arry["Message"],
                                    phone=arg_arry["PhoneNumber"])

class server:
    def PUT(self):
        ctx=readPlistFromString(web.data())
        status = ctx.get('Status')
        UDID   = ctx.get('UDID')
        g_cmd_queue = MDMDB("./mdm.db")
        g_cmd_queue.open()
        cmdinfo = g_cmd_queue.getCommandInfo(UDID=UDID)
        if not cmdinfo:
            g_cmd_queue.close()
            return web.ok()

        cmd_status = int(cmdinfo["Status"])
        print cmd_status
        if cmd_status == 0:
            plist=getCommandPlist(cmdinfo["Command"],args=cmdinfo["Arguments"])
            g_cmd_queue.setCommandStatus(UDID=UDID, status=1)
            g_cmd_queue.close()
            return plist
        elif cmd_status == 1:
            print ctx
            #TODO:Add code here to check device status.
            g_cmd_queue.removeCommand(UDID=UDID)
            g_cmd_queue.close()
            return web.ok()
        else:
            return web.unauthorized

if __name__ == "__main__":
    if not initMDM():
        sys.exit(1)
    thread.start_new_thread (createInternalServer, ())
    app = web.application(urls, globals())
    app.run()
