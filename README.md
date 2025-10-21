# llm_code_opt
C++ code optimization using LLMs 

# Prerequiremetns 
- WSL
- cmake
- python3.12
- Gemini API Key

# Set you API Key
Get an API key from: [text](https://aistudio.google.com/)
Setup your environment
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```


# Build C++ project
```bash
mkdir build
cd build
cmake ..
make
```

# Setup Python environent:
```bash
git clone https://github.com/katanim/llm_code_opt.git​
cd <llm_code_opt>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
