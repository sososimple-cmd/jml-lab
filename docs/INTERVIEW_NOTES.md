# Interview talking points — IAM JML capstone

## 30-second version

> I completed a hands-on identity lifecycle capstone using OrangeHRM as the HR source and Authentik as the identity provider. I used Python scripts to provision new hires, update group access after department changes, disable terminated accounts, and reactivate a rehire. I also diagnosed an access-creep defect caused by a Python indentation error and fixed the mover logic so obsolete group membership was removed.

## 90-second walkthrough

**Situation:** HR made five staffing changes: two new hires, one transfer, one termination, and one rehire. Identity access needed to follow those changes.

**Task:** Predict which HR/identity mismatches would appear, run the correct automation, and reconcile the results with least-privilege principles.

**Action:** I used three Python scripts in a hosted IAM lab. The joiner handled new account provisioning and reactivation. The mover aligned department memberships. The leaver disabled terminated identities and removed groups. During testing, Illyana retained both X-Men and Defenders membership after transferring. I inspected `mover.py` and found that the removal loop was outside the employee loop. I corrected the indentation and retested.

**Result:** Illyana's outdated membership was removed. The exercise reinforced the importance of checking **actual entitlements**, not simply verifying that the new group was added. [Add your final verified dashboard count here.]

## Questions a hiring manager might ask

**Q: What was the HR source of truth?**  
**A:** OrangeHRM. The scripts used employee status, work email, and Sub Unit to decide which identity operations were required.

**Q: What is access creep?**  
**A:** The accumulation of access that is no longer appropriate after someone changes jobs or departments. In this lab, a transferred user kept the old X-Men group while receiving Defenders access.

**Q: Why does a rehire need both joiner and mover?**  
**A:** The joiner reactivates the existing account, but the former leaver process removed its groups. The mover restores current-department group membership.

**Q: Would this exact code be safe to run in production?**  
**A:** No, not without hardening. I would scope removals to IAM-managed group categories, add logging, retries, dry-run tests, review and approval controls, and API security measures.

**Q: Can you run the code from this GitHub repo by itself?**  
**A:** Not as-is. The lab relies on its provided `jml_common` utilities and hosted OrangeHRM/Authentik setup. The public repository is a portfolio record of the exercise and scripts I authored.

**Q: How does this translate to Entra ID or Okta?**  
**A:** The same core principles apply: HR-authoritative attributes, account provisioning and deprovisioning, department entitlements, rehires, access reconciliation, and auditing. I would learn and adapt the vendor-specific APIs and workflow tools rather than claim this lab used them directly.
