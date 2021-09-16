# Discord-Music-Bot

Recently at the time of writing Youtube has forced popular music bots such as the Rhythm bot to shut down.  
  
This repository contains code for my own music discord bot that can be privately hosted and used to play songs and audio from youtube on a discord server.

For this code to work you must have FFMPEG installed and added to your PATH on the machine you intend to run this code from.

## Commands
Below are the commands available for the discord music bot.

#### !join
This command is used to make the bot join a voice channel. The user must be in a voice channel for the bot to join.

#### !leave
This command will cause the bot to stop what is playing and leave the voice channel.

#### !play  
This command either takes a youtube URL as an argument and will then play that youtube videos audio in the voice channel, or it can take in a search term such as "Ed Sheeran new song" and will play the audio of the first song that comes up on youtube search. If a song is already playing when this command is run then it will be added to a queue.

#### !pause
Pauses the audio.

#### !resume
Resumes audio.

#### !skip
Skips the current song and plays the next song in the queue if the queue is not empty.

#### !queue
Displays the current song queue

#### !search
Takes in a search term as parameters such as "Rick Astley Songs" and will display the URLs for the first 5 results when the terms are searched for on youtube.
