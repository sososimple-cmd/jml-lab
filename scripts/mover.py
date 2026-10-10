"""MOVER: when someone changes department, give the new group AND take the old one away.

This script already GIVES the new group. Run it after a transfer and look at the
person's groups in the HR vs Identity tab. Then fix TODO 3 so it also TAKES the
old group away.
"""
from jml_common import hr_employees, ak_users, ak_add_to_group, ak_remove_from_group, dept_group, user_groups

accounts = ak_users()

for emp in hr_employees():
    user = accounts.get(emp["email"])
    if emp["terminated"] or user is None:
        continue
    should_have = dept_group(emp["department"])
    has_now = user_groups(user)

    if should_have not in has_now:
        print(f"Mover: {emp['name']} is now in {emp['department']}")
        ak_add_to_group(user, should_have)

    # TODO 3: you write this. Take away every group they should NOT have anymore.
    # has_now is a list of their current group names. Loop over it, and for any
    # group that isn't should_have, call ak_remove_from_group(user, <that group>).
    for old in has_now:
        if old != should_have:
            ak_remove_from_group(user, old)


print("Mover done.")
