Magstats Response
=========================

.. list-table:: Magstats Response Model
  :widths: 20 10 70
  :header-rows: 1

  * - Name
    - Type
    - Description
  * - fid
    - integer
    - Filter ID (1=g; 2=r; 3=i)
  * - stellar
    - boolean
    - Whether the object appears to be unresolved in the given band
  * - corrected
    - boolean
    - Whether the corrected photometry should be used
  * - ndet
    - integer
    - Number of detections in the given band
  * - ndubious
    - integer
    - Number of dubious corrections
  * - dmdt_first
    - number
    - Initial rise estimate, the maximum slope between the first detection and any previous non-detection
  * - dm_first
    - number
    - The magnitude difference used to compute dmdt_first
  * - sigmadm_first
    - number
    - The error of the magnitude difference used to compute dmdt_first
  * - dt_first
    - number
    - The time difference used to compute dmdt_first
  * - magmean
    - number
    - The mean magnitude for the given fid
  * - magmedian
    - number
    - The median magnitude for the given fid
  * - magmax
    - number
    - The max magnitude for the given fid
  * - magmin
    - number
    - The min magnitude for the given fid
  * - magsigma
    - number
    - Magnitude standard deviation for the given fid
  * - maglast
    - number
    - The last magnitude for the given fid
  * - magfirst
    - number
    - The first magnitude for the given fid
  * - magmean_corr
    - number
    - The mean corrected magnitude for the given fid
  * - magmedian_corr
    - number
    - The median corrected magnitude for the given fid
  * - magmax_corr
    - number
    - The max corrected magnitude for the given fid
  * - magmin_corr
    - number
    - The min corrected magnitude for the given fid
  * - magsigma_corr
    - number
    - Corrected magnitude standard deviation for the given fid
  * - maglast_corr
    - number
    - The last corrected magnitude for the given fid
  * - magfirst_corr
    - number
    - The first corrected magnitude for the given fid
  * - firstmjd
    - number
    - The time of the first detection in the given fid
  * - lastmjd
    - number
    - The time of the last detection in the given fid
  * - step_id_corr
    - string
    - Correction step pipeline version
