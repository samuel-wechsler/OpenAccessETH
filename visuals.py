import numpy as np
from matplotlib.gridspec import GridSpec
from brokenaxes import brokenaxes
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# establish connection to SQL database
db_path = "lecture_data.db"
conn = sqlite3.connect(db_path)

# query to obtain accessible vs recorded lectures by department
portal_department_qry = '''
    SELECT department,
            SUM(CASE WHEN access = 1 THEN 1 ELSE 0 END) AS accessible_count,
            COUNT(*) AS total_count
    FROM lectures WHERE year < 2024
    GROUP BY department
'''

# query to obtain accessible vs recorded lecture by year
portal_year_qry = '''
    SELECT year,
            SUM(CASE WHEN access = 1 THEN 1 ELSE 0 END) AS accessible_count,
            COUNT(*) AS total_count
    FROM lectures WHERE year < 2024
    GROUP BY year
    ORDER BY year
'''

# qry to obtain total number of lectures registered in ETH course catalogue by year
catalogue_qry = '''
    SELECT year, COUNT(*) AS total_count
    FROM catalogue WHERE year < 2024
    GROUP BY year
    ORDER BY year
'''

# execute queries and convert to DataFrames
portal_department_data = pd.read_sql(portal_department_qry, conn)
portal_year_data = pd.read_sql(portal_year_qry, conn)
catalogue_data = pd.read_sql(catalogue_qry, conn)


# Compute fraction of accessible recordings by department
portal_department_data['accessible_fraction'] = portal_department_data['accessible_count'] / \
    portal_department_data['total_count']

portal_department_data = portal_department_data.sort_values(
    # department data according to descending accessibility
    by='accessible_fraction', ascending=False
)

# enforce upper case on department names
portal_department_data['department'] = portal_department_data['department'].str.upper()

# Compute fraction of accessible recordings by year
portal_year_data['accessible_fraction'] = portal_year_data['accessible_count'] / \
    portal_year_data['total_count']

# caculate fraction of series uploaded, public
catalogue_data['uploaded_fraction'] = portal_year_data['total_count'] / \
    catalogue_data['total_count']
catalogue_data['accessible_fraction'] = portal_year_data['accessible_count'] / \
    catalogue_data['total_count']

## Create plots of data ##
# standardize colors for consistency
colors = {
    'catalogue': 'mediumpurple',
    'portal': 'salmon',
    'accessible': 'skyblue'
}

# Figure 1: illustrate data collected from video.ethz.ch #
# Create figure and axes
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Plot A: Department vs. Fraction of Accessible Lecture Series
axes[0, 0].bar(portal_department_data['department'],
               portal_department_data['accessible_fraction'],
               color="mediumpurple",
               edgecolor="black",
               label="Accessible")

axes[0, 0].set_xlabel('Department')
axes[0, 0].set_ylabel('Fraction of Accessible Lecture Series')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[0, 0].text(-0.1, 1.1, 'A', transform=axes[0, 0].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')

# Plot B: Department vs Total number of lectures uploaded
axes[0, 1].bar(portal_department_data["department"],
               portal_department_data["total_count"],
               color=colors['portal'],
               edgecolor="black",
               label="restricted")

axes[0, 1].bar(portal_department_data['department'],
               portal_department_data['accessible_count'],
               color=colors['accessible'],
               edgecolor='black',
               label="accessible")

axes[0, 1].set_xlabel('Department')
axes[0, 1].set_ylabel('Total Number of Lecture Series')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[0, 1].text(-0.1, 1.1, 'B', transform=axes[0, 1].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')
axes[0, 1].legend(loc='upper left', frameon=False)

# Plot C: year vs accessible fraction
axes[1, 0].bar(portal_year_data['year'],
               portal_year_data['accessible_fraction'],
               color='mediumpurple',
               edgecolor='black',
               label='Accessible')

axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('Fraction of Accessible Lecture Series')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[1, 0].text(-0.1, 1.1, 'C', transform=axes[1, 0].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')

# Plot D: Year vs lectures uploaded
axes[1, 1].bar(portal_year_data['year'],
               portal_year_data['total_count'],
               color=colors['portal'],
               edgecolor='black',
               label="restricted")

axes[1, 1].bar(portal_year_data['year'],
               portal_year_data['accessible_count'],
               color=colors['accessible'],
               edgecolor='black',
               label="accessible")

axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Number of Lecture Series Uploaded')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(True, which='both', linestyle='--',
                linewidth=0.5, alpha=0.5, zorder=0)
axes[1, 1].text(-0.1, 1.1, 'D', transform=axes[1, 1].transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')
axes[1, 1].legend(loc='upper left', frameon=False)

plt.tight_layout()
plt.savefig("figures/portal.pdf")
plt.savefig("figures/portal.jpeg")


# Figure 2: compare portal data to course catalogue (=reference for total lecture output) #
# create the plot layout

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.subplots_adjust(right=0.80, bottom=0.15)

axes[0].grid(True, which='both', linestyle='--',
             linewidth=0.5, alpha=0.5, zorder=0)
axes[0].tick_params(axis='x', rotation=45)
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Total Number of Lecture Series at ETH")

axes[0].bar(catalogue_data['year'],
            catalogue_data['total_count'],
            color=colors['catalogue'],
            edgecolor='black',
            label='Course Catalogue')

axes[0].bar(portal_year_data['year'],
            portal_year_data['total_count'],
            color=colors['portal'],
            edgecolor='black',
            label='Video Portal (Total)')

axes[0].bar(portal_year_data['year'],
            portal_year_data['accessible_count'],
            color=colors['accessible'],
            edgecolor='black',
            label='Video Portal (Accessible)')
axes[0].text(-0.1, 1.1, 'A', transform=axes[0].transAxes,
             fontsize=16, fontweight='bold', va='top', ha='right')

# axes[0].legend(loc='upper left', frameon=False)

# Plot B: Fraction of lectures recorded and publicly uploaded
axes[1].grid(True, which='both', linestyle='--',
             linewidth=0.5, alpha=0.5, zorder=0)
axes[1].set_xlabel("Year")
axes[1].set_ylabel(
    "Fraction of Respective Lecture Type")
axes[1].tick_params(axis='x', rotation=45)

axes[1].bar(catalogue_data['year'],
            catalogue_data['uploaded_fraction'],
            color=colors['portal'],
            edgecolor='black',
            label='Fraction uploaded')
axes[1].bar(catalogue_data['year'],
            catalogue_data['accessible_fraction'],
            color=colors['accessible'],
            edgecolor='black',
            label="Fraction accessible")
# axes[1].legend(loc='upper left', frameon=False)
axes[1].text(-0.1, 1.1, 'B', transform=axes[1].transAxes,
             fontsize=16, fontweight='bold', va='top', ha='right')

# Create a common legend for both subplots
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right',
           bbox_to_anchor=(1.0, 0.9), frameon=False, ncol=1)

plt.savefig("figures/catalogue.pdf")
plt.savefig("figures/catalogue.jpeg")
plt.show()
