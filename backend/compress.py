from joblib import load, dump

input_file = "ctg_best_pipeline_XGB.joblib"  
output_file = "model_compressed.joblib"

model = load(input_file)
dump(model, output_file, compress=3)

print("✅ Compression complete!")
