# symscribe
A repository for transcribing audio files using Whisper. It provides guidelines for creating chapters at logical topic transitions, with concise headings and respect for timestamps. It performs transcription and export the results as `chapters.csv` and `transcript.csv` files.

## Installation
1. Install `symbolicai`
```bash
pip install symbolicai[whisper]
```
2. Use the builtin `sympkg` to install the package
```bash
sympkg i ExtensityAI/symscribe
```
3. Create an alias for the `symscribe` command
```bash
symrun c symscribe ExtensityAI/symscribe
```
## Usage
Supported features:
- Whisper models: all models supported by `symbolicai` (default: `"base"`)
  - To change the model, before you run the `symscribe` do `export SPEECH_ENGINE_MODEL="..."`, where `...` is the model name ([available](https://github.com/openai/whisper#available-models-and-languages)).
- Language: `"language=..."` (default: `"language=en"`)
- Export directory: `"export_dir=..."` (default: `"export_dir=."`)
- Bin size: `"bin_size_s=..."` (default: `"bin_size_s=300"`)
  - The bin size is the duration of each audio file in seconds when splitting the audio file into smaller chunks.

Example:
```bash
symrun symscribe "path_to_file.mp3/mp4/..." "language=en" "export_dir=/tmp" "bin_size_s=300"

