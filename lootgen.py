from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from rich.console import Console
from rich.table import Table


@dataclass
class LootItem:
    name: str
    rarity: str
    drop_chance: float  # вероятность за один сундук (0–1)


LOOT_POOL: List[LootItem] = [
    LootItem("Обычный меч", "Обычный", 0.6),
    LootItem("Редкий амулет", "Редкий", 0.25),
    LootItem("Эпический посох", "Эпический", 0.1),
    LootItem("Легендарный драконий клинок", "Легендарный", 0.05),
]


console = Console()


def simulate_drops(chests: int) -> List[int]:
    counts = [0 for _ in LOOT_POOL]
    for _ in range(chests):
        for index, item in enumerate(LOOT_POOL):
            if random.random() < item.drop_chance:
                counts[index] += 1
    return counts


def print_result_table(chests: int, counts: List[int]) -> None:
    table = Table(title=f"Имитация  {chests} сундуков с сокровищами")

    table.add_column("Элемент", justify="left")
    table.add_column("Редкость", justify="center")
    table.add_column("Падения", justify="right")
    table.add_column("Шанс выпадения", justify="right")

    for item, count in zip(LOOT_POOL, counts):
        empirical = count / chests if chests > 0 else 0.0
        table.add_row(
            item.name,
            item.rarity,
            str(count),
            f"{empirical:.3f}",
        )

    console.print(table)


def ask_chest_count() -> int:
    while True:
        try:
            raw = console.input("Введите количество сундуков, которые нужно открыть: ")
            value = int(raw)
            if value < 0:
                console.print("[red]Number must be non‑negative[/red]")
                continue
            return value
        except ValueError:
            console.print("[red]Please enter an integer[/red]")


def main() -> None:
    console.print("[bold cyan]LootGen — симулятор выпадения добычи[/bold cyan]")
    chests = ask_chest_count()
    counts = simulate_drops(chests)
    print_result_table(chests, counts)


if __name__ == "__main__":
    main()
