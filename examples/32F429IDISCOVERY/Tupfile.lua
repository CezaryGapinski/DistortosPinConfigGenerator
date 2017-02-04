--
-- file: Tupfile.lua
--
-- author: Copyright (C) 2014-2016 Kamil Szczygiel http://www.distortec.com http://www.freddiechopin.info
--
-- This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
-- distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
--

if CONFIG_BOARD_32F429IDISCOVERY == "y" then

	CXXFLAGS += STANDARD_INCLUDES
	CXXFLAGS += CHIP_INCLUDES
	CXXFLAGS += BOARD_INCLUDES

	tup.include(DISTORTOS_TOP .. "compile.lua")

end	-- if CONFIG_BOARD_32F429IDISCOVERY == "y" then
