
# Identity Lifecycle Automation | Python, Authentik & OrangeHRM

**Hands-on IAM engineering project** · Joiner–Mover–Leaver (JML) · RBAC · HR-driven provisioning · Identity reconciliation

Developed, executed, and troubleshot Python-based identity lifecycle workflows in a **simulated enterprise IAM environment**. The project aligns employee status and department assignments in OrangeHRM with account status and group membership in Authentik. It covers hiring, internal transfers, termination, and rehire—including the investigation and remediation of an access-creep finding within the lab.

## Results at a glance

| Validation checkpoint | Employee records | IAM findings |
|---|---:|---:|
| Clean baseline | 11 | **0** |
| After five HR changes, before automation | 13 | **3** |
| After JML automation and remediation | **13** | **0** |

**Outcome:** Reconciled all 13 employee records with zero outstanding HR-to-identity findings. Identified and corrected a Python group-removal defect that allowed a transferred employee to retain access to a previous department.

## Environment and architecture

| Component | Function |
|---|---|
| **OrangeHRM** | Authoritative source for employee status, work email, and department (Sub Unit) |
| **Authentik** | Identity provider holding user accounts and department-based access groups |
| **Python** | Joiner, mover, and leaver workflows through lab-provided `jml_common` functions |
| **IAM Lab Dashboard** | Runs the scripts and compares HR records with identity account status and access |
| **WordPress** | Sample application configured to authenticate through Authentik; not directly modified in this project |

```mermaid
flowchart LR
    A[OrangeHRM HR records] --> B[IAM dashboard and Python JML scripts]
    B -->|Joiner: provision or reactivate| C[Authentik accounts]
    B -->|Mover: reconcile groups| D[Authentik department groups]
    B -->|Leaver: disable and revoke| C
    C --> E[HR vs identity validation]
    D --> E
    E --> B
```

Employees are matched using **work email**. Department group names derive from HR **Sub Unit** values. The workflows were executed manually through the hosted lab dashboard rather than deployed as scheduled production services.

## Business scenario: five lifecycle events

| Employee | HR change | Expected identity action | Automation |
|---|---|---|---|
| **Sam Wilson** | New hire — Avengers | Create account; assign `dept-avengers` | `joiner.py` |
| **Carol Danvers** | New hire — Cosmic Division | Create account; assign `dept-cosmic-division` | `joiner.py` |
| **Illyana Rasputin** | Transfer — X-Men → Defenders | Add `dept-defenders`; remove `dept-x-men` | `mover.py` |
| **Billy Kaplan** | Employment termination | Disable account and remove all group memberships | `leaver.py` |
| **Jessica Jones** | Rehire — Defenders | Reactivate existing account and restore `dept-defenders` | `joiner.py` + `mover.py` |

### Predicting the findings before running automation

Before executing scripts, I compared each HR change against the expected identity state. Two hires appeared as **No account yet**; three additional issues were counted by the lab dashboard as findings:

| Finding | Affected employee | Remediation |
|---|---|---|
| No account yet *(not counted as a finding)* | Sam Wilson | Joiner |
| No account yet *(not counted as a finding)* | Carol Danvers | Joiner |
| Wrong groups | Illyana Rasputin | Mover |
| Terminated but still active | Billy Kaplan | Leaver |
| Employed but account disabled | Jessica Jones | Joiner, then Mover |

### Evidence: before and after the HR changes

**Baseline — 11 records, 0 findings.** Before changing HR records, I confirmed that employee and identity states were synchronized.

<img src="https://github.com/user-attachments/assets/c34edf0b-f38e-4375-9d01-80f7397fa227" alt="IAM dashboard before HR changes showing 11 rows and zero findings" width="940" />

**After HR updates — 13 records, 3 findings.** The hires, transfer, termination, and rehire created the expected discrepancies before automation was executed.

<img src="https://github.com/user-attachments/assets/338bdced-2a40-4828-804e-a0182c218939" alt="IAM dashboard after HR changes showing 13 rows and three findings" width="940" />

### Employee profile evidence — OrangeHRM

The following screenshots document the **HR-side records and lifecycle actions** that drove the identity automation. They complement the IAM dashboard and script output; a profile screenshot alone does not verify provisioning or access revocation in Authentik.

<details>
<summary><strong>View employee profile evidence (7 screenshots)</strong></summary>

#### New hire — Sam Wilson

Sam's OrangeHRM job record shows his assigned **Avengers** subunit. The joiner workflow subsequently provisioned his identity and associated department access.

<img src="screenshots/08-sam-wilson-profile.png" alt="OrangeHRM job profile for Sam Wilson showing Avengers subunit" width="900" />

#### New hire — Carol Danvers

Carol's OrangeHRM job record shows **Cosmic Division**, the source department for her identity group assignment.

<img src="screenshots/09-carol-danvers-profile.png" alt="OrangeHRM job profile for Carol Danvers showing Cosmic Division subunit" width="900" />

#### Department transfer — Illyana Rasputin

Illyana's OrangeHRM job record shows her new **Defenders** subunit. Her access discrepancy and remediation are documented separately in the mover section.

<img src="screenshots/10-illyana-rasputin-profile.png" alt="OrangeHRM job profile for Illyana Rasputin showing Defenders subunit" width="900" />

#### Termination — Billy Kaplan

The termination dialog shows the selected effective date and reason before submission; the subsequent job profile confirms Billy's **Past Employee** status.

<img src="screenshots/13-billy-kaplan-termination-modal.png" alt="OrangeHRM Terminate Employment form for Billy Kaplan showing termination date and reason" width="900" />

<img src="screenshots/11-billy-kaplan-terminated-profile.png" alt="OrangeHRM job profile for Billy Kaplan showing Past Employee status and termination date" width="900" />

#### Rehire — Jessica Jones

Jessica's record initially shows **Past Employee** and the **Activate Employment** action. The second screenshot shows her job profile after reactivation, without the Past Employee label. Her Authentik account and group restoration are verified in the final reconciliation dashboard.

<img src="screenshots/12-jessica-jones-reactivation.png" alt="OrangeHRM job profile for Jessica Jones before rehire, with Past Employee status and Activate Employment button" width="900" />

<img src="screenshots/14-jessica-jones-active-profile.png" alt="OrangeHRM job profile for Jessica Jones after rehire, showing Defenders department without Past Employee status" width="900" />

</details>

## Automation implementation

### 1. Joiner — account provisioning and reactivation

**[`joiner.py`](scripts/joiner.py)** identifies active HR employees without an identity account, creates their Authentik accounts, and assigns the appropriate department group. For returning employees with disabled accounts, it restores account activation.

- Provisioned Sam Wilson with `dept-avengers`.
- Provisioned Carol Danvers with `dept-cosmic-division`.
- Reactivated Jessica Jones's previously disabled identity.

**Rehire consideration:** Re-enabling an existing account does not restore department groups removed at termination. The mover workflow reconciles the returning employee's access separately.

<details>
<summary>Joiner implementation and execution evidence</summary>

<img src="https://github.com/user-attachments/assets/c9268010-2e16-4c93-a76e-5e3187cac7c6" alt="Joiner Python script in the IAM lab editor" width="850" />

<img src="https://github.com/user-attachments/assets/8b192590-87e9-4840-bb88-412d6c210bc1" alt="Joiner workflow evidence from the IAM lab" width="850" />

</details>

### 2. Mover — least-privilege department access

**[`mover.py`](scripts/mover.py)** compares an employee's Authentik group membership with the department recorded in OrangeHRM. It grants the required department group and removes outdated access to reduce **access creep**.

#### Security finding: old department access retained

After Illyana Rasputin transferred to Defenders, her identity retained both the old and new department groups:

```text
HR Sub Unit:       Defenders
Current groups:    dept-x-men, dept-defenders
Required group:    dept-defenders
Dashboard finding: Wrong groups
```

![IAM dashboard finding showing Illyana assigned both X-Men and Defenders groups](screenshots/03-mover-finding.png)

*Figure 1 — Access creep: the identity retained access from a previous department.*

#### Root cause and remediation

I inspected the mover script and found that the `for old in has_now:` removal loop had been placed **outside** the employee-processing loop.

Consequently, old-group removal was not evaluated for each employee as intended. The workflow could assign the correct department group without properly removing outdated memberships.

I corrected the indentation, reran the script, and verified that `dept-x-men` was removed while `dept-defenders` remained assigned.

The relevant corrected logic is:

```python
# Within the employee-processing loop:
for old in has_now:
    if old != should_have:
        ak_remove_from_group(user, old)
```

**Observed remediation output:**

```text
- illyana.rasputin removed from dept-x-men
Mover done.
```

<img src="https://github.com/user-attachments/assets/9d92dac1-cbd0-4e6f-86b7-c6ee973d76fc" alt="Mover script remediation and execution evidence" width="850" />

*Figure 2 — Mover remediation evidence from the IAM lab.*

**Production design consideration:** The lab's group-removal logic assumes the reconciled memberships are department groups. In a production environment, the workflow should remove **only explicitly managed department groups**, preserving unrelated security, application, and privileged-access entitlements.

This restriction would reduce the risk of unintentionally revoking access outside the automation's authorized scope.

### 3. Leaver — account deactivation and access revocation

**[`leaver.py`](scripts/leaver.py)** identifies terminated employees in OrangeHRM, disables their corresponding Authentik accounts, and removes **all existing group memberships** from those accounts.

The current script iterates through the user's assigned groups and removes each membership rather than filtering exclusively for department groups.

This ensures the terminated identity no longer retains group-based access within the training environment.

In this scenario, Billy Kaplan's termination in OrangeHRM was reconciled with a disabled identity account and removal of his assigned group memberships in Authentik.

<details>
<summary>Leaver workflow evidence</summary>

<img src="https://github.com/user-attachments/assets/8eebafda-75c5-4890-8e31-c6576075988f" alt="Leaver automation evidence in the IAM lab" width="850" />

</details>

**Production security consideration:** This implementation demonstrates complete group removal in a controlled training environment.

In a production IAM environment, offboarding should follow an approved access-revocation policy. The automation should identify which entitlements it is authorized to manage, handle privileged or application-specific access according to established controls, and record all revocation actions for audit purposes.

Appropriate safeguards would help prevent unintended changes to unrelated entitlements while ensuring terminated employees no longer retain unauthorized access.

### 4. Rehire — coordinating account and access state

Jessica Jones's rehire required two separate actions:

1. **Joiner:** Re-enable her existing Authentik identity.
2. **Mover:** Reassign `dept-defenders`, since the prior termination had removed department memberships.

This case illustrates why **authentication account state** and **authorization/group membership** must be reconciled independently during a rehire.

Simply enabling an existing account does not guarantee that the employee has the correct permissions for their current role.

## Final validation

The final **HR vs Identity** dashboard confirmed all five lifecycle events were reconciled successfully:

| Employee | Verified state |
|---|---|
| Sam Wilson | Active; `dept-avengers` |
| Carol Danvers | Active; `dept-cosmic-division` |
| Illyana Rasputin | Active; `dept-defenders` only |
| Billy Kaplan | Terminated in HR; identity disabled; group memberships removed |
| Jessica Jones | Rehired and active; `dept-defenders` |

**Final result: 13 records · 0 findings.**

<img src="https://github.com/user-attachments/assets/395f491a-7651-4f3a-8080-9cd518bf27c2" alt="Final HR versus identity dashboard showing all 13 rows with zero findings" width="940" />

*Figure 3 — Final reconciliation: HR and Authentik agree on employee status and department access.*

## Engineering takeaways

- **Identity lifecycle changes must follow the authoritative HR record.** Hiring, transfers, terminations, and rehires have different effects on account and access state.
- **Adding the correct access is only half a mover workflow.** Removing prior department memberships is essential for least privilege and preventing access creep.
- **A successful script run is not the same as a correct security outcome.** Dashboard reconciliation and inspection of script output exposed the Python control-flow defect.
- **Root cause analysis matters in IAM engineering.** Investigating the underlying script logic helped identify why an employee retained access despite receiving the correct new department assignment.
- **Rehires may require multiple workflows.** Account activation and entitlement restoration are separate operations.
- **Access revocation requires appropriate boundaries.** Production automation should distinguish managed department groups from unrelated entitlements and apply approved offboarding controls.

## Production-oriented improvements

The current project uses manually executed scripts and lab-provided APIs. To strengthen a production implementation, I would add:

1. **Scheduled or event-driven reconciliation** to process HR changes promptly.
2. **Structured audit logging** with timestamps, identity identifiers, actions, and results—without exposing secrets.
3. **Scoped entitlement removal** limited to groups the automation is authorized to manage.
4. **Error handling and automated tests** for API failures, rehires, duplicate records, and unusual group assignments.
5. **Alerts and approvals** for unresolved identity discrepancies and higher-risk entitlements.

## Repository navigation

| Location | Contents |
|---|---|
| [`scripts/`](scripts/) | Joiner, mover, and leaver Python source files and script documentation |
| [`screenshots/`](screenshots/) | Lab evidence and screenshots |
| [`docs/VALIDATION_LOG.md`](docs/VALIDATION_LOG.md) | Validation record |

---

**Project context:** This capstone was completed through the *All Things Identity — IAM Career Launchpad* training environment. Employee information is fictional, and all workflows were implemented and tested in a simulated IAM environment. The scripts depend on lab-provided `jml_common` integration helpers and are not presented as independently deployable production services.

**Skills Demonstrated:** Python · IAM Lifecycle Management · RBAC · Least Privilege · Identity Provisioning & Deprovisioning · Access-Creep Remediation · Root Cause Analysis · Identity Reconciliation
