from amaranth import *
from amaranth.lib import data, enum

class ColorPhase(enum.Enum, shape=3):
    RED_GREEN = 0
    GREEN_BLUE = 1
    BLUE_RED = 2

def rgb_layout(r_bits, g_bits, b_bits):
    return data.StructLayout({
        "red":   unsigned(r_bits),
        "green": unsigned(g_bits),
        "blue":  unsigned(b_bits)
    })

class ControlUnit(Elaboratable):
    def __init__(self, width=8):
        self.width      = width
        self.r_led   = Signal()
        self.g_led   = Signal()
        self.b_led   = Signal()
    
    def elaborate(self, platform):
        m = Module()

        max        = Const(2**self.width - 1)
        rgb_led    = Signal(rgb_layout(1, 1, 1))
        rgb_count  = Signal(rgb_layout(self.width, self.width, self.width))
        duty       = Signal(self.width)
        rgb_phase  = Signal(ColorPhase)

        m.d.comb += [
            self.r_led.eq(rgb_led.red),
            self.g_led.eq(rgb_led.green),
            self.b_led.eq(rgb_led.blue),
        ]

        # rgb_led = platform.request("rgb_led", "r")

        with m.If(duty < rgb_count.red):
            m.d.sync += rgb_led.red.eq(1)
        with m.Else():
            m.d.sync += rgb_led.red.eq(0)

        with m.If(duty < rgb_count.green):
            m.d.sync += rgb_led.green.eq(1)
        with m.Else():
            m.d.sync += rgb_led.green.eq(0)

        with m.If(duty < rgb_count.blue):
            m.d.sync += rgb_led.blue.eq(1)
        with m.Else():
            m.d.sync += rgb_led.blue.eq(0)
        

        # BEGIN FSM_COLOR_CYCLE
        with m.FSM(domain="sync") as fsm_color_cycle:
            with m.State("INIT"):
                m.d.sync += [
                    rgb_count.red.eq(max),
                    rgb_count.green.eq(0),
                    rgb_count.blue.eq(0),
                    duty.eq(0),
                ]
                m.next = "INCR_DUTY"
            with m.State("INCR_DUTY"):
                with m.If(duty < max):
                    m.d.sync += duty.eq(duty + 1)
                    m.next = "INCR_DUTY"
                with m.Else():
                    m.d.sync += duty.eq(0) # Is this statement necessary?
                    m.next = "SHIFT_COLOR"
            with m.State("SHIFT_COLOR"):
                with m.Switch(rgb_phase):
                    with m.Case(ColorPhase.RED_GREEN):
                        with m.If(rgb_count.red > 0):
                            m.d.sync += [
                                rgb_count.red.eq(rgb_count.red - 1), # Decrement RED Count
                                rgb_count.green.eq(rgb_count.green + 1), # Increment GREEN Count
                            ]
                        with m.Else():
                            m.d.sync += rgb_phase.eq(ColorPhase.GREEN_BLUE)
                    with m.Case(ColorPhase.GREEN_BLUE):
                        with m.If(rgb_count.green > 0):
                            m.d.sync += [
                                rgb_count.green.eq(rgb_count.green - 1), # Decrement GREEN Count
                                rgb_count.blue.eq(rgb_count.blue + 1), # Increment BLUE Count
                            ]
                        with m.Else():
                            m.d.sync += rgb_phase.eq(ColorPhase.BLUE_RED)
                    with m.Case(ColorPhase.BLUE_RED):
                        with m.If(rgb_count.blue > 0):
                            m.d.sync += [
                                rgb_count.blue.eq(rgb_count.blue - 1), # Decrement BLUE Count
                                rgb_count.red.eq(rgb_count.red + 1), # Increment RED Count
                            ]
                        with m.Else():
                            m.d.sync += rgb_phase.eq(ColorPhase.RED_GREEN)
                m.next = "INCR_DUTY"
        # END FSM_COLOR_CYCLE

        return m

# --- TEST ---
from amaranth.sim import Simulator


dut = ControlUnit(width=8)
def bench():
    # Observe two full color cycles
    for _ in range(256*256*3*2):
        yield

sim = Simulator(dut)
sim.add_clock(1e-6) # 1 MHz
sim.add_sync_process(bench)
with sim.write_vcd("color_cycle.vcd"):
    sim.run()
# --- CONVERT ---
from amaranth.back import verilog


top = ControlUnit(width=8)
with open("color_cycle.v", "w") as f:
    f.write(verilog.convert(top, ports=[dut.r_led, dut.g_led, dut.b_led]))




# from amaranth_boards.arty_z7 import ArtyZ720Platform
# # ArtyZ720Platform().build(LEDBlinker(), do_program=True)

# # Using PRJXRAY instead of default Vivado
# # Add AMARANTH_ENV_XRAY to environment PATH variables and set to prjxray directory
# # Also add PYTHONPATH and set to same prjxray directory
# platform = ArtyZ720Platform()
# platform.toolchain="Xray"
# platform.build(ColorCycleAHDL(), do_program=True)
