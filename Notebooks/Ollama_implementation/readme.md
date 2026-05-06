# Ollama Implementation Guide

This guide explains how to take the merged model files produced by the merger notebook, convert them to GGUF with llama.cpp, and then load the GGUF model into Ollama from the terminal.

## Prerequisites

Before starting, make sure you have:

- The merged model folder produced by the merger notebook.
- The Hugging Face-style model files in that folder, especially `model.safetensors` or `model.safetensors.index.json`.
- A working Python environment.
- `git` and `python3` installed.
- Ollama installed on your machine.

## Step 1: Prepare the merged model output

The merger output should contain the model weights and tokenizer files in one directory, for example:

- `model.safetensors` or sharded `model-00001-of-000xx.safetensors`
- `config.json`
- tokenizer files such as `tokenizer.json`, `tokenizer.model`, or `tokenizer_config.json`
- copy the contents of `chat_template.jinja` and past it in `tokenizer_config.json` with key chat_template
    ```json
    {
        .
        .
        "chat_template": "content of chat_template.jinja"
        .
        .
    }
    ```

If the merged model was saved in Kaggle, download the full output directory first and copy it to your local machine.

## Step 2: Convert safetensors to GGUF with llama.cpp

Clone `llama.cpp` and install its Python dependencies:

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
python3 -m pip install -r requirements.txt
```

Run the converter on the merged model directory:

```bash
python3 convert_hf_to_gguf.py /path/to/merged-model --outfile /path/to/output/model.gguf
```

If your `llama.cpp` checkout uses the `convert_hf_to_gguf.py` script under a different path, run the equivalent converter from that repository location.

quantize the GGUF file after conversion. Example:

```bash
./llama-quantize /path/to/output/model.gguf /path/to/output/model.Q4_K_M.gguf Q4_K_M
```

Use the quantization format that best matches your hardware.

## Step 3: Create an Ollama model from the GGUF file

Create a `Modelfile` in the same folder as the GGUF file:

```text
FROM /path/to/output/model.gguf

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
```

Then create the Ollama model from the terminal:

```bash
ollama create my-merged-model -f Modelfile
```

This registers the model locally in Ollama under the name `my-merged-model`.

## Step 4: Run the model in Ollama

After creation, start a chat with the model:

```bash
ollama run my-merged-model
```

You can also list available models:

```bash
ollama list
```

## Example workflow

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
python3 -m pip install -r requirements.txt
python3 convert_hf_to_gguf.py /home/user/merged-model --outfile /home/user/merged-model/model.gguf

cd /home/user/merged-model
cat > Modelfile <<'EOF'
FROM /home/user/merged-model/model.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
EOF

ollama create my-merged-model -f Modelfile
ollama run my-merged-model
```

## Common issues

- If the converter cannot find the weights, confirm that you are pointing it at the merged model folder, not just the `.safetensors` file.
- If Ollama cannot load the model, check that the `FROM` path in the `Modelfile` points to the GGUF file.
- If the model is too large for your machine, use a quantized GGUF such as `Q4_K_M`.
- If the model output is unstable, adjust `temperature`, `top_p`, or `num_ctx` in the `Modelfile`.

## Notes

- The correct project name is `llama.cpp`, not `llama.ccp`.
- Ollama does not usually convert safetensors directly; the recommended flow is `safetensors -> GGUF -> Ollama model`.
