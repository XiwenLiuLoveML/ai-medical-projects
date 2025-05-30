"""
utils.py

This module provides utility functions for file traversal, token counting, singleton management,
and text processing for LLM-based document analysis systems.
"""

import os
import re
import tiktoken
from strenum import StrEnum
from config.path_conf import PROJECT_BASE

# Enum for LLM task types
class LLMType(StrEnum):
    CHAT = 'chat'
    EMBEDDING = 'embedding'
    SPEECH2TEXT = 'speech2text'
    IMAGE2TEXT = 'image2text'
    RERANK = 'rerank'
    TTS = 'tts'

# GPU check (if torch is installed)
try:
    import torch.cuda
    PARALLEL_DEVICES = torch.cuda.device_count()
except Exception:
    PARALLEL_DEVICES = None

# Base project directory for tokenizer cache
def get_project_base_directory(*args):
    global PROJECT_BASE
    if PROJECT_BASE is None:
        PROJECT_BASE = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
        )
    return os.path.join(PROJECT_BASE, *args) if args else PROJECT_BASE

# Walk through all files under a directory
def traversal_files(base):
    for root, _, fs in os.walk(base):
        for f in fs:
            yield os.path.join(root, f)

# Singleton factory (based on PID)
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        key = str(cls) + str(os.getpid())
        if key not in instances:
            instances[key] = cls(*args, **kw)
        return instances[key]
    return _singleton

# Remove extra space in text
def rmSpace(txt):
    txt = re.sub(r"([^a-z0-9.,\)>]) +([^ ])", r"\1\2", flags=re.IGNORECASE)
    return re.sub(r"([^ ]) +([^a-z0-9.,\(<])", r"\1\2", flags=re.IGNORECASE)

# Find max timestamp in a file (string-based)
def findMaxDt(fnm):
    m = "1970-01-01 00:00:00"
    try:
        with open(fnm, "r") as f:
            for line in f:
                line = line.strip()
                if line == 'nan':
                    continue
                if line > m:
                    m = line
    except Exception:
        pass
    return m

# Find max number in a file
def findMaxTm(fnm):
    m = 0
    try:
        with open(fnm, "r") as f:
            for line in f:
                line = line.strip()
                if line == 'nan':
                    continue
                m = max(m, int(line))
    except Exception:
        pass
    return m

# Tokenizer for LLM input handling
tiktoken_cache_dir = get_project_base_directory()
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir
encoder = tiktoken.get_encoding("cl100k_base")

# Count number of tokens in string
def num_tokens_from_string(string: str) -> int:
    try:
        return len(encoder.encode(string))
    except Exception:
        return 0

# Truncate string by max token length
def truncate(string: str, max_len: int) -> str:
    return encoder.decode(encoder.encode(string)[:max_len])

# Clean markdown block symbols
def clean_markdown_block(text):
    text = re.sub(r'^\s*```markdown\s*\n?', '', text)
    text = re.sub(r'\n?\s*```\s*$', '', text)
    return text.strip()

# Safely convert to float
def get_float(v):
    if v is None:
        return float('-inf')
    try:
        return float(v)
    except Exception:
        return float('-inf')
