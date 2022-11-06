import os
import overview_recommend
from discord.ext import commands

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

# Command to find recommended movie based on overview of the movies
@bot.command()
async def recommend_title(ctx, *args):

	# Joining the args to get movie name
	movie_name = ' '.join(args)
	print(movie_name)

	# User , Guild, Movie Name
	print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {movie_name}\nType: Title")

	if movie_name not in movie_titles:
		probable_movie_list = difflib.get_close_matches(movie_name,movie_list['original_title'])
		print(probable_movie_list)

		await ctx.reply("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again\n"+'\n'.join(probable_movie_list))
	else:
		# Writing logs of the command
		with open("logs.txt","a") as logs:
			logs.write(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {movie_name}\nType: Title")
		recommended_movies = overview_recommend.give_only_title(movie_name)
		
		print('\n'.join(recommended_movies))
		await ctx.send('\n'.join(recommended_movies))

@bot.command()
async def rt(ctx, *args):
	movie_name = ' '.join(args)
	print(movie_name)
	print(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {movie_name}\nType:Title_Score")
	if movie_name not in movie_titles:
		probable_movie_list = difflib.get_close_matches(movie_name,movie_list['original_title'])
		print(probable_movie_list)
		await ctx.reply("**Is the movie you wanted in one of these?**\nIf yes copy paste and use the command with this again"+'\n'.join(probable_movie_list))
	else:
		with open("logs.txt","a") as logs:
			logs.write(f"User: {ctx.author.name}\nGuild: {ctx.guild}\nMovie: {movie_name}\nType: Title_Score\n")

		recommended_movies = overview_recommend.give_title_score(movie_name)
		print('\n'.join(recommended_movies))
		await ctx.send('\n'.join(recommended_movies))


# Running the discord bot
token = os.environ["DISCORD_BOT_SECRET"]
bot.run(token)
