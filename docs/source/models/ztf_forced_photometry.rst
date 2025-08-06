ZTF Forced Photometry Response
=================================

.. list-table:: ZTF Forced Photometry Model
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
  * - mag
    - number
    - Forced photometry magnitude [mag]
  * - e_mag
    - number
    - 1-sigma uncertainty in magnitude [mag]
  * - mag_corr
    - number
    - Corrected forced photometry magnitude [mag]
  * - e_mag_corr
    - number
    - 1-sigma uncertainty in corrected magnitude [mag]
  * - e_mag_corr_ext
    - number
    - Error of corrected magnitude assuming contribution from extended component [mag]
  * - isdiffpos
    - integer
    - 1: candidate is from positive subtraction; -1: candidate is from negative subtraction
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
  * - field
    - integer
    - ZTF field identifier
  * - rcid
    - integer
    - Readout channel ID
  * - rfid
    - integer
    - Processing ID for reference image to facilitate archive retrieval
  * - sciinpseeing
    - number
    - Effective FWHM of PSF in science image [arcsec]
  * - scibckgnd
    - number
    - Background flux in science image [DN]
  * - scisigpix
    - number
    - Robust sigma per pixel in science image [DN]
  * - magzpsci
    - number
    - Magnitude zero point for photometry in science image [mag]
  * - magzpsciunc
    - number
    - Uncertainty in magzpsci [mag]
  * - magzpscirms
    - number
    - RMS scatter in magzpsci [mag]
  * - clrcoeff
    - number
    - Color coefficient from linear fit
  * - clrcounc
    - number
    - Uncertainty in clrcoeff
  * - exptime
    - number
    - Exposure time [sec]
  * - adpctdif1
    - number
    - Adaptative moment 1st order diff image
  * - adpctdif2
    - number
    - Adaptative moment 2nd order diff image
  * - diffmaglim
    - number
    - 5-sigma mag limit in difference image [mag]
  * - programid
    - integer
    - Program ID
  * - procstatus
    - string
    - Processing status for image
  * - distnr
    - number
    - Distance to nearest source in reference image PSF-catalog [arcsec]
  * - ranr
    - number
    - Right Ascension of nearest source in reference image [deg]
  * - decnr
    - number
    - Declination of nearest source in reference image [deg]
  * - magnr
    - number
    - Magnitude of nearest source in reference image [mag]
  * - sigmagnr
    - number
    - 1-sigma uncertainty in magnr [mag]
  * - chinr
    - number
    - DAOPhot chi parameter of nearest source in reference image
  * - sharpnr
    - number
    - DAOPhot sharp parameter of nearest source in reference image