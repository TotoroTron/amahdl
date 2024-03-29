from amaranth import *


class LEDBlinker(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        led = platform.request("led")

        half_freq = int(platform.default_clk_frequency // 2)
        timer = Signal(range(half_freq + 1))

        with m.If(timer == half_freq):
            m.d.sync += led.eq(~led.o)
            m.d.sync += timer.eq(0)
        with m.Else():
            m.d.sync += timer.eq(timer + 1)

        return m

from amaranth_boards.arty_z7 import ArtyZ720Platform
# ArtyZ720Platform().build(LEDBlinker(), do_program=True)

# Using PRJXRAY instead of default Vivado
# Add AMARANTH_ENV_XRAY to environment PATH variables and set to prjxray directory
# Also add PYTHONPATH and set to same prjxray directory
platform = ArtyZ720Platform()
platform.toolchain="Xray"
platform.build(LEDBlinker(), do_program=True)
