import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_data():
    # Connect to the SQLite database
    db_path = 'lecture_data.db'
    conn = sqlite3.connect(db_path)

    # Define SQL queries
    department_query = '''
        SELECT department,
               SUM(CASE WHEN access = 1 THEN 1 ELSE 0 END) AS accessible_count,
               COUNT(*) AS total_count
        FROM lectures
        GROUP BY department
    '''

    year_query = '''
        SELECT year, COUNT(*) AS series_count
        FROM lectures
        GROUP BY year
        ORDER BY year
    '''

    year_accessible_query = '''
        SELECT year,
               SUM(CASE WHEN access = 1 THEN 1 ELSE 0 END) AS accessible_count,
               COUNT(*) AS total_count
        FROM lectures
        GROUP BY year
        ORDER BY year
    '''

    # Execute queries and convert to DataFrames
    department_data = pd.read_sql(department_query, conn)
    year_data = pd.read_sql(year_query, conn)
    year_accessible_data = pd.read_sql(year_accessible_query, conn)

    # Compute fractions
    department_data['accessible_fraction'] = department_data['accessible_count'] / \
        department_data['total_count']
    year_accessible_data['accessible_fraction'] = year_accessible_data['accessible_count'] / \
        year_accessible_data['total_count']

    # Sort by accessible fraction in descending order
    department_data_sorted = department_data.sort_values(
        by='accessible_fraction', ascending=False)
    department_data_sorted['department'] = department_data_sorted['department'].str.upper(
    )

    return department_data_sorted, year_data, year_accessible_data


# Load data
department_data_sorted, year_data, year_accessible_data = load_data()

# Create figure and axes
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Colors and style
colors = ['steelblue', 'salmon', 'seagreen', 'mediumpurple']

# Plot A: Department vs. Fraction of Accessible Lecture Series
axes[0, 0].bar(department_data_sorted['department'],
               department_data_sorted['accessible_fraction'],
               label='Accessible', color='mediumpurple', edgecolor='black')

axes[0, 0].set_xlabel('Department')
axes[0, 0].set_ylabel('Fraction of Accessible Lecture Series')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[0, 0].text(-0.1, 1.1, 'A', transform=axes[0, 0].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')

# Plot B: Department vs. Lectures Uploaded
axes[0, 1].bar(department_data_sorted['department'],
               department_data_sorted['total_count'],
               color='salmon', edgecolor='black', label="restricted")
axes[0, 1].bar(department_data_sorted['department'],
               department_data_sorted['accessible_count'],
               color='skyblue', edgecolor='black', label="accessible")

axes[0, 1].set_xlabel('Department')
axes[0, 1].set_ylabel('Total Number of Lecture Series')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[0, 1].text(-0.1, 1.1, 'B', transform=axes[0, 1].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')
axes[0, 1].legend(loc='upper left', frameon=False)

# Plot D: Year vs Lectures Uploaded
axes[1, 1].bar(year_data['year'], year_data['series_count'],
               color='salmon', edgecolor='black', label="restricted")
axes[1, 1].bar(year_data['year'], year_accessible_data['accessible_count'],
               color='skyblue', edgecolor='black', label="accessible")
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Number of Lecture Series Uploaded')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[1, 1].text(-0.1, 1.1, 'D', transform=axes[1, 1].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')
axes[1, 1].legend(loc='upper left', frameon=False)


axes[1, 0].bar(year_accessible_data['year'],
               year_accessible_data['accessible_fraction'],
               label='Accessible', color='mediumpurple', edgecolor='black')

axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('Fraction of Accessible Lecture Series')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[1, 0].text(-0.1, 1.1, 'C', transform=axes[1, 0].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')

plt.tight_layout()
plt.savefig("plot.pdf")
plt.savefig("plot.jpeg")
plt.show()
