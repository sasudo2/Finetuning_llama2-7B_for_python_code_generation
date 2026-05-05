# LLaMA-2-7B Fine-Tuning for Python Code Generation

This repository contains the minor project work for Thapathali College students. It demonstrates a complete fine-tuning pipeline for the **LLaMA-2-7B Chat** model on Python code generation tasks using **QLoRA** and **Optuna**.

## Huggingface repository for model
https://huggingface.co/pradip777/llama-2-PCG/tree/main

## Project Summary

- Fine-tune `meta-llama/Llama-2-7b-chat-hf` for competitive programming and Python code generation.
- Use QLoRA with 4-bit NF4 quantization to reduce memory requirements.
- Use Optuna to optimize LoRA and training hyperparameters.
- Maintain a dataset of cleaned Python coding instruction examples for training and validation.

## Repository Structure

- `Datasets/`
  - `refined_train.jsonl` — training dataset for fine-tuning
  - `refined_test.jsonl` — evaluation/test dataset
  - `optuna1 (1).db` — Optuna study database for HPO experiments
- `Documentation/`
  - `Data_preparation/` — dataset cleaning and classification documentation
  - `Fine_tuning/` — final fine-tuning pipeline documentation
  - `Hyperparameter Optimization/` — Optuna and HPO strategy documentation
- `Notebooks/`
  - `Data_preparation/` — data cleaning and preparation notebooks
  - `Fine_tuning/` — training notebook with QLoRA and model push examples
  - `HPO/` — hyperparameter tuning notebooks for Optuna experiments
  - `Evaluation/` - evaluation notebooks for final model
- `final_report/` — project report files and thesis documentation

## Key Components

### Data Preparation

- The dataset is derived from Alpaca-style Python instruction examples.
- Filtering is applied to keep high-quality competitive programming and algorithmic tasks.
- The data preparation documentation describes dataset sources, cleaning, and classification methodology.

### Fine-Tuning

- The main training pipeline uses a quantized LLaMA-2-7B model with LoRA adapters.
- Instruction masking ensures only generated code tokens contribute to the training loss.
- The workflow supports distributed training and Hugging Face Trainer integration.

### Hyperparameter Optimization

- Optuna is used to search for the best learning rate, scheduler, LoRA rank, alpha, dropout, batch size, and warmup ratio.
- A pruning strategy accelerates experiments by stopping poor trials early.
- The repository stores HPO results in the Optuna database inside `Datasets/`.

## How to Use

1. Review the documentation in `Documentation/`.
2. Open the notebooks in `Notebooks/` for data preparation, fine-tuning, and HPO.
3. Use `refined_train.jsonl` and `refined_test.jsonl` from `Datasets/` for training and validation.
4. Follow `Documentation/Hyperparameter Optimization/HPO.md` to tune the model.

## Notes

- The repository is primarily organized around notebooks and documentation.
- The dataset used for training is included locally in `Datasets/`.
- The project demonstrates efficient fine-tuning of a large model for Python code generation on constrained hardware.

## Recommended Next Steps

- Run `Notebooks/Fine_tuning/fine-tuning.ipynb` to reproduce training.
- Explore `Notebooks/HPO/hyperparameter-tuning (3).ipynb` and `Notebooks/HPO/hyperparameter-tuning (4).ipynb` for Optuna workflows.
- Read `Documentation/Fine_tuning/final_fine-tuning.md` for a full step-by-step training reference.
