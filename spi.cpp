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

#include "include/spi.hpp"

#ifdef CONFIG_BOARD_SPIS_ENABLE

#include "distortos/chip/ChipOutputPin.hpp"
#include "distortos/chip/ChipAlternativePin.hpp"
#include "distortos/board/STM32-SPI-Pins.hpp"

namespace distortos
{

namespace board
{

/*---------------------------------------------------------------------------------------------------------------------+
| global objects
+---------------------------------------------------------------------------------------------------------------------*/

distortos::chip::ChipAlternativePin spi1_clk { chip::Pin::pb7,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	chip::PinAlternateFunction::af0
};

distortos::chip::ChipAlternativePin spi1_miso { chip::Pin::pb8,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	chip::PinAlternateFunction::af0
};
distortos::chip::ChipAlternativePin spi1_mosi { chip::Pin::pb9,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	chip::PinAlternateFunction::af0
};
distortos::chip::ChipOutputPin spi1_cs { chip::Pin::pb9,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	False
};

distortos::board::SpiPins spi1_pins(spi1_clk, spi1_miso, spi1_mosi, spi1_cs);

distortos::chip::ChipAlternativePin spi2_clk { chip::Pin::pb10,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	chip::PinAlternateFunction::af0
};

distortos::chip::ChipAlternativePin spi2_miso { chip::Pin::pb11,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	chip::PinAlternateFunction::af0
};
distortos::chip::ChipAlternativePin spi2_mosi { chip::Pin::pb12,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	chip::PinAlternateFunction::af0
};
distortos::chip::ChipOutputPin spi2_cs { chip::Pin::pb13,
	false,
	chip::PinOutputSpeed::high,
	chip::PinPull::up,
	False
};

distortos::board::SpiPins spi2_pins(spi2_clk, spi2_miso, spi2_mosi, spi2_cs);


}	// namespace board

}	// namespace distortos

#endif	// def CONFIG_BOARD_SPIS_ENABLE