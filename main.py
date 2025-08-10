from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.text import Text
import os, time

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console()

def chat_with_chad(prompt):
    system_message = """You are a Pilot AI, a specialized aviation assistant.
    Use [bold blue] Rich formatting [/bold blue] in your responses.
    Use rich formatting in your responses like:
    - [bold]bold text[/bold text]
    - [italic]italic text[/italic]
    - [yellow]colored text[/yellow]
    - [bold red]combined formatting[bold red]
    
    For weather conditions, use colors like:
    - [bold green]VFR conditions[/bold green]
    - [bold dark blue]MVFR conditions[/bold dark blue]
    - [bold red]IFR conditions[/bold red]
    - [bold pink]LIFR conditions[/bold pink]
    
    Keep the responses aviation focused. Technical but accessible.
    User can override the aviation responses if they want to, but remind them 
    you are a aviation assistant"""
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini", messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def animate_typing(text, prefix=None, speed=0.01):
    with Live(refresh_per_second=20, console=console) as live:
        displayed = prefix if prefix else ""
        for char in text:
            displayed += char
            live.update(Text.from_markup(displayed))
            time.sleep(speed)
    
def main():
    while True:
        user_input = console.input("[bold cyan]You: [/bold cyan]")
        console.print()
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        with console.status(
            "Generating Response", spinner="dots12"
        ): response = chat_with_chad(user_input)
        
        animate_typing(response, prefix="[bold green]Pilotbot: [/bold green]")
        console.print()
    
    with console.status(
            "Generating Response", spinner="dots12"
        ): response = chat_with_chad("User said bye or quit the program")
    
    animate_typing(response, prefix="[bold green]Pilotbot: [/bold green]")
    
if __name__ == "__main__":
    main()