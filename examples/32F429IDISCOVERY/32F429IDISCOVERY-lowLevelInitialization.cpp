/**
 * File generated by:
 * https://github.com/CezaryGapinski/DistortosPinConfigGenerator
 * Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
 *
 * \file
 * \brief Definition of lowLevelInitializations for 32F429IDISCOVERY
 *
 * \author Copyright (C) 2016 Kamil Szczygiel http://www.distortec.com http://www.freddiechopin.info
 * \par License
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
 * distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 */

#include "distortos/board/lowLevelInitialization.hpp"

#include "distortos/chip/CMSIS-proxy.h"

namespace distortos
{

namespace board
{

/*---------------------------------------------------------------------------------------------------------------------+
| global functions
+---------------------------------------------------------------------------------------------------------------------*/

void lowLevelInitialization()
{ 	
	RCC->AHB1ENR |=
	RCC_AHB1ENR_GPIOAEN |
	RCC_AHB1ENR_GPIOGEN |
	0;
}

}	// namespace board

}	// namespace distortos
