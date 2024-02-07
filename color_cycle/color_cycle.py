from amaranth import *
from amaranth.lib import enum

class BidirectionalCounter(Elaboratable):
    def __init__(self, width):
        self.op     = Signal()
        self.en     = Signal()
        self.count  = Signal(width)

    def elaborate(self, platform):
        m = Module()
        with m.If(self.op):
            m.d.sync += self.count.eq(self.count + 1) # If op == 1, increment counter
        with m.Else():
            m.d.sync += self.count.eq(self.count - 1) # If op == 0, decrement counter
        return EnableInserter(self.en)(m)

class Counter(Elaboratable):
    def __init__(self, width):
        self.en     = Signal()
        self.count  = Signal(width)

    def elaborate(self, platform):
        m = Module()
        with m.If(self.en):
            m.d.sync += self.count.eq(self.count + 1)
        return m

class ControlUnit(Elaboratable):
    def __init__(self, width):
        self.R = BidirectionalCounter(width)
        self.G = BidirectionalCounter(width)
        self.B = BidirectionalCounter(width)
        self.duty = Counter(width)
        self.max = Const(2**width - 1)
        return

    def elaborate(self, platform):
        m = Module()
        m.submodules.R = self.R
        m.submodules.G = self.G
        m.submodules.B = self.B
        
        # led = platform.request("rgb_led")

        # Duty counter always counting up.
        # Produce a single color frame every 0 to 255 duty cycles
        # We want it to overflow and reset to 0.
        m.d.comb += self.duty.en.eq(1)
        # Todo
        # If R/G/B.count < duty, LED = ON, else LED = OFF

        
        # Maybe an awkwardly placed FSM but maybe will work.
        # BEGIN FSM_COLOR_CYCLE
        with m.FSM(domain="comb") as fsm_color_cycle:
            with m.State("INIT"):
                m.next = "RED_GREEN"
                m.d.comb += [
                    self.R.en.eq(0),
                    self.R.op.eq(0),
                    self.R.count.eq(self.max),
                    self.G.en.eq(0),
                    self.G.op.eq(0),
                    self.G.count.eq(0),
                    self.B.en.eq(0),
                    self.B.op.eq(0),
                    self.B.count.eq(0),
                ]
            with m.State("RED_GREEN"):
                with m.If(self.R.count > 0):
                    m.d.comb += [
                        self.R.en.eq(1), # Red Counter Enable
                        self.R.op.eq(0), # Red Decrement
                        self.G.en.eq(1), # Green Counter Enable
                        self.G.op.eq(1), # Green Increment
                        self.B.en.eq(0), # Blue Counter Disable
                    ]
                    m.next = "RED_GREEN"
                with m.Else():
                    m.next = "GREEN_BLUE"
            with m.State("GREEN_BLUE"):
                with m.If(self.G.count > 0):
                    m.d.comb += [
                        self.R.en.eq(0), # Red Counter Disable
                        self.G.en.eq(1), # Green Counter Enable
                        self.G.op.eq(0), # Green Decrement
                        self.B.en.eq(1), # Blue Counter Enable
                        self.B.op.eq(1), # Blue Increment
                    ]
                    m.next = "GREEN_BLUE"
                with m.Else():
                    m.next = "BLUE_RED"
            with m.State("BLUE_RED"):
                with m.If(self.B.count > 0):
                    m.d.comb += [
                        self.R.en.eq(1), # Red Counter Enable
                        self.R.op.eq(1), # Red Increment
                        self.G.en.eq(0), # Green Counter Disable
                        self.B.en.eq(1), # Blue Counter Enable
                        self.B.op.eq(0), # Blue Decrement
                    ]
                    m.next = "BLUE_RED"
                with m.Else():
                    m.next = "RED_GREEN"
        # END FSM_COLOR_CYCLE

        return m

class ColorCycleAHDL(Elaboratable):
    def __init__(self, width=8):
        pass

    def elaborate(self, platform):
        m = Module()
        return m


from amaranth_boards.arty_z7 import ArtyZ720Platform
# ArtyZ720Platform().build(LEDBlinker(), do_program=True)

# Using PRJXRAY instead of default Vivado
# Add AMARANTH_ENV_XRAY to environment PATH variables and set to prjxray directory
# Also add PYTHONPATH and set to same prjxray directory
platform = ArtyZ720Platform()
platform.toolchain="Xray"
platform.build(ColorCycleAHDL(), do_program=True)
