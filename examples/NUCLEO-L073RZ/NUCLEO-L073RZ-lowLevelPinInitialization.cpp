/**
 * File generated by:
 * https://github.com/CezaryGapinski/DistortosPinConfigGenerator
 * Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
 *
 * \file
 * \brief Declaration of lowLevelPinInitializations for NUCLEO-L073RZ
 *
 * \author Copyright (C) 2016 Kamil Szczygiel http://www.distortec.com http://www.freddiechopin.info
 * \par License
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
 * distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 */

#include "distortos/board/lowLevelPinInitialization.hpp"

#include "distortos/chip/CMSIS-proxy.h"

namespace distortos
{

namespace board
{

/*---------------------------------------------------------------------------------------------------------------------+
| global functions
+---------------------------------------------------------------------------------------------------------------------*/

void lowLevelPinInitialization()
{
	RCC->IOPENR |=
	RCC_IOPENR_GPIOCEN |
	RCC_IOPENR_GPIOAEN |
			0;
}

}	// namespace board

}	// namespace distortos
