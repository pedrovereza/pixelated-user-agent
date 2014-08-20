from behave import *
from common import *

def find_current_mail(context):
    return find_element_by_xpath(context, '//*[@id="mail-list"]/li[@id="mail-%s"]//a' % context.current_mail_id)


def check_current_mail_is_visible(context):
    find_current_mail(context)

def open_current_mail(context):
    e = find_current_mail(context)
    e.click()

@then('I see that mail under the \'{tag}\' tag')
def impl(context, tag):
    context.execute_steps("when I select the tag '%s'" % tag)
    check_current_mail_is_visible(context)

@when('I open that mail')
def impl(context):
	open_current_mail(context)

@when('I open the first mail in the mail list')
def impl(context):
    elements = context.browser.find_elements_by_xpath('//*[@id="mail-list"]//a')
    context.current_mail_id = elements[0].get_attribute('href').split('/')[-1]
    elements[0].click()
