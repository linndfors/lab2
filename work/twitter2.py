import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

def main(argm):
    # https://apps.twitter.com/
    # Create App and get the four strings, put them in hidden.py

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while True:
        print('')
        # acct = input('Enter Twitter Account:')
        acct = argm
        if (len(acct) < 1): break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': 20})
        print('Retrieving', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)
        with open('twiter2.json', 'w') as f_ile:
            json.dump(js, f_ile, indent=2)
        # print(json.dumps(js, indent=2))

        headers = dict(connection.getheaders())
        print('Remaining', headers['x-rate-limit-remaining'])

        for u in js['users']:
            print(u['screen_name'])
            if 'status' not in u:
                print('   * No status found')
                continue
            s = u['status']['text']
            print('  ', s)
        break
