# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.course -t test_kurs.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.course.testing.EDI_COURSE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/course/tests/robot/test_kurs.robot
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

Scenario: As a site administrator I can add a Kurs
  Given a logged-in site administrator
    and an add Kurs form
   When I type 'My Kurs' into the title field
    and I submit the form
   Then a Kurs with the title 'My Kurs' has been created

Scenario: As a site administrator I can view a Kurs
  Given a logged-in site administrator
    and a Kurs 'My Kurs'
   When I go to the Kurs view
   Then I can see the Kurs title 'My Kurs'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Kurs form
  Go To  ${PLONE_URL}/++add++Kurs

a Kurs 'My Kurs'
  Create content  type=Kurs  id=my-kurs  title=My Kurs

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Kurs view
  Go To  ${PLONE_URL}/my-kurs
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Kurs with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Kurs title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
