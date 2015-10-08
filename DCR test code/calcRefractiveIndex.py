import numpy as np

def p_s(atmospheric_pressure, water_vapor_pressure = 0.02):
#
# both atmospheric_pressure and water_vapor_pressure are input in atmospheres.
# output is converted to millibars
#

	effective_pressure = 760. * 1.333224 * (atmospheric_pressure - water_vapor_pressure)

	return effective_pressure


def p_w(water_vapor_pressure = 0.02):
	water_vapor_pressure_millibar = 760. * 1.333224 * water_vapor_pressure
	return water_vapor_pressure_millibar


def d_s(atmospheric_pressure, water_vapor_pressure, temperature):
	# calculate dry air pressure term to refractive index calculation
	T_use = 273.15 + temperature

	eqn_1 = (1. + p_s(atmospheric_pressure, water_vapor_pressure) * 
		(57.90E-8 - (9.3250E-4 / T_use) + (0.25844 / np.power(T_use, 2.))))

	return eqn_1 * p_s(atmospheric_pressure, water_vapor_pressure) / T_use


def d_w(water_vapor_pressure, temperature):
	# calculate water vapor pressure term to refractive index calculation
	T_use =	273.15 + temperature

	eqn_1 = (-2.37321E-3 + (2.23366 / T_use) - (710.792 / np.power(T_use, 2.)) + 
			(7.75141E-4 / np.power(T_use, 3.)))
	eqn_2 = 1. + p_w(water_vapor_pressure) * (1. + 3.7E-4 * p_w(water_vapor_pressure)) * eqn_1

	return eqn_2 * p_w(water_vapor_pressure) / T_use


def n_delta(wavelength, atmospheric_pressure, water_vapor_pressure, temperature):
	# calculate difference of refractive index of air from 1, multiplied by 1E8

	# want wave number in units 1/micron
	# wavelength is input in nm
	wave_num = 1E3 / wavelength

	dry_air = (2371.34 + (683939.7 / (130. - np.power(wave_num, 2.))) + 
			  (4547.3 / (38.9 - np.power(wave_num, 2.))))

	wet_air = (6487.31 + 58.058 * np.power(wave_num, 2.) + 
			  -0.71150 * np.power(wave_num, 4.) +0.08851 * np.power(wave_num, 6.))

	#print(dry_air, d_s(atmospheric_pressure, water_vapor_pressure, temperature))
	#print(wet_air, d_w(water_vapor_pressure, temperature))
	return (dry_air * d_s(atmospheric_pressure, water_vapor_pressure, temperature) +
		    wet_air * d_w(water_vapor_pressure, temperature))


def refraction(zenith_angle, wavelength, atmospheric_pressure, water_vapor_pressure, 
	temperature, latitude = -30.244639, altitude = 2663.):
	
	reduced_n = n_delta(wavelength, atmospheric_pressure, water_vapor_pressure, temperature) * 1E-8

	atmos_scale = 0.001254 * ((273.15 + temperature) / 273.15) # eqn 9 of Stone 1996
	relative_gravity = (1. + 0.005302 * np.sin(np.radians(latitude))**2. + 
		-0.00000583 * np.sin(np.radians(2.*latitude))**2. - 0.000000315 * altitude)

	tanZ = np.tan(np.radians(zenith_angle))

	atmos_term_1 = reduced_n * relative_gravity * (1. - atmos_scale) 
	atmos_term_2 = reduced_n * relative_gravity * (atmos_scale - reduced_n / 2.) 
	
	if (type(zenith_angle) == np.ndarray) and (type(temperature) == np.ndarray):
		atmos_term_1 = np.matrix(atmos_term_1)
		atmos_term_2 = np.matrix(atmos_term_2)
		tanZ = np.matrix(tanZ)

		result = np.array(atmos_term_1.T * tanZ + atmos_term_2.T * np.power(tanZ, 3.))
	else:
		result = atmos_term_1 * tanZ + atmos_term_2 * np.power(tanZ, 3.)


	return np.degrees(result)



def diff_refraction(zenith_angle, wavelength, bandwidth = None, atmospheric_pressure = 1., 
	water_vapor_pressure = 0.02, temperature = 20. , latitude = -30.244639, altitude = 2663.):
	
	if bandwidth is None: 
		bandwidth = wavelength / 4.
	wavelength_start = wavelength - bandwidth / 2.
	wavelength_end = wavelength + bandwidth / 2.

	refraction_start = refraction(zenith_angle, wavelength_start, atmospheric_pressure, water_vapor_pressure,
		temperature, latitude, altitude)
	refraction_end = refraction(zenith_angle, wavelength_end, atmospheric_pressure, water_vapor_pressure,
		temperature, latitude, altitude)

	return refraction_start - refraction_end	