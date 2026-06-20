from dataclasses import dataclass

NUMPY_AVAILABLE: bool = False
NUMPY_VERSION: str | None = None
PANDAS_AVAILABLE: bool = False
PANDAS_VERSION: str | None = None
MATPLOTLIB_AVAILABLE: bool = False
MATPLOTLIB_VERSION: str | None = None
REQUESTS_AVAILABLE: bool = False
REQUESTS_VERSION: str | None = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
    NUMPY_VERSION = np.__version__
except ImportError:
    pass

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
    PANDAS_VERSION = pd.__version__
except ImportError:
    pass

try:
    import matplotlib
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
    MATPLOTLIB_VERSION = matplotlib.__version__
except ImportError:
    pass

try:
    import requests
    REQUESTS_AVAILABLE = True
    REQUESTS_VERSION = requests.__version__
except ImportError:
    pass


@dataclass
class PackageStatus:
    available: bool
    version: str | None


def check_dependencies() -> dict[str, PackageStatus]:
    return {
        "numpy": PackageStatus(NUMPY_AVAILABLE, NUMPY_VERSION),
        "pandas": PackageStatus(PANDAS_AVAILABLE, PANDAS_VERSION),
        "matplotlib": PackageStatus(MATPLOTLIB_AVAILABLE, MATPLOTLIB_VERSION),
        "requests": PackageStatus(REQUESTS_AVAILABLE, REQUESTS_VERSION),
    }


def print_dependency_status(status: dict[str, PackageStatus]) -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")
    for pkg in ["numpy", "pandas", "matplotlib", "requests"]:
        info = status[pkg]
        if info.available:
            print(f"[OK] {pkg} ({info.version}) - Ready")
        else:
            print(f"[ERROR] {pkg} - Not found")
    print()


def print_installation_instructions(status: dict[str, PackageStatus]) -> None:
    required_packages = ["numpy", "pandas", "matplotlib"]
    missing = [pkg for pkg in required_packages if not status[pkg].available]
    if not missing:
        return
    print("ERROR: Missing required dependencies!")
    print()
    print("To install with pip:")
    print(f"  pip install {' '.join(missing)}")
    print()
    print("To install with Poetry:")
    print(f"  poetry add {' '.join(missing)}")
    print()
    if not status["requests"].available:
        print(
            "Note: requests is optional - install it if you want to "
            "fetch real API data"
        )
        print()


def generate_matrix_data(n_points: int = 100, seed: int = 42) -> "np.ndarray":
    np.random.seed(seed)
    timestamps = np.arange(n_points)
    sensor_alpha = (
        10 * np.sin(timestamps / 10) + np.random.randn(n_points) * 0.5
    )
    sensor_beta = (
        8 * np.cos(timestamps / 15) + np.random.randn(n_points) * 0.5
    )
    sensor_gamma = (
        2 + (timestamps / 20) + np.random.randn(n_points) * 0.5
    )
    data = np.column_stack(
        (timestamps, sensor_alpha, sensor_beta, sensor_gamma)
    )
    return data


def create_dataframe(data: "np.ndarray") -> "pd.DataFrame":
    df = pd.DataFrame(
        data,
        columns=[
            "timestamp", "sensor_alpha", "sensor_beta", "sensor_gamma"
        ]
    )
    df["rolling_alpha"] = df["sensor_alpha"].rolling(window=5).mean()
    return df


def create_visualization(
    df: "pd.DataFrame",
    filename: str = "matrix_analysis.png"
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(
        df["timestamp"], df["sensor_alpha"],
        label="Sensor Alpha", color="blue"
    )
    plt.plot(
        df["timestamp"], df["sensor_beta"],
        label="Sensor Beta", color="green"
    )
    plt.plot(
        df["timestamp"], df["sensor_gamma"],
        label="Sensor Gamma", color="red"
    )
    plt.plot(
        df["timestamp"], df["rolling_alpha"],
        label="Rolling Alpha (5pts)",
        color="purple", linestyle="--", linewidth=1.5
    )
    plt.title("Matrix Sensor Readings")
    plt.xlabel("Time")
    plt.ylabel("Signal Strength")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(filename, dpi=100, bbox_inches="tight")
    plt.close()


def run_analysis(filename: str = "matrix_analysis.png") -> None:
    print("Analyzing Matrix data...")
    data = generate_matrix_data()
    df = create_dataframe(data)
    print(f"Processing {len(df)} data points...")
    create_visualization(df, filename)
    print("Generating visualization...")
    print()
    print("Analysis complete!")
    print(f"Results saved to: {filename}")


def main() -> None:
    status = check_dependencies()
    print_dependency_status(status)

    required = ["numpy", "pandas", "matplotlib"]
    if all(status[pkg].available for pkg in required):
        run_analysis()
    else:
        print_installation_instructions(status)


if __name__ == "__main__":
    main()
