ZTF Detection Response
=========================

.. list-table:: ZTF Detection Model
  :widths: 20 10 70
  :header-rows: 1

  * - Name
    - Type
    - Description
  * - oid
    - integer
    - Object identifier
  * - measurement_id
    - integer
    - Measurement unique identifier
  * - pid
    - integer
    - Processing ID for image
  * - diffmaglim
    - number
    - 5-sigma mag limit in difference image based on PSF-fit photometry [mag]
  * - isdiffpos
    - integer
    - 1: candidate is from positive (sci minus ref) subtraction; -1: candidate is from negative (ref minus sci) subtraction
  * - nid
    - integer
    - Night ID
  * - magpsf
    - number
    - Magnitude from PSF-fit photometry [mag]
  * - sigmapsf
    - number
    - 1-sigma uncertainty in magpsf [mag]
  * - magap
    - number
    - Aperture mag using 8 pixel diameter aperture [mag]
  * - sigmagap
    - number
    - 1-sigma uncertainty in magap [mag]
  * - distnr
    - number
    - Distance to nearest source in reference image PSF-catalog within 30 arcsec [pixels]
  * - rb
    - number
    - RealBogus quality score; range is 0 to 1 where closer to 1 is more reliable
  * - rbversion
    - string
    - Version of RealBogus model/classifier used to assign rb quality score
  * - drb
    - number
    - RealBogus quality score from Deep-Learning-based classifier; range is 0 to 1 where closer to 1 is more reliable
  * - drbversion
    - string
    - Version of Deep-Learning-based classifier model used to assign RealBogus (drb) quality score
  * - magapbig
    - number
    - Aperture mag using 18 pixel diameter aperture [mag]
  * - sigmagapbig
    - number
    - 1-sigma uncertainty in magapbig [mag]
  * - rfid
    - integer
    - Processing ID for reference image to facilitate archive retrieval
  * - magpsf_corr
    - integer
    - Corrected PSF magnitude
  * - sigmapsf_corr
    - integer
    - Error of the corrected PSF magnitude assuming no contribution from an extended component
  * - sigmapsf_corr_ext
    - integer
    - Error of the corrected PSF magnitude assuming a contribution from an extended component
  * - corrected
    - boolean
    - Whether the corrected photometry was applied
  * - dubious
    - boolean
    - Whether the corrected photometry should be flagged
  * - parent_candid
    - integer
    - Parent candid if alert coming from prv_detection (null if no parent)
  * - has_stamp
    - boolean
    - Whether the detection has an associated image stamp triplet