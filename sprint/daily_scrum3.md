## Meeting

20/4 (planning)
- Clarified meeting structure and purpose. Suggested to have meetings on Mondays, Wednesdays and Fridays.
- Discussed major goals for the sprint.
  - Frontend: Dashboard to show balance, add transactions via sparate page.
  - Backend: Connect the frontend and database.
  - Database: Make sure transactions are stored correctly and balance gets calculated.

22/4 (preparation for lab)
- All teams presented their current progress. Frontend and database work was reviewed and aligned.No new features were added to scope during the meeting. Backend will focus solely on implementing the required routes for the dashboard for tomorrows lab. 

- Discussed and aligned in today’s team meeting on updates to the budget logic. (Which will be implemented next week).
  - Agreed to add a separate counter for savings.
  - Introduce “Other” as a new transaction category.
  - Include a “saved from previous month” value that contributes to the current budget.
  - The remaining budget should reset on a monthly basis.

- Frontend: (Next week)
  - Update the dashboard UI to:
    - Display a separate savings counter.
    - Display “saved from previous month” as part of the current budget.
    - Add “Other” as a selectable category in the transaction form.
  - Clearly distinguish:
    - Current month budget.
    - Savings.
    - Carry‑over from previous month.
    - Prepare UI logic for monthly reset (values reset visually when backend signals a new month).
    - Coordinate with backend on required response fields.

- Backend: (Next week)
  - Define/update API responses to include:
    - ```current_budget```
    - ```savings_total```
    - ```saved_from_previous_month```

  - Ensure dashboard routes return all required values in a clear structure.

  - Prepare logic to:
    - Include “saved from previous month” in the budget calculation.
    - Reset monthly values when a new month starts (or rely on database flags).
    - Add backend support for the “Other” category (no hardcoding in routes)
    - Create/adjust backend issues reflecting the new requirements

- Database Team: (Next week)
  - Extend the data model to support:
    - A savings counter.
    - A field/value for saved from previous month. [141](https://github.com/tmuk26-group-1/budget-tool/issues/141)

  - Decide and implement monthly reset logic, e.g.:
    - Scheduled reset.
    - Reset on first transaction of a new month.

  - Ensure:
    - “Other” exists as a valid category. [128](github.com/tmuk26-group-1/budget-tool/pull/128)
    - Carry‑over value is preserved correctly between months.

  - Expose or update CRUD functions so backend can:
  - Fetch savings.
  - Fetch carry‑over.
  - Reset monthly values safely.

## Ellen Pennebratt
20/4
- Did: Created backend‑related GitHub issues outlining the required transaction flow and integration between frontend and database. Documented the dependency on the database team for transaction handling functionality and clarified expectations through the issues.
- Blockers: Waiting for the database team to implement the transaction handling function required by the backend.
- Next: Wait for the database team to implement the transaction handling function. Once available, proceed with backend integration and connect the frontend to the database logic.

24/4
- Did: Integration testing was added to verify the interaction between Flask routes, session handling, and the database layer using an isolated in‑memory SQLite database.
- Blockers: None
- Next: Continue with issues. 


## Gresa Hoxha
20/4
- Did: Meeting. Took a look at issues.
- Blockers: Had to wait for frontend and database to create their stuff regarding "add-transaction".
- Next: make the backend connection.

22/4
- Did: Connected the dashboard design and the add transaction page to the database logic behind it. At this stage it works to alter the balance based on each individual user. 
- Blockers: problems occured due to the many pull requests and branches. Sugessted that we all be a little more careful when creating new pull requests, meaning that we make sure none are sitting from earlier. Problem was fixed by hard-merging the branches as for now. Otherwise no blockers.
- Next: See list we discussed during Wednesday meeting.

## Vasilis Segersköld
20/4
- Did:
- Blockers:
- Next:

22/4
- Did:
- Blockers:
- Next:

24/4
- Did:
- Blockers:
- Next:


## Jafar Gohari
20/4
- Did:
- Blockers:
- Next:

22/4
- Did:
- Blockers:
- Next:

24/4
- Did:
- Blockers:
- Next:


## Albin Törnberg
20/4
- Did: Added daily scrum notes template for sprint 3. Added coverage omit configuration in `pyproject.toml`.
- Blockers: None
- Next: Add function for deleting a user (old, low priority issue [#83](https://github.com/tmuk26-group-1/budget-tool/issues/83)). Look into excluding files from coverage report.

22/4
- Did: Added function for deleting a user. Finalized and merged PRs [#134](https://github.com/tmuk26-group-1/budget-tool/pull/134) and [#138](https://github.com/tmuk26-group-1/budget-tool/pull/138) into main.
- Blockers: None
- Next: Structure database tasks for the coming sprint.

24/4
- Did: Added issue [#146](https://github.com/tmuk26-group-1/budget-tool/issues/146). Finalized and merged [PR #143 (CRUD fixes after meeting)](https://github.com/tmuk26-group-1/budget-tool/pull/143).
- Blockers: None
- Next: Prepare and plan for next sprint.


## Simon Rignell 
20/4
- Did: Created function that adds predetermined categories on startup 
- Blockers: none 
- Next: add function that calculate and subtract salary when transaction is added 

22/4
- Did: commit the functions to the PR and merge the branch to main 
- Blockers: none
- Next: Create more Crud-tests

24/4
- Did: Creating more Crud-tests, example test_get_balance
- Blockers: None 
- Next: create Filter for CRUD-functions by month


