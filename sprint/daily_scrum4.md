## Meeting

27/4 (Planning)
Meeting Monday 27/4

- Discussed plans for this week. Goals:
    - Add logout function.
    - Add "BudgetGoal" function".


28/4 (Preparation for lab)


29/4 (Sprint review)


## Ellen Pennebratt
27/4
- Did: Worked on implementing backend support for the Monthly Goal feature. Added logic to store the goal per user in the database and updated CRUD functions to retrieve and display the value on the dashboard. Ensured the goal is user‑specific and not tied to a specific month.
- Blockers: None
- Next: Start implementing savings functionality in the backend, including updating CRUD logic and reviewing how savings should be stored separately from transactions.

29/4
- Did: (Got sick for a week and got very little work done.)
- Blockers:
- Next:

## Gresa Hoxha
27/4
- Did:
- Blockers: 
- Next: 

29/4
- Did: Fixed issue #58 and also PR #156
- Blockers: Waiting for other teams to implement features.
- Next: issue #163

## Vasilis Segersköld
27/4
- Did: Spread out stylizing from one big CSS file (styles.css) to multiple smaller ones [#147](https://github.com/tmuk26-group-1/budget-tool/pull/147)
- Blockers: None
- Next: Add variables instead of hardcode for monthly goal in dashboard.html

29/4
- Did: Added variables instead of hardcoding for monthly goal [#162](https://github.com/tmuk26-group-1/budget-tool/pull/162)
- Blockers: None
- Next: Remove 'remember me' from the login page

## Jafar Gohari
27/4
- Did:
- Blockers: 
- Next: 

29/4
- Did:
- Blockers:
- Next:

## Albin Törnberg
27/4
- Did: Worked on artifact generation (coverage report)
- Blockers: A test was failing due to new hashing of passwords, this is already being worked on. 
- Next: Finalize above and work on transaction dates.

29/4
- Did: Worked on and finalized transaction dates, informed backend team of changed functions.
- Blockers: None
- Next: Start working on the next goal (monthly goal)

## Simon Rignell 
27/4
- Did: added month and year filtering with Albin
added unit tests for delete_user, get_transaction and get_category and 
update tests get_balance and get_transaction with year and moth fiter
- Blockers: tests failed because of new hashed password
- Next: Fix failed tests by updating the plaintext password to the generated hashed password

29/4
- Did: Finalized year and month filter so it works correctly and fixed failing tests for hased passwords
- Blockers: none
- Next: Start with monthly goal 



