# Submission Checklist

## Required Files for Submission

### ✅ 1. Full Report (PDF or DOCX)
- [x] `report/main.tex` - LaTeX source
- [x] `report/main.pdf` - Compiled PDF report

### ✅ 2. All Code (Organized and Runnable)
- [x] All notebooks in `notebooks/Phase 1/`
- [x] All notebooks in `notebooks/Phase 1.5/`
- [x] All notebooks in `notebooks/Phase 2/`
- [x] Supporting Python files (e.g., `P2_00_5_parking_augment.py`)
- [x] Deployment code in `Deployment/` folder
- [x] Model checkpoints (best models only)

### ✅ 3. Model Outputs on Sample Inputs (5-10 examples)
- [x] SAM outputs: sam1.png - sam6.png (6 examples)
- [x] SSD output: SSD - Output image .png (1 example)
- [x] Faster R-CNN output: FRCNN - Output image .png (1 example)
- [x] Deployment interface screenshots (5 examples)
- **Total: 13 examples** ✅

### ✅ 4. Presentation Slides
- [ ] **TODO: Add presentation slides (.pptx or .ppt)**
- [ ] Place in project root or create `presentation/` folder

### ✅ 5. Dataset (if custom-made)
- [x] Dataset documentation included in report
- [x] Annotation format examples in notebooks
- [x] Dataset info files (if any)
- **Note:** Large dataset files are excluded (use .gitignore)

### ✅ 6. Agile Development Documentation
- [x] Sprint planning (`agile/sprint_planning.md`)
- [x] Agile summary (`agile/AGILE_SUMMARY.md`)
- [x] Burndown charts (4 charts)
- [x] Scrum board (`agile/scrum_board.png`)
- [x] Velocity chart
- [x] Team workload
- [x] Epic summary
- [x] Sprint timeline
- [x] Sprint summary
- [x] Team contributions chart

## Files Excluded (via .gitignore)

### Virtual Environments
- `.venv/`, `.venv_detr/`, `.venv_comparison/`

### Build Artifacts
- LaTeX build files (`.aux`, `.log`, `.toc`, etc.)
- Python cache (`__pycache__/`, `*.pyc`)

### Helper/Development Files
- Report generation scripts
- README files (except main README.md)
- Agile helper scripts
- Temporary files

### Large Data Files
- Raw dataset images
- Training outputs (`runs/`)
- All checkpoints (except best models in Deployment/)

### Deleted/Obsolete
- `notebooks/Tobedeleted/` folder

## Git Commands

### To add all required files:
```powershell
powershell -ExecutionPolicy Bypass -File git_add_submission.ps1
```

### To verify:
```bash
git status
```

### To create submission zip:
```powershell
# After committing, create zip excluding .git
# Or use: git archive -o submission.zip HEAD
```

## Important Notes

1. **Presentation Slides**: Make sure to add presentation slides before final submission
2. **Dataset**: Large dataset files are excluded. Include dataset documentation and format examples instead
3. **Checkpoints**: Only best models in `Deployment/checkpoints/` are included
4. **Report Images**: All images in `report/temp/` needed for LaTeX compilation are included
5. **Code Organization**: All notebooks and deployment code are organized and runnable

## Final Verification

Before submission, verify:
- [ ] Report PDF compiles correctly
- [ ] All notebooks are executable
- [ ] All model output images are present
- [ ] Presentation slides are included
- [ ] Agile documentation is complete
- [ ] No unnecessary files in submission
- [ ] All code is organized and documented


