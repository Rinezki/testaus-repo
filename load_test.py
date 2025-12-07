import cProfile, pstats, psutil, os, time
from main import Application

def run_app():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    process = psutil.Process(os.getpid())
    print("Alkuperäinen muisti:", process.memory_info().rss / 1024**2, "MB")

    profiler = cProfile.Profile()
    profiler.enable()
    run_app()
    profiler.disable()

    print("Lopullinen muisti:", process.memory_info().rss / 1024**2, "MB")
    print("CPU:", process.cpu_percent(interval=1), "%")

    stats = pstats.Stats(profiler).sort_stats("time")
    stats.print_stats(20)