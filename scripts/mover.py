
"""
IAM Mover Automation

Purpose:
Synchronize employee department-based access between
OrangeHRM and Authentik.

This script identifies department changes, assigns the
appropriate access group, and removes outdated department
memberships to enforce least-privilege access.

Security Controls:
- Role-Based Access Control (RBAC)
- Least-Privilege Enforcement
- Access-Creep Prevention
- HR-Driven Identity Reconciliation
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

    # Reconcile group memberships with the HR department.
    # Remove outdated access to prevent privilege creep.
    
    for old in has_now:
        if old != should_have:
            ak_remove_from_group(user, old)


print("Mover done.")
