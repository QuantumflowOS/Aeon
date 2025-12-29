# aeon/cli.py
"""
Advanced CLI tool with rich formatting and interactive features.
"""

import click
import json
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.tree import Tree
from rich import box
import time

console = Console()


@click.group()
@click.option('--api-url', default='http://localhost:8000', help='AEON API URL')
@click.pass_context
def cli(ctx, api_url):
    """🧠 AEON CLI - Autonomous Evolving Orchestration Network"""
    ctx.ensure_object(dict)
    ctx.obj['API_URL'] = api_url


@cli.command()
@click.pass_context
def status(ctx):
    """Check system status and health."""
    api_url = ctx.obj['API_URL']
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Fetching system status...", total=None)
        
        try:
            response = requests.get(f"{api_url}/system/health", timeout=5)
            progress.update(task, completed=True)
            
            if response.status_code == 200:
                data = response.json()
                
                # Status panel
                status_text = f"[bold green]● ONLINE[/bold green]"
                console.print(Panel(status_text, title="System Status", border_style="green"))
                
                # Metrics table
                table = Table(title="System Metrics", box=box.ROUNDED)
                table.add_column("Metric", style="cyan", no_wrap=True)
                table.add_column("Value", style="magenta")
                
                table.add_row("Protocol Count", str(data.get('protocol_count', 0)))
                table.add_row("Memory Items", str(data.get('memory_items', 0)))
                
                context = data.get('context', {})
                table.add_row("Emotion", context.get('emotion', 'N/A'))
                table.add_row("Intent", context.get('intent', 'N/A'))
                table.add_row("Environment", context.get('environment', 'N/A'))
                
                console.print(table)
                
                # Protocols
                if data.get('protocols'):
                    console.print("\n[bold]Active Protocols:[/bold]")
                    protocol_table = Table(box=box.SIMPLE)
                    protocol_table.add_column("Name", style="cyan")
                    protocol_table.add_column("Reward", style="green")
                    protocol_table.add_column("Executions", style="yellow")
                    
                    for p in data['protocols']:
                        protocol_table.add_row(
                            p.get('name', 'N/A'),
                            f"{p.get('reward', 0):.2f}",
                            str(p.get('executions', 0))
                        )
                    
                    console.print(protocol_table)
            else:
                console.print(f"[bold red]✗ Error: {response.status_code}[/bold red]")
        
        except requests.exceptions.ConnectionError:
            console.print("[bold red]✗ Cannot connect to AEON API[/bold red]")
            console.print(f"Make sure the server is running at: {api_url}")


@cli.command()
@click.option('--emotion', prompt='Emotion', help='Agent emotion')
@click.option('--intent', prompt='Intent', help='Agent intent')
@click.option('--environment', default='default', help='Environment context')
@click.pass_context
def update(ctx, emotion, intent, environment):
    """Update agent context."""
    api_url = ctx.obj['API_URL']
    
    data = {
        "emotion": emotion,
        "intent": intent,
        "environment": environment
    }
    
    with console.status("[bold green]Updating context..."):
        try:
            response = requests.post(f"{api_url}/context/update", json=data)
            
            if response.status_code == 200:
                result = response.json()
                console.print("[bold green]✓ Context updated successfully![/bold green]")
                
                # Display updated context
                tree = Tree("📋 Updated Context")
                tree.add(f"Emotion: [cyan]{emotion}[/cyan]")
                tree.add(f"Intent: [magenta]{intent}[/magenta]")
                tree.add(f"Environment: [yellow]{environment}[/yellow]")
                console.print(tree)
            else:
                console.print(f"[bold red]✗ Error: {response.status_code}[/bold red]")
        
        except Exception as e:
            console.print(f"[bold red]✗ Error: {e}[/bold red]")


@cli.command()
@click.pass_context
def run(ctx):
    """Execute agent with current context."""
    api_url = ctx.obj['API_URL']
    
    with console.status("[bold green]Running agent..."):
        try:
            response = requests.post(f"{api_url}/agent/run")
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {})
                
                console.print("\n[bold green]✓ Agent execution complete![/bold green]\n")
                
                # Results panel
                thought = result.get('thought', 'N/A')
                protocol = result.get('protocol', 'N/A')
                action = result.get('action', 'N/A')
                reward = result.get('reward', 'N/A')
                
                console.print(Panel(
                    f"[bold cyan]Protocol:[/bold cyan] {protocol}\n"
                    f"[bold yellow]Reward:[/bold yellow] {reward}\n\n"
                    f"[bold magenta]Thought:[/bold magenta]\n{thought}\n\n"
                    f"[bold green]Action:[/bold green]\n{action}",
                    title="Agent Output",
                    border_style="green"
                ))
            else:
                console.print(f"[bold red]✗ Error: {response.status_code}[/bold red]")
        
        except Exception as e:
            console.print(f"[bold red]✗ Error: {e}[/bold red]")


@cli.command()
@click.option('--goal', prompt='Goal', help='Goal to execute')
@click.pass_context
def goal(ctx, goal):
    """Execute a specific goal."""
    api_url = ctx.obj['API_URL']
    
    with console.status(f"[bold green]Executing goal: {goal}..."):
        try:
            response = requests.post(
                f"{api_url}/agent/goal",
                json={"goal": goal}
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {})
                
                console.print(f"\n[bold green]✓ Goal '{goal}' executed![/bold green]\n")
                
                steps = result.get('steps', [])
                
                if steps:
                    console.print("[bold]Execution Steps:[/bold]")
                    for i, step in enumerate(steps, 1):
                        console.print(f"  {i}. {step.get('step', 'N/A')}")
                        console.print(f"     → {step.get('result', 'N/A')}")
            else:
                console.print(f"[bold red]✗ Error: {response.status_code}[/bold red]")
        
        except Exception as e:
            console.print(f"[bold red]✗ Error: {e}[/bold red]")


@cli.command()
@click.option('--type', 'mem_type', type=click.Choice(['all', 'semantic', 'episodic']), 
              default='all', help='Memory type to view')
@click.pass_context
def memory(ctx, mem_type):
    """View agent memory."""
    api_url = ctx.obj['API_URL']
    
    with console.status("[bold green]Fetching memory..."):
        try:
            response = requests.get(f"{api_url}/memory")
            
            if response.status_code == 200:
                data = response.json()
                memory = data.get('memory', {})
                
                if mem_type in ['all', 'semantic']:
                    semantic = memory.get('semantic', [])
                    console.print(f"\n[bold cyan]Semantic Memory ({len(semantic)} items):[/bold cyan]")
                    for item in semantic[-10:]:
                        console.print(f"  • {item}")
                
                if mem_type in ['all', 'episodic']:
                    episodic = memory.get('episodic', [])
                    console.print(f"\n[bold magenta]Episodic Memory ({len(episodic)} events):[/bold magenta]")
                    
                    table = Table(box=box.ROUNDED)
                    table.add_column("Time", style="dim")
                    table.add_column("Emotion", style="cyan")
                    table.add_column("Action", style="green")
                    
                    for event in episodic[-5:]:
                        ctx = event.get('context', {})
                        table.add_row(
                            event.get('timestamp', 'N/A')[:19],
                            ctx.get('emotion', 'N/A'),
                            event.get('action', 'N/A')[:50] + "..."
                        )
                    
                    console.print(table)
            else:
                console.print(f"[bold red]✗ Error: {response.status_code}[/bold red]")
        
        except Exception as e:
            console.print(f"[bold red]✗ Error: {e}[/bold red]")


@cli.command()
@click.pass_context
def protocols(ctx):
    """List all registered protocols."""
    api_url = ctx.obj['API_URL']
    
    with console.status("[bold green]Fetching protocols..."):
        try:
            response = requests.get(f"{api_url}/protocols")
            
            if response.status_code == 200:
                data = response.json()
                protocols = data.get('protocols', [])
                
                console.print(f"\n[bold]Registered Protocols ({len(protocols)}):[/bold]\n")
                
                table = Table(title="Protocol Registry", box=box.DOUBLE)
                table.add_column("Name", style="cyan", no_wrap=True)
                table.add_column("Reward", style="green", justify="right")
                table.add_column("Executions", style="yellow", justify="right")
                table.add_column("Status", style="magenta")
                
                for p in sorted(protocols, key=lambda x: x.get('reward', 0), reverse=True):
                    reward = p.get('reward', 0)
                    status = "🔥 Hot" if reward > 4 else "✓ Good" if reward > 3 else "⚠ Low"
                    
                    table.add_row(
                        p.get('name', 'N/A'),
                        f"{reward:.2f}",
                        str(p.get('executions', 0)),
                        status
                    )
                
                console.print(table)
            else:
                console.print(f"[bold red]✗ Error: {response.status_code}[/bold red]")
        
        except Exception as e:
            console.print(f"[bold red]✗ Error: {e}[/bold red]")


@cli.command()
@click.pass_context
def interactive(ctx):
    """Start interactive mode."""
    api_url = ctx.obj['API_URL']
    
    console.print(Panel.fit(
        "[bold cyan]🧠 AEON Interactive Mode[/bold cyan]\n"
        "Type 'help' for commands, 'exit' to quit",
        border_style="cyan"
    ))
    
    while True:
        try:
            cmd = Prompt.ask("\n[bold cyan]aeon>[/bold cyan]")
            
            if cmd.lower() in ['exit', 'quit']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            elif cmd.lower() == 'help':
                console.print("""
[bold]Available Commands:[/bold]
  status    - Show system status
  run       - Execute agent
  update    - Update context
  memory    - View memory
  protocols - List protocols
  exit      - Exit interactive mode
                """)
            
            elif cmd.lower() == 'status':
                ctx.invoke(status)
            
            elif cmd.lower() == 'run':
                ctx.invoke(run)
            
            elif cmd.lower() == 'memory':
                ctx.invoke(memory, mem_type='all')
            
            elif cmd.lower() == 'protocols':
                ctx.invoke(protocols)
            
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == '__main__':
    cli(obj={})
