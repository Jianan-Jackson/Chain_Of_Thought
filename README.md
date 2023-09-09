# CoT Hackathon Project

* GPT as CPU
* Context window as RAM
* Chain-of-Thought as call stack

# Install

Create new virtual environment called venv by

```
python -m venv venv
```

On Macos, enter this new venv by

```
source venv/Scripts/activate
```

On Windows, enter by

```
venv\Scripts\activate
```

Then run

```
pip install -r requirements.txt
```

You also need to create a file called `config.py` under the same directory as `requirements.txt` that contians the following content:

```
import os
os.environ['OPENAI_API_KEY'] = '<YOUR_OPENAI_API_KEY>'
```

Swap out that place with your openai api. You can now run this project with

```
python app.py
```

