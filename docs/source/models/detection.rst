Detection Response
=========================

.. list-table:: Detection Response Model
  :widths: 20 10 70
  :header-rows: 1

  * - Name
    - Type
    - Description
  * - mjd
    - number
    - Modified julian Date
  * - candid
    - string
    - Alert unique identifier.
  * - fid
    - integer
    - Filter ID (1=g; 2=r; 3=i)
  * - pid
    - integer
    - Processing ID for image
  * - diffmaglim
    - number
    - 5-sigma mag limit in difference image based on PSF-fit photometry [mag]
  * - isdiffpos
    - number
    - 1: candidate is from positive (sci minus ref) subtraction; -1: didate is from negative (ref minus sci) subtraction
