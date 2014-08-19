from behave import *

def check_current_mail_is_visible(context):
    e = context.browser.find_element_by_xpath('//*[@id="mail-list"]/li[@id="mail-%s"]' % context.current_mail_id)


@then('I see that mail under the \'{tag}\' tag')
def impl(context, tag):
    context.execute_steps("when I select the tag '%s'" % tag)
    #check_current_mail_is_visible(context)

@when('I open that mail')
def impl(context):
	pass

@then('I see that the subject reads {subject}')
def impl(context, subject):
	pass

@when('I open the first mail in the mail list')
def impl(context):
    elements = context.browser.find_elements_by_xpath('//*[@id="mail-list"]//a')
    context.current_mail_id = elements[0].get_attribute('href').split('/')[-1]
    elements[0].click()
