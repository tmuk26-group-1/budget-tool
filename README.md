## Budget Tool
BudgetBuddy is a webapplication budgeting tool designed to help users track income, expenses, and monthly budgets. The goal is to provide a clean, simple interface where users can:
- Create and manage monthly budgets,
- Add expenses with categories and dates,
- View summaries of spending,
- Track remaining budget,
- Visualize spending patterns.

## Project plan (Draft)
The first version of BudgetBuddy will include:
- user registration & login,
- create a monthly budget,
- add expenses (amount, category, date, description),
- view total spending and remaining budget,
- simple dashboard page,
- basic data storage using a database.

Future milestones may include:
- spending charts,
- category-based analytics,
- export/import of data,
- saving goals.

## How will it work?
The __frontend__ will provide pages for login, dashboard, and expense entry.  
The __backend__ will expose routes for authentication, budget managment, and expense handling.  
The __database__ will store users, budgets, and expenses.  
The system will follow a clean separation between frontend, backend, and data layers.  

## Technology Choices
- __Python__ for backend
- __Flask__ as the web framework
- __HTML__ for frontend.

## Workflow
Work devided into three teams:  
- Team 1 __FRONTEND__ : Jafar and Vasilis  
    Decide on the look of the webbapplication and the user interface.
- Team 2 __BACKEND__  : Gresa and Ellen  
    Implement the logic behind the application. This is the bridge between the fronend nd the database.
- Team 3 __DATABASE__ : Albin and Simon  
    Implement the part of storing users, budgets and expenses.  

__COMMUNICATION IS KEY__

## Kanban Board  
We track our workflow using a GitHub Project KanBan Board:  
https://github.com/orgs/tmuk26-group-1/projects/2

## Project Structure Overview
The project follows a standard Flask layout to keep frontend, backend, and future database logic organised.
- _app.py_ - main application file (__BACKEND__). This will ater intialize Flask, register routes, connect to the database, and start the server.
- _requirements.txt_ - Lists all Python dependencies (currently only Flask).
- _templates/_ - Contains all HTML pages (__FRONTEND__).
    - _base.html_ is the shared layout.
    - _login-html_ and dashboard.html will become real pages later.
- _static/_ - Stores CDD, images, and other static files (__FRONTEND__).
    - _styles.css_ will hold the app's styling.
- Nothing is created yet for the __DATABASE__, that will come once the basic Flask app is running.  

This structure forms the foundation of the BudgetBuddy web application and allows the frontend, backend, and database teams to work in parallel as the project grows.

## How to run the project  
To be added...  

## Members

| Name               | JU Email               | GitHub Username |
|--------------------|------------------------|-----------------|
| Albin Törnberg     | toal24ui@student.ju.se | Altornberg      |
| Vasilis Segersköld | phva23yl@student.ju.se | Glimba          |
| Simon Rignell      | risi23vx@student.ju.se | llengiR         |
| Gresa Hoxha        | hogr24bj@student.ju.se | hogr24bj        |
| Jafar Gohari       | goja23ll@student.ju.se | jafgo0          |
| Ellen Pennebratt   | peel24jb@student.ju.se | peel24jb        |

## Declaration

I, __Albin Törnberg__, declare that I am the sole author of the content I add to this repository.  
I, __Simon Rignell__, declare that I am the sole author of the content I add to this repository.  
I, __Vasilis Segersköld__, declare that I am the sole author of the content I add to this repository.  
I, __Gresa Hoxha__, declare that I am the sole author of the content I add to this repository.  
I, __Jafar Gohari__, declare that I am the sole author of the content I add to this repository.  
I, __Ellen Pennebratt__, declare that I am the sole author of the content I add to this repository.  


This project is developed as part of the __Mjukvaruutveckling__ course 2026, and follows the software-engeneering practices taught in the lectures.
