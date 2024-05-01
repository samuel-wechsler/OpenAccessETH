import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# load data from SQL database
db_path = 'lecture_data.db'
conn = sqlite3.connect(db_path)


## Define and execute SQL queries ##

# SQL queries part 1: video portal #
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


d_chab_year_accessible_query = '''
        SELECT year,
               SUM(CASE WHEN access = 1 THEN 1 ELSE 0 END) AS accessible_count,
               COUNT(*) AS total_count
        FROM lectures WHERE department = "d-chab"
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
portal_department_data = pd.read_sql(department_query, conn)
portal_year_data = pd.read_sql(year_query, conn)
portal_dchab_year_accessible_data = pd.read_sql(
    d_chab_year_accessible_query, conn)
portal_year_accessible_data = pd.read_sql(year_accessible_query, conn)

# Compute fractions
portal_department_data['accessible_fraction'] = portal_department_data['accessible_count'] / \
    portal_department_data['total_count']

portal_year_accessible_data['accessible_fraction'] = portal_year_accessible_data['accessible_count'] / \
    portal_year_accessible_data['total_count']

# Sort by accessible fraction in descending order
department_data_sorted = portal_department_data.sort_values(
    by='accessible_fraction', ascending=False)
department_data_sorted['department'] = department_data_sorted['department'].str.upper(
)

# SQL queries part 2: course catalogue data #
year_query = '''
        SELECT year, COUNT(*) AS series_count
        FROM catalogue
        GROUP BY year
        ORDER BY year
    '''

dchab_year_query = '''
        SELECT year, COUNT(*) AS series_count
        FROM catalogue WHERE department = "d-chab"
        GROUP BY year
        ORDER BY year
    '''

catalogue_year_data = pd.read_sql(year_query, conn)
catalogue_dchab_year_data = pd.read_sql(dchab_year_query, conn)

## Create visualization of data ##

# Part 1: Evaluate data gathered from video.ethz.ch #
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
axes[1, 1].bar(portal_year_data['year'], portal_year_data['series_count'],
               color='salmon', edgecolor='black', label="restricted")
axes[1, 1].bar(portal_year_data['year'], portal_year_accessible_data['accessible_count'],
               color='skyblue', edgecolor='black', label="accessible")
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Number of Lecture Series Uploaded')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[1, 1].text(-0.1, 1.1, 'D', transform=axes[1, 1].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')
axes[1, 1].legend(loc='upper left', frameon=False)


axes[1, 0].bar(portal_year_accessible_data['year'],
               portal_year_accessible_data['accessible_fraction'],
               label='Accessible', color='mediumpurple', edgecolor='black')

axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('Fraction of Accessible Lecture Series')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[1, 0].text(-0.1, 1.1, 'C', transform=axes[1, 0].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')

plt.tight_layout()
plt.savefig("figures/portal.pdf")
plt.savefig("figures/portal.jpeg")

# Part 2: comparison to course catalogue data #
# Create the plot layout
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Standardize colors for consistency
colors = {'catalogue': 'mediumpurple',
          'portal': 'salmon',
          'accessible': 'skyblue'}

# Figure 2A: Yearly lectures in catalogue vs video portal (split in accessible v. inaccessible)
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Total Number of Lecture Series at ETH")
axes[0].grid(True, which='both', linestyle='--',
             linewidth=0.5, alpha=0.5, zorder=0)

axes[0].bar(catalogue_year_data['year'], catalogue_year_data['series_count'],
            color=colors['catalogue'], edgecolor='black')

# Filter data (not all years available in course catalogue online)
filtered_year_data = portal_year_data[portal_year_data['year'].isin(
    catalogue_year_data['year']
)]

filtered_year_accessible_data = portal_year_accessible_data[portal_year_accessible_data['year'].isin(
    catalogue_year_data['year']
)]

axes[0].bar(filtered_year_data['year'], filtered_year_data['series_count'],
            bottom=filtered_year_accessible_data['accessible_count'], color=colors['portal'], edgecolor='black')
axes[0].bar(filtered_year_accessible_data['year'], filtered_year_accessible_data['accessible_count'],
            color=colors['accessible'], edgecolor='black')
axes[0].text(-0.1, 1.1, 'A', transform=axes[0].transAxes,
             fontsize=16, fontweight='bold', va='top', ha='right')

# Figure 2B: Yearly lectures of D-CHAB in catalogue vs video portal
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Total Number of Lecture Series at D-CHAB")
axes[1].grid(True, which='both', linestyle='--',
             linewidth=0.5, alpha=0.5, zorder=0)

axes[1].bar(catalogue_dchab_year_data['year'], catalogue_dchab_year_data['series_count'],
            color=colors['catalogue'], label='Catalogued Lectures', edgecolor='black')

# filter data
filetered_dchab_year_data = portal_dchab_year_accessible_data[portal_dchab_year_accessible_data['year'].isin(
    catalogue_dchab_year_data['year']
)]

axes[1].bar(filetered_dchab_year_data['year'],
            filetered_dchab_year_data['total_count'],
            color=colors['portal'], edgecolor='black',
            label='Video Portal (total)')


axes[1].bar(filetered_dchab_year_data['year'],
            filetered_dchab_year_data['accessible_count'],
            color=colors['accessible'], edgecolor='black',
            label='Video Portal (accesible)')

axes[1].text(-0.1, 1.1, 'B', transform=axes[1].transAxes,
             fontsize=16, fontweight='bold', va='top', ha='right')
axes[1].legend(frameon=False, loc='upper left', bbox_to_anchor=(1.05, 1))

# Improving overall layout and saving the figures
plt.tight_layout()
plt.subplots_adjust(right=0.8)  # Adjust subplot to fit legends
plt.savefig("figures/catalogue.pdf")
plt.savefig("figures/catalogue.jpeg")
plt.show()
