import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from discord.ext import commands
import difflib
from recommendationKNN import predict_score
import json

knn_recommendations=json.load(open('KNN_recommendation.json'))


movies = pd.read_csv('movie recommendations/processedfinalfile.csv')


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def recommend_KNN(ctx,*args):
    print(ctx.author.id)
    moviename = ' '.join(args)

    print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {moviename}\nType: Title")

    await ctx.reply(f"Trying to look up the movie")
    
    print(f"Searched term : {moviename}")
    
    if moviename not in movies['original_title']:
        probable_movie_list=difflib.get_close_matches(moviename,movies['original_title'])
        print(probable_movie_list)
        await ctx.reply("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
    else:

        await ctx.channel.send("Is the movie you are searching for ? ")
        await ctx.send(moviename)

        print("search begins")
        await ctx.send('\n\n\n\n'+ predict_score(moviename) + '\n\n\n\n')
        print("search complete")

@bot.command()
async def rKNN(ctx,*args):
    print(ctx.author.id)
    moviename = ' '.join(args)

    print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {moviename}\nType: Title")

    await ctx.reply(f"Trying to look up the movie")
    
    print(f"Searched term : {moviename}")
    
    if moviename not in movies['original_title'].tolist():
        probable_movie_list=difflib.get_close_matches(moviename,movies['original_title'])
        print(probable_movie_list)
        await ctx.reply("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
	
    else:

        await ctx.channel.send("Is the movie you are searching for ? ")
        await ctx.send(moviename)
        
        print("search begins")
        await ctx.send('\n\n\n\n'+ predict_score(moviename) + '\n\n\n\n')
        print("search complete")


@bot.command()
async def rKNN_indexed(ctx,*args):
    print(ctx.author.id)
    moviename = ' '.join(args)

    print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {moviename}\nType: Title")

    await ctx.reply(f"Trying to look up the movie")
    
    print(f"Searched term : {moviename}")
    
    if moviename not in knn_recommendations.keys():
        probable_movie_list=difflib.get_close_matches(moviename,knn_recommendations.keys())
        print(probable_movie_list)
        await ctx.reply("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
	
    else:

        await ctx.channel.send("Is the movie you are searching for ? ")
        await ctx.send(moviename)

        outputtext='Here are the recommendations :'
        movielist=knn_recommendations[moviename]
        for nameofmovie in movielist:
          outputtext=outputtext+'\n' + nameofmovie

        print("search begins")
        await ctx.send('\n\n\n\n'+ outputtext + '\n\n\n\n')
        print("search complete")

	
TOKEN = os.environ['DISCORD_BOT_SECRET']

bot.run(TOKEN)
