#! /usr/bin/env python3.3
# encoding: utf-8
'''
AWSDNSAuth -- AWS Route 53 Authorization Tool

AWSDNSAuth is a command line tool to create an AWS Authentication v3 header for Route 53 API then pass it to standard CURL

@author:     sst
        
@copyright:  2013 Sébastien Stormacq. All rights reserved.
        
@license:    BSD 3-Clause License
             http://opensource.org/licenses/BSD-3-Clause

@contact:    sebastien.stormacq@gmail.com
@deffield    updated: Updated
'''

import sys, os, datetime
import configparser, logging

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '23 March 2013'
__updated__ = '2013032301'

DEBUG = 0

def checkCredentialsFilePermission(filepath):
    import stat
    st = os.stat(filepath)
    return bool(st.st_mode & stat.S_IMODE(0o600))

def getLocalDateTime():
    return datetime.datetime.today().strftime("%a, %d %b %Y %H:%M:%S %Z")

def getAmazonDateTime():
    import urllib.request
    httpResponse=urllib.request.urlopen("https://route53.amazonaws.com/date")
    httpHeaders=httpResponse.info()
    logging.debug(httpHeaders)
    return httpHeaders['Date']

def getSignatureAsBase64(text, key):
    import hmac, hashlib, base64
    hm  = hmac.new(bytes(key, "utf-8"), bytes(text, "utf-8"), hashlib.sha256)
    return base64.b64encode(hm.digest())

def getAmazonV3AuthHeader(accessKey, signature):
    # AWS3-HTTPS AWSAccessKeyId=MyAccessKey,Algorithm=ALGORITHM,Signature=Base64( Algorithm((ValueOfDateHeader), SigningKey) )
    return "AWS3-HTTPS AWSAccessKeyId=%s,Algorithm=HmacSHA256,Signature=%s" % (accessKey,signature)

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by sst on %s.
  Copyright 2013 Sébastien Stormacq. All rights reserved.
  
  Licensed under the BSD 3 Clauses License
  http://opensource.org/licenses/BSD-3-Clause
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter, epilog="AWS Credentials File Format:\n\t[credentials]\n\tAWS_ACCESS_KEY=<access key>\n\tAWS_SECRET_KEY=<secret key>")
        parser.add_argument("-c", "--credentials", dest="credentials", action="store", required=True, help="path to a file containing AWS credentials [required]")
        parser.add_argument("-a", "--amazonDate", dest="amazonDate", action="store_true", help="use the date provided by Amazon instead of local date [default = False]", default=False )
        parser.add_argument("curl_parameters", nargs="+", help="parameters to be passed to curl command, starting with the URL")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="display more information during execution [default = False]", default=False )
        
        # Process arguments
        args = parser.parse_args()
        
        if args.verbose:
            logging.getLogger().setLevel(logging.INFO)
        
        # Read AWS credentials
        if not checkCredentialsFilePermission(args.credentials):
            logging.warning("Credential file must be restricted to your own user, use chmod 600 %s" % args.credentials)
            sys.exit(-1)
        logging.info("Reading configuration from %s" % args.credentials)
        config = configparser.SafeConfigParser()
        config.read(args.credentials)
        
        AWS_ACCESS_KEY=config.get("credentials", "AWS_ACCESS_KEY") 
        AWS_SECRET_KEY=config.get("credentials", "AWS_SECRET_KEY") 
        logging.debug("AWS_ACCESS_KEY = %s" % AWS_ACCESS_KEY)    
        logging.debug("AWS_SECRET_KEY = %s" % AWS_SECRET_KEY) 

        # Retrieve System date        
        AWS_DATE=None
        if args.amazonDate:
            logging.info("Retrieving Date from Amazon Route 53")
            AWS_DATE=getAmazonDateTime()
        else:
            logging.info("Retrieving Date from local computer")
            AWS_DATE=getLocalDateTime()
        logging.debug("AWS_DATE = %s" % AWS_DATE)  
                
        # Sign the date
        sig = getSignatureAsBase64(AWS_DATE, AWS_SECRET_KEY)
        logging.debug("SIG BASE 64 = %s" % sig)
        
        # generate the AWS v3 authentication header
        AWS_AUTH = getAmazonV3AuthHeader(AWS_ACCESS_KEY, sig)
        logging.debug("AWS AUTH HEADER = %s" % AWS_AUTH)
        
        import subprocess
        return subprocess.call(["/usr/bin/curl",
                        "-s", "-S",
                        "--header",
                        "X-Amzn-Authorization: %s" % AWS_AUTH,
                        "--header",
                        "x-amz-date: %s" % AWS_DATE] +
                        args.curl_parameters)
                        
        
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        #sys.argv.append("-h")
        #sys.argv.append("-v")
        logging.getLogger().setLevel(logging.DEBUG)
        
    sys.exit(main())