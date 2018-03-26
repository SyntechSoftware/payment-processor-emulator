import json
import urllib
import requests


url = "http://127.0.0.1:8000/cgi-bin/tranzila71u.cgi"

token_payload22 = {
    'supplier': "dmatcher",
    'tranmode': 'C6616',
    'authnr': '0000000',
    'TranzilaTK': 'V54997800bd3ef31111',
    'expdate': '0818',
    'sum': 100,
}

token_payload3 = {
    'supplier': 'syntech',
    'tranmode': 'K',
    'expdate': '0419',
    'ccno': '4111111111111111',
    'mycvv': '333',
    'currency': 1,
    'cred_type': 1,
    'sum': 25,
    'myid': 12312312,
}

token_payload = {
        'supplier': 'syntech',
        'TranzilaTK': 'V001eq13oxv2ald3cev',
        'expdate': '0818',
        'tranmode': 'A',
        'cred_type': 1,
        'currency': 1,
        'sum': 100,
    }


token_payload5 = {
    'supplier': 'syntech',
    'TranzilaTK': 1,
    'ccno': '4444333322221111',
}

#currency=1&cred_type=1&tranmode=A&supplier=syntech&myid=12312312&sum=1&ccno=4444333322221111&expdate=0919
#Response=000&myid=12312312&currency=1&cred_type=1&ccno=1111&DclickTK=&supplier=syntech&tranmode=A&expdate=0919&sum=1&ConfirmationCode=0000000&index=1&Responsesource=0&Responsecvv=0&Responseid=3&Tempref=01170001&DBFIsForeign=1&DBFcard=2&cardtype=2&DBFcardtype=2&cardissuer=2&DBFsolek=6&cardaquirer=6&tz_parent=syntech


#currency=1&cred_type=1&tranmode=V&supplier=syntech&myid=12312312&sum=1&ccno=4444333322221111&expdate=0919
#Response=003&myid=12312312&currency=1&cred_type=1&ccno=1111&DclickTK=&supplier=syntech&tranmode=V&expdate=0919&sum=1&ConfirmationCode=0000000&index=2&Responsesource=1&Responsecvv=3&Responseid=0&Tempref=01240001&DBFIsForeign=1&DBFcard=2&cardtype=2&DBFcardtype=2&cardissuer=2&DBFsolek=6&cardaquirer=6&tz_parent=syntech


print urllib.urlencode(token_payload)

result = requests.get(
    url=url + "?" + urllib.urlencode(token_payload))
message = getattr(result, 'content', 'unknown error')
print message
