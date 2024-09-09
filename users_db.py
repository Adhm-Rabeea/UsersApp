"""
Users Database App
"""

import sqlite3


input_message = """
What do you want to do ?
Users List => l
Add => a
Add by Id => abi
Delelt => d
Update => u
Search => s
"""

db = sqlite3.connect("Users.db")


cr = db.cursor()

cr.execute("create table if not exists Users (Id  intger, Name text)")

print("Program is opened enter q to quit")


while True:

    db.commit()  # Save changes

    cr.execute("select * from Users order by Id")

    process = input(input_message).lower().strip()  # input from user

    # close the program
    if process == "q":
        print("Program is closed")
        break

    # Addition
    if process in ("a", "abi"):

        # Default Add
        if process == "a":

            name_list = input("Enter Users => ").split(",")

            # Fetch Id to check
            cr.execute("select Id from Users")
            id_list = cr.fetchall()

            ls = []
            for i in id_list:
                ls.append(i[0])

            for user_id, user_name in enumerate(name_list, len(id_list) + 1):

                # Check Id
                if user_id not in ls:
                    cr.execute(
                        "insert into Users values(? , ?)",
                        (user_id, user_name.title().strip()),
                    )
                else:
                    user_id += 1
                    if user_id not in ls:
                        cr.execute(
                            "insert into Users values(? , ?)",
                            (user_id, user_name.title().strip()),
                        )
                    else:
                        cr.execute(
                            "insert into Users values(? , ?)",
                            (user_id + 1, user_name.title().strip()),
                        )
            print("Uesers added")

        # Add by Id
        elif process == "abi":
            name_list = input("Enter User Name And User Id => ").split(",")

            # Check Id
            cr.execute("select Id from Users")
            id_list = cr.fetchall()

            ls = []
            for i in id_list:
                ls.append(str(i[0]))

            if name_list[1] not in ls:
                cr.execute(
                    "insert into Users values(?,?)",
                    (name_list[1], name_list[0].title().strip()),
                )
                print("User is added")
            else:
                print("Sorry Id is used")

    # Delete
    elif process == "d":

        user_id = input("Enter User Id => ").split()
        for i in user_id:
            cr.execute("delete from Users where Id = ?", (i,))
        print("User Deleted")

    # Update
    elif process == "u":
        user_id = input("Enter User Id => ")
        new_name = input("Enter new name => ")

        cr.execute(
            f"update Users set Name = ? where Id = ?",
            (new_name.title().strip(), user_id),
        )
        print("User Updated")

    # Print Users list
    elif process == "l":

        users_list = cr.fetchall()

        print(f"Id | Name | Count: {len(users_list)}")
        print("=" * 20)

        for user in users_list:
            print(f"{user[0]}  |  {user[1]}")

    # Search
    elif process == "s":

        name = input("Enter Name to search => ").strip().title()

        s = cr.execute("select * from Users WHERE Name = ?", name)
        # s = cr.execute(f"select * from  Users where SUBSTR(Name, 1,1) = 'A'")
        ls = s.fetchall()
        # print(ls)

        if ls != []:
            print(f"Name: {ls[0][1]}")
            print(f"Id: {ls[0][0]}")

        else:
            print("Soryy, Name not found")

    else:
        print("Error!")
        print("Please select the correct process")


db.commit()
db.close()
