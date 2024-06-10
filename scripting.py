import ldap

username = 'alex'
password = 'secretpassword'
basedn = 'ou=users,dc=orbital,dc=com'
conn = ldap.initialize('ldap://localhost:389/')
conn.set_option(ldap.OPT_REFERRALS, 0)
try:
    res = conn.simple_bind_s(f'cn={username},{basedn}', password)
    print(conn.result)
    result = conn.search_s(f'cn={username},{basedn}',
                           ldap.SCOPE_SUBTREE,
                           f'cn={username}',
                           None)
    print(result)
except ldap.INVALID_CREDENTIALS as e:
    print(e)
