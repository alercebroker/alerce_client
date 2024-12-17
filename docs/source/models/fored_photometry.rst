Forced Photometry Response
=========================

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
    - Description
  * - fid
    - integer
    - Filter ID (1=g; 2=R; 3=i)
  * - ra
    - number
    - Description
  * - dec
    - number
    - Description
  * - e_ra
    - number
    - Description
  * - e_dec
    - number
    - Description
  * - mag
    - number
    - Description
  * - e_mag
    - number
    - Description
  * - e_mag_corr
    - number
    - Description
  * - e_mag_corr_ext
    - number
    - Description
  * - isdiffpos
    - integer
    - Description
  * - corrected
    - boolean
    - Description
  * - dubious
    - boolean
    - Description
  * - parent_candid
    - number
    - Description
  * - has_stamp
    - boolean
    - Description
  * - field
    - integer
    - Description
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
    - DescriptionMagnitude zero point uncertainty (in magzpsci) [mag]
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