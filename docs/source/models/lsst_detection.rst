LSST Detection Response
=========================

.. list-table:: LSST Detection Model
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
  * - parentDiaSourceId
    - integer
    - Parent DiaSource identifier for associated detections
  * - psfFlux
    - number
    - PSF flux measurement [nJy]
  * - psfFluxErr
    - number
    - 1-sigma uncertainty in psfFlux [nJy]
  * - psfFlux_flag
    - boolean
    - General flag for PSF flux measurement
  * - psfFlux_flag_edge
    - boolean
    - Flag indicating if PSF flux measurement is near image edge
  * - psfFlux_flag_noGoodPixels
    - boolean
    - Flag indicating if PSF flux measurement has no good pixels