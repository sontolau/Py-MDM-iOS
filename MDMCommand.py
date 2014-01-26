__author__ = 'sonto'
import uuid, json, os
from plistlib import *
from plist import *
from APNSWrapper import *
import base64

class MDMCommand:
    cmdInstallProfile = 0
    cmdRemoveProfile = 1
    cmdProvisioningProfileList = 2
    cmdInstallProvisioningProfile = 3
    cmdRemoveProvisioningProfile = 4
    cmdCertificateList = 5
    cmdInstalledApplicationList = 6
    cmdDeviceInformation = 7
    cmdSecurityInfo = 8
    cmdDeviceLock = 9
    cmdClearPasscode = 10
    cmdEraseDevice = 11
    cmdRequestMirroring = 12
    cmdRestrictions = 13
    cmdInstallApplication = 14
    cmdApplyRedemptionCode = 15
    cmdManagedApplicationList = 16
    cmdRemoveApplication = 17
    cmdInviteToProgram = 18
    cmdSettings = 19
    cmdManagedApplicationConfiguration = 20
    cmdManagedApplicationAttributes = 21
    cmdManagedApplicationFeedback = 22
    cmdProfileList = 23
    cmdInvalidCommand = 24
    commandList = []

    def __init__(self):
        self.commandList.insert(self.cmdInstallProfile, {
            'Command': 'InstallProfile',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdRemoveProfile, {
            'Command': 'RemoveProfile',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdProvisioningProfileList, {
            'Command': 'ProvisioningProfileList',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdInstallProvisioningProfile, {
            'Command': 'InstallProvisionngProfile',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdRemoveProvisioningProfile, {
            'Command': 'RemoveProvisioningProfile',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdCertificateList, {
            'Command': 'CertificateList',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdInstalledApplicationList, {
            'Command': 'InstalledApplicationList',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdDeviceInformation, {
            'Command': 'DeviceInformation',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdSecurityInfo, {
            'Command': 'SecurityInfo',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdDeviceLock, {
            'Command': 'DeviceLock',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdClearPasscode, {
            'Command': 'ClearPasscode',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdEraseDevice, {
            'Command': 'EraseDevice',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdRequestMirroring, {
            'Command': 'RequestMirroring',
            'CommandUUID':str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdRestrictions, {
            'Command': 'Restrictions',
            'CommandUUID':str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdInstallApplication, {
            'Command': 'InstallApplication',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdApplyRedemptionCode, {
            'Command': 'ApplyRedemptionCode',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdManagedApplicationList, {
            'Command': 'ManagedApplicationList',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdRemoveApplication, {
            'Command': 'RemoveApplication',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdInviteToProgram, {
            'Command': 'InviteToProgram',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdSettings, {
            'Command': 'Settings',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdManagedApplicationConfiguration, {
            'Command': 'ManagedApplicationConfiguration',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdManagedApplicationAttributes, {
            'Command': 'ManagedApplicationAttributes',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdManagedApplicationFeedback, {
            'Command': 'ManagedApplicationFeedback',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdProfileList, {
            'Command': 'ProfileList',
            'CommandUUID': str (uuid.uuid4()),
        })

        self.commandList.insert(self.cmdInvalidCommand, {
            'Command': None,
            'CommandUUID': None,
        })

    def __getSamplePlist(self,command=24):
        prolist = dict (
            CommandUUID = self.getCommandUUID(command),
            Command     = dict (
                RequestType = self.getCommandString(command),
            )
        )
        return writePlistToString(prolist)

    def getCommandString(self, command=24):
        cmddict = self.commandList[command]
        return cmddict['Command']

    def getCommandUUID(self, command=24):
        cmddict = self.commandList[command]
        return cmddict['CommandUUID']

    def installProfile(self, data=''):
        prolist = dict (
            CommandUUID= self.getCommandUUID(self.cmdInstallProfile),
            Command    = dict(
                RequestType= self.getCommandString(self.cmdInstallProfile),
                Payload    = Data (data),
            ),
        )

        plist = writePlistToString(prolist)
        print plist
        return plist

    def removeProfile(self, identifier=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdRemoveProfile),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdRemoveProfile),
                Identifier  = identifier,
            )
        )
        return writePlistToString(prolist)

    def provisioningProfileList(self):
        return self.__getSamplePlist(self.cmdProvisioningProfileList)

    def installProvisioningProfile(self,profile=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdInstallProvisioningProfile),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdInstallProvisioningProfile),
                ProvisionProfile = Data(profile),
            )
        )

        return writePlistToString(prolist)

    def removeProvisioningProfile(self,uuid=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdRemoveProvisioningProfile),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdRemoveProvisioningProfile),
                UUID        = uuid,
            )
        )

        return writePlistToString(prolist)

    def certificateList(self):
        return self.__getSamplePlist(self.cmdCertificateList)

    def installedApplicationList(self, identifiers=[], maonly=False):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdInstalledApplicationList),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdInstalledApplicationList),
                Identifiers = identifiers,
                ManagedAppsOnly = maonly,
            )
        )

        return writePlistToString(prolist)

    def deviceInformation(self,queries=[]):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdDeviceInformation),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdDeviceInformation),
                Queries = identifiers,
            )
        )

        return writePlistToString(prolist)

    def securityInfo(self):
        return self.__getSamplePlist(self.cmdSecurityInfo)

    def deviceLock(self,pin='', msg='', phone=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdDeviceLock),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdDeviceLock),
                PIN         = pin,
                Message     = msg,
                PhoneNumber = phone,
            )
        )

        return writePlistToString(prolist)

    def clearPasscode(self,utoken=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdClearPasscode),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdClearPasscode),
                UnlockToken = utoken,
            )
        )

        return writePlistToString(prolist)

    def eraseDevice(self,pin=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdEraseDevice),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdEraseDevice),
                PIN         = pin,
            )
        )

        return writePlistToString(prolist)

    def requestMirroring(self,destname='', destdevid='',scantime='', passwd=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdRequestMirroring),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdRequestMirroring),
                DestinationName = destname,
                DestinationDeviceID = destdevid,
                ScanTime = scantime,
                Password = passwd,
            )
        )

        return writePlistToString(prolist)

    def restrictions(self,pres=False):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdRestrictions),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdRestrictions),
                ProfileRestrictions = pres,
            )
        )

        return writePlistToString(prolist)


    def installApplication(self,itunresID=1, identifier='', options=dict(), url='', mflags=0, config=dict(), attris=dict()):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdInstallApplication),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdInstallApplication),
                iTunesStoreID = itunresID,
                Identifier    = identifier,
                Options       = options,
                ManifestURL   = url,
                ManagementFlags = mflags,
                Configuration = config,
                Attributes    = attris,
            )
        )

        return writePlistToString(prolist)

    def applyRedemptionCode(self,identifier='', code=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdApplyRedemptionCode),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdApplyRedemptionCode),
                Identifier  = identifier,
                RedemptionCode = code,
            )
        )

        return writePlistToString(prolist)
    def managedApplicationList(self,identifiers = []):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdManagedApplicationList),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdManagedApplicationList),
                Identifiers = identifiers,
            )
        )

        return writePlistToString(prolist)

    def removeApplication(self, identifier=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdRemoveApplication),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdRemoveApplication),
                Identifier  = identifier,
            )
        )

        return writePlistToString(prolist)

    def inviteToProgram(self, programID='', url=''):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdInviteToProgram),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdInviteToProgram),
                ProgramID   = programID,
                InvitationURL = url,
            )
        )

        return writePlistToString(prolist)

    def settings(self, settings=[]):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdSettings),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdSettings),
                Settings    = settings,
            )
        )

        return writePlistToString(prolist)

    def managedApplicationConfiguraion(self, identifiers=[]):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdManagedApplicationConfiguration),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdManagedApplicationConfiguration),
                Identifiers = identifiers,
            )
        )

        return writePlistToString(prolist)

    def managedApplicationAttributes(self, identifiers=[]):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdManagedApplicationAttributes),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdManagedApplicationAttributes),
                Identifiers = identifiers,
            )
        )

        return writePlistToString(prolist)

    def managedApplicationFeedback(self,identifiers=[], delfeedback=False):
        prolist = dict (
            CommandUUID = self.getCommandUUID(self.cmdManagedApplicationFeedback),
            Command     = dict (
                RequestType = self.getCommandString(self.cmdManagedApplicationFeedback),
                Identifiers = identifiers,
                DeleteFeedback = delfeedback,
            )
        )
        return writePlistToString(prolist)

    def wakeUpDevice(self,topic='', token=None, magic=None, cert=''):
        wrapper = APNSNotificationWrapper(cert, False)
        message = APNSNotification()
        message.tokenHex(token)
        message.appendProperty(APNSProperty('mdm',magic))
        wrapper.append(message)
        wrapper.notify()


#if __name__ == '__main__':
#    mdm = MDMCommands()
#    print (mdm.installApplication(1.0,'sdfsdf',url='http://www.baidu.com', mflags=1))
