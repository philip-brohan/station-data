Argentine Daily Weather Reports 1902: Comparing with 20CR
=========================================================

It's helpful to separate comparing station data with 20CR into two steps:

* Get the 20CRv3 data at the time and location of the station observations
* Make the comparison with the new obs.

This page documents the first step. It uses the `IRData <http://brohan.org/IRData/>`_ library to handle the 20CR data

Get the 20CRv3 data at one time-point
-------------------------------------

Extracts 20CRv3 data at one point in time and pickles comparators at the location of each station.

.. literalinclude:: ../../../../ToDo/sources/Argentinian_DWR/analyses/20CRv3_comparisons/get_comparators.py


Run the script above for all time-points in a year
--------------------------------------------------

.. literalinclude:: ../../../../ToDo/sources/Argentinian_DWR/analyses/20CRv3_comparisons/make_all_comparators.py

This script makes the list of commands needed to do all the extractions, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.
