./AWSDNSAuth.py -a -c /Users/sst/.aws-secret https://route53.amazonaws.com/2012-12-12/hostedzone/Z3SV7IM8JLB1QB/rrset | xmllint --format -

/AWSDNSAuth.py -a -c /Users/sst/.aws-secret https://route53.amazonaws.com/2012-12-12/hostedzone/Z3SV7IM8JLB1QB/rrset  -X POST -H "Content-Type: text/xml; charset=UTF-8" --upload-file ./DeleteResourceRecordSet.xml