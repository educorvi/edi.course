# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.course -t test_notiz.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.course.testing.EDI_COURSE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/course/tests/robot/test_notiz.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Notiz
  Given a logged-in site administrator
    and an add Notizbuch form
   When I type 'My Notiz' into the title field
    and I submit the form
   Then a Notiz with the title 'My Notiz' has been created

Scenario: As a site administrator I can view a Notiz
  Given a logged-in site administrator
    and a Notiz 'My Notiz'
   When I go to the Notiz view
   Then I can see the Notiz title 'My Notiz'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Notizbuch form
  Go To  ${PLONE_URL}/++add++Notizbuch

a Notiz 'My Notiz'
  Create content  type=Notizbuch  id=my-notiz  title=My Notiz

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Notiz view
  Go To  ${PLONE_URL}/my-notiz
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Notiz with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Notiz title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
