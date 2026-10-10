
"""
IAM Joiner Automation

Purpose:
Automate employee identity provisioning and account
reactivation using OrangeHRM and Authentik.

This script identifies active employees in the HR system,
creates identity accounts for new hires, and assigns
department-based access groups.

For rehired employees, existing disabled accounts are
reactivated. Department group reconciliation for returning
employees is handled separately by the Mover workflow.

Security Controls:
- HR-Driven Identity Provisioning
- Role-Based Access Control (RBAC)
- Department-Based Access Assignment
- Identity Lifecycle Management
- Account Reactivation
"""

from jml_common import (
    hr_employees,
    ak_users,
    ak_create_user,
    ak_add_to_group,
    ak_set_active,
    dept_group,
)

accounts = ak_users()

for emp in hr_employees():

    # Skip employees whose employment has been terminated.
    if emp["terminated"]:
        continue

    user = accounts.get(emp["email"])

    # Reactivate existing accounts for rehired employees.
    if user is not None:
        if not user["is_active"]:
            print(f"Rehire: {emp['name']}")
            ak_set_active(user, True)
        continue

    # Provision an identity for a new employee.
    print(f"New hire: {emp['name']} ({emp['department']})")
    user = ak_create_user(emp)

    # Assign the employee's HR-defined department group.
    ak_add_to_group(user, dept_group(emp["department"]))

print("Joiner done.")
