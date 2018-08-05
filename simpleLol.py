import ldap
import config
from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/info/<username>')
def getInfo(username):
    ldap.set_option(ldap.OPT_REFERRALS,0)

    # Open a connection
    l = ldap.initialize("ldap://diamond.octa.edu")
    l.protocol_version = ldap.VERSION3

    # Bind/authenticate with a user with apropriate rights to add objects
    l.simple_bind_s(config.LOGIN_USERNAME,config.LOGIN_PASSWORD)

    ldap_base = "dc=octa,dc=edu"
    query = "(cn="+username+")"
    result = l.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)

    returnValue = {}
    facultyInfo = result[0][0]

    if facultyInfo is None:
        returnValue['name'] = "User doesn't exist"
        returnValue['faculty'] = False
    else:
        name = result[0][1]['displayName'][0].strip()
        returnValue['name'] = name

        if 'OU=FACULTY' in facultyInfo:
            returnValue['faculty'] = True
        else:
            returnValue['faculty'] = False

    # Its nice to the server to disconnect and free resources when done
    l.unbind_s()

    return jsonify(returnValue)

if __name__ == '__main__':
   app.run()