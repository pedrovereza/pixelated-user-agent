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

@then('I see if the mail has html content')
def impl(context):
    #find('#mail-view .bodyArea').should have_css('h2[style*=\'color: #3f4944\']', :text => "cborim")

    dump_source_to(context, '/tmp/see_html.html')
    e = find_element_by_css_selector(context, '#mail-view .bodyArea')
    h2 = e.find_element_by_css_selector("h2[style*='color: #3f4944']")
    assert_that(h2.text, contains_string('cborim'))

@when('I try to delete the first mail')
def impl(context):
    context.execute_steps(u"When I open the first mail in the mail list")
    find_element_by_css_selector(context, '#mail-view #view-more-actions').click()
    context.browser.execute_script("$('#delete-button-top').click();")

    e = find_element_by_css_selector(context, '#user-alerts')
    assert_that(e.text, equal_to('Your message was moved to trash!'))

