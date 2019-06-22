# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.course -t test_notizbuch.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.course.testing.EDI_COURSE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/course/tests/robot/test_notizbuch.robot
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

Scenario: As a site administrator I can add a Notizbuch
  Given a logged-in site administrator
    and an add Notizbuch form
   When I type 'My Notizbuch' into the title field
    and I submit the form
   Then a Notizbuch with the title 'My Notizbuch' has been created

Scenario: As a site administrator I can view a Notizbuch
  Given a logged-in site administrator
    and a Notizbuch 'My Notizbuch'
   When I go to the Notizbuch view
   Then I can see the Notizbuch title 'My Notizbuch'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Notizbuch form
  Go To  ${PLONE_URL}/++add++Notizbuch

a Notizbuch 'My Notizbuch'
  Create content  type=Notizbuch  id=my-notizbuch  title=My Notizbuch

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Notizbuch view
  Go To  ${PLONE_URL}/my-notizbuch
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Notizbuch with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Notizbuch title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
