![image](https://github.com/dspcad/systems-puzzle_wu/blob/master/blockdiagram.png)

The block diagram is based on my understanding of the Puzzle details and ```docker-compose.yml```. I consider ```Nginx``` as a gateway that can performs NAT so it plays the role of managing the requets from outside and responses from the application server. Thus, I think the bugs could be classified into two parts:

1. Networking managment of ```Nginx```, ```Flask``` and ```Postgres```.
2. Functionality of the application server and database.

First, I checked the setting of the ports and fixed their wrong mapping. At that time, I could see the form but it went wrong after I submitted the order. It is not easy for me to identify which part caused it so I decided to isolate Nginx and debug only the functionality of the application server and database. 

I created a new decoker-compose.yml that contains only ```Flask``` and ```Postgres``` (I name it as ```docker-compose.yml.debug```). I found the returned responsed was a list composed of the empty strings. Out of my curiosity, I turned on the debug mode and made the ```app.py``` return ```len(results)```. The value of ```len(results)``` increased as I submitted the form, which meaned the database worked well. 

After googling, I figured out how to extract the information. I made ```app.py``` return all the records displayed in plain text. So far, I though I fixed the bugs of the application server and database. I went back to include ```Nginx``` and found the response was not found. At that time, I was more confident that there was supposed be some bug in ```Nginx``` and then, I checked out ```conf.d/flaskapp.conf```. There were two seetings about ```proxy_set_header Host``` and I removed ```proxy_set_header Host $host;``` since I saw the URL of the response contained ```localhost%2clocalhost:8080```.

Now it works when I submit the form by returning the table that shows all the records.
