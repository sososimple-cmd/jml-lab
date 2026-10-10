"""LEAVER: anyone terminated in HR loses their account and every department group.

This one is yours to build. The steps are below, in order. Look at joiner.py and
mover.py: you've already used every piece you need.
"""
from jml_common import hr_employees, ak_users, ak_set_active, ak_remove_from_group, user_groups

accounts = ak_users()

for emp in hr_employees():
    # TODO 4: skip anyone who is NOT terminated.  (emp["terminated"] is True or False)

    if not emp["terminated"]:
        continue

    # TODO 5: find their account with accounts.get(emp["email"]). If there isn't one, skip them.

    user = accounts.get(emp["email"])
    if user is None:
        continue
    # TODO 6: if their account is still active (user["is_active"]), turn it off:
    #         ak_set_active(user, False)
    
    if user["is_active"]:
        ak_set_active(user, False)

    # TODO 7: take away every group they're in. user_groups(user) lists them.

    for group in user_groups(user):
        ak_remove_from_group(user, group)

    pass

print("Leaver done.")
