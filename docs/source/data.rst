Data Module
===========

The ``data`` module provides functions for loading coal plant datasets and network graphs.

For detailed information on the data sources, dataset construction, aggregation methods, and preprocessing choices, please refer to our `Supporting Information <https://static-content.springer.com/esm/art%3A10.1038%2Fs41560-025-01871-0/MediaObjects/41560_2025_1871_MOESM1_ESM.pdf>`_.

.. automodule:: retire.data.data
   :members:
   :undoc-members:
   :show-inheritance:

Data Loading Functions
---------------------

Coal Plant Datasets
~~~~~~~~~~~~~~~~~~

.. autofunction:: retire.data.data.load_dataset
.. autofunction:: retire.data.data.load_clean_dataset
.. autofunction:: retire.data.data.load_projection
.. autofunction:: retire.data.data.load_generator_level_dataset

Graph and Network Data
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: retire.data.data.load_graph

Data Utilities
-------------

These functions help with processing and managing the datasets:

.. autofunction:: retire.data.data.get_data_path
.. autofunction:: retire.data.data.get_resource_path
