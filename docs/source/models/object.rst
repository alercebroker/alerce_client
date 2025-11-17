.. _object response:

Object Response
======================

.. list-table:: Object Response Model
   :widths: 20 10 70
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - oid
     - string
     - ZTF Object identifier
   * - ndethist
     - string
     - Number of spatially-coincident detections falling within 1.5 arcsec going back to beginning of survey; only detections that fell on the same field and readout-channel ID where the input candidate was observed are counted. All raw detections down to a photometric S/N of ~ 3 are included.
   * - ncovhist
     - integer
     - Number of times input candidate position fell on any field and readout-channel going back to beginning of survey
   * - mjdstarthist
     - number
     - Earliest Modified Julian date of epoch corresponding to ndethist [days]
   * - mjdendhist
     - number
     - Latest Modified Julian date of epoch corresponding to ndethist [days]
   * - corrected
     - boolean
     - Whether the corrected light curve was computed and can be used
   * - stellar
     - boolean
     - Whether the object is a likely stellar-like source
   * - ndet
     - integer
     - Total number of detections for the object
   * - g_r_max
     - number
     - Difference between the minimum g and r band difference magnitudes ( min(g) - min(r) )
   * - g_r_max_corr
     - number
     - Difference between the minimum g and r band corrected magnitudes  ( min(corrected(g)) - min(corrected(r)) )
   * - g_r_mean
     - number
     - Difference between the mean g and r band difference magnitudes ( mean(g) - mean(r) )
   * - g_r_mean_corr
     - number
     - Difference between the mean g and r band corrected magnitudes ( mean(corrected(g)) - mean(corrected(r)) )
   * - firstmjd
     - number
     - First detection's modified julian date
   * - lastmjd
     - number
     - Last detection's modified julian date
   * - deltajd
     - number
     - Difference between last and first detection date
   * - meanra
     - number
     - Mean Right Ascension
   * - meandec
     - number
     - Mean Declination
   * - sigmara
     - number
     - Right Ascension standard deviation
   * - sigmadec
     - number
     - Declination standard deviation
   * - class
     - string
     - Highest probability class or according to specified classifier and ranking (Default classifier: *lc_classifier*, ranking: 1)
   * - classifier
     - string
     - Classifier name.
   * - probability
     - number
     - Highest probability or according to specified classifier and ranking (Default classifier: *lc_classifier*, ranking: 1)
   * - step_id_corr
     - string
     - CorrectionStep pipeline version.
