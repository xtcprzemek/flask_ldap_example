from sqlite3 import connect
import ldap
from my_app import app
from flask_login import UserMixin


def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn


class User(UserMixin):
    id = ""
    aonid = ""
    cn = ""
    name = ""
    groups = []

    def __init__(self, user):
        self.id = int(user['uidNumber'][0])
        # self.id=user['mail'][0]
        self.cn = user['cn'][0]
        # self.name=user['displayName'][0]
        # self.groups=user['memberOf']

    def __repr__(self):
        return f"<User {self.name}>"


def ldap_login(username, password):

    def decode_string(val):
        return (val.decode("utf-8"))

    result_ldap = ""
    conn = get_ldap_connection()

    try:
        conn.simple_bind_s(
            f'cn={username},ou=users,dc=orbital,dc=com',
            password
        )
    except ldap.INVALID_CREDENTIALS as e:
        print(e)

    #onn.simple_bind_s(username, password)
    #ldap_result_id=conn.search_st('DC=domain,DC=com', ldap.SCOPE_SUBTREE, '(objectClass=container)', 'name', 0, 30)
    # The next lines will also need to be changed to accroding to the search requirements
    # and the ldap directory structure.
    # For this example, lets use
    base_dn = f"cn={username}, ou=users,dc=orbital,dc=com"
    # SCOPE_ONELEVEL to search for immediate children
    # ldap.SCOPE_SUBTREE to search the object and all its descendants.
    search_scope = ldap.SCOPE_SUBTREE
    # retrieve specified attributes.
    #retrieve_attributes = ['cn']
    # To retrieve all attributes, Use
    retrieve_attributes = None
    search_filter = "cn=psmialy"

    try:
        l_search = conn.search(base_dn, search_scope,
                               search_filter, retrieve_attributes)
        result_status, result_data = conn.result(l_search, 0)
        print(result_data)
    except ldap.LDAPError as e:
        print(e)

    ldap_result_id = conn.search(
        "dc=orbital,dc=com", ldap.SCOPE_SUBTREE, f"cn={username}", None)
    # print(ldap_result_id)
    while 1:
        result_type, res_data = conn.result(ldap_result_id, 1)
        if (res_data == []):
            break
        else:
            result_ldap = res_data[0][1]
            # print(result_data1)

            for key, value in result_ldap.items():
                interm_list = []
                for index, val in enumerate(value):
                    v = decode_string(val)

                    if key == 'memberOf':
                        v = v[3:v.find(',')]
                    interm_list.append(v)

                result_ldap[key] = interm_list
    return result_ldap
