## Meeting 

13/4
- Main concerns for the week:
    - Log into a real user instead of mock user.
    - Reset password functionality.
- Discussed what we can perform unit testing on. For now, we can do one test per person inside db/crud.py.

15/4
- Brief discussion on how CI / unit testing should be performed, Albin and Simon will take on the initial set-up.

17/4
- Made sure everyone was done or close to done with their unit tests.
- Cleared up some merge conflicts that were not resolved accurately.


## Ellen Pennebratt

12/4
- Did: Fixed issue #56 by implementing and correcting session timeout logic, protecting the dashboard, and ensuring proper redirect to the login page on logout or inactivity. Also created this week’s checklists and helped organize sprint tasks.

- Next: Begin improving authentication (e.g., proper user validation) and support the team with further testing.

- Blockers: none

14/4 
- Did: Created a new GitHub branch to work on the login/authentication functionality and followed the team’s branching workflow. Ensured changes are isolated from the main branch to support safer development and collaboration.

- Next: Continue working on routing the backend and frontend for register page.

- Blockers: none

17/4
- Did: Worked on backend unit tests for the CRUD/database layer and added an edge‑case test that revealed a data integrity issue related to transaction category validation. Created a GitHub issue and handed it over to the database team for investigation and fixing. Also updated the README with backend‑related instructions for unit tests, code coverage, and linting.
- Next: Continue backend work where possible and review/integrate the database team’s fix once it is available.
- Blockers: Waiting for the database team to fix the reported transaction category validation bug. (Which they did the same day.)

## Gresa Hoxha

16/4
- Did: Completed the login/authentication system. Added 'get_user_by_email' in 'crud.py' and updated the login route to validate credentials against the database. Connected the frontend routes for registration and forgot‑password to the backend, ensuring proper error handling and session management. Tested registration, password reset, and login flows successfully. The whole login process now works with real users.  

- Next: Implement password hashing for secure authentication and begin writing unit tests for CRUD functions.  

- Blockers: None for the time being.

17/4
- Did: unit testing for get_user_by_email. Test passed without bugs or conflicts.


## Jafar Gohari

13/4

- Discussed the checklist and action items for the current week.
- Set a goal to complete and deploy the dashboard by the end of the week.


## Albin Törnberg

13/4
- Did: Looked through issues for things that could be prioritized/closed. Thought about next steps.
- Blockers: None
- Next: Start working on issues #83 and #75.

15/4
- Did: Started implementing CI and Unit Testing with Simon.
- Blockers: None.
- Next: Finish CI and issues.

17/4
- Did: Got CI working, set up taskipy to use for linting and testing.
- Blockers: Some merge issues prevented CI from running right, easily fixed.
- Next: Set expectations and priorities for next sprint.


## Simon Rignell 
13/4
- Did: planned issues for sprint-2
- Blockers: None
- Next: working on issues #89 and #75.

15/4
- Did: Fixed [#89](https://github.com/tmuk26-group-1/budget-tool/issues/89) , added unit test for [#93](https://github.com/tmuk26-group-1/budget-tool/issues/93), updating eqivalent to makefile and added function for updating password and relevant test [978d54d](https://github.com/tmuk26-group-1/budget-tool/commit/978d54d) , [6fa5b9d](https://github.com/tmuk26-group-1/budget-tool/commit/6fa5b9d), [44c9278](https://github.com/tmuk26-group-1/budget-tool/commit/44c9278), [c2f6807](https://github.com/tmuk26-group-1/budget-tool/commit/c2f6807)
- Blockers: None
- Next: working on code coverage and lint
  

16/7
- Did: Added code covarage and flake8 [0721596](https://github.com/tmuk26-group-1/budget-tool/commit/0721596), [e7105e9
](https://github.com/tmuk26-group-1/budget-tool/commit/e7105e9)
- Blockers: None
- Next: planning sprint-3

17/4
- Did: Fixed bug with create_transaction, added a check to see if a category exist [bc83a35](https://github.com/tmuk26-group-1/budget-tool/commit/bc83a35), fixing issue [#118](https://github.com/tmuk26-group-1/budget-tool/issues/118)
- Blockers: Merge conflict between branches. But we fixed it pretty quickly
- Next: planning sprint-3

## Vasilis Segersköld
14/4
- Did: Completed the forgot-password page structure [#105](https://github.com/tmuk26-group-1/budget-tool/commit/10aaeab6517d78d9e2d3208f67d06169435ce733)
- Blockers: None
- Next: Stylize the forgot-password page

15/4
- Did: Stylized the forgot-password page [#120](https://github.com/tmuk26-group-1/budget-tool/commit/b5babea4d57303ed007a9b454a197cfa6608138d)
- Blockers: None
- Next: Unit testing

17/4
- Did: Created a unit test
- Blockers: None
- Next: Build dashboard.html