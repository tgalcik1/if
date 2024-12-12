HOW TO RUN
Replace api_key.txt with your OpenAI API key
Create a virtual environment:
- `python -m venv venv`
- `venv\Scripts\activate` on Windows, or `source venv/bin/activate` on mac/linux
- `pip install openai`

To start dev server (and the game):
- `cd game-frontend`
- `npm install`
- `npm run electron:serve`