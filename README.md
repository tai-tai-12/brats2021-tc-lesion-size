# BraTS2021 TC Lesion Size Quantification

Reproducible **lesion-level size quantification** pipeline for BraTS2021 MRI segmentation masks.  
This project focuses on **Tumor Core (TC)** only — BraTS labels **{1, 4}** — excluding edema (label 2).  
Outputs include lesion volume (mm³), equivalent spherical diameter (mm), size-bin distribution, and summary statistics.

---

## Why this repo
This repository demonstrates an end-to-end data science workflow on real medical-imaging data:

- **Recursive data discovery** over nested folders
- **Lesion-level feature extraction** via 3D connected components (26-neighborhood)
- **CSV export → re-ingest** round-trip for reproducibility
- Explicit **data type management**
- Data **wrangling + size binning**
- **Visualization** and compact statistical summary

---

## Demo output (abridged)
```
cases=1245 lesions=3254 medianD=4.79 meanD=16.40 <10mm%=57.0 >=40mm%=16.8
```

---

## Requirements
- Python >= 3.8
- numpy
- pandas
- nibabel
- scikit-image
- matplotlib

Install dependencies:
```
pip install -r requirements.txt
```
---

## Data (BraTS2021)

BraTS2021 dataset is required but NOT included in this repository.

To obtain the data:
1. Go to the official BraTS 2021 release / Synapse platform.
2. Create an account and agree to the BraTS Data Usage Agreement (DUA).
3. Download the BraTS2021 Training Data (or Validation Data).
4. Unzip to a local folder.

Expected file pattern:
```
BRATS_ROOT/**/**_seg.nii.gz
```
Example folder layout:
```
D:\BraTS2021_Training_Data\
  BraTS2021_00000\
    BraTS2021_00000_seg.nii.gz
  BraTS2021_00001\
    BraTS2021_00001_seg.nii.gz
  ...
```
Please follow the official BraTS terms. Do not redistribute the dataset via this repo.

---

## Usage
1. Set your dataset root in the script:
```
ROOT = r"D:\BraTS2021_Training_Data"
```
2. Run:
```
python src/brats_tc_lesion_size.py
```

---

## What the script does
1. Loads segmentation masks (*_seg.nii.gz)
2. Extracts Tumor Core mask (labels 1 & 4)
3. Performs 3D connected components → lesion-wise measurement
4. Computes per-lesion:
   - voxel count
   - volume (mm³) using NIfTI voxel spacing
   - equivalent spherical diameter (mm)
5. Exports lesion table to CSV and re-ingests (round-trip reproducibility)
6. Bins lesions by diameter (2-mm bins up to 40 mm)
7. Plots size distribution and prints summary stats

---

## Outputs
Generated artifacts:
- brats_tc_lesions.csv — lesion-level table
- Bar plot of lesion size distribution
- Console summary:
  number of cases / lesions
  median & mean diameter
  small-lesion and large-lesion proportions

---

## Reproducibility notes
- All quantitative measurements use voxel spacing from each NIfTI header.
- Binning thresholds and connectivity are parameterized at the top of the script.
- The CSV round-trip demonstrates stable downstream analysis independent of in-memory objects.


---

## License
MIT License.


---

## Citation

If you use this pipeline, please cite:
- BraTS2021 dataset (official BraTS citation)
- This repository

