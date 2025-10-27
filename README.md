# llm_code_opt
C++ code optimization using LLMs 

# Prerequiremetns 
- WSL
- cmake
- python3.12
- Gemini API Key

# Set you API Key
Get an API key from: [Google AI Studio](https://aistudio.google.com/)

Setup your environment
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

# Setup Python environment:
```bash
git clone https://github.com/katanim/llm_code_opt.git​
cd llm_code_opt
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade setuptools
pip install -r requirements.txt
```

# Build C++ project
```bash
mkdir build
cd build
cmake ..
make
```


