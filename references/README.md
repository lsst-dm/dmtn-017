# Summary of References on DCR #

1. [Report on Summer 2014 Production: Analysis of DCR (Andy Becker)](https://github.com/lsst-dm/S14DCR/blob/master/report/S14report_V0-00.pdf)

    * Estimated DCR effects directly for LSST using catSim's stellar
	  SEDs.
    * Investigated only airmass effects (no temperature,
	  etc. dependence).
    * Summmary of DCR estimates:
        - For *g* and *r*, nearly all stars will exhibit differential DCR
	      of > 5 mas at parallactic angle differences > 20 deg. or airmass
	      differences of > 0.15.
	    - For *i*, similar effects for parallactic angle differences > 25
	      deg. or airmass differences > 0.2, mostly for M-dwarf stars.
	    - For *z*, only very large differences in parallactic angle or
          airmass lead to DCR > 5 mas.
	* DCR corrections tested based on modeling using colors and airmass
      terms.
	    - Random forest regression models provided most accurate
          modeling of DCR and refraction.
		- *u* and *g* models worked but would be degraded by 10% color
          errors (*u*) or 2.5% color errors (*g*).
		- *riz* models could correct all but 10<sup>-5</sup> stars to
          < 5 mas residuals.
	* **Recommendations**:
	    - Code provided [here](https://github.com/lsst-dm/S14DCR)
		  should be updated to use latest version of sims_photUtils
		  and include estimates for galaxies and SNe.
		- Potentially merge capabilities of SED and Bandpass in
          sims_photUtils with those from
          [chroma](https://github.com/DarkEnergyScienceCollaboration/chroma/);
          see below.
		- Incorporate DCR calcs into sims pipeline to enable effects
          of DCR corrections on image coadds and differences (see also
          [here](https://github.com/lsst-dm/W14ImageDifferencing)).

2. Meyers and Burchat (2015).
    * Estimates of DCR on weak lensing measurements.
	* Source code for analysis is [available](https://github.com/DarkEnergyScienceCollaboration/chroma/).
	* Primarily measured effects of DCR on shape measurements (2nd
      moments); code can be used to estimate 1st moments for a given
      SED. [Preliminary code](https://github.com/isullivan/LSST-DCR/tree/master/code/notebooks).