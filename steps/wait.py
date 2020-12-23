import os
from behave import given, when, then
import sys
import time
# context: where behave runs
sys.path.insert(1, 'lib/')
import wcommon as wc
wc.jenkins_header(); # load inputs from Jenkinsfile
wc.wcheader['packages']['wc'] = wc.__file__
wc.jd(wc.wcheader)
ARC = '10.88.240.60'; # CHASSIS2
WP = '10.44.0.21'; # CHASSIS1
os.environ['STC_PRIVATE_INSTALL_DIR'] = STC_PRIVATE_INSTALL_DIR = '/opt/STC_5.16/Spirent_TestCenter_5.16/Spirent_TestCenter_Application_Linux'
# import Stc

@given(u'Nothing')
def step_impl(context):
	assert True

@when(u'I try to wait "{secs}"')
def step_impl(context, secs):
	time.sleep(int(secs))
	pass

@then(u'I expect response "{expectationBoolean}"')
def step_impl(context, expectationBoolean):
	assert True
