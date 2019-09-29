from argparse import ArgumentParser
from datetime import datetime
import urllib2, time, ssl, json, sys
import xml.etree.ElementTree as ET

##### start helper functions #####

# this ssl context bypasses the certificate and hostname validation
# within an enterprise environment this is not as bad, as it's still running on
# controlled hosts and networks. The connection will still be TLS, so the
# traffic can't be eavesdropped, it'll just save having to set up the cert trust on the
# machine exactly right for the connection to be trusted.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def apply_template(file, vars):
    """
    reads the file, and vars are passed in to substitute where there are
    matching template names in the document
    """
    return open(file, 'r').read() % vars


def read_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--firstname", dest="first_name",
                        help="the user's first name", metavar="first_name")
    parser.add_argument("-l", "--lastname", dest="last_name",
                        help="the user's last name", metavar="last_name")
    parser.add_argument("-u", "--userid", dest="user_id",
                        help="the user's dhs logon/user id", metavar="user_id")
    parser.add_argument("-e", "--email", dest="email",
                        help="the user's email address", metavar="email")
    return parser.parse_args()


def get_config():
    with open('config.json') as json_data_file:
        to_return = json.load(json_data_file)
    lastUpdatedTimestamp = to_return["lastUpdated"]
    # We have to parse the timestamp from an ISO Timestamp into a datetime
    # object. This is easier in Python3, but this seems to work for python 2
    if lastUpdatedTimestamp != "":
        to_return["lastUpdated"] = datetime.strptime(lastUpdatedTimestamp, "%Y-%m-%d %H:%M:%S.%f")
    else:
        to_return["lastUpdated"] = datetime.now()

    return to_return


def write_config(config_to_write):
    lastUpdatedTimestamp = datetime.now().__str__()
    to_write = config_to_write
    to_write["lastUpdated"] = lastUpdatedTimestamp
    
    with open('config.json', 'w') as outfile:
        json.dump(to_write, outfile, indent=4, separators=(',', ': '))
    
    return True


def test_config(config_to_test):
    return True


def build_auth_payload(user_name, password):
    return apply_template('auth.xml', {
        'username': user_name,
        'password': password
    })


def build_action_payload(first_name, last_name, user_id, email, hostname):
    return apply_template('create_account.xml', {
        'firstname': first_name,
        'lastname': last_name,
        'userid': user_id,
        'email': email,
        'hostname': hostname
    })


def parse_xml_response(xml):
    root = ET.fromstring(xml)
    toReturn = {}
    for child in root:
        toReturn[child.tag] = child.text
    return toReturn


def parse_xml_response_test():
    tree = ET.parse('exampleresponse.xml')
    root = tree.getroot()
    toReturn = {}
    for child in root:
        toReturn[child.tag] = child.text

    return toReturn


def authenticate_to_amis(uri, body, ctx):
    req = urllib2.Request(uri)
    req.add_header('Content-Type', 'application/xml')
    req.add_data(body)
    response = urllib2.urlopen(req, context = ctx)
    read_response = response.read()

    # parsed_auth_response = parse_xml_response_test()
    parsed_auth_response = parse_xml_response(read_response)

    try:
        authenticated = (parsed_auth_response["authenticated"] == "true")
    except:
        authenticated = False

    try:
        new_service_password = parsed_auth_response["newServiceAccountPassword"]
    except:
        new_service_password = None

    try:
        auth_token = parsed_auth_response["authenticationToken"]
    except:
        auth_token = None

    if authenticated == True:
        print('auth success')
        
        if new_service_password == None:
            print('password not rotated')
        else:
            print('password rotated')
            config["serviceAccountPassword"] = new_service_password # this will rotate the password in the config for the next call

        if auth_token == None:
            print('no auth token provided')
        else:
            print('auth token provided')
            config["rsaAuthenticationToken"] = auth_token

        return True
    else:
        return False


def call_prime():
    return True


##### end helper functions #####

##### start script #####

args = read_args()
print('parsed args')

config = get_config()
print('read config')

try:
    current_auth_token = config["rsaAuthenticationToken"]
except:
    current_auth_token = None

# if we have an auth token in the config, try that first
if current_auth_token == None:
    authenticate_first = True
else:
    authenticate_first = False;

# if the auth token fails, call the auth endpoint to get a new one

if authenticate_first == True:
    auth_payload = build_auth_payload(config["serviceAccountUsername"], config["serviceAccountPassword"])
    print('built auth payload')
    
    is_authenticated = authenticate_to_amis(config["authUri"], auth_payload, ctx)
    print('authentication response received')



action_payload = build_action_payload(args.first_name, args.last_name, args.user_id, args.email, "localhost")
print('built action payload')




# response_root = parse_amis_response(response)




# if authenticated 
    # if password rotated, update config
    # if we have an auth token, update config

write_config(config)
print('config updated')

# create it if it doesn't exist


##### end script #####