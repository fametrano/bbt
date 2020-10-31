from btclib import bms, dsa, ssa

msg = "Hello, I'm Alice!"
print("\n", msg)

# ECDSA
print("\n ECDSA")

dsa_prv, dsa_pub = dsa.gen_keys()
print("prv", hex(dsa_prv))
print("pub", hex(dsa_pub[0]), hex(dsa_pub[1]))

dsa_sig = dsa.sign(msg, dsa_prv)
print("r:", hex(dsa_sig[0]))
print("s:", hex(dsa_sig[1]))

dsa_valid = dsa.verify(msg, dsa_pub, dsa_sig)
print("valid ECDSA sig:", dsa_valid)

# ECSSA
print("\n ECSSA")

ssa_prv, ssa_pub = ssa.gen_keys()
print("prv", hex(ssa_prv))
print("pub", hex(ssa_pub))

ssa_sig = ssa.sign(msg, ssa_prv)
print("r:", hex(ssa_sig[0]))
print("s:", hex(ssa_sig[1]))

ssa_valid = ssa.verify(msg, ssa_pub, ssa_sig)
print("valid ECSSA sig:", ssa_valid)

# ECBMS
print("\n ECBMS")

bms_prv, bms_pub = bms.gen_keys()
print("prv", bms_prv)
print("pub", bms_pub)

bms_sig = bms.sign(msg, bms_prv)
print("rf:", hex(bms_sig[0]))
print("r:", hex(bms_sig[1]))
print("s:", hex(bms_sig[2]))

bms_valid = bms.verify(msg, bms_pub, bms_sig)
print("valid ECBMS sig:", bms_valid)
