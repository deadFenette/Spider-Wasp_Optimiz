# Spider Wasp Optimizer (SWO)

![SWO Logo](images/swo_logo.png)

This project implements the Spider Wasp Optimizer (SWO) algorithm in Python and demonstrates its performance on several standard test functions. The SWO algorithm is a novel meta-heuristic optimization algorithm inspired by the hunting behavior of spider wasps.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Graphical User Interface (GUI)](#graphical-user-interface-gui)
- [Test Functions](#test-functions)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Project Structure


- `sw_optimizer`: Contains the implementation of the SWO algorithm.
- `test_functions`: Contains the implementation of test functions.
- `utils`: Contains utility functions.
- `main.py`: The entry point of the project.
- `requirements.txt`: List of dependencies.
- `gui.py`: Graphical user interface entry point.
- `report`: Directory for the project report.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd SpiderWaspOptimizer
   ```
2. Install the dependencies:
```bash
   pip install -r requirements.txt
```
## Usage

To run the SWO algorithm on a specific test function, use the following command:

```bash
python main.py --projection <projection> --function <function_name> --dim <dimension>
```
### Arguments:
- `--projection`:  
  Choose between `'2d'` and `'3d'` projection.  
- `--function`:  
  Select the test function.  
- `--dim`:  
  Dimension of the test function.

## Graphical User Interface (GUI)

![SWO GUI Interface](images/gui_screenshot.png)

The SWO Optimizer features a modern graphical interface for interactive optimization workflows.

### Key Features

- 🌓 **Theme Support** - Toggle between light/dark modes
- 📊 **Multi-Function Optimization** - Select multiple test functions simultaneously
- 🎚️ **Dimension Control** - Choose problem dimensionality (2D-4D)
- 📈 **Real-Time Visualization** - Live convergence curve plotting
- 📋 **Results Table** - Sortable table with optimal values/solutions
- ⚡ **Progress Feedback** - Status bar with operation updates
- 🔄 **Session Persistence** - Remembers last used settings
- 📥 Results import - Ability to export results in CSV format

### Usage

### Usage

1. Launch the GUI:
```bash
python gui.py
```

**Interface workflow:**

- Check desired test functions in left panel
- Select dimension from dropdown (2-4)
- Click ▶️ Start Optimization
- View convergence plots in upper panel
- Inspect numerical results in table below
- Toggle theme using the 🌞/🌙 icon in top-right corner

**Interface Elements**

| Panel          | Components                                      |
|----------------|-------------------------------------------------|
| Left Sidebar   | Function selection, dimension control, run button |
| Main Area      | Convergence plot (top), results table (bottom)   |
| Toolbar        | Theme toggle, status indicators                  |

**Technical Notes**

- Settings automatically saved in QSettings registry
- Tooltips available for all interactive elements
- Requires PyQt5 and pyqtgraph dependencies
- Compatible with Windows/Linux/macOS
- Optimal resolution: 1280×800 or higher

## Example

To run the SWO algorithm on the Eggholder function with a 2D projection, use the following command:

```bash
python main.py --projection 2d --function eggholder_function --dim 2
```

This command will execute the SWO algorithm on the Eggholder function and generate a 3D plot of the function along with the convergence plot.

## Test Functions

The following test functions are implemented:

- **Ackley**
- **Bukin Function N. 6**
- **Eggholder Function**
- **Himmelblau**
- **Rastrigin**
- **Rosenbrock**
- **Schwefel Function**
- **Sphere**

Each function is defined in a separate file within the `test_functions` directory. These functions are standard benchmark functions used to evaluate the performance of optimization algorithms.

## Results

The results of the optimization are saved in the `main` directory and include:

- **Optimal Value (fmin):** The best value of the function found during optimization.
- **Optimal Solution (xmin):** The coordinates corresponding to the optimal value.
- **Total Evaluations (neval):** The total number of function evaluations.
- **Convergence Plots:** A visual representation of the algorithm's progress over iterations.

The convergence plot is saved as `convergence.png`. Function plots are saved as `<function_name>_3d.png` or `<function_name>_contour.png`, depending on the projection type.
### Example Output

Results for `eggholder_function`:

- **Optimal Value (fmin):** -959.6407
- **Optimal Solution (xmin):** `[512.0, 404.2319]`
- **Total Evaluations (neval):** 50000 
- Evaluations for `eggholder_function`: 50000 
- Convergence plot saved successfully.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Open a pull request.

Please ensure that your code follows the existing style and passes all tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or suggestions, please contact `dead@dead.com`.

## Acknowledgements

All credit goes to the researchers, I have just made a rough  implementation in Python.

The researchers are:
- Mohamed Abdel-Basset
- Reda Mohamed
- Mohammed Jameel
- Mohamed Abouhawwash

Source pages:
- [Springer article](https://link.springer.com/article/10.1007/s10462-023-10446-y)
- [Spider Wasp Optimizer on MathWorks](https://www.mathworks.com/matlabcentral/fileexchange/126010-spider-wasp-optimizer-swo)



Happy Optimizing!
