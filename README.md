# EpFindr (a small dashboard interface to imdb)
This app is a visualizes the ratings of diffrent episodes for any show, using IMDbPY. 

# Why?
Say you're stuck in a lockdown and you're feeling nostalgic for an old show buut, you don't want to rewatch the whole thing.
You remember some good episodes but cant really place which season that was in. 

If this at all describes you then this app could be handy! It will essentially interface with IMDb to fetch all of the ratings
for a show, then graph it- making it obvious what episode you're looking for. 


## How to run locally 
1. start a fresh python env with version 3.7+  
2. install requirements with ```pip install -r requirements.txt``` 
3. finally, within that environment, use ```python app.py``` to launch the app 
4. navigate to http://127.0.0.1:8050 in your favorite browser 

# Future improvements
- finish styling! (colours and alignment)
- improve UX/UI (I dont like the input -> dropdown selection but it's easy to implement)
- handle more edge-cases (need more testing)
- show some more interesting data (maybe histograms of ratings/seasons?)
- add year to labels in dropdown so the selection is more obvious 
