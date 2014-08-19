from behave import given, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def wait_until_element_is_visible_by_locator(context, locator_tuple):
    wait = WebDriverWait(context.browser, 10)
    wait.until(EC.visibility_of_element_located(locator_tuple))


def fill_by_xpath(context, xpath, text):
    field = context.browser.find_element_by_xpath(xpath)
    field.send_keys(text)


@given('I compose a message with')
def impl(context):
    toggle = context.browser.find_element_by_id('compose-mails-trigger')
    toggle.click()

    for row in context.table:
        fill_by_xpath(context, '//*[@id="subject"]', row['subject'])
        fill_by_xpath(context, '//*[@id="text-box"]', row['body'])

@given("for the '{recipients_field}' field I type '{to_type}' and chose the first contact that shows")
def choose_impl(context, recipients_field, to_type):
    browser = context.browser
    browser.find_element_by_css_selector(
        '#recipients-to-area span input.tt-input'
        ).click()
    recipients_field = recipients_field.lower()
    css_selector = '#recipients-%s-area' % recipients_field
    recipients_element = browser.find_element_by_css_selector(css_selector)
    recipients_element.find_element_by_css_selector(
        '.tt-input'
        ).send_keys(to_type)
    wait_until_element_is_visible_by_locator(context, (By.CLASS_NAME, 'tt-dropdown-menu'))
    browser.find_element_by_css_selector('.tt-dropdown-menu div div').click()


@given('I save the draft')
def save_impl(context):
    context.browser.find_element_by_id('draft-button').click()


@when('I open the saved draft and send it')
def send_impl(context):
    context.execute_steps('I select the tag \'drafts\'')
    context.execute_steps('I open the first mail in the mail list')
