# Set up this GitHub portfolio project

This template is designed for your **existing `jml-lab` repository**. It is safe to use without overwriting your working Python scripts; the template deliberately contains **no** `joiner.py`, `mover.py`, or `leaver.py`.

## Method A — GitHub website (no command line)

1. Extract `jml-capstone-github-template.zip` on your computer.
2. Open your existing GitHub repository (or create a new one named `jml-lab`).
3. Open the extracted folder. **Upload the contents**, not an extra surrounding `jml-capstone-github-template/` folder.
4. In GitHub, select **Add file → Upload files**. Drag the `README.md`, `SETUP.md`, `.gitignore`, and the `docs/`, `screenshots/`, and `scripts/` folders into the upload area. If your browser does not preserve folders, use Method B or upload individual files into folders created via the GitHub interface.
5. Review and commit the new files. If GitHub asks about replacing an existing README, keep a copy of your original README first, then decide whether to merge it or use this one.
6. Upload your **actual** downloaded `joiner.py`, **corrected** `mover.py`, and `leaver.py` to the repository's **`scripts/` folder**.
7. Replace each matching screenshot placeholder with your own screenshot, **keeping the same filename** (for example, replace `screenshots/07-final-dashboard.png`).
8. Edit `docs/VALIDATION_LOG.md` to report the *actual* final row/finding count and outcome checks, then check off verified items in `README.md`.
9. Reopen the repository home page: GitHub renders `README.md` as the project landing page. Confirm the images display properly.

> NOTE: When uploading through the GitHub website, Windows may hide `.gitignore` from casual view because it starts with a dot. It can also be uploaded later or created directly from GitHub.

## Method B — Git on Windows (reliable for folders)

Prerequisite: Install Git for Windows, and sign into GitHub as usual.

Open **PowerShell** in a workspace folder:

```powershell
git clone https://github.com/YOUR_USERNAME/jml-lab.git
cd jml-lab
```

Extract the ZIP. Then copy **its contents** into this cloned `jml-lab` folder using File Explorer. **Do not overwrite your existing scripts.** If you already have a README, either back it up first or merge the sections you want.

Copy your three downloaded Python files into `jml-lab\scripts\`. Keep your corrected `mover.py`.

Commit your changes:

```powershell
git status
git add .
git commit -m "Document JML capstone and capture validation evidence"
git push
```

`git add .` includes only files not excluded by `.gitignore`; inspect `git status` before committing to ensure no sensitive material is staged.

## Screenshot replacement map

Most images in `screenshots/` say **PLACEHOLDER**, so nobody will mistake them for actual lab proof. The Illyana access-creep screenshot (`03-mover-finding.png`) is **already included from your screenshot**. Replace the remaining placeholders one by one without renaming:

| Filename | Replace with |
|---|---|
| `01-hr-changes-board.png` | HR vs Identity after the five HR updates, before scripts (if saved) |
| `02-joiner-output.png` | `joiner.py` successful Run output (if saved) |
| `03-mover-finding.png` | **Included: your actual Illyana `Wrong groups` screenshot** |
| `04-mover-code-fix.png` | Correct `mover.py` indentation / TODO 3 code |
| `05-mover-output.png` | `mover.py` successful Run output (if saved) |
| `06-leaver-output.png` | `leaver.py` Run output (if saved) |
| `07-final-dashboard.png` | Final HR vs Identity dashboard, with zero findings |

If you didn't save an earlier screenshot, **do not fabricate one or alter the lab to recreate the error**. Keep the placeholder explicitly marked as missing, or remove that image/link from the README and describe the observed behavior in text.

## Before publishing

- Make sure the script files came from **your own Lab 1 implementation** rather than an instructor-only example.
- Remove tokens, passwords, private endpoints, secrets, session cookies, and unneeded real employee information from code and screenshots.
- Confirm the instructor's lab terms allow public sharing of your completed code and screenshots.
- Remember these scripts import lab-provided `jml_common`, so they are **not** standalone production code.
- Confirm the actual reconciliation count in `docs/VALIDATION_LOG.md`.
