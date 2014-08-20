from selenium.webdriver.common.keys import Keys
from behave import *
from common import *
from hamcrest import *

@then('I see that the subject reads \'{subject}\'')
def impl(context, subject):
    e = find_element_by_css_selector(context, '#mail-view .subject')
    assert_that(e.text, equal_to(subject))

@then('I see that the body reads \'{expected_body}\'')
def impl(context, expected_body):
    e = find_element_by_css_selector(context, '#mail-view .bodyArea')
    assert_that(e.text, equal_to(expected_body))

@then('that email has the \'{tag}\' tag')
def impl(context, tag):
    elements = find_elements_by_css_selector(context, '#mail-view .tagsArea .tag')
    tags = [e.text for e in elements]
    assert_that(tags, has_item(tag.upper()))

@when('I add the tag \'{tag}\' to that mail')
def impl(context, tag):
    context.browser.execute_script("$('#new-tag-button').click();")
    context.browser.execute_script("$('#new-tag-input').val('%s');" % tag)
    e = find_element_by_css_selector(context, '#new-tag-input')
    e.send_keys(Keys.ENTER)

@then('I reply to it')
def impl(context):
    click_button(context, 'Reply')
    click_button(context, 'Send')
    context.reply_subject = reply_subject(context)

