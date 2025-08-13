from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
import os, time, json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
HISTORY_FILE = "history.json"
console = Console()

message_history: str = []

def chat_with_chad(prompt: str) -> str:
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
    
    message_history.append({"role": "user", "content": prompt})
    
    messages = [{"role": "system", "content": system_message}]
    
    messages.extend(message_history[-10:])
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini", messages=messages
    )

    assistant_message = response.choices[0].message.content.strip()
    
    message_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

def save_history() -> None:
    with open(HISTORY_FILE, "w") as file:
        json.dump(message_history, file)

def load_history() -> None:
    global message_history
    try:
        with open(HISTORY_FILE, "r") as file:
            message_history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        message_history = []
        
def clear_history() -> str:
    global message_history
    message_history = []
    
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return "Conversation History Cleared..." 

def animate_typing(text, prefix=None, speed=0.01) -> None:
    with Live(refresh_per_second=20, console=console) as live:
        displayed = prefix if prefix else ""
        for char in text:
            displayed += char
            live.update(Text.from_markup(displayed))
            time.sleep(speed)
    
def main():
    
    welcome = Panel("""[bold blue]✈️ PilotAI[/bold blue] - Your Aviation Assistant
    [yellow]Commands:[/yellow]
    • Type [bold cyan]/clear[/bold cyan] to clear conversation history
    • Type [bold cyan]/save[/bold cyan] to manually save conversation
    • Type [bold cyan]exit[/bold cyan] to quit""",
        title="[bold]Welcome to PilotAI",
        border_style="blue",
        padding=(1, 2))
    
    console.print(welcome, end="\n")
    
    load_history()
    
    while True:
        user_input = console.input("[bold cyan]You: [/bold cyan]")
        console.print()
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        elif user_input.lower() == "/clear":
            message_history.clear()
            console.print("[bold green]System: [/bold green]Conversational history cleared...\n")
            continue
        with console.status(
            "Generating Response", spinner="dots12"
        ): response = chat_with_chad(user_input)
        
        animate_typing(response, prefix="[bold green]Pilotbot: [/bold green]")
        console.print()
    
    with console.status(
            "Generating Response", spinner="dots12"
        ): response = chat_with_chad("User said bye or quit the program")
    
    animate_typing(response, prefix="[bold green]Pilotbot: [/bold green]")
    save_history()
    
if __name__ == "__main__":
    main()