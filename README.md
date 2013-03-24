AWSDNSAuth
==========

Creates AWS Authentication Header for Route 53 API Calls.

This is a python script that creates proper AWS Route 53 HTTP headers before calling CURL.


Usage
-----

```
usage: AWSDNSAuth.py [-h] -c CREDENTIALS [-a] [-V] [-v]
                     curl_parameters [curl_parameters ...]

AWSDNSAuth -- AWS Route 53 Authorization Tool

  Created by sst on 23 March 2013.
  Copyright 2013 Sébastien Stormacq. All rights reserved.
  
  Licensed under the BSD 3 Clauses License
  http://opensource.org/licenses/BSD-3-Clause
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE

positional arguments:
  curl_parameters       parameters to be passed to curl command, starting with
                        the URL

optional arguments:
  -h, --help            show this help message and exit
  -c CREDENTIALS, --credentials CREDENTIALS
                        path to a file containing AWS credentials [required]
  -a, --amazonDate      use the date provided by Amazon instead of local date
                        [default = False]
  -V, --version         show program's version number and exit
  -v, --verbose         display more information during execution [default =
                        False]

AWS Credentials File Format:
  [credentials]
	AWS_ACCESS_KEY=<access key>
	AWS_SECRET_KEY=<secret key>
```
  
Usage Example
-------------

```xml
sst:src sst$ ./AWSDNSAuth.py -a -c /Users/sst/.aws-secret https://route53.amazonaws.com/2012-12-12/hostedzone | xmllint --format -
<?xml version="1.0"?>
<ListHostedZonesResponse xmlns="https://route53.amazonaws.com/doc/2012-12-12/">
  <HostedZones>
    <HostedZone>
      <Id>/hostedzone/MY_ZONE_ID</Id>
      <Name>aws.mydomain.com.</Name>
      <CallerReference>22F684C6-3886-3FFF-8437-E22C5DCB56E7</CallerReference>
      <Config>
        <Comment>AWS Route53 Hosted subdomain</Comment>
      </Config>
      <ResourceRecordSetCount>4</ResourceRecordSetCount>
    </HostedZone>
  </HostedZones>
  <IsTruncated>false</IsTruncated>
  <MaxItems>100</MaxItems>
</ListHostedZonesResponse>
```
