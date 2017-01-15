/**
 * \file
 * \brief Declaration of BUTTONs for NUCLEO_L073RZ_CUSTOM
 *
 * File generated by DistortosPinConfigGenerator
 * https://github.com/CezaryGapinski/DistortosPinConfigGenerator
 * \author Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
 *
 * \par License
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
 * distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 */

#include "distortos/board/buttons.hpp"

#ifdef CONFIG_BOARD_BUTTONS_ENABLE

#include "distortos/chip/ChipInputPin.hpp"

namespace distortos
{

namespace board
{

/*---------------------------------------------------------------------------------------------------------------------+
| global objects
+---------------------------------------------------------------------------------------------------------------------*/

const chip::ChipInputPin buttons[totalButtons]
{
{  
	/// index of chip::Pin::pc7
	chip::ChipInputPin{ chip::Pin::pc7, chip::PinPull::up }, 

};

}	// namespace board

}	// namespace distortos

#endif	// def CONFIG_BOARD_BUTTONS_ENABLE