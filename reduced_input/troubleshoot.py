import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

old_path = "/Users/ziyang/Documents/GitHub/MLDA-Lifeline-2025-Webapp/reduced_input/ctg_best_pipeline_XGB.joblib"

model = joblib.load(old_path)
print(f"Loaded trained model: {old_path}")

keep_cols = [
    "LB", "AC", "FM", "UC", "ASTV", "MSTV", "ALTV", "MLTV",
    "DL", "DS", "DP", "Width", "Mode", "Mean", "Median",
    "Variance", "Tendency"
]

prep: ColumnTransformer = model.named_steps["prep"]
new_transformers = []

for name, trans, cols in prep.transformers_:
    kept_cols = [c for c in cols if c in keep_cols]
    if kept_cols:
        new_transformers.append((name, trans, kept_cols))

new_prep = ColumnTransformer(transformers=new_transformers, remainder="drop")

clf = model.named_steps["clf"]
reduced_model = Pipeline([
    ("prep", new_prep),
    ("clf", clf)
])

new_path = "ctg_best_pipeline_XGB_reduced.joblib"
joblib.dump(reduced_model, new_path)

print(f"Saved reduced model as {new_path}")
print(f"Model now expects only these {len(keep_cols)} features:")
print(keep_cols)
