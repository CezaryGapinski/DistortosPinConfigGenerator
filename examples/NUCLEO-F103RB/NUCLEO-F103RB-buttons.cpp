/**
 * File generated with scripts/generateBoard.py:
 * Copyright (C) 2017 Cezary Gapinski cezary.gapinski@gmail.com
 *
 * \file
 * \brief Definition of buttons for NUCLEO-F103RB
 *
 * \author Copyright (C) 2016-2017 Kamil Szczygiel http://www.distortec.com http://www.freddiechopin.info
 *
 * \par License
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
 * distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
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
#if DISTORTOS_BOARD_B1_BUTTON_ENABLE == 1
		chip::ChipInputPin{chip::Pin::pc13, chip::PinPull::none, true},
#endif	// DISTORTOS_BOARD_B1_BUTTON_ENABLE == 1
};

}	// namespace board

}	// namespace distortos

#endif	// def CONFIG_BOARD_BUTTONS_ENABLE
