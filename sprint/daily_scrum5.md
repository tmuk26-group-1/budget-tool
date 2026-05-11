## Meeting
We met last week on friday, decided that this week should be a pretty much finalized version of the webapp.

## Ellen Pennebratt

### 4/5
- Did:
- Blockers:
- Next:

### 6/5
- Did: Implemented backend support for savings. Added a savings field to the User model and updated CRUD logic to store and retrieve savings per user. Implemented functionality to manually update savings (add/remove money) and connected it to the dashboard.
- Blockers: Minor issues with existing tests due to previous savings logic being based on transactions.
- Next: Update tests to match the new savings implementation and support frontend integration for updating savings.

### 9/5
- Did: Updated existing tests to match the new savings implementation. Replaced transaction‑based savings calculations with the new update_savings logic and ensured tests correctly validate manual add/remove behavior. Added additional tests to cover savings updates and edge cases.
- Blockers: None
- Next: Verify all tests pass consistently and ensure frontend integration works smoothly with the new savings functionality.

---

## Gresa Hoxha

### 4/5
- Did: Completed full backend integration test suite, fixed failing tests, added missing coverage for helper functions and routes, and merged PR #174 (backend test coverage ~91%). Cleaned up branches and prepared backend–database integration plan.
- Blockers: Waiting for database team to implement monthly goal, total savings, category totals, and transaction history queries.
- Next: Create backend–database integration issue and prepare for dynamic dashboard implementation once DB updates are ready.

### 6/5
- Did:
- Blockers:
- Next:

### 9/5
- Did:
- Blockers:
- Next:

---

## Vasilis Segersköld

### 3/5
- Did: Removed 'remember me' from the login page [#148](https://github.com/tmuk26-group-1/budget-tool/issues/148)
- Blockers: None
- Next: Add 'update monthly goal' button on the dashboard

### 4/5
- Did: Added 'update monthly goal' button [#171](https://github.com/tmuk26-group-1/budget-tool/pull/171), and finalized the frontend together with Jafar
- Blockers: None
- Next: Not sure at this point; frontend is pretty much done for now.

### 9/5
- Did:
- Blockers:
- Next:

---

## Jafar Gohari

### 4/5
- Did:
- Blockers:
- Next:

### 6/5
- Did:
- Blockers:
- Next:

### 9/5
- Did:
- Blockers:
- Next:

---

## Albin Törnberg

### 4/5
- Did: Adjusted the User class to include the monthly goal. Implemented function to update.
- Blockers: None
- Next: Work on total savings with Simon.

### 6/5
- Did: Added some testing, fixed description input and routing, and some other small frontend changes.
- Blockers: None
- Next: Work on monthly "rollover" implementation.

### 9/5
- Did: Fixed some code structure of DB files using linter.
- Blockers: None
- Next: Work on monthly "rollover" implementation.

---

## Simon Rignell

### 4/5
- Did: Added function that calculates the totalt incomes. Also added function add get_transaction with join, get_total_savings and get_category_totals 
- Blockers: none 
- Next: Panning and fixing everython for the upcoming lab 

### 6/5
- Did: Connected everything for the lab, so that everything works as it should. Also added my integration-test
- Blockers: none
- Next: Work with total saving with albin 

### 9/5
- Did:
- Blockers:
- Next:
