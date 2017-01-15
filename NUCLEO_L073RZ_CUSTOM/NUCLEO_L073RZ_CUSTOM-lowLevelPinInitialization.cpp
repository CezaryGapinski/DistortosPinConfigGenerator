/**
 * \file
 * \brief Declaration of LEDs for NUCLEO_L073RZ_CUSTOM
 *
 * \author Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
 *
 * \par License
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
 * distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * File generated automaticly - do not edit!
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
	RCC->IOPENR |=


RCC_IOPENR_GPIOBEN |





RCC_IOPENR_GPIOCEN |


RCC_IOPENR_GPIOAEN |




			0;
}

}	// namespace board

}	// namespace distortos