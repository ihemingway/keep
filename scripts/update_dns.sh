#!/bin/bash

mydomain="boxclever.me"
myarecord="home"
api_url="https://desec.io/api/v1/domains/${mydomain}/rrsets/${myarecord}/A/"
apikey="xxxxxxx"

myip=`curl -s "https://api.ipify.org"`
desec_ip=`curl -s ${api_url} --header "Authorization: Token ${apikey}" | jq -r '.records[0]'`
echo "`date '+%Y-%m-%d %H:%M:%S'` - Current External IP is $myip, Desec.io DNS IP is $desec_ip"

if [ "$desec_ip" != "$myip" -a "$myip" != "" -a "$desec_ip" != "" ]; then
  echo "IP has changed. Updating on Desec.io"
  curl -X PATCH ${api_url} --header "Authorization: Token ${apikey}" --header "Content-Type: application/json" --data @- <<< '{"records": ["'${myip}'"]}'
  logger -t $0 "Changed IP for ${myarecord}.${mydomain} from ${desec_ip} to ${myip}"
fi

