## Difference in output

## From femtoRV risc_v:
```
Info: Running post-routing legalisation...

Info: Program finished normally.
+ fasm2frames.py --part xc7z020clg400-1 --db-root /usr/share/nextpnr/prjxray-db/zynq7 color_cycle.fasm
/usr/local/lib/python3.10/dist-packages/fasm-0.0.2.post88-py3.10-linux-x86_64.egg/fasm/parser/__init__.py:30: RuntimeWarning: Unable to import fast Antlr4 parser implementation.
  ImportError: cannot import name 'antlr_to_tuple' from partially initialized module 'fasm.parser' (most likely due to a circular import) (/usr/local/lib/python3.10/dist-packages/fasm-0.0.2.post88-py3.10-linux-x86_64.egg/fasm/parser/__init__.py)

  Falling back to the much slower pure Python textX based parser
  implementation.

  Getting the faster antlr parser can normally be done by installing the
  required dependencies and then reinstalling the fasm package with:
    pip uninstall
    pip install -v fasm

  warn(
+ xc7frames2bit --part_file /usr/share/nextpnr/prjxray-db/zynq7/xc7z020clg400-1/part.yaml --part_name xc7z020clg400-1 --frm_file color_cycle.frames --output_file color_cycle.bit
+ openFPGALoader --board arty_z7_20 color_cycle.bit
empty
Jtag frequency : requested 6.00MHz   -> real 6.00MHz
Open file DONE
Parse file DONE
load program
Load SRAM: [===================================================] 100.00%
Done
```

## From amahdl:
```
Info: Running post-routing legalisation...

Info: Program finished normally.
Traceback (most recent call last):
  File "/usr/local/bin/fasm2frames", line 33, in <module>
    sys.exit(load_entry_point('prjxray==0.0.1', 'console_scripts', 'fasm2frames')())
  File "/usr/local/bin/fasm2frames", line 25, in importlib_load_entry_point
    return next(matches).load()
  File "/usr/lib/python3.10/importlib/metadata/__init__.py", line 171, in load
    module = import_module(match.group('module'))
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 992, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1004, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'utils'
Traceback (most recent call last):
  File "/home/bcheng/dev/amahdl/led_blinker/led_blinker.py", line 28, in <module>
    platform.build(LEDBlinker(), do_program=True)
  File "/home/bcheng/.local/lib/python3.10/site-packages/amaranth/build/plat.py", line 109, in build
    products = plan.execute_local(build_dir)
  File "/home/bcheng/.local/lib/python3.10/site-packages/amaranth/build/run.py", line 117, in execute_local
    subprocess.check_call(["sh", f"{self.script}.sh"],
  File "/usr/lib/python3.10/subprocess.py", line 369, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command '['sh', 'build_top.sh']' returned non-zero exit status 1.
```