from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
import requests
import datetime
import json
import re

console = Console()

client = OpenAI(
    base_url="http://10.0.0.231:1234/v1",
    api_key="lm-studio"
)

MODEL = "mistralai/mistral-7b-instruct-v0.3"

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime('%A, %B %d, %Y at %I:%M %p')

def calculate(expression: str):
    try:
        allowed = set('0123456789+-*/(). ')
        if all(c in allowed for c in expression):
            return str(eval(expression))
        return "Invalid expression."
    except Exception as e:
        return f"Error: {e}"

def search_wikipedia(query: str):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("extract", "No summary found.")[:500]
        return "Not found."
    except Exception:
        return "Wikipedia search failed."

TOOLS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "search_wikipedia": search_wikipedia,
}

SYSTEM_PROMPT = """You are a helpful AI assistant with access to these tools:

1. get_current_time() - returns the current date and time
2. calculate(expression) - calculates a math expression
3. search_wikipedia(query) - searches Wikipedia for a topic

When you need to use a tool, respond ONLY with this exact JSON format:
{"tool": "tool_name", "args": {"arg_name": "value"}}

For get_current_time, use: {"tool": "get_current_time", "args": {}}

Only use a tool when it is actually needed. If you can answer directly, just answer normally."""

def run_agent(user_question: str):
    console.print(Panel(f"[bold cyan]You:[/bold cyan] {user_question}", border_style="cyan"))

    messages = [
        {"role": "user", "content": SYSTEM_PROMPT + "\n\nUser question: " + user_question}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1
    )

    reply = response.choices[0].message.content.strip()

    # Check if model wants to use a tool
    json_match = re.search(r'\{.*\}', reply, re.DOTALL)
    if json_match:
        try:
            tool_call = json.loads(json_match.group())
            tool_name = tool_call.get("tool")
            tool_args = tool_call.get("args", {})

            if tool_name in TOOLS:
                console.print(f"[yellow]⚙ Using tool:[/yellow] [bold]{tool_name}[/bold]")
                tool_result = TOOLS[tool_name](**tool_args) if tool_args else TOOLS[tool_name]()
                console.print(f"[green]✓ Tool result:[/green] {tool_result}")

                # Send result back to model for final answer
                messages.append({"role": "assistant", "content": reply})
                messages.append({"role": "user", "content": f"Tool result: {tool_result}\n\nNow give me a friendly final answer."})

                final = client.chat.completions.create(model=MODEL, messages=messages, temperature=0.3)
                answer = final.choices[0].message.content.strip()
            else:
                answer = reply
        except json.JSONDecodeError:
            answer = reply
    else:
        answer = reply

    console.print(Panel(f"[bold green]Agent:[/bold green] {answer}", border_style="green"))

if __name__ == "__main__":
    console.print(Panel(
        "[bold]🤖 Local AI Agent[/bold]\n"
        "Powered by Mistral 7B via LM Studio\n"
        "Tools: Time · Calculator · Wikipedia\n"
        "Type [bold cyan]quit[/bold cyan] to exit",
        border_style="magenta",
        title="Blaine's AI Agent"
    ))

    while True:
        try:
            question = input("\n💬 Ask me anything: ").strip()
            if question.lower() in ("quit", "exit", "q"):
                console.print("[dim]Goodbye![/dim]")
                break
            if question:
                run_agent(question)
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break
