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

# TODO

* **Function Expansion**: everything that fits into Function.execute()). APIs calls are made in execute, and GPT-4 uses description to judge whether it wants to use a specific function. If yes, what parameter.
* **Retrieval Process**: Under indices.index.
* **Castaway**: Implementation based on 

If you'd like to play with HTTP request. I created this fake cafe server you could send post request to:

* `http://3.133.95.18/order` with form data key-value pair `input:<whatever text you'd like>`
* `http://3.133.95.18/clear` to clear out current shown on the website.

You can see the website at `http://3.133.95.18`
