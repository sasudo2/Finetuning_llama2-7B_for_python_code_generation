# LLaMA-2-7B Fine-Tuning for Python Code Generation (QLoRA + DDP)

This repository contains a distributed fine-tuning pipeline for **LLaMA-2-7B Chat** using **QLoRA (4-bit NF4 quantization)** for efficient training on Python code generation tasks.

---

## 🚀 Project Overview

The goal of this project is to fine-tune a large language model for **competitive programming and Python code generation** using:

- **Model:** LLaMA-2-7B-Chat
- **Technique:** QLoRA (Low-Rank Adaptation with 4-bit quantization)
- **Training Setup:** Distributed Data Parallel (DDP)
- **Experiment Tracking:** Weights & Biases (W&B)

---

## ⚙️ Training Configuration

### Model & Quantization
- **Base Model:** `meta-llama/Llama-2-7b-chat-hf`
- **Quantization:** 4-bit (NF4)
- **Double Quantization:** Enabled
- **Compute dtype:** FP16

### LoRA Parameters (Optimized via Optuna)
- **Rank (r):** 8  
- **Alpha:** 32  
- **Dropout:** 0.0961  

---

## 📊 Hyperparameters

| Parameter | Value |
|----------|------|
| Epochs | 2 |
| Batch Size | 4 |
| Gradient Accumulation | 4 |
| Learning Rate | 2.91e-5 |
| Max Sequence Length | 512 |
| Scheduler | Cosine |
| Warmup Ratio | 0.069 |

---

## 🧠 Key Features

### 1. Instruction Masking
Only the **completion (code)** contributes to loss:
- Prompt tokens → masked with `-100`
- Completion tokens → used for training

This ensures:
- Better code generation quality
- Reduced noise from instructions

---

### 2. Custom Data Collator
A specialized collator:
- Dynamically pads sequences
- Preserves label masking
- Ensures efficient batching

---

### 3. Distributed Training (DDP)
- Uses `LOCAL_RANK` for GPU assignment
- Scales efficiently across multiple GPUs

---

### 4. QLoRA Optimization
Memory-efficient fine-tuning:
- Reduces ~14GB → ~5GB VRAM usage
- Enables training large models on limited hardware

---

## 📂 Dataset

- **Format:** JSONL
- **Fields:**
  - `prompt`: Problem description / instruction
  - `code`: Target Python solution

### Splitting Strategy
- **Train:** 95%
- **Validation:** 5%

---

## 🔄 Training Pipeline

1. Load dataset
2. Shuffle and split
3. Apply preprocessing with masking
4. Tokenize input
5. Load quantized model
6. Apply LoRA adapters
7. Train using Hugging Face Trainer
8. Save model & tokenizer

---

## 📈 Experiment Tracking

- **Tool:** Weights & Biases (W&B)
- Logs:
  - Training loss
  - Evaluation loss
  - Learning rate schedule

---

## ☁️ Hugging Face Hub Integration

- Model is automatically pushed to: