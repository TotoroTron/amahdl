from amaranth import *
from amaranth_boards.arty_z7 import ArtyZ720Platform

# Reference for Instance examples
# https://github.com/search?q=repo%3Aapertus-open-source-cinema%2Fnaps%20pll&type=code 

class TopLevel (Elaboratable):
    def __init__(self, width=8):
        self.width = width

    def elaborate(self, platform):
        m = Module()
        m.domains.clk_pll = cd_clk_pll = ClockDomain(local=True)
        m.domains.clk_bufgctrl = cd_clk_bufgctrl = ClockDomain(local=True)
        m.domains.clk_bufg = cd_clk_bufg = ClockDomain(local=True)

        
        counter_sync = Signal(8)
        counter_pll = Signal(8)
        counter_bufgctrl = Signal(8)
        counter_bufg = Signal(8)

        
        m.d.sync += counter_sync.eq(counter_sync + 1)
        m.d.clk_pll += counter_pll.eq(counter_pll + 1)
        m.d.clk_bufgctrl += counter_bufgctrl.eq(counter_bufgctrl + 1)
        m.d.clk_bufg += counter_bufg.eq(counter_bufg + 1)

        PLL = Instance("PLLE2_BASE",
            ("p", "BANDWIDTH", "OPTIMIZED"),
            ("p", "CLKFBOUT_MULT", 5),
            ("p", "CLKFBOUT_PHASE", 0.0),
            ("p", "CLKIN1_PERIOD", 10.0),
            ("p", "CLKOUT0_DIVIDE", 1),
            ("p", "CLKOUT0_DUTY_CYCLE", 0.5),
            ("p", "CLKOUT0_PHASE", 0.0),
            ("p", "DIVCLK_DIVIDE", 1),
            ("p", "REF_JITTER1", 0.0),
            ("p", "STARTUP_WAIT", "FALSE"),
            ("o", "CLKOUT0", ClockSignal("clk_pll")),
            ("i", "CLKIN1", ClockSignal("sync")),
            ("i", "PWRDWN", Const(0)),
            ("i", "RST", Const(0)),
            ("i", "CLKFBIN", ClockSignal("clk_pll")),
            # ("i", "ASDFASDF_DUMMY", Const(0))
        )
        m.submodules += PLL

        BUFGCTRL = Instance("BUFGCTRL",
            ("i", "I0", ClockSignal("sync")),
            ("i", "CE0", Const(1)),
            ("i", "S0", Const(1)),
            ("o", "O", ClockSignal("clk_bufgctrl")),
        )
        m.submodules += BUFGCTRL

        BUFG = Instance("BUFG",
            ("i", "I", ClockSignal("sync")),
            ("o", "O", ClockSignal("clk_bufg")),
        )
        m.submodules += BUFG
        return m


top = TopLevel(width=8)

# --- TEST ---
from amaranth.sim import Simulator
def bench():
    for _ in range(256*16):
        yield
sim = Simulator(top)
sim.add_clock(1e-8) # 100 MHz
sim.add_sync_process(bench)
with sim.write_vcd("clock_gen.vcd"):
    sim.run()

# --- CONVERT ---
from amaranth.back import verilog
with open("clock_gen.v", "w") as f:
    f.write(verilog.convert(top, ports=[]))

# --- BUILD ---
plat = ArtyZ720Platform()
plat.toolchain="Xray"
plat.build(top, do_program=False)