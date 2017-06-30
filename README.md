# killfeedOW
This program lets you have the killfeed of a match (or matches) from an Overwatch video. It needs python and opencv. The output, the actual killfeed, goes on the standard output as tuples with three elements. For example, if the killfeed is enemy Winston killing the friendly Genji, and then Mercy resurrecting the Genji, the output will be:
("winstonEN", "genjiFR", frame1)
("mercyFR", "genjiFR", frame2)
where frame1 and frame2 are the frames where each action is detected.

I've run the program with a video made by myself and on two videos from streamers, and there hasn't been errors on the output. If someone finds a problem on a video, please let me know.

### How to run

This program is used as "python killfeedOW video start end". Video is an overwatch video that must be on the same folder as the file killfeedOW.py . Start and end are optional arguments, they are integers and the program will search on the killfeed from the second "start" to the second "end". I have tested it with python 2.7.6.

### To do list

I'd like to save the nicks from the killfeed, but between the difficult of that task (template matching on letters of more than one font, I don't think is that hard, but is not easy either) and the value of the information, which in this case I don't know what could be used for, I'm not going to work on this right now.

I'm still thinking what to do with the data collected with this script, I'm open to ideas. Maybe a database that let you know what's the main counter of some hero (which one has the most eliminations on that hero), which targets GM Mercy's prioritize when resurrecting in comparation with Diamond Mercy's. It could be used on plenty of things, but each one needs a large database of videos collected. The main problem is how to collect that data. Some good references on that could be HSReplay and Hearthstone Deck Tracker of the Hearthstone community, they automatically save thousands of games just uploading each one when someones plays with the application open.


