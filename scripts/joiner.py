"""JOINER: everyone active in HR gets an account and their department's group.

Most of this is written for you. Fill in the two TODO lines, click Save, then Run.
"""
from jml_common import hr_employees, ak_users, ak_create_user, ak_add_to_group, ak_set_active, dept_group

accounts = ak_users()

for emp in hr_employees():
    if emp["terminated"]:
        continue
    user = accounts.get(emp["email"])
    if user is not None:
        if not user["is_active"]:  # a rehire: HR brought them back, so turn the account back on
            print(f"Rehire: {emp['name']}")
            ak_set_active(user, True)
        continue  # already has an account
    print(f"New hire: {emp['name']} ({emp['department']})")

    # TODO 1: you write this. Create their account.
    # Replace None with a call to ak_create_user(emp)
    user = ak_create_user(emp)

    # TODO 2: you write this. Add them to their department's group.
    # Their group's name is dept_group(emp["department"]).
    # Use ak_add_to_group(user, <group name>)
    ak_add_to_group(user, dept_group(emp["department"]))

    if user is None:
        print("  (TODO 1 isn't done yet, so no account was created)")

print("Joiner done.")
