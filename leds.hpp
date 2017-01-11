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

#ifndef SOURCE_BOARD_STM32_STM32F0_NUCLEO_L073RZ_INCLUDE_DISTORTOS_BOARD_LEDS_HPP_
#define SOURCE_BOARD_STM32_STM32F0_NUCLEO_L073RZ_INCLUDE_DISTORTOS_BOARD_LEDS_HPP_

#include "distortos/chip/STM32-GPIOv2.hpp"

#include <array>

namespace distortos
{

#ifdef CONFIG_BOARD_LEDS_ENABLE

namespace chip
{

class ChipOutputPin;

}	// namespace chip

#endif	// def CONFIG_BOARD_LEDS_ENABLE

namespace board
{

/// total number of LEDs on the board
constexpr size_t totalLeds { 2 };

/*---------------------------------------------------------------------------------------------------------------------+
| LED indexes
+---------------------------------------------------------------------------------------------------------------------*/


/// index of led0
constexpr size_t led0 { 0 };

/// index of led1
constexpr size_t led1 { 1 };


/*---------------------------------------------------------------------------------------------------------------------+
| indexed access to pin identifiers
+---------------------------------------------------------------------------------------------------------------------*/

/// array with pin identifiers of all LEDs
constexpr std::array<chip::Pin, totalLeds> ledPins
{
	
	chip::Pin::pa7,
	chip::Pin::pa8,
};

}

#endif	// SOURCE_BOARD_STM32_STM32F0_NUCLEO_L073RZ_INCLUDE_DISTORTOS_BOARD_LEDS_HPP_
