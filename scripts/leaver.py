
"""
IAM Leaver Automation

Purpose:
Automate employee offboarding by synchronizing
termination status between OrangeHRM and Authentik.

This script identifies terminated employees, disables
their existing identity accounts, and removes assigned
group memberships to prevent unauthorized access.

Security Controls:
- HR-Driven Identity Deprovisioning
- Account Deactivation
- Access Revocation
- Least-Privilege Enforcement
- Identity Lifecycle Management
"""

from jml_common import (
    hr_employees,
    ak_users,
    ak_set_active,
    ak_remove_from_group,
    user_groups,
)

accounts = ak_users()

for emp in hr_employees():

    # Process only terminated employees.
    if not emp["terminated"]:
        continue

    # Identify the employee's existing identity account.
    user = accounts.get(emp["email"])
    if user is None:
        continue

    # Disable active accounts for terminated employees.
    if user["is_active"]:
        ak_set_active(user, False)

    # Revoke all assigned group memberships.
    for group in user_groups(user):
        ak_remove_from_group(user, group)

print("Leaver done.")
