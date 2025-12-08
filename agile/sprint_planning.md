# Sprint Planning Documentation

## Project Overview
**Project Name:** Parking Vision - Deep Learning Parking Space Detection  
**Team Size:** 5 members  
**Sprint Duration:** Variable (1 week sprints)  
**Total Sprints:** 3

## Team Members and Roles

- **Francis Cho** - Project Manager
  - SAM model training, results analysis, report writing assistance, model comparison

- **Hitakshi Chugh** - Scrum Master
  - YOLO implementation, model training, results analysis, report writing assistance, model comparison

- **Sugakabiyrarosha** - Lead Developer
  - Dataset exploration, CNN baseline development, SSD, DETR model training, results analysis, hyperparameter tuning, Main report writing, model comparison, Local model deployment for SSD and FRCNN

- **Alvis Chi Hin Ngan** - Developer
  - Data augmentation, Faster R-CNN implementation, hyperparameter tuning, report writing assistance, GPU Code running Assistance for Teammates

- **John Allan Ellingson** - Developer
  - YOLO implementation and Clustering pipeline, visualizations and statistical analyses, report writing assistance

---

## Sprint 1: Project Setup and Idea Finalization (Nov 16-23, 2025)
**Sprint Goal:** Finalize project idea and establish project foundation

### Sprint Backlog (13 Story Points)
- Project Setup and Idea Finalization (3 SP)
- Dataset Exploration and Analysis (5 SP)
- CNN Baseline Model Implementation (5 SP)

### Key Deliverables
- ✅ Project idea finalized (Parking Lot Detection)
- ✅ Development environment configured
- ✅ Dataset exploration completed with EDA
- ✅ CNN baseline model trained and evaluated

### Team Assignments
- **Francis Cho**: Project setup and idea finalization
- **Sugakabiyrarosha**: Dataset exploration, CNN baseline development

### Sprint Retrospective
**What went well:**
- Team successfully discussed multiple project ideas and finalized parking lot detection
- Successfully explored both Roboflow and HuggingFace datasets
- Established clear project structure
- CNN baseline provided good starting point

**Challenges:**
- Dataset format conversion complexity
- Initial environment setup coordination

**Action Items:**
- Standardize data loading pipeline
- Improve documentation for dataset formats

---

## Sprint 2: Phase 1 & Phase 1.5 Implementation (Nov 23-30, 2025)
**Sprint Goal:** Implement Phase 1 object detection models and Phase 1.5 SAM fine-tuning

### Sprint Backlog (55 Story Points)
**Phase 1 (37 SP):**
- SSD Model Training (8 SP)
- Faster R-CNN Model Training (8 SP)
- DETR Model Training (8 SP)
- YOLO Model Training (8 SP)
- Model Comparison and Evaluation (5 SP)

**Phase 1.5 (18 SP):**
- SAM Model Fine-tuning (8 SP)
- Image Alignment and Template Matching (5 SP)
- Training Data Clustering (5 SP)

### Key Deliverables
- ✅ Four object detection models trained (SSD, Faster R-CNN, DETR, YOLO)
- ✅ SAM model fine-tuned for parking segmentation
- ✅ Image alignment pipeline implemented
- ✅ Data clustering analysis completed
- ✅ Comprehensive model comparison report

### Team Assignments
- **Sugakabiyrarosha**: SSD, DETR model training, image alignment
- **Alvis Chi Hin Ngan**: Faster R-CNN implementation and training
- **Hitakshi Chugh**: YOLO implementation and training
- **Francis Cho**: SAM fine-tuning, model comparison
- **John Allan Ellingson**: Clustering pipeline, visualizations

### Sprint Retrospective
**What went well:**
- Successfully implemented all four detection architectures
- SAM fine-tuning improved segmentation accuracy
- Model comparison revealed clear performance differences
- YOLO showed best speed/accuracy balance
- Clustering approach identified stable parking space locations

**Challenges:**
- DETR training required significant computational resources
- Hyperparameter tuning was time-consuming
- Model evaluation metrics needed standardization
- SAM fine-tuning required careful prompt engineering

**Action Items:**
- Create standardized evaluation framework
- Document hyperparameter configurations
- Plan for Phase 2 improvements with augmentation

---

## Sprint 3: Phase 2, Deployment & Report (Dec 1-7, 2025)
**Sprint Goal:** Complete Phase 2 model optimization, deploy API, and finalize report

### Sprint Backlog (50 Story Points)
**Phase 2 (34 SP):**
- Data Augmentation Pipeline (8 SP)
- Augmented Dataset EDA (5 SP)
- SSD Phase 2 Training with Hyperparameter Tuning (8 SP)
- Faster R-CNN Phase 2 Training with Optimization (8 SP)
- DETR Phase 2 Training (8 SP)
- YOLO Phase 2 Training (8 SP)
- CNN Patch Classifier Implementation (5 SP)
- Phase 2 Model Comparison (5 SP)

**Deployment (13 SP):**
- API Development - FastAPI Backend (8 SP)
- Model Loader and Architecture Abstraction (5 SP)
- Inference Pipeline Implementation (5 SP)
- Docker Containerization (3 SP)
- Deployment Documentation (2 SP)

**Report (8 SP):**
- Main Report Writing (8 SP)
- Report Writing Assistance (5 SP)

### Key Deliverables
- ✅ Comprehensive data augmentation pipeline
- ✅ All models retrained with optimized hyperparameters
- ✅ CNN patch classifier implemented
- ✅ Phase 2 model comparison completed
- ✅ FastAPI backend with all endpoints
- ✅ Unified model loading system
- ✅ Single and batch inference pipelines
- ✅ Docker containerization
- ✅ Comprehensive deployment documentation
- ✅ Complete project report

### Team Assignments
- **Sugakabiyrarosha**: SSD/DETR Phase 2 training, hyperparameter tuning, API development, model deployment, main report writing
- **Alvis Chi Hin Ngan**: Data augmentation, Faster R-CNN Phase 2 optimization, GPU assistance
- **Hitakshi Chugh**: YOLO Phase 2 training, model comparison
- **Francis Cho**: Model comparison, results analysis, report assistance
- **John Allan Ellingson**: Augmented dataset EDA, visualizations, statistical analyses, report assistance

### Sprint Retrospective
**What went well:**
- Data augmentation significantly improved model robustness
- Hyperparameter tuning found optimal configurations
- All models showed improved performance in Phase 2
- FastAPI provided excellent API framework
- Model loader abstraction simplified deployment
- Docker containerization worked smoothly
- Team collaboration on report was effective

**Challenges:**
- Hyperparameter tuning was computationally expensive
- Augmentation pipeline needed careful validation
- Model comparison required extensive testing
- Report writing required coordination across team
- Tight timeline for final sprint

**Action Items:**
- Document optimal hyperparameters for each model
- Create augmentation validation pipeline
- Implement model caching for production
- Add API monitoring

---

## Overall Project Metrics

### Velocity Tracking
- Sprint 1: 13 SP completed
- Sprint 2: 55 SP completed
- Sprint 3: 50 SP completed
- **Total: 118 Story Points**

### Team Velocity
- Average: 39.3 SP per sprint
- Range: 13-55 SP

### Burndown Summary
- Initial backlog: 118 SP
- Completed: 118 SP
- Completion rate: 100%

### Sprint Duration
- Sprint 1: 1 week (Nov 16-23)
- Sprint 2: 1 week (Nov 23-30)
- Sprint 3: 1 week (Dec 1-7)
- **Total project duration: 3 weeks**

---

## Key Achievements
1. ✅ Implemented 5 different model architectures (CNN, SSD, Faster R-CNN, DETR, YOLO)
2. ✅ Fine-tuned SAM model for parking segmentation
3. ✅ Created comprehensive data augmentation pipeline
4. ✅ Achieved significant performance improvements in Phase 2
5. ✅ Developed production-ready API
6. ✅ Complete deployment infrastructure
7. ✅ Comprehensive project report

---

## Lessons Learned
1. **Early baseline establishment** was crucial for comparison
2. **Hyperparameter tuning** significantly improved results
3. **Data augmentation** was key to model robustness
4. **Unified model loader** simplified deployment
5. **Team collaboration** essential for tight timeline
6. **GPU resource sharing** (Alvis) helped team efficiency
7. **Comprehensive documentation** essential for reproducibility
8. **Agile methodology** helped manage rapid development

---

## Team Contributions Summary

### Francis Cho (Project Manager)
- Project planning and coordination
- SAM model fine-tuning
- Results analysis and model comparison
- Report writing assistance

### Hitakshi Chugh (Scrum Master)
- Scrum process management
- YOLO implementation and training (Phase 1 & 2)
- Results analysis
- Model comparison
- Report writing assistance

### Sugakabiyrarosha (Lead Developer)
- Dataset exploration and EDA
- CNN baseline development
- SSD and DETR model training (Phase 1 & 2)
- Hyperparameter tuning
- Main report writing
- Model comparison
- API development and deployment
- Local model deployment (SSD, Faster R-CNN)

### Alvis Chi Hin Ngan (Developer)
- Data augmentation pipeline
- Faster R-CNN implementation and training (Phase 1 & 2)
- Hyperparameter tuning
- GPU code running assistance for teammates
- Report writing assistance

### John Allan Ellingson (Developer)
- YOLO implementation support
- Clustering pipeline development
- Visualizations and statistical analyses
- Augmented dataset EDA
- Report writing assistance
