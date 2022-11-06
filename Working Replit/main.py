import os
import pandas as pd
import overview_recommend
from discord.utils import get
from discord.ext import commands
import difflib
import json

knn_recommendations=json.load(open('KNN_recommendation.json'))

movie_list = pd.read_csv("preprocessed.csv")
movie_titles = movie_list['original_title'].tolist()

movie_genre_based = pd.read_csv("first_timer_score.csv")

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def recommend_genre(ctx,*genre):
	exception = difflib.get_close_matches(' '.join(genre),["Science Fiction","TV Movie"])

	if len(genre) == 1 or len(exception) :
		if  genre[0] not in movie_genre_based.columns:
			probable_genres = difflib.get_close_matches(genre[0],movie_genre_based.columns)
			try:
				genre = probable_genres[0]
			except:
				genre = '\0'
		else:
			genre = genre[0]
		if len(exception):
			genre = exception[0]
		try:
			if genre == "TV Movie":
				l = movie_genre_based[genre].to_list()[:-2]
				await ctx.send('\n'.join(l))
			else:
				await ctx.send('\n'.join(movie_genre_based[genre].to_list()))
		except:
			await ctx.send("**Genre not found**\nTry these genres\n```"+'\n'.join(movie_genre_based.columns[2:].to_list())+'```')
		
	else:
		return_message = "```The format of the command is\n!rg <genre_name>```"
		await ctx.send(return_message)

	
@bot.command()
async def rg(ctx,*genre):
	exception = difflib.get_close_matches(' '.join(genre),["Science Fiction","TV Movie"])
	if len(genre) == 1 or len(exception):
		if  genre[0] not in movie_genre_based.columns:
			probable_genres = difflib.get_close_matches(genre[0],movie_genre_based.columns)
			try:
				genre = probable_genres[0]
			except:
				genre = '\0'
		else:
			genre = genre[0]
		if len(exception):
			genre = exception[0]
		try:
			if genre == "TV Movie":
				l = movie_genre_based[genre].to_list()[:-2]
				await ctx.send('\n'.join(l))
			else:
				await ctx.send('\n'.join(movie_genre_based[genre].to_list()))
		except:
			await ctx.send("**Genre not found**\nTry these genres\n```"+'\n'.join(movie_genre_based.columns[2:].to_list())+'```')
		
	else:
		return_message = "```The format of the command is\n!rg <genre_name>```"
		await ctx.send(return_message)

@bot.command()
async def recommend_title(ctx, *args):

    global method
    method = "rt"
    # Joining the args to get movie name
    movie_name = ' '.join(args)
    print(movie_name)

    # User , Guild, Movie Name
    print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {movie_name}\nType: Title")
    
    if movie_name not in movie_titles:
        probable_movie_list = difflib.get_close_matches(movie_name,movie_list['original_title'])
        print(probable_movie_list)

        # Reply text to select emoji
        sent = await ctx.send("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
        emojis = ['1️⃣', '2️⃣', '3️⃣']
        msg =  await ctx.fetch_message(sent.id)
    for emoji in emojis[:len(probable_movie_list)]:
        await msg.add_reaction(emoji)
    else:
        recommended_movies = overview_recommend.give_only_title(movie_name)
        
        print('\n'.join(recommended_movies))
        await ctx.send('\n'.join(recommended_movies))

@bot.command()
async def rt(ctx, *args):
    global method
    method = "rt"
    movie_name = ' '.join(args)
    print(movie_name)
    print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {movie_name}\nType:Title_Score")
    if movie_name not in movie_titles:
        probable_movie_list = difflib.get_close_matches(movie_name,movie_list['original_title'])
        print(probable_movie_list)

        # Reply text to select emoji
        sent = await ctx.send("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
        emojis = ['1️⃣', '2️⃣', '3️⃣']
        msg =  await ctx.fetch_message(sent.id)
    for emoji in emojis[:len(probable_movie_list)]:
        await msg.add_reaction(emoji)
    else:
        recommended_movies = overview_recommend.give_title_score(movie_name)
        print('\n'.join(recommended_movies))
        await ctx.send('\n'.join(recommended_movies))


@bot.command()
async def rk(ctx,*args):
    global method
    method = "rk"
    print(ctx.author.id)
    moviename = ' '.join(args)

    print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {moviename}\nType: Title")
    await ctx.reply(f"Trying to look up the movie")
    
    print(f"Searched term : {moviename}")
    
    if moviename not in knn_recommendations.keys():
        probable_movie_list=difflib.get_close_matches(moviename,knn_recommendations.keys())
        print(probable_movie_list)
        sent = await ctx.send("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
        emojis = ['1️⃣', '2️⃣', '3️⃣']
        msg =  await ctx.fetch_message(sent.id)
        for emoji in emojis[:len(probable_movie_list)]:
            await msg.add_reaction(emoji)

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


@bot.command()
async def recommend_KNN(ctx,*args):
    global method
    method = "rk"
    print(ctx.author.id)
    moviename = ' '.join(args)

    print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {moviename}\nType: Title")

    await ctx.reply(f"Trying to look up the movie")
    
    print(f"Searched term : {moviename}")
    
    if moviename not in knn_recommendations.keys():
        probable_movie_list=difflib.get_close_matches(moviename,knn_recommendations.keys())
        print(probable_movie_list)
        sent = await ctx.send("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
        emojis = ['1️⃣', '2️⃣', '3️⃣']
        msg =  await ctx.fetch_message(sent.id)
        for emoji in emojis[:len(probable_movie_list)]:
            await msg.add_reaction(emoji)

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


@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name in ['1️⃣', '2️⃣', '3️⃣',':regional_indicator_a: ', ':regional_indicator_b:', ':regional_indicator_c:']:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)
        if reaction and reaction.count > 1:
            await message.delete()

@bot.event
async def on_reaction_add(reaction,user):
    global method
    if user == bot.user:
        return
    message1=reaction.message.content

    message=message1.split('\n')
	
    if(message[0]=='**Is the movie you wanted in one of these?**'):
        if str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣']:
            if str(reaction.emoji) == '1️⃣':
                moviename=message[2]
            elif str(reaction.emoji)=='2️⃣':
                moviename=message[3]
            elif str(reaction.emoji)=='3️⃣':
                moviename=message[4]
    else:
        return

    await reaction.message.channel.send("The movie you are searching for is")
    await reaction.message.channel.send('**'+moviename+'**')

    output='Here are the recommendations :'

    if method == "rk":
        movielist=knn_recommendations[moviename]
        output = '\n'+'\n'.join(movielist)

        print("search begins")
        await reaction.message.channel.send('\n\n\n\n'+ output + '\n\n\n\n')
        print("search complete")
    elif method == "rt":
        recommended_movies = overview_recommend.give_title_score(moviename)
        print('\n'.join(recommended_movies))
        await reaction.message.channel.send('\n'.join(recommended_movies))
        
token = os.environ["DISCORD_BOT_SECRET"]
bot.run(token)
