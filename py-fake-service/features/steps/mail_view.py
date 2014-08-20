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

