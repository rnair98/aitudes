import time
import shutil
import math
import sys
from typing import Iterable, Iterator, Generic, Optional, TypeVar, Any

T = TypeVar("T")


class tqdm(Generic[T]):
    def __init__(
        self,
        iterable: Iterable[T] | None = None,
        desc: str = "",
        disable: bool = False,
        unit: str = "it",
        unit_scale: bool = False,
        total: Optional[int] = None,
        rate: int = 100,
    ):
        """
        Initializes a progress bar for an iterable, configuring display options and internal state.
        
        Args:
            iterable: The iterable to track progress over. If None, progress bar operates without iteration.
            desc: Optional description prefix for the progress bar.
            disable: If True, disables the progress bar display.
            unit: Label for the unit of iteration (e.g., "it", "items").
            unit_scale: If True, scales the unit count with SI prefixes.
            total: Total number of iterations. If not provided, attempts to infer from the iterable.
            rate: Maximum number of progress bar updates per second.
        """
        self.iterable, self.disable, self.unit, self.unit_scale, self.rate = (
            iterable,
            disable,
            unit,
            unit_scale,
            rate,
        )
        self.start_time, self.current_index, self.count, self.skip, self.total = (
            time.perf_counter(),
            -1,
            0,
            1,
            getattr(iterable, "__len__", lambda: 0)() if total is None else total,
        )
        self.set_description(desc)
        self.update(0)

    def __iter__(self) -> Iterator[T]:
        """
        Iterates over the wrapped iterable, updating the progress bar after each item.
        
        Yields each item from the iterable and updates the progress bar to reflect progress.
        Finalizes the progress bar display when iteration completes.
        """
        assert self.iterable is not None, "need an iterable to iterate"
        for item in self.iterable:
            yield item
            self.update(1)
        self.update(close=True)

    def __enter__(self):
        """
        Enables use of the progress bar as a context manager.
        
        Returns:
            The progress bar instance itself.
        """
        return self

    def __exit__(self, *_):
        """
        Finalizes the progress bar display when exiting a context manager.
        """
        self.update(close=True)

    def set_description(self, desc: str):
        """
        Sets the progress bar description prefix.
        
        If a non-empty description is provided, appends ": " to it; otherwise, clears the prefix.
        """
        self.desc = f"{desc}: " if desc else ""

    def update(self, n: int = 0, close: bool = False):
        """
        Updates the progress bar display to reflect the current iteration state.
        
        Increments the internal counters, recalculates progress, and prints an updated
        progress bar to standard error. Dynamically adjusts update frequency based on
        iteration rate to minimize overhead. When `close` is True, finalizes the display
        and moves to a new line.
        
        Args:
            n: Number of iterations to increment the progress by.
            close: If True, finalizes and closes the progress bar display.
        """
        self.n, self.i = self.n + n, self.i + 1

        if self.disable or (not close and self.i % self.skip != 0):
            return

        prog, elapsed, ncols = (
            self.n / self.t if self.t else 0,
            time.perf_counter() - self.st,
            shutil.get_terminal_size().columns,
        )

        if self.i / elapsed > self.rate and self.i:
            self.skip = max(int(self.i / elapsed) // self.rate, 1)

        def HMS(t: float) -> str:
            """
            Converts a time duration in seconds to a human-readable H:MM:SS or M:SS format.
            
            Args:
                t: Time duration in seconds.
            
            Returns:
                A string representing the duration in hours, minutes, and seconds, omitting leading zero hours if not needed.
            """
            return ":".join(
                f"{x:02d}" if i else str(x)
                for i, x in enumerate(
                    [int(t) // 3600, int(t) % 3600 // 60, int(t) % 60]
                )
                if i or x
            )

        def SI(x: float) -> str:
            """
            Converts a numeric value to a string with an appropriate SI prefix.
            
            Args:
                x: The numeric value to convert.
            
            Returns:
                A string representing the value scaled with an SI prefix (e.g., k, M, G).
            """
            return (
                (
                    f"{x / 1000 ** int(g := math.log(x, 1000)):.{int(3 - 3 * math.fmod(g, 1))}f}"[
                        :4
                    ].rstrip(".")
                    + " kMGTPEZY"[int(g)].strip()
                )
                if x
                else "0.00"
            )

        prog_text = (
            f"{SI(self.n)}{f'/{SI(self.t)}' if self.t else self.unit}"
            if self.unit_scale
            else f"{self.n}{f'/{self.t}' if self.t else self.unit}"
        )

        est_text = (
            f"<{HMS(elapsed / prog - elapsed) if self.n else '?'}" if self.t else ""
        )

        it_text = (
            (SI(self.n / elapsed) if self.unit_scale else f"{self.n / elapsed:5.2f}")
            if self.n
            else "?"
        )

        suf = f"{prog_text} [{HMS(elapsed)}{est_text}, {it_text}{self.unit}/s]"
        sz = max(ncols - len(self.desc) - 3 - 2 - 2 - len(suf), 1)

        bar = (
            "\r"
            + self.desc
            + (
                f"{100 * prog:3.0f}%|{('█' * int(num := sz * prog) + ' ▏▎▍▌▋▊▉'[int(8 * num) % 8].strip()).ljust(sz, ' ')}| "
                if self.t
                else ""
            )
            + suf
        )

        print(bar[: ncols + 1], flush=True, end="\n" * close, file=sys.stderr)

    @classmethod
    def write(cls, s: str):
        """
        Clears the current line and writes a message to standard error.
        
        Args:
            s: The string to display on the progress bar line.
        """
        print(f"\r\033[K{s}", flush=True, file=sys.stderr)


class trange(tqdm[int]):
    def __init__(self, n: int, **kwargs: Any):
        """
        Initializes a progress bar for iterating over a range of integers from 0 to n - 1.
        
        Args:
            n: The number of iterations for the progress bar.
            **kwargs: Additional keyword arguments passed to the tqdm base class.
        """
        super().__init__(iterable=range(n), total=n, **kwargs)
