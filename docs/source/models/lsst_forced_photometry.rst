LSST Forced Photometry Response
==================================

.. list-table:: LSST Forced Photometry Model
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
  * - visit
    - integer
    - Visit identifier for the observation
  * - detector
    - integer
    - Detector identifier within the focal plane
  * - psfFlux
    - number
    - Forced PSF flux measurement [nJy]
  * - psfFluxErr
    - number
    - 1-sigma uncertainty in psfFlux [nJy]