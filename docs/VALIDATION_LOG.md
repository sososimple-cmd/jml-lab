
# IAM Lifecycle Automation — Validation Log

**Validation Date:** October 10, 2026

**Environment:** Simulated Enterprise IAM Environment

**Technologies:** Python | OrangeHRM | Authentik | RBAC

**Project:** HR-Driven Identity Lifecycle Automation

---

## Validation Overview

This document records the expected and observed results of Python-based Joiner-Mover-Leaver (JML) automation.

Validation was performed by comparing employee records in OrangeHRM against identity accounts and department group memberships in Authentik.

**Objective:** Ensure that identity accounts, employment status, and department-based access remain synchronized with the authoritative HR source.

---

## Test Execution Results

| Validation Checkpoint | Expected Result | Observed Result | Status |
|---|---|---|---|
| Initial baseline | 11 records, 0 findings | 11 records, 0 findings | PASS |
| After HR changes | 13 records, 3 findings | 13 records, 3 findings | PASS — Expected discrepancies detected |
| Joiner automation | New hires provisioned; rehire enabled | Sam and Carol provisioned; Jessica reactivated | PASS |
| Mover automation | Correct groups assigned; outdated groups removed | Illyana's old access removed after Python fix; Jessica's access restored | PASS |
| Leaver automation | Terminated account disabled; groups removed | Billy's account disabled; department groups removed | PASS |
| Final reconciliation | 13 records, 0 findings | 13 records, 0 findings | PASS |

---

## 1. Baseline Validation

**Expected:** 11 employee records with zero identity findings.

**Observed:** 11 records, 0 findings.

**Result:** PASS

The initial dashboard confirmed that employee status and department access were synchronized between OrangeHRM and Authentik.

[View Baseline Dashboard Evidence](https://github.com/user-attachments/assets/c34edf0b-f38e-4375-9d01-80f7397fa227)

---

## 2. HR Lifecycle Changes

**Expected:** 13 records, 3 findings.

**Observed:** 13 records, 3 findings.

**Result:** PASS — Expected discrepancies detected

Five HR lifecycle events were introduced:

- Sam Wilson — New hire
- Carol Danvers — New hire
- Illyana Rasputin — Department transfer
- Billy Kaplan — Employment termination
- Jessica Jones — Rehire

The dashboard identified three counted discrepancies and two employees awaiting identity provisioning.

[View HR Changes Evidence](https://github.com/user-attachments/assets/338bdced-2a40-4828-804e-a0182c218939)

---

## 3. Joiner Automation Validation

**Script:** `joiner.py`

**Result:** PASS

### Observed Outcomes

- Sam Wilson's account was created and assigned `dept-avengers`.
- Carol Danvers's account was created and assigned `dept-cosmic-division`.
- Jessica Jones's disabled identity was reactivated.

The Joiner workflow successfully handled new account provisioning and identity reactivation.

[View Joiner Evidence](https://github.com/user-attachments/assets/8b192590-87e9-4840-bb88-412d6c210bc1)

---

## 4. Mover Automation Validation

**Script:** `mover.py`

**Result:** PASS after remediation


### Initial Security Finding

Illyana Rasputin transferred from X-Men to Defenders but retained access to both departments.

**Current Group Memberships:**
- `dept-x-men` — Outdated access
- `dept-defenders` — Required access

**Security Finding:** Access creep caused by retained membership in the previous department group.

**Expected Result:** Remove `dept-x-men` while preserving `dept-defenders`.


### Root Cause

An indentation error caused the old-group removal loop to execute outside the employee-processing loop.

### Corrective Action

Corrected the Python loop structure to evaluate each employee's group memberships and remove outdated department access.

### Verified Outcome

- Removed `dept-x-men`.
- Retained `dept-defenders`.
- Restored appropriate department access for Jessica Jones.
- Resolved the access-creep finding.

**Execution Output:**

```text
- illyana.rasputin removed from dept-x-men
Mover done.
```

[View Mover Remediation Evidence](https://github.com/user-attachments/assets/9d92dac1-cbd0-4e6f-86b7-c6ee973d76fc)

---

## 5. Leaver Automation Validation

**Script:** `leaver.py`

**Result:** PASS

### Observed Outcomes

- Billy Kaplan's account was disabled.
- Outdated department group membership was removed.
- HR termination status matched the identity account state.

[View Leaver Evidence](https://github.com/user-attachments/assets/8eebafda-75c5-4890-8e31-c6576075988f)

---

## 6. Final Identity Reconciliation

### Final Result: PASS

| Validation Metric | Final Result |
|---|---|
| Employee records | 13 |
| Outstanding IAM findings | 0 |
| New-hire provisioning | Successful |
| Department access changes | Successful |
| Access-creep remediation | Successful |
| Employee termination | Successful |
| Account reactivation | Successful |

The final HR vs Identity dashboard confirmed that all 13 employee records were reconciled with zero outstanding identity discrepancies.

[View Final Reconciliation Dashboard](https://github.com/user-attachments/assets/395f491a-7651-4f3a-8080-9cd518bf27c2)

---

## Validation Conclusion

**All defined JML lifecycle scenarios passed final validation following remediation of the Mover automation defect.**

This project demonstrated the ability to:

- Execute and validate Python IAM automation.
- Identify discrepancies between HR and identity systems.
- Troubleshoot Python control-flow errors.
- Remediate excessive department access.
- Verify identity provisioning and deprovisioning.
- Document test outcomes and supporting evidence.

**Final Status: 13 Records Reconciled | 0 Outstanding Findings**

---

[Return to Main Project README](../README.md)
