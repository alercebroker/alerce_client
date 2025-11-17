
Forced Photometry Response
==========================

.. list-table:: Forced Photometry Response Model
  :widths: 20 10 70
  :header-rows: 1

  * - Name
    - Type
    - Description
  * - pid
    - integer
    - Processing ID for image
  * - mjd
    - number
    - Modified julian Date
  * - fid
    - integer
    - Filter ID (1=g; 2=r; 3=i)
  * - ra
    - number
    - Right Ascension of epoch (same as of candidate) [deg]
  * - dec
    - number
    - Declination of epoch (same as of candidate) [deg]
  * - e_ra
    - number
    - Right Ascension uncertainty
  * - e_dec
    - number
    - Declination uncertainty
  * - mag
    - number
    - Magnitude from PSF-fit photometry [mag], obtained from magzpsci and forcediffimflux avro fields
  * - e_mag
    - number
    - 1-sigma uncertainty in mag [mag], obtained from forcediffimflux and forcediffimfluxunc avro fields
  * - mag_corr
    - number
    - Corrected PSF magnitude
  * - e_mag_corr
    - number
    - Error of the corrected PSF magnitude assuming no contribution from an extended component
  * - e_mag_corr_ext
    - number
    - Error of the corrected PSF magnitude assuming a contribution from an extended component
  * - isdiffpos
    - integer
    - 1: candidate is from positive (sci minus ref) subtraction; -1: didate is from negative (ref minus sci) subtraction
  * - corrected
    - boolean
    - Whether the corrected photometry was applied
  * - dubious
    - boolean
    - Whether the corrected photometry should be flagged
  * - parent_candid
    - number
    - candid of the alert for which forced photometry was triggered
  * - has_stamp
    - boolean
    - Whether the epoch has an associated image stamp triplet (always False for forced photometry)
  * - field
    - integer
    - ZTF field ID
  * - rcid
    - integer
    - Readout channel ID [00 .. 63]
  * - rfid
    - integer
    - Processing ID for reference image to facilitate archive retrieval
  * - sciinpseeing
    - number
    - Effective FWHM of sci image [pixels]
  * - scibckgnd
    - number
    - Background level in sci image [DN]
  * - scisigpix
    - number
    - Robust sigma per pixel in sci image [DN]
  * - magzpsci
    - number
    - Magnitude zero point for photometry estimates [mag]
  * - magzpsciunc
    - number
    - Magnitude zero point uncertainty (in magzpsci) [mag]
  * - magzpscirms
    - number
    - RMS (deviation from average) in all differences between instrumental photometry and matched photometric calibrators from science image processing [mag]
  * - clrcoeff
    - number
    - Color coefficient from linear fit from photometric calibration of science image
  * - clrcounc
    - number
    - Color coefficient uncertainty from linear fit (corresponding to clrcoeff)
  * - exptime
    - number
    - Integration time of camera exposure [sec]
  * - adpctdif1
    - number
    - Full sci image astrometric RMS along R.A. with respect to Gaia1 [arcsec]
  * - adpctdif2
    - number
    - Full sci image astrometric RMS along Dec. with respect to Gaia1 [arcsec]
  * - diffmaglim
    - number 
    - Expected 5-sigma mag limit in difference image based on global noise estimate [mag]
  * - programid
    - integer
    - Program ID: encodes either public, collab, or caltech mode
  * - procstatus
    - string
    - Forced photometry processing status codes (0 => no warnings); see documentation
  * - distnr
    - number
    - distance to nearest source in reference image PSF-catalog [arcsec]
  * - ranr
    - number
    - Right Ascension of nearest source in reference image PSF-catalog; J2000 [deg]
  * - decnr
    - number
    - Declination of nearest source in reference image PSF-catalog; J2000 [deg]
  * - magnr
    - number
    - magnitude of nearest source in reference image PSF-catalog [mag]
  * - sigmagnr
    - number
    - 1-sigma uncertainty in magnr [mag]    
  * - chinr
    - number
    - DAOPhot chi parameter of nearest source in reference image PSF-catalog
  * - sharpnr
    - number 
    - DAOPhot sharp parameter of nearest source in reference image PSF-catalog