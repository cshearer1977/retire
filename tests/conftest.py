# tests/conftest.py
"""
Shared pytest fixtures and configuration for the retire test suite.

This module provides reusable fixtures for testing the retire package,
including sample data, mock objects, and test utilities.
"""

import pytest
import pandas as pd
import networkx as nx
import numpy as np
from unittest.mock import Mock, patch


@pytest.fixture
def sample_raw_df():
    """
    Create a minimal sample DataFrame that mimics the structure of the coal plants dataset.

    Returns
    -------
    pd.DataFrame
        Sample DataFrame with key columns from the coal plants dataset.
    """
    return pd.DataFrame(
        {
            "Plant Name": ["Plant A", "Plant B", "Plant C", "Plant D"],
            "ORISPL": ["12345", "23456", "34567", "45678"],
            "State": ["TX", "CA", "OH", "WV"],
            "LAT": [32.5, 36.8, 40.1, 38.9],
            "LON": [-97.3, -119.4, -82.9, -80.5],
            "Total Nameplate Capacity (MW)": [500.0, 750.0, 300.0, 1200.0],
            "Age": [35, 42, 28, 55],
            "ret_STATUS": [0, 1, 2, 0],
            "Percent Capacity Retiring": [0.0, 0.3, 1.0, 0.0],
            "Number of Coal Generators": [2, 3, 1, 4],
            "Utility Name": [
                "Utility A",
                "Utility B",
                "Utility C",
                "Utility D",
            ],
            "Average Capacity Factor": [0.45, 0.62, 0.38, 0.71],
            "Mapped Fuel Type": ["Coal", "Coal", "Coal", "Coal"],
            "Renewables or Coal": ["renewables", "coal", "coal", "renewables"],
            "Percent difference": [15.2, -8.3, 12.7, 22.1],
            "Retirement Date": [np.nan, 2025.0, 2024.0, np.nan],
            "Date of Last Unit or Planned Retirement": [
                "n/a",
                "2025",
                "2024",
                "n/a",
            ],
            "Estimated percentage who somewhat/strongly oppose setting strict limits on existing coal-fire power plants": [
                65.2,
                42.8,
                71.3,
                58.9,
            ],
        }
    )


@pytest.fixture
def sample_clean_df():
    """
    Create a minimal cleaned/scaled DataFrame for testing.

    Returns
    -------
    pd.DataFrame
        Sample cleaned DataFrame with standardized numeric features.
    """
    np.random.seed(42)  # For reproducible test data
    n_plants = 4

    # Create standardized numeric features
    data = {
        "capacity_scaled": np.random.normal(0, 1, n_plants),
        "age_scaled": np.random.normal(0, 1, n_plants),
        "efficiency_scaled": np.random.normal(0, 1, n_plants),
        "emissions_scaled": np.random.normal(0, 1, n_plants),
        "economic_factor_scaled": np.random.normal(0, 1, n_plants),
    }

    return pd.DataFrame(data)


@pytest.fixture
def sample_graph():
    """
    Create a simple NetworkX graph that mimics the coal plant network structure.

    Returns
    -------
    nx.Graph
        Sample graph with nodes representing plant clusters and realistic attributes.
    """
    G = nx.Graph()

    # Add nodes with membership attributes (indices into the raw_df)
    G.add_node("cluster_0", membership=[0, 1], cluster_id=0)
    G.add_node("cluster_1", membership=[2], cluster_id=1)
    G.add_node("cluster_2", membership=[3], cluster_id=2)

    # Add edges with weights
    G.add_edge("cluster_0", "cluster_1", weight=0.75)
    G.add_edge("cluster_1", "cluster_2", weight=0.60)

    return G


@pytest.fixture
def sample_group_analysis():
    """
    Create sample group analysis results DataFrame.

    Returns
    -------
    pd.DataFrame
        Sample group analysis with typical columns and metrics.
    """
    return pd.DataFrame(
        {
            "Group": [0, 1, 2],
            "Plant_Count": [145, 89, 67],
            "Avg_Capacity_MW": [425.3, 678.9, 312.1],
            "Avg_Age_Years": [38.2, 45.7, 32.8],
            "Retirement_Rate": [0.12, 0.34, 0.08],
            "Avg_Emissions_Rate": [2.15, 2.78, 1.92],
        }
    )


@pytest.fixture
def sample_target_explanations():
    """
    Create sample target explanations DataFrame.

    Returns
    -------
    pd.DataFrame
        Sample explanations with plant-level targeting rationale.
    """
    return pd.DataFrame(
        {
            "ORISPL": ["12345", "23456", "34567", "45678"],
            "Plant_Name": ["Plant A", "Plant B", "Plant C", "Plant D"],
            "Priority": ["medium", "high", "high", "low"],
            "Economic_Score": [0.67, 0.89, 0.92, 0.34],
            "Environmental_Score": [0.45, 0.78, 0.83, 0.23],
            "Political_Feasibility": [0.72, 0.56, 0.41, 0.88],
            "Explanation": [
                "Moderate retirement candidate due to age and economics",
                "High priority - poor economics and environmental impact",
                "High priority - environmental justice concerns",
                "Low priority - recent investments and political opposition",
            ],
        }
    )


@pytest.fixture
def mock_resources_path():
    """
    Mock the importlib.resources.files function for testing data loading.

    This fixture can be used to simulate missing files or control
    what data is returned during testing.
    """
    with patch("retire.data.data.files") as mock_files:
        # Create a mock path object
        mock_path = Mock()
        mock_files.return_value.joinpath.return_value = mock_path
        yield mock_path


@pytest.fixture
def temp_csv_file(tmp_path, sample_raw_df):
    """
    Create a temporary CSV file with sample data for testing file I/O.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Pytest's temporary directory fixture
    sample_raw_df : pd.DataFrame
        Sample DataFrame to write to the temp file

    Returns
    -------
    pathlib.Path
        Path to the temporary CSV file
    """
    csv_path = tmp_path / "test_data.csv"
    sample_raw_df.to_csv(csv_path, index=False)
    return csv_path


# Test markers for different types of tests
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "unit: mark test as a unit test (fast, no external dependencies)",
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test (slower, may require external data)",
    )
    config.addinivalue_line(
        "markers",
        "compute: mark test as computationally intensive (skip in CI)",
    )
    config.addinivalue_line(
        "markers",
        "plotting: mark test as involving matplotlib/plotly (may require display)",
    )


# Utility functions for testing
def assert_dataframe_structure(df, expected_columns=None, min_rows=0):
    """
    Assert that a DataFrame has the expected structure.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate
    expected_columns : list, optional
        List of columns that must be present
    min_rows : int, default=0
        Minimum number of rows expected
    """
    assert isinstance(df, pd.DataFrame), "Expected pandas DataFrame"
    assert (
        len(df) >= min_rows
    ), f"Expected at least {min_rows} rows, got {len(df)}"

    if expected_columns:
        missing_cols = set(expected_columns) - set(df.columns)
        assert not missing_cols, f"Missing expected columns: {missing_cols}"


def assert_graph_structure(G, min_nodes=0, min_edges=0):
    """
    Assert that a NetworkX graph has the expected structure.

    Parameters
    ----------
    G : nx.Graph
        Graph to validate
    min_nodes : int, default=0
        Minimum number of nodes expected
    min_edges : int, default=0
        Minimum number of edges expected
    """
    assert isinstance(G, nx.Graph), "Expected NetworkX Graph"
    assert (
        G.number_of_nodes() >= min_nodes
    ), f"Expected at least {min_nodes} nodes, got {G.number_of_nodes()}"
    assert (
        G.number_of_edges() >= min_edges
    ), f"Expected at least {min_edges} edges, got {G.number_of_edges()}"
