Process to install db:

1) make the project

2) run in your internet client: http://localhost:8081/?pgsql=postgres

3) inside the first page:
  - select in system field: PostgresSQL
  - put in Server, Username and Database field: postgres
  - password field is: 1234
  - click on login

4) inside the database tool: You have to insert two specifics files in the right table target.
  - auth_user_db.csv(file) -> Auth_user(table)
  - twofa_db.csv(file) -> Twofa_usertwofa(table)

  To do this, there is a main menu on the right.
    1) Click on the target table (like Auth_user)
    2) Do <ctrl-f> "select data" - click
    3) Do <ctrl -f> "Import" - click
    4) Choose the right file in your own transcendence directory. (both files are in testing_db)

5) Now you have access to 6 users
  - username: "Guillaume" password: "g"
  - username: "Charles" password: "c"
  - username: "Jean" password: "j"
  - username: "Jimmy" password: "j"
  - username: "Valentin" password: "v"
  - username: "Thilbaut" password: "t"
