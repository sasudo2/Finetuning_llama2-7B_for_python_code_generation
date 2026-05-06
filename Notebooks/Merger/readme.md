# Merger Notebook

This notebook merges a LoRA adapter into a base causal language model and saves the merged model to Kaggle working storage.

## What it does

The notebook performs these steps:

1. Loads your Hugging Face token from Kaggle Secrets.
2. Downloads the base model.
3. Loads the LoRA adapter with PEFT.
4. Merges the adapter weights into the base model.
5. Saves the merged model and tokenizer to `/kaggle/working/`.

## Requirements

- A Kaggle notebook environment.
- Access to the Hugging Face model you want to merge.
- A Kaggle Secret named `huggingface_token`.
- A trained LoRA adapter folder containing the adapter weights, such as `adapter_model.safetensors`. Download adapter from https://huggingface.co/pradip777/llama-2-PCG.

## Before you run it

Update these values in the notebook:

- `base_model_id`: the base model you trained on, for example `meta-llama/Llama-2-7b-chat-hf`.
- `adapter_path`: the path to your saved adapter folder.

Make sure the adapter path points to the folder that contains the PEFT adapter files, not just a single file.

## How to use it

1. Open `merger.ipynb` in kaggle.
2. Run the first cell if you want to confirm the Kaggle input files.
4. Upload the adapter folder to notebook environment.
3. Set `base_model_id` and `adapter_path` in the merge cell.
4. Run the merge cell.
5. Wait for the model to finish loading and merging.
6. Check `/kaggle/working/` for the merged model and tokenizer files.

## Output

The notebook saves the result to:

- `/kaggle/working/`

Typical saved files include:

- model weights
- tokenizer files
- configuration files

## Notes

- The base model is loaded in `float16` with `device_map="auto"`, so a GPU runtime is recommended.
- If the base model is gated, your Hugging Face token must have access to it.
- After saving the merged model, you can download the `/kaggle/working/` output from Kaggle.

## Common issues

- If authentication fails, check that the Kaggle Secret is named exactly `huggingface_token`.
- If the merge fails, verify that `adapter_path` points to a valid PEFT adapter directory.
- If the model does not fit in memory, use a larger GPU runtime.
