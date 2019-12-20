# Import third party libs
import libnacl.dual
import libnacl.public


def __init__(hub):
    print('pb works!')
    msg = b'You\'ve got two empty halves of coconut and you\'re bangin\' \'em together.'
    bob = libnacl.dual.DualSecret()
    alice = libnacl.dual.DualSecret()
    bob_box = libnacl.public.Box(bob.sk, alice.pk)
    alice_box = libnacl.public.Box(alice.sk, bob.pk)
    bob_ctxt = bob_box.encrypt(msg)
    assert msg != bob_ctxt
    bclear = alice_box.decrypt(bob_ctxt)
    assert msg == bclear
    alice_ctxt = alice_box.encrypt(msg)
    assert msg != alice_ctxt
    aclear = alice_box.decrypt(alice_ctxt)
    assert msg == aclear
    assert bob_ctxt != alice_ctxt
    print('libsodium works!')
