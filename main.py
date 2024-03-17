import os
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random
def replace_latex(text):
    with open('latex.txt', 'r') as file:
        latex_mapping = dict(line.strip().split() for line in file)
    for key, value in latex_mapping.items():
        text = text.replace(key, value)
    return text
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
client = commands.Bot(command_prefix="!", intents=intents)
@client.command(name="usaco")
async def usaco(ctx):
    while True:
        cpid = random.randint(84, 2000)
        url = f"https://usaco.org/index.php?page=viewproblem2&cpid={cpid}"
        response = requests.get(url)
        if response.status_code != 200:
            await ctx.send(f"Failed to retrieve the USACO webpage for cpid={cpid}. Trying again...")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        problem_div = soup.find('div', class_='problem-text')

        if problem_div:
            problem_nam = soup.find('div', class_='panel')
            await ctx.send(f"**{problem_nam.text}**")
            problem_text = problem_div.get_text(separator=' ')
            problem_text = replace_latex(problem_text)
            input_format_index = problem_text.find("INPUT FORMAT")
            if input_format_index != -1:
                problem_text = problem_text[:input_format_index].replace('\n', ' ') + problem_text[input_format_index:]
            problem_text = problem_text.replace('\n\n', ' ')
            problem_text = problem_text.replace('\n.out', '.out')
            problem_text = problem_text.replace('$', '')
            problem_text = problem_text.replace('\text', '')
            problem_text = problem_text.replace('\n:', ':')
            problem_text = problem_text.replace('  ', ' ')
            problem_text = problem_text.replace('  ', ' ')
            problem_text = problem_text.replace('SCORING:', '**SCORING**\n')
            problem_text = problem_text.replace('PROBLEM NAME', '\n**PROBLEM NAME**')
            problem_text = problem_text.replace('\n.', '')
            problem_text = problem_text.replace('(input arrives from the terminal / stdin):','')
            problem_text = problem_text.replace('(print output to the terminal / stdout):','')
            problem_text = problem_text.replace('INPUT FORMAT (input arrives from the terminal / stdin):', '\n\n**INPUT FORMAT**\n\n')
            problem_text = problem_text.replace('INPUT FORMAT:', '\n\n**INPUT FORMAT**\n\n')
            problem_text = problem_text.replace('INPUT FORMAT', '\n\n**INPUT FORMAT**\n\n')

            problem_text = problem_text.replace('OUTPUT FORMAT:', '\n\n**OUTPUT FORMAT**\n\n')
            problem_text = problem_text.replace('OUTPUT FORMAT', '\n\n**OUTPUT FORMAT**\n\n')

            problem_text = problem_text.replace(' SAMPLE INPUT:', '\n**SAMPLE INPUT**\n')
            problem_text = problem_text.replace(' SAMPLE OUTPUT:', '\n**SAMPLE OUTPUT**\n')
            chunk_size = 1900
            chunks = [chunk + '.' if '' not in chunk else chunk for chunk in problem_text.split('.')]

            current_chunk = ''
            for chunk in chunks:
                if len(current_chunk + chunk) <= chunk_size:
                    current_chunk += chunk
                else:
                    await ctx.send(current_chunk.strip())
                    current_chunk = chunk
            if current_chunk:
                await ctx.send(current_chunk.strip())
            return
        else:
            pass

@client.command(name="cf")
async def codeforces(ctx):
    max_attempts = 10000  # Set the maximum number of attempts for finding a valid problem

    for attempt in range(1, max_attempts + 1):
        # Generate a random contest number (adjust the range as needed)
        forbidden = [929]
        contest_num = random.randint(1, 2500)
        while contest_num in forbidden:
            contest_num = random.randint(1, 2500)
        # Generate a random problem index within the contest
        problem_index = random.randint(1, 7)

        # Construct the Codeforces problem URL
        url = f"https://codeforces.com/problemset/problem/{contest_num}/{chr(ord('A') + problem_index - 1)}"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            problem_div = soup.find('div', class_='ttypography')

            if problem_div:
                problem_text = problem_div.get_text(separator=' ')
                problem_text = replace_latex(problem_text)
                problem_text = "**​" + problem_text
                problem_text = problem_text.replace('​A', 'A. ')
                problem_text = problem_text.replace('​B', 'B. ')
                problem_text = problem_text.replace('​C', 'C. ')
                problem_text = problem_text.replace('​D', 'D. ')
                problem_text = problem_text.replace('​E', 'E. ')
                problem_text = problem_text.replace('​F', 'F. ')
                problem_text = problem_text.replace('$', '')
                problem_text = problem_text.replace('  ', ' ')
                problem_text = problem_text.replace('\n\n', '\n')
                problem_text = problem_text.replace('megabytes', 'megabytes\n')
                problem_text = problem_text.replace('time limit per test', '**\n**time limit per test:**')
                problem_text = problem_text.replace('memory limit per test', '\n**memory limit per test:**')
                problem_text = problem_text.replace('input standard input', '')
                problem_text = problem_text.replace('output standard output', '')
                problem_text = problem_text.replace(' Output', '\n**Output**\n')
                problem_text = problem_text.replace(' Input', '\n**Input**\n')

                # Check if "time limit per test" is present in the problem_text
                if 'time limit per test' not in problem_text:
                    continue  # Skip to the next iteration to generate a new problem

                # Chunk-sending logic
                chunk_size = 1900
                chunks = [chunk + '.' if '' not in chunk else chunk for chunk in problem_text.split('.')]

                current_chunk = ''
                for chunk in chunks:
                    if len(current_chunk + chunk) <= chunk_size:
                        current_chunk += chunk
                    else:
                        await ctx.send(current_chunk.strip())
                        current_chunk = chunk
                if current_chunk:
                    await ctx.send(current_chunk.strip())

                return  # Exit the function if a valid problem is found
            else:
                pass

    await ctx.send(f"Unable to find a valid problem after {max_attempts} attempts.")





@client.command(name="usacow")
async def cow(ctx, *params):
    eyes = "(oo)"  # Default eyes

    if params:
        # Check if a specific cow is requested and update eyes accordingly
        cow_names = ["Elsie", "Henrietta", "Gertie", "Daisy", "Annabelle", "Maggie"]
        name = params[0]
        if name in cow_names:
            eyes = {"Elsie": "(..)", "Henrietta": "(~~)", "Gertie": "(OO)", "Daisy": "(@@)", "Annabelle": "(##)", "Maggie": "(**)"}.get(name, eyes)
        else:
            name = "Bessie"
    else:
        name = "Bessie"

    greeting = f"Hi! I'm {name}."
    dashes = '-' * len(greeting)

    await ctx.send(f"""```
{greeting}
{dashes}
 \   ^__^
  \  {eyes} \\_______
     (__)\       )\\/\\
         ||----w |
         ||     ||

If you want your own cow, all you need is a dollar!
DM kl4659 for more info.
```""")




token = os.getenv("bot_token")
client.run(token)
#https://cses.fi/problemset/task/1068
