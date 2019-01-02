Argentine Daily Weather Reports 1902 (Version 0.0.3)
====================================================

.. warning::

   These data should be used with caution. 11 stations have known date problems, and two have no known location. The others look OK, but little QC has been done.

The `Daily Weather Reports <https://www.metoffice.gov.uk/learning/library/archive-hidden-treasures/daily-weather-reports>`_ (DWR), were started by the UK in 1860. The idea spread rapidly to other countries, and Argentina started issuing its own DWRs in 1902.

The Argentine DWRs are being scanned, `put online <http://data.ceda.ac.uk/badc/corral/images/metobs/south_america/Argentina/>`_, and transcribed, as part of the Argentine capacity-building program of the `Copernicus C3S Data Rescue Service <http://ensembles-eu.metoffice.com/C3S-DR/index_C3SDR.html>`_, led by `Pablo Canziani <http://conicet.academia.edu/PabloCanziani>`_. The transcription was done by `Jürg Luterbacher <https://www.uni-giessen.de/faculties/f07/geography/sections/climate/staff/luterbacher>`_ and his team at the `University of Giessen <http://www.uni-giessen.de/welcome>`_. So far we only have transcribed data for the first year: 1902. The data are reported once a day from each station, but many stations have many days of missing data.

The precipitation data in the source documents was not transcribed. The wind speed data is in non-standard units. So this version includes only the mean-sea-level pressure; instantanious, daily maximum, and daily minimum temperatures (dry bulb); and relative humidity. 

Transcribed observations
------------------------

* As-received `Excel file <https://github.com/philip-brohan/station-data/blob/master/ToDo/sources/Argentinian_DWR/raw_data/South_America_1902.xlsx>`_. 
* `individual csv files for each of the 124 stations included <https://github.com/philip-brohan/station-data/tree/master/ToDo/sources/Argentinian_DWR/raw_data>`_ split from the .xlsx file using `ssconvert <https://linux.die.net/man/1/ssconvert>`_.

Station metadata was created for each station:

.. toctree::
   :maxdepth: 1

   Standard name <names>
   Estimated location <Positions>

The raw data for each station was converted into `SEF files <http://brohan.org/SEF>`_:

.. toctree::
   :maxdepth: 1

   Conversion scripts <conversion_scripts>

* `SEF files <https://github.com/philip-brohan/station-data/tree/master/ToDo/sef/Argentinian_DWR/1902>`_


Individual stations that look OK
--------------------------------

.. toctree::
   :maxdepth: 1

   auto_stations/DWR_9_de_Julio/index
   auto_stations/DWR_Abra_Pampa/index
   auto_stations/DWR_Acha_Pampa/index
   auto_stations/DWR_Andalgala/index
   auto_stations/DWR_Arias/index
   auto_stations/DWR_Arroyitos/index
   auto_stations/DWR_Arroyitos_Nq/index
   auto_stations/DWR_Asuncion_Pgy/index
   auto_stations/DWR_Azul_BA/index
   auto_stations/DWR_B._Mitre/index
   auto_stations/DWR_B._Parada/index
   auto_stations/DWR_Bahia_Blanca/index
   auto_stations/DWR_Balcarce/index
   auto_stations/DWR_Bernasconi/index
   auto_stations/DWR_Bolivar/index
   auto_stations/DWR_Burruyacu/index
   auto_stations/DWR_C._Rivadavia/index
   auto_stations/DWR_Cabo_Blanco/index
   auto_stations/DWR_Cabo_Raso/index
   auto_stations/DWR_Caleta_Oliv./index
   auto_stations/DWR_Camarones/index
   auto_stations/DWR_Canada_Verde/index
   auto_stations/DWR_Capital_Fed./index
   auto_stations/DWR_Carcarana/index
   auto_stations/DWR_Catamarca-Cp/index
   auto_stations/DWR_Ceres/index
   auto_stations/DWR_Chaco-La_Sb./index
   auto_stations/DWR_Chilecito/index
   auto_stations/DWR_Chilecito_Rj/index
   auto_stations/DWR_Chivilcoy/index
   auto_stations/DWR_Choele_Choel/index
   auto_stations/DWR_Chubut-Mdryn/index
   auto_stations/DWR_Concep.-Tuc./index
   auto_stations/DWR_Conesa/index
   auto_stations/DWR_Cordoba-Cap./index
   auto_stations/DWR_Coronel_Prg./index
   auto_stations/DWR_Corrientes-C/index
   auto_stations/DWR_Curuzu-Cuat./index
   auto_stations/DWR_Delicias_ER/index
   auto_stations/DWR_Dique_Sn_Rq/index
   auto_stations/DWR_Dolores/index
   auto_stations/DWR_Dos_Pozos/index
   auto_stations/DWR_Esperanza/index
   auto_stations/DWR_Esquina/index
   auto_stations/DWR_Estc_Pereyra/index
   auto_stations/DWR_Gen_Uriburu/index
   auto_stations/DWR_Gen_Villegas/index
   auto_stations/DWR_Goya/index
   auto_stations/DWR_Gualeguay/index
   auto_stations/DWR_Guamini/index
   auto_stations/DWR_Humahuaca/index
   auto_stations/DWR_Jujuy-Cap./index
   auto_stations/DWR_Junin_BA/index
   auto_stations/DWR_La_Carlota/index
   auto_stations/DWR_La_Cautiva/index
   auto_stations/DWR_La_Cocha/index
   auto_stations/DWR_La_Plata/index
   auto_stations/DWR_Las_Flores/index
   auto_stations/DWR_Las_Lajas/index
   auto_stations/DWR_Malaspina/index
   auto_stations/DWR_Mar_dl_Plata/index
   auto_stations/DWR_Mendoza-Cap./index
   auto_stations/DWR_N._Huapi/index
   auto_stations/DWR_Necochea/index
   auto_stations/DWR_Neuquen/index
   auto_stations/DWR_Olavarria/index
   auto_stations/DWR_P._Deseado/index
   auto_stations/DWR_Paso_Libres/index
   auto_stations/DWR_Patagones/index
   auto_stations/DWR_Pico_Salama./index
   auto_stations/DWR_Piedra_Agui./index
   auto_stations/DWR_Pilcaneyen/index
   auto_stations/DWR_Posadas_Mis./index
   auto_stations/DWR_Pueblo_Brugo/index
   auto_stations/DWR_Puerto_Mili./index
   auto_stations/DWR_Quiaca/index
   auto_stations/DWR_Quilino/index
   auto_stations/DWR_Rioja-Cap./index
   auto_stations/DWR_Roca_Rio_N./index
   auto_stations/DWR_Rosario/index
   auto_stations/DWR_Rosario_dlF./index
   auto_stations/DWR_Saladillo/index
   auto_stations/DWR_Salta-La_Mcd/index
   auto_stations/DWR_Salta/index
   auto_stations/DWR_San_Blas/index
   auto_stations/DWR_San_Carlos/index
   auto_stations/DWR_San_Jorge/index
   auto_stations/DWR_San_Juan-Cp./index
   auto_stations/DWR_San_L-V._Mcd/index
   auto_stations/DWR_San_Lorenzo/index
   auto_stations/DWR_San_Luis/index
   auto_stations/DWR_San_Martin/index
   auto_stations/DWR_San_Nicolas/index
   auto_stations/DWR_Santa_Cruz/index
   auto_stations/DWR_Santa_Fa-Cp./index
   auto_stations/DWR_Santa_Maria/index
   auto_stations/DWR_Santo_Tome/index
   auto_stations/DWR_Sierra_Grnde/index
   auto_stations/DWR_St._Cruz-Mzd/index
   auto_stations/DWR_Tandil/index
   auto_stations/DWR_Trancas/index
   auto_stations/DWR_Tratayen/index
   auto_stations/DWR_Trenque_Lauq/index
   auto_stations/DWR_Tres_Arroyos/index
   auto_stations/DWR_Tucman-Captl/index
   auto_stations/DWR_Tumbaya/index
   auto_stations/DWR_Vera/index
   auto_stations/DWR_Villa_Maria/index
   auto_stations/DWR_Villa_Mrced./index
   auto_stations/DWR_Villaguay/index
   auto_stations/DWR_Zarate/index
   
  
Additional stations with no known locations
-------------------------------------------

.. toctree::
   :maxdepth: 1

   auto_stations/DWR_Rio_Quartro/index
   auto_stations/DWR_Ytaybate/index

Additional stations with known data problems (bad dates in the as-digitised files)
----------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 1

   auto_stations/DWR_Cabo_Alarcon/index
   auto_stations/DWR_Concep.-Mis./index
   auto_stations/DWR_Concordia/index
   auto_stations/DWR_Formosa_Arg./index
   auto_stations/DWR_Junin/index
   auto_stations/DWR_Recreo/index
   auto_stations/DWR_Rio_Cuarto/index
   auto_stations/DWR_San_Antonio/index
   auto_stations/DWR_Tinogasta/index
   auto_stations/DWR_Uruguay/index
   auto_stations/DWR_V._Casilda/index

