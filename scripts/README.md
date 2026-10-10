# Python IAM Automation | Identity Lifecycle Management

**Technologies:** Python | Authentik | OrangeHRM | REST APIs | RBAC | Identity Lifecycle Management

## Project Overview

This project demonstrates hands-on Identity and Access Management (IAM) engineering through Python-based **Joiner-Mover-Leaver (JML) automation**.

Using OrangeHRM as the authoritative HR source and Authentik as the identity provider, I implemented, tested, and troubleshot identity lifecycle workflows that align employee accounts and access permissions with employment status and departmental assignments.

The project focuses on three critical IAM responsibilities:

- **Identity Provisioning:** Creating accounts and assigning appropriate access to new employees.
- **Access Management:** Updating permissions when employees transfer between departments.
- **Identity Deprovisioning:** Disabling accounts and revoking access when employees leave the organization.

A key accomplishment was identifying and resolving an **access-creep vulnerability** caused by incorrect Python control flow.

---

## 1. Joiner Automation — `joiner.py`

### Business Objective

Ensure new employees receive appropriate identity accounts and department-based access while supporting account reactivation for rehired employees.

### Technical Implementation

- Retrieved employee records from OrangeHRM.
- Identified employees without existing Authentik accounts.
- Provisioned new identities using Python automation.
- Assigned appropriate department-based groups.
- Reactivated disabled accounts for returning employees.

### Test Scenarios

| Employee | Department | Lifecycle Action |
|---|---|---|
| Sam Wilson | Avengers | New account provisioning |
| Carol Danvers | Cosmic Division | New account provisioning |
| Jessica Jones | Defenders | Identity reactivation |

**IAM Concepts:** Automated Provisioning, Birthright Access, HR-Driven Identity Management, Account Reactivation.

---

## 2. Mover Automation — `mover.py`

### Business Objective

Maintain least-privilege access by updating employee group memberships whenever departmental assignments change.

### Technical Implementation

- Compared employees' HR department assignments against Authentik group memberships.
- Added users to their required department groups.
- Removed outdated group memberships.
- Validated that access aligned with current departmental assignments.

### Security Finding: Access Creep

**Employee:** Illyana Rasputin

**Original Department:** X-Men

**New Department:** Defenders

During testing, I discovered an identity access discrepancy.

The employee retained membership in both `dept-x-men` and `dept-defenders` after transferring departments.

This represented an **access-creep risk**, where permissions from a previous department remained assigned after a role change.

### Root Cause Analysis

I investigated the Python mover automation and identified an indentation error that placed the group-removal loop outside the employee processing loop.

As a result, the automation failed to evaluate and remove outdated access for each applicable employee.

### Remediation

I corrected the Python loop structure and verified the logic responsible for identifying and removing unauthorized department group memberships.

The remediation involved:

1. Identifying existing group memberships.
2. Determining the required department group from HR records.
3. Comparing assigned groups against the expected group.
4. Removing outdated group memberships.
5. Rerunning the automation and validating the result.

### Validation Results

| Validation Check | Result |
|---|---|
| Correct department assigned | Defenders |
| Required group membership | `dept-defenders` |
| Outdated membership removed | `dept-x-men` |
| Access-creep finding | Resolved |

### Engineering Takeaway

This scenario reinforced the importance of validating both **access provisioning and access revocation** during employee transitions.

It also demonstrated how a Python control-flow error can result in excessive access privileges.

**IAM Concepts:** Least Privilege, RBAC, Access Creep, Identity Reconciliation, Root Cause Analysis, Security Troubleshooting.

---

## 3. Leaver Automation — `leaver.py`

### Business Objective

Reduce unauthorized access risks by automatically disabling accounts and removing access following employee termination.

### Technical Implementation

- Retrieved termination status from OrangeHRM.
- Identified terminated employees with active identity accounts.
- Disabled corresponding Authentik accounts.
- Removed department group memberships.
- Supported alignment between HR employment status and identity access.

### Test Scenario

| Employee | HR Event | Required Security Action |
|---|---|---|
| Billy Kaplan | Employment termination | Disable account and revoke department access |

**IAM Concepts:** Identity Deprovisioning, Offboarding, Access Revocation, Security Compliance.

---

## 4. Identity Reconciliation and Validation

The project used an IAM dashboard to identify discrepancies between HR employee records and corresponding identity accounts.

### Baseline Validation

**11 records | 0 findings**

### After HR Lifecycle Changes

**13 records | 3 findings**

The two newly hired employees appeared as awaiting accounts and were not counted as findings.

### Automation Workflow

1. Execute Joiner automation to provision new identities and reactivate rehired accounts.
2. Execute Mover automation to align department permissions and remove outdated access.
3. Execute Leaver automation to disable terminated accounts and revoke access.
4. Refresh the IAM dashboard to confirm successful reconciliation.

**Final validation target: 13 records | 0 findings.**

The project's final dashboard screenshot provides evidence of the completed reconciliation.

---

## 5. IAM Engineering Skills Demonstrated

| Technical Skill | Hands-On Application |
|---|---|
| Python Automation | Implementing and troubleshooting JML logic |
| Identity Provisioning | Creating new accounts |
| Identity Deprovisioning | Disabling accounts and removing access |
| RBAC | Managing department-based group membership |
| Least Privilege | Removing unnecessary permissions |
| Access Creep Remediation | Detecting and correcting excessive access |
| Troubleshooting | Identifying Python indentation and logic errors |
| Identity Reconciliation | Comparing HR records with identity state |
| Technical Documentation | Recording findings, remediation, and validation |

---

## 6. Engineering Improvements

For a production implementation, I would expand this solution with:

- Automated scheduling of identity synchronization.
- Structured audit logging and change tracking.
- Exception handling and retry mechanisms.
- Approval workflows for sensitive access changes.
- Automated unit and integration tests.
- Alerts for unresolved identity discrepancies.
- More granular entitlement management to ensure unrelated or privileged access groups are never removed unintentionally.

---

## 7. Project Environment and Scope

This hands-on engineering project was completed using a simulated enterprise IAM environment provided through the **All Things Identity IAM Career Launchpad**.

The original lab supplied portions of the Python framework and helper functions. My work included completing lifecycle automation exercises, executing and validating JML workflows, investigating identity discrepancies, and correcting the mover script's group-removal logic.

The scripts use the lab-provided `jml_common` module and are not standalone production deployments.

This repository documents practical IAM engineering experience gained through implementation, troubleshooting, testing, and validation.

---

## Project Summary

**Python-based IAM lifecycle automation integrating HR-driven identity provisioning, department-based access management, and account deprovisioning.**

**Key technical accomplishment:** Identified and corrected a Python automation defect that allowed outdated department access to remain assigned after an employee transfer.

[Return to Main IAM Automation Project](../README.md)
