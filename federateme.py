#!/usr/bin/env python3
import boto.utils, json, requests

def detect_ec2():
    try:
        r = requests.get('http://169.254.169.254/latest/meta-data/ami-id')
        print(r)
        # probably should check for something in the response here.
        return True
    except:
        return False


def gen_link():
    s = json.dumps({'sessionId': boto.utils.get_instance_metadata()['identity-credentials']['ec2']['security-credentials']['ec2-instance']['AccessKeyId'], 
                    'sessionKey': boto.utils.get_instance_metadata()['identity-credentials']['ec2']['security-credentials']['ec2-instance']['SecretAccessKey'],
                    'sessionToken': boto.utils.get_instance_metadata()['identity-credentials']['ec2']['security-credentials']['ec2-instance']['Token']})

    r = requests.get("https://signin.aws.amazon.com/federation", params={'Action': 'getSigninToken', 'SessionDuration': 7200, 'Session': s})

    t = r.json()

    rs = requests.Request('GET', 'https://signin.aws.amazon.com/federation',
                              params={'Action': 'login', 'Issuer': 'Internet Widgets Pty.', 'Destination': 'https://console.aws.amazon.com/', 'SigninToken': t['SigninToken']})
    l = rs.prepare()

    return l.url

if detect_ec2():
    print(gen_link())
else:
    print("This is not an AWS instance.  Please run on an AWS EC2 instance.")
