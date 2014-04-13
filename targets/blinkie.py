from migen.fhdl.std import *
from migen.bank.description import *

from targets.simple import SimpleSoC

# For Mixxeo and Milkymist One:
# from targets.mlabs_video import MiniSoC
# (also replace SimpleSoC with MiniSoC below)

class Blinker(Module, AutoCSR):
	def __init__(self, led, countbits=32):
		self._r_frequency = CSRStorage(countbits, reset=15000000)

		counter = Signal(countbits)
		self.sync += \
			If(counter == 0,
				led.eq(~led),
				counter.eq(self._r_frequency.storage)
			).Else(
				counter.eq(counter - 1)
			)

class BlinkieSoC(SimpleSoC):
	csr_map = {
		"blinker":				16,
	}
	csr_map.update(SimpleSoC.csr_map)

	def __init__(self, platform):
		SimpleSoC.__init__(self, platform)
		self.submodules.blinker = Blinker(platform.request("user_led"))

default_subtarget = BlinkieSoC
