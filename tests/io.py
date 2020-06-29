import droit

success = True

rpack = droit.models.DroitResourcePackage()

try:
    rpack.io.activateModule("console")
except:
    success = False

if not("console.py" in rpack.io.moduleList):
    success = False

if not(rpack.io.mode + ".py" in rpack.io.moduleList or rpack.io.mode in rpack.io.moduleList):
    success = False


if success:
    try:
        rpack.io.output("test: 'io' successful")
    except:
        print("test: 'io' failed")
else:
    print("test: 'io' failed")