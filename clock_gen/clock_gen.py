from amaranth import *
from amaranth_boards.arty_z7 import ArtyZ720Platform

# Reference for Instance examples
# https://github.com/search?q=repo%3Aapertus-open-source-cinema%2Fnaps%20pll&type=code 

class TopLevel (Elaboratable):
    def __init__(self, width=8):
        self.width = width

    def elaborate(self, platform):
        m = Module()
        m.domains.clk196 = cd_clk196 = ClockDomain(local=True)

        m.submodules.PLL = Instance("PLLE2_BASE",
            ("p", "DIVISOR_0", 5),
            ("i", "CLKFBIN", cd_clk196.clk),
            ("i", "CLKIN1", ClockSignal()),
            ("i", "PWRDWN", 0),
            ("i", "RST", ResetSignal()),
            ("o", "CLKOUT0", ClockSignal("clk196")),
        )
        return m


# --- TEST ---
from amaranth.sim import Simulator
dut = TopLevel(width=8)
def bench():
    for _ in range(256*16):
        yield
sim = Simulator(dut)
sim.add_clock(1e-8) # 100 MHz
sim.add_sync_process(bench)
with sim.write_vcd("clock_gen.vcd"):
    sim.run()

# --- CONVERT ---
from amaranth.back import verilog
top = TopLevel(width=8)
with open("clock_gen.v", "w") as f:
    f.write(verilog.convert(top, ports=[]))

# # --- BUILD ---

# plat = ArtyZ720Platform()
# plat.toolchain="Xray"
# plat.build(TopLevel(width=8), do_program=False)