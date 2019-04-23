# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.course -t test_videoseite.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.course.testing.EDI_COURSE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/course/tests/robot/test_videoseite.robot
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

Scenario: As a site administrator I can add a Videoseite
  Given a logged-in site administrator
    and an add Lerneinheit form
   When I type 'My Videoseite' into the title field
    and I submit the form
   Then a Videoseite with the title 'My Videoseite' has been created

Scenario: As a site administrator I can view a Videoseite
  Given a logged-in site administrator
    and a Videoseite 'My Videoseite'
   When I go to the Videoseite view
   Then I can see the Videoseite title 'My Videoseite'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Lerneinheit form
  Go To  ${PLONE_URL}/++add++Lerneinheit

a Videoseite 'My Videoseite'
  Create content  type=Lerneinheit  id=my-videoseite  title=My Videoseite

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Videoseite view
  Go To  ${PLONE_URL}/my-videoseite
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Videoseite with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Videoseite title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
