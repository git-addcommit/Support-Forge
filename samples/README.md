# Sample Files for File Reader Tool

This directory contains sample files that the **File Reader tool** can safely access.

## Files

- **README.md** (this file)
- **example.py** — Simple Python code sample
- **sample_data.json** — Example JSON data structure

## Adding More Samples

To add a new sample file:

```bash
echo "Your content here" > sample_name.txt
```

The file reader will:
1. List all files in this directory
2. Read any file < 1 MB
3. Display content in a code block

## Security Note

The File Reader tool is **sandboxed** to this directory only. It cannot:
- Read files outside `samples/`
- Follow symlinks
- Execute files
- Access system directories

This is intentional and tested.
