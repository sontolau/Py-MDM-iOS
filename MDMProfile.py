__author__ = 'sonto'
from plistlib import *
from plist import *
import os, uuid, sys

class MDMProfile:
    identifier   = ''
    organization = ''
    version      = 1

    def __init__(self):
        return None

    def sign(self, profile='',certfile='', keyfile='', ca=''):
        if (not self.sign):
            return profile
        unsigned_file = ".mobileconfig.unsigned"
        signed_file   = ".mobileconfig.signed"
        open(unsigned_file, "w").write(profile)

        openssl='openssl smime -sign -in %s -out %s ' \
                '-signer %s -inkey %s -certfile %s ' \
                '-outform der -nodetach'%(unsigned_file,
                                        signed_file,
                                        certfile,
                                        keyfile,
                                        ca)
        os.system(openssl)
        return open(signed_file,"r").read()

    def profile(self,
                content = [],
                description = '',
                removaldisallowed = False,
                scope = 'System',
                uuid=str(uuid.uuid4())):
        profile = dict(
            PayloadContent = content,
            PayloadDescription = description,
            PayloadDisplayName = 'The Profile for %s'%self.organization,
            PayloadIdentifier  = '%s.profile'%self.identifier,
            PayloadOrganization= self.organization,
            PayloadUUID        = uuid,
            PayloadRemovalDisallowed = removaldisallowed,
            PayloadType        = 'Configuration',
            PayloadVersion     = self.version,
            PayloadScope       = scope,
        )
        return writePlistToString(profile)


    def SCEPPayload(self,
                    challenge='',
                    keysize=2048,
                    name='scep',
                    subject=[],
                    url='',
                    uuid=str(uuid.uuid4())):
        scep = dict (
            Challenge = challenge,
            Keysize   = keysize,
            Name      = name,
            Subject   = subject,
            URL       = url,
        )

        plist = dict (
            PayloadContent = scep,
            PayloadDescription = 'Configures SCEP',
            PayloadDisplayName = 'SCEP (%s)'%name,
            PayloadIdentifier  = '%s.%s'%(self.identifier, name),
            PayloadOrganization= self.organization,
            PayloadType        = 'com.apple.security.scep',
            PayloadUUID        = uuid,
            PayloadVersion     = self.version,
        )
        return plist

    def MDMPayload(self,
                   serverURL='',
                   checkInURL='',
                   rights=8191,
                   certificateUUID=str(uuid.uuid4()),
                   topic='',
                   checkoutwhenremoved=False,
                   uuid=str(uuid.uuid4())):

        return dict (
            AccessRights = rights,
            CheckInURL   = checkInURL,
            IdentityCertificateUUID = certificateUUID,
            CheckOutWhenRemoved= checkoutwhenremoved,
            PayloadDescription = 'Configures MobileDeviceManagement',
            PayloadIdentifier  = '%s.mdm'%self.identifier,
            PayloadOrganization= self.organization,
            PayloadType        = 'com.apple.mdm',
            PayloadUUID        = uuid,
            PayloadVersion     = self.version,
            ServerURL          = serverURL,
            Topic              = 'com.apple.mgmt.%s'%topic,
        )
