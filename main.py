from datetime import datetime

import sqlite3
import discord
from discord.ext import commands

conn = sqlite3.connect('main.db')
cursor = conn.cursor()



bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
	print("Bot Has been runned")
	for guild in bot.guilds:  # т.к. бот для одного сервера, то и цикл выводит один сервер
		print(guild.id)  # вывод id сервера
		for member in guild.members:  # цикл, обрабатывающий список участников
			cursor.execute(create_select_request('discord_id', 'discord_id', member.id))
			if not cursor.fetchone():
				sql = f"""
					INSERT INTO users (discord_id, join_date, is_old)
					VALUES (
						{member.id},
						
						{datetime.today().strftime("%m/%d/%y")},
						false
					);
				"""
				cursor.execute(sql)
			# else:
			# 	sql = f"""
			# 		UPDATE users
			# 		SET name = {member.display_name}#{member.discriminator}
			# 		WHERE discord_id = {member.id}
			# 	"""
			#
			# 	print(sql)
		conn.commit()  # применение изменений в БД


@bot.event
async def on_message(message):
	if message.content.startswith('!old'):
		user_id = message.author.id
		cursor.execute(create_select_request('join_date', 'discord_id', user_id))
		# print(cursor.fetchone()[0])
		date = cursor.fetchone()[0]

		d = datetime.strptime(date, '%m/%d/%y').date()
		# print(d, datetime.today().date())
		print(datetime.today().date() - d)

@bot.event
async def on_member_join(member):
	cursor.execute(create_select_request('discord_id', 'discord_id', member.id))

	if not cursor.fetchone():
		sql = f"""
			INSERT INTO users (discord_id, join_date, is_old)
			VALUES (
				{member.id},
				
				{datetime.today().strftime("%m/%d/%y")},
				false
			);
		"""
		cursor.execute(sql)
	# else:
	# 	sql = f"""
	# 		UPDATE users
	# 		SET name = {member.display_name}#{member.discriminator}
	# 		WHERE discord_id = {member.id}
	# 	"""

		# cursor.execute(sql)
	conn.commit()


def create_select_request(selector, field, value):
	sql = f"""
			SELECT {selector} 
			FROM users 
			WHERE {field}={value}
		"""
	return sql


# def shielding(value):
# 	if isinstance(value, str):
# 		if value.find('"'):
# 			return value.replace('"', '\\\"')
# 		if value.find("'"):
# 			return value.replace("'", "\\\'")
# 	return value


bot.run(TOKEN)
