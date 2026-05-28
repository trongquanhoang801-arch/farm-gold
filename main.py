import os
import asyncio
import random
import discord
from discord.ext import commands
from keep_alive import keep_alive

prefix = "!"
intents = discord.Intents.all()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    case_insensitive=True,
    intents=intents,
    self_bot=True
)

farm_exp = False
TARGET_CHANNEL_ID = 1381302690335952988

@bot.event
async def on_ready():
    print(f'✅ Self-bot {bot.user} đã lên sóng thành công!')
    print(f'🎯 ID Kênh chỉ định farm EXP: {TARGET_CHANNEL_ID}')
    print(f'💡 Gõ {prefix}startexp hoặc {prefix}se trên Discord để bắt đầu cày.')

@bot.command(aliases=["se"])
async def startexp(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
        
    global farm_exp
    if farm_exp:
        print("⚠️ Luồng farm EXP hiện tại vốn đã đang chạy rồi!")
        return

    farm_exp = True
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    
    if not channel:
        print(f"❌ Không tìm thấy kênh với ID {TARGET_CHANNEL_ID}. Vui lòng kiểm tra lại ID hoặc quyền hạn của tài khoản!")
        farm_exp = False
        return

    emoji_list = [em for em in ctx.guild.emojis if not em.animated]

    print("===== 🔥 BẮT ĐẦU LUỒNG CÀY EXP =====")
    print(f"📦 Đã nạp thành công {len(emoji_list)} emoji tĩnh từ máy chủ.")

    if not emoji_list:
        print("⚠️ Máy chủ này không có emoji tĩnh nào. Luồng tự động chuyển sang gửi chữ mặc định để tránh lỗi.")

    while farm_exp:
        try:
            if emoji_list:
                so_luong = random.randint(1, 1)
                chosen = random.sample(emoji_list, so_luong)
                text = "".join(str(em) for em in chosen)
            else:
                text = f"farm exp {random.randint(100, 999)}"

            await channel.send(text)
            print(f"✨ [FARM EXP] Đã gửi: {text}", flush=True)
            
        except Exception as e:
            print(f"❌ [FARM EXP] Gặp lỗi khi gửi tin nhắn: {e}", flush=True)
          
        await asyncio.sleep(random.randint(60, 90))

@bot.command(aliases=["xe"])
async def stopexp(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
        
    global farm_exp
    farm_exp = False
    print("===== 🛑 ĐÃ DỪNG LUỒNG CÀY EXP =====", flush=True)

keep_alive()
try:
    bot.run(TOKEN, bot=False, reconnect=True)
except Exception as e:
    print(f"❌ Lỗi kết nối không thể khởi động Self-bot: {e}")
