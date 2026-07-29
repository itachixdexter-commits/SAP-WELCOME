import discord
from discord.ext import commands
from discord import app_commands
import json
import os


# قراءة البيانات
try:
    with open("data.json", "r") as f:
        welcome_channels = json.load(f)
except:
    welcome_channels = {}


def save_data():
    with open("data.json", "w") as f:
        json.dump(welcome_channels, f, indent=4)


# إعداد البوت

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# تشغيل البوت

@bot.event
async def on_ready():

    await bot.tree.sync()

    print(
        f"تم تشغيل البوت {bot.user}"
    )


# أمر التفعيل

@bot.tree.command(
    name="up",
    description="تفعيل روم الترحيب"
)
async def up(interaction: discord.Interaction):

    guild = str(interaction.guild.id)

    welcome_channels[guild] = interaction.channel.id

    save_data()


    embed = discord.Embed(
        title="✅ تم التفعيل",
        description=
        "تم تشغيل نظام الترحيب في هذه الروم بنجاح 🔥",
        color=0x00ff99
    )


    await interaction.response.send_message(
        embed=embed
    )



# رسالة دخول العضو

@bot.event
async def on_member_join(member):

    guild_id = str(member.guild.id)


    if guild_id not in welcome_channels:
        return


    channel_id = welcome_channels[guild_id]


    channel = bot.get_channel(
        channel_id
    )


    if channel is None:
        return



    embed = discord.Embed(

        title=
        "🎉 عضو جديد وصل!",

        description=f"""

🔥 أهلاً وسهلاً بك {member.mention}

✨ نورت سيرفرنا الغالي

━━━━━━━━━━━━━━

👤 الاسم:
{member.name}

🌍 السيرفر:
{member.guild.name}

👥 عدد الأعضاء:
{member.guild.member_count}

━━━━━━━━━━━━━━

💎 نتمنى لك وقت ممتع معنا

📜 لا تنسى قراءة القوانين

🚀 استمتع وكن جزءاً من العائلة

        """,

        color=0x5865F2
    )


    embed.set_thumbnail(
        url=member.avatar.url
    )


    embed.set_footer(
        text=
        "Welcome System • Powered by Bot"
    )


    await channel.send(
        embed=embed
    )



# تشغيل

TOKEN = os.getenv(
    "TOKEN"
)


bot.run(TOKEN)
