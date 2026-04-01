Hyperparameter Optimization (HPO) for LLaMA-2-7B Fine-Tuning

This repository implements automated hyperparameter optimization (HPO) for fine-tuning LLaMA-2-7B Chat on Python code generation tasks using QLoRA and Optuna.

🚀 Overview
The goal of this module is to identify optimal training configurations that minimize validation loss while maintaining efficient GPU memory usage.

We combine:

QLoRA (4-bit NF4 quantization) → memory-efficient fine-tuning
LoRA adapters → parameter-efficient training
Optuna (TPE sampler) → intelligent hyperparameter search
Hugging Face Trainer → scalable training pipeline
⚙️ Optimization Strategy
Search Algorithm
Sampler: Tree-structured Parzen Estimator (TPE)
Multivariate Sampling: Enabled
Reproducibility: Fixed seed (42)
Pruning Strategy
Pruner: Median Pruner
Startup Trials: 5
Warmup Steps: 1

This allows early stopping of poorly performing trials to save compute.

🔍 Search Space

The following hyperparameters are optimized:

Parameter	Range / Options
Learning Rate	8e-6 → 3e-5 (log scale)
Scheduler	linear, cosine, cosine_with_restarts
LoRA Rank (r)	8, 16, 32
LoRA Alpha	8, 16, 32
LoRA Dropout	0.05 → 0.15
Batch Size	4, 8, 16
Warmup Ratio	0.03 → 0.15
🧠 Key Techniques
1. QLoRA (4-bit Fine-Tuning)
Quantization type: NF4
Double quantization: Enabled
Compute dtype: FP16 / BF16

💡 Reduces memory usage from ~16GB → ~5GB

2. Instruction Masking (SFT)
Prompt tokens → masked with -100
Code tokens → contribute to loss

This ensures:

Focus on code generation quality
Avoids learning irrelevant prompt structure
3. Dataset Subsampling

To speed up HPO:

Training subset: 5% of full train dataset
Validation split: 20%

This significantly reduces optimization time while preserving signal.

4. Robust Trial Handling

Each trial includes:

GPU memory cleanup (torch.cuda.empty_cache)
Exception handling for crashes
NaN / Inf loss checks

Failed trials are safely discarded.

🔄 Optimization Pipeline
Load dataset
Shuffle and create subset
Train/validation split
Apply tokenization with masking
Load quantized LLaMA-2-7B
Apply LoRA adapters
Train model
Evaluate on validation set
Return validation loss to Optuna
Repeat for multiple trials


Lower validation loss indicates better generalization.

📈 Output

After optimization:

Best hyperparameters are printed
Saved to: best_params.json

Each trial stored in:

./optuna_results/trial_{n}
🧪 Running the Optimization
python train_optuna.py
📌 Best Practices
Use small subset for HPO → full dataset for final training
Keep batch size consistent with GPU memory
Monitor for overfitting (train vs validation loss)
Avoid too large LoRA rank unless necessary
🧾 Example Output
========== BEST TRIAL ==========
Value: 1.8421

Params:
learning_rate: 2.91e-5
lr_scheduler: cosine
lora_r: 8
lora_alpha: 32
lora_dropout: 0.0961
batch_size: 4
warmup_ratio: 0.069
🔑 Key Takeaways
Optuna + QLoRA enables efficient large-model tuning
Smart pruning drastically reduces compute cost
Proper masking significantly improves code generation
Small dataset subsets are effective for HPO