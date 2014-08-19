from behave import given, when


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
    context.browser.find_element_by_css_selector('#recipients-to-area span input.tt-input').click()


@given('I save the draft')
def save_impl(context):
    context.browser.find_element_by_id('draft-button').click()


@when('I open the saved draft and send it')
def send_impl(context):
    context.execute_steps(
        """
        I select the tag 'drafts'
        I open the first mail in the mail list"
        """
    )
