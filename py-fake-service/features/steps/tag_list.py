from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def wait_until_element_is_visible_by_locator(context, locator_tuple):
    wait = WebDriverWait(context.browser, 10)
    wait.until(EC.visibility_of_element_located(locator_tuple))

def wait_until_element_is_invisible_by_locator(context, locator_tuple):
    wait = WebDriverWait(context.browser, 10)
    wait.until(EC.invisibility_of_element_located(locator_tuple))

def wait_for_user_alert_to_disapear(context):
    wait_until_element_is_invisible_by_locator(context, (By.ID, 'user-alerts'))

def click_first_element_with_class(context, classname):
    elements = context.browser.find_elements_by_class_name(classname)
    elements[0].click()


def dump_source_to(context, filename):
    with open(filename, 'w') as out:
        out.write(context.browser.page_source.encode('utf8'))

@when('I select the tag \'{tag}\'')
def impl(context, tag):
    wait_for_user_alert_to_disapear(context)
    #context.browser.save_screenshot('/tmp/screenshot-tag.jpeg')
    click_first_element_with_class(context, 'left-off-canvas-toggle')
    context.browser.execute_script("window.scrollBy(0, -200)")
    dump_source_to(context, '/tmp/foobar.html')
    e = context.browser.find_element_by_xpath('//*[@id="tag-list"]/ul/li[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "%s")]' % tag)
    e.click()
