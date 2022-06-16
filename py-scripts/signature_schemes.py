from btclib.ecc import bms, dsa, ssa

msg = "Hello, I'm Alice!".encode()
print("\n", msg.decode())

# ECDSA
print("\n ECDSA")

dsa_prv, dsa_pub = dsa.gen_keys()
print("prv", hex(dsa_prv))
print("pub", hex(dsa_pub[0]), hex(dsa_pub[1]))

dsa_sig = dsa.sign(msg, dsa_prv)
print("r:", hex(dsa_sig.r))
print("s:", hex(dsa_sig.s))

dsa_valid = dsa.verify(msg, dsa_pub, dsa_sig)
print("valid ECDSA sig:", dsa_valid)

# ECSSA
print("\n ECSSA")

ssa_prv, ssa_pub = ssa.gen_keys()
print("prv", hex(ssa_prv))
print("pub", hex(ssa_pub))

ssa_sig = ssa.sign(msg, ssa_prv)
print("r:", hex(ssa_sig.r))
print("s:", hex(ssa_sig.s))

ssa_valid = ssa.verify(msg, ssa_pub, ssa_sig)
print("valid ECSSA sig:", ssa_valid)

# ECBMS
print("\n ECBMS")

bms_prv, bms_pub = bms.gen_keys()
print("prv", bms_prv)
print("pub", bms_pub)

bms_sig = bms.sign(msg, bms_prv)
print("rf:", hex(bms_sig.rf))
print("r:", hex(bms_sig.dsa_sig.r))
print("s:", hex(bms_sig.dsa_sig.r))

bms_valid = bms.verify(msg, bms_pub, bms_sig)
print("valid ECBMS sig:", bms_valid)
