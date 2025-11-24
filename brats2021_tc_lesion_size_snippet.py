# brats2021_tc_lesion_size_snippet.py
# (opt) GitHub: https://github.com/yourname/yourrepo
# BraTS2021 TC lesion-level size quantification + CSV round-trip.

import os, glob, math
import numpy as np, pandas as pd, nibabel as nib, matplotlib.pyplot as plt
from skimage.measure import label, regionprops_table

ROOT=r"D:\BraTS2021_Training_Data"; SUF="_seg.nii.gz"
KEEP=(1,4); CONN=3; STEP=2.0; MAXMM=40.0

def find_seg(root=ROOT):  # own function
    return sorted(glob.glob(os.path.join(root,"**",f"*{SUF}"), recursive=True))

def scan_one(fp):         # own function + analysis
    img=nib.load(fp); seg=img.get_fdata().astype(np.int16)
    sx,sy,sz=map(abs,img.header.get_zooms()[:3]); vvol=sx*sy*sz
    m=np.isin(seg,KEEP);
    if not m.any(): return pd.DataFrame()
    cc=label(m,connectivity=CONN)
    p = regionprops_table(cc, properties=("label", "area", "centroid"))
    cid=os.path.basename(fp).replace(SUF,"")
    df=pd.DataFrame({"case_id":cid,
                     "lesion_label":p["label"].astype(int),
                     "voxel_count":p["area"].astype(int),
                     "volume_mm3":p["area"]*vvol})
    df["equiv_diameter_mm"]=(6*df["volume_mm3"]/math.pi)**(1/3)
    return df

def bin_sizes(df):        # own function + wrangling
    edges=list(np.arange(0,MAXMM+STEP,STEP))+[np.inf]
    labs=[f"[{int(edges[i])},{int(edges[i+1])})" for i in range(len(edges)-2)]+[f">={int(MAXMM)}"]
    df["SizeGroup"]=pd.cut(df["equiv_diameter_mm"],edges,labels=labs,right=False)
    return df, df["SizeGroup"].value_counts().reindex(labs,fill_value=0)

# ----- pipeline -----
lesions=pd.concat([scan_one(f) for f in find_seg()], ignore_index=True)

csv="brats_tc_lesions.csv"; lesions.to_csv(csv,index=False)  # ingest demo
df=pd.read_csv(csv)

df["case_id"]=df["case_id"].astype("category")              # dtype mgmt
df["lesion_label"]=df["lesion_label"].astype(int)
df["equiv_diameter_mm"]=pd.to_numeric(df["equiv_diameter_mm"],errors="coerce")
df=df.dropna(subset=["equiv_diameter_mm"])
df, bc=bin_sizes(df)

# ----- compact outputs -----
print(df.head(2).to_string(index=False))
kb=["[0,2)","[2,4)","[4,6)","[6,8)","[8,10)",">=40"]
print("key bins:", dict(bc.loc[kb]))
print(f"cases={df.case_id.nunique()} lesions={len(df)} "
      f"medianD={df.equiv_diameter_mm.median():.2f} meanD={df.equiv_diameter_mm.mean():.2f} "
      f"<10mm%={(df.equiv_diameter_mm<10).mean()*100:.1f} >=40mm%={(df.equiv_diameter_mm>=40).mean()*100:.1f}")

# ----- visualization -----
plt.figure(figsize=(8,2.6),dpi=120)
bc.plot(kind="bar"); plt.xlabel("Equiv diameter (mm)"); plt.ylabel("Count")
plt.title("BraTS2021 TC lesion size distribution"); plt.tight_layout(); plt.show()
