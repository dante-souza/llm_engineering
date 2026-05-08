import os

from dotenv import load_dotenv
from rich.console import Console
from rich.pretty import pprint
from rich.table import Table
from openai import OpenAI


console = Console()


def check_torch():
    """
    Checks whether PyTorch is installed and whether CPU/GPU execution works.
    """

    try:
        import torch
    except ImportError:
        console.print("[red]PyTorch is not installed.[/red]")
        console.print("Install it with one of these commands:")
        console.print("\nCPU:")
        console.print("  uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
        console.print("\nCUDA/GPU:")
        console.print("  uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130")
        return

    table = Table(title="PyTorch Environment Check")
    table.add_column("Check", style="bold")
    table.add_column("Result")

    table.add_row("Torch version", torch.__version__)
    table.add_row("CUDA build version", str(torch.version.cuda))
    table.add_row("CUDA available", str(torch.cuda.is_available()))
    table.add_row("CUDA device count", str(torch.cuda.device_count()))

    # CPU check
    try:
        x_cpu = torch.tensor([1.0, 2.0, 3.0])
        y_cpu = x_cpu * 2
        table.add_row("CPU tensor check", f"OK: {y_cpu.tolist()}")
    except Exception as e:
        table.add_row("CPU tensor check", f"FAILED: {e}")

    # GPU check
    if torch.cuda.is_available():
        try:
            device = torch.device("cuda")
            gpu_name = torch.cuda.get_device_name(0)

            x_gpu = torch.tensor([1.0, 2.0, 3.0], device=device)
            y_gpu = x_gpu * 2

            table.add_row("GPU name", gpu_name)
            table.add_row("GPU tensor check", f"OK: {y_gpu.cpu().tolist()}")

        except Exception as e:
            table.add_row("GPU tensor check", f"FAILED: {e}")
    else:
        table.add_row("GPU tensor check", "CUDA GPU not available")

    console.print(table)


def check_openai():
    """
    Checks whether the OpenAI client works.
    """

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        console.print("[red]OPENAI_API_KEY not found in environment variables.[/red]")
        return

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5.2",
        input="Write a short bedtime story about a unicorn."
    )

    console.print("\n[bold green]OpenAI API response:[/bold green]")
    pprint(response.output_text)


if __name__ == "__main__":
    check_torch()
    check_openai()