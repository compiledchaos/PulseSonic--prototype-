# PulseSonic-(prototype) 🎵  
Python-only prototype for PulseSonic.  
Built with PySide6 UI + Jamendo API backend.

## Features
- Search songs via Jamendo API  
- Stream audio from Jamendo
- Play audio locally

## Future Features
- Basic AI-powered recommendations  
- Offline downloads (SQLite)
- Playlists
- Favourites

## In Progress Features
- Login/Signup
- User info caching (SQLite)

## Tech Stack
- **UI**: PySide6  
- **Backend Logic**: Python (requests, SQLite, scikit-learn, SQLAlchemy)  
- **Playback**: VLC
- **Music Data**: Jamendo API  

## Getting Started
```bash
git clone https://github.com/yourusername/pulsesonic-(prototype)
cd pulsesonic-(prototype)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.core.main
