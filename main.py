import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
import importlib
import sys
import os
from sw_optimizer.sw_optimizer import swo


def plot_function(func, lb, ub, dim, optimal_solution, projection='3d'):
    if dim > 2 and projection == '3d':
        # Plot only the first two dimensions
        x = np.linspace(lb[0], ub[0], 100)
        y = np.linspace(lb[1], ub[1], 100)
        X, Y = np.meshgrid(x, y)
        Z = np.array([func(np.array([x, y] + [0] * (dim - 2))) for x, y in zip(np.ravel(X), np.ravel(Y))])
        Z = Z.reshape(X.shape)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.scatter(optimal_solution[0], optimal_solution[1], func(optimal_solution), color='red')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.savefig(f'{func.__name__}_3d.png')
        plt.close(fig)  # Close the figure to free up memory
    else:
        # Plot the function
        x = np.linspace(lb[0], ub[0], 100)
        y = np.linspace(lb[1], ub[1], 100)
        X, Y = np.meshgrid(x, y)
        if dim > 2:
            Z = np.array([func(np.array([x, y] + [0] * (dim - 2))) for x, y in zip(np.ravel(X), np.ravel(Y))])
        else:
            Z = np.array([func(np.array([x, y])) for x, y in zip(np.ravel(X), np.ravel(Y))])
        Z = Z.reshape(X.shape)

        fig, ax = plt.subplots()
        cs = ax.contour(X, Y, Z)
        ax.clabel(cs, inline=1, fontsize=10)
        ax.scatter(optimal_solution[0], optimal_solution[1], color='red')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.savefig(f'{func.__name__}_contour.png')
        plt.close(fig)  # Close the figure to free up memory


def main():
    parser = argparse.ArgumentParser(description='Run SWO algorithm with 2D or 3D projection.')
    parser.add_argument('--projection', type=str, choices=['2d', '3d'], default='3d',
                        help='Choose between 2D and 3D projection')
    parser.add_argument('--function', type=str, required=True, help='Select the test functions, separated by commas')
    parser.add_argument('--dim', type=int, default=4, help='Dimension of the test functions')
    args = parser.parse_args()

    search_agents_no = 30
    Tmax = 1000
    dim = args.dim  # Use the dimension provided by the user
    lb = [-512] * dim
    ub = [512] * dim

    # Add the directory containing the test functions to the Python path
    test_functions_dir = os.path.join(os.path.dirname(__file__), 'test_functions')
    sys.path.append(test_functions_dir)

    # Split the functions and process each one
    functions = args.function.split(',')

    # Initialize a figure for the convergence plot
    plt.figure()

    for func_name in functions:
        # Dynamically import the selected function
        func_module = importlib.import_module(func_name.strip().lower())
        func = getattr(func_module, func_name.strip())

        optimal_value, optimal_solution, convergence_curve, total_evaluations, evaluations_per_function = swo(
            search_agents_no, Tmax, ub, lb, dim, func)

        print(f"Results for {func_name.strip()}:")
        print(f"Optimal Value (fmin): {optimal_value}")
        print(f"Optimal Solution (xmin): {optimal_solution}")
        print(f"Total Evaluations (neval): {total_evaluations}")
        print(f"Evaluations for {func_name.strip()}: {evaluations_per_function[func_name.strip()]}")

        # Plot the convergence curve
        if convergence_curve.size > 0:
            plt.plot(convergence_curve, label=func_name.strip())
        else:
            print(f"Warning: Convergence curve for {func_name.strip()} is empty.")

        # Plot the function surface or contour
        plot_function(func, lb, ub, dim, optimal_solution, projection=args.projection)

    # Ensure there are labeled plots to include in the legend
    if plt.gca().get_legend_handles_labels()[0]:
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.title('Convergence Curve')
        plt.legend()
        try:
            plt.savefig('convergence.png')
            print("Convergence plot saved successfully.")
        except Exception as e:
            print(f"Error saving convergence plot: {e}")
    else:
        print("No labeled plots to save.")
    plt.close()  # Close the figure to free up memory


if __name__ == "__main__":
    main()

