# Generated by the windmill services transformer
from windmill.authoring import WindmillTestClient

def test_admin_open():
    client = WindmillTestClient(__name__)

    client.open(url=u'http://localhost:8000/account/login')
    client.waits.forPageLoad(timeout=u'8000')
    client.type(text=u'admin', id=u'id_username')
    client.type(text=u'changeme', id=u'id_password')
    client.click(value=u'Log in \xbb')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(xpath=u"//div[@id='home_tab']/a[3]/span", timeout=u'8000')
    client.click(xpath=u"//div[@id='home_tab']/a[3]/span")
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'Log out', timeout=u'8000')
    client.click(link=u'Log out')