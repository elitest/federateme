#!/usr/bin/env python3
import boto.utils, json, requests
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


print(gen_link())
