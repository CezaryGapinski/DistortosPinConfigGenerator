/**
 * \file
 * \brief Declaration of LEDs for STM32F0_NUCLEO_L073RZ
 *
 * \author Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
 *
 * \par License
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
 * distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * File generated automaticly - do not edit!
 */


#include "distortos/board/leds.hpp"

#ifdef CONFIG_BOARD_LEDS_ENABLE

#include "distortos/chip/ChipOutputPin.hpp"

namespace distortos
{

namespace board
{

/*---------------------------------------------------------------------------------------------------------------------+
| global objects
+---------------------------------------------------------------------------------------------------------------------*/

chip::ChipOutputPin leds[totalLeds]
{  
	/// index of chip::Pin::pa7
	chip::ChipOutputPin{ chip::Pin::pa7, False, high, up, False }, 
 
	/// index of chip::Pin::pa8
	chip::ChipOutputPin{ chip::Pin::pa8, False, high, up, False }, 
 
};

}	// namespace board

}	// namespace distortos

#endif	// def CONFIG_BOARD_LEDS_ENABLE