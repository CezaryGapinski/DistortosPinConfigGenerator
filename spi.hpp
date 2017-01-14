/**
 * \file
 * \brief Declaration of SPIs for STM32F0_NUCLEO_L073RZ
 *
 * \author Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
 *
 * \par License
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
 * distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * File generated automaticly - do not edit!
 */

#ifndef SOURCE_BOARD_STM32_STM32F0_NUCLEO_L073RZ_INCLUDE_DISTORTOS_BOARD_SPIS_HPP_
#define SOURCE_BOARD_STM32_STM32F0_NUCLEO_L073RZ_INCLUDE_DISTORTOS_BOARD_SPIS_HPP_

#include "distortos/chip/STM32-GPIOv2.hpp"

#include <array>

namespace distortos
{

#ifdef CONFIG_BOARD_SPIS_ENABLE

namespace board
{

class SpiPins;

}	// namespace chip

#endif	// def CONFIG_BOARD_SPIS_ENABLE

namespace board
{

/// total number of SPIs on the board
constexpr size_t totalSpis { 2 };

/*---------------------------------------------------------------------------------------------------------------------+
| spis indexes
+---------------------------------------------------------------------------------------------------------------------*/


/// index of spi1_pins
constexpr size_t spi1_pinsIndex { 0 };

/// index of spi2_pins
constexpr size_t spi2_pinsIndex { 1 };


/*---------------------------------------------------------------------------------------------------------------------+
| indexed access to pin identifiers
+---------------------------------------------------------------------------------------------------------------------*/


/// index of spi1_pins
extern distortos::board::SpiPins spi1_pins;

/// index of spi2_pins
extern distortos::board::SpiPins spi2_pins;


/// array with pin identifiers of all spi Pins
constexpr std::array<SpiPins *, totalSpis> spiPins
{

/// index of spi1_pins
 &spi1_pins,

/// index of spi2_pins
 &spi2_pins,

};

#ifdef CONFIG_BOARD_SPIS_ENABLE

/*---------------------------------------------------------------------------------------------------------------------+
| indexed access to spi pins objects
+---------------------------------------------------------------------------------------------------------------------*/

/// array with all spi pins objects
extern const distortos::board::SpiPins spis[totalSpis];

#endif	// def CONFIG_BOARD_SPIS_ENABLE

}	// namespace board

}	// namespace distortos

#endif	// SOURCE_BOARD_STM32_STM32L0_NUCLEO_L073RZ_CUSTOM_INCLUDE_DISTORTOS_BOARD_SPIS_HPP_