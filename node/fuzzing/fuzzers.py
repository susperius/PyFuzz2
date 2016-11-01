import random
import pickle
import os
import browser.javascript as javascript
from browser.javascript_ng import JsFuzzer
import bytemutation


"""
If you want to implement a new fuzzer just inherit from the Fuzzer Class and implement the abstract methods.
After this add a column for your fuzzer.
The dictionary key is the fuzzers name and the contents is a tupel with all the necessary configuration
parameters as first value and a reference to your fuzzers class as the second value.
"""
#  FUZZERS = {FuzzerName: (CONFIG_PARAMS, CONSTRUCTOR())}
FUZZERS = {bytemutation.ByteMutation.NAME: (bytemutation.ByteMutation.CONFIG_PARAMS, bytemutation.ByteMutation),
           javascript.JsDomFuzzer.NAME: (javascript.JsDomFuzzer.CONFIG_PARAMS, javascript.JsDomFuzzer),
           JsFuzzer.NAME: (JsFuzzer.CONFIG_PARAMS, JsFuzzer)
           }


def init_random_seed(seed=None):
    random.seed(seed)


def check_for_prng_state():
    if os.path.isfile("fuzz_state.pickle"):
        return True
    else:
        return False


def restore_prng_state():
    msg = "Prng state restored successfully"
    try:
        with open("fuzz_state.pickle", 'r') as fd:
            state = pickle.load(fd)
        random.setstate(state)
    except Exception as ex:
        msg = "Error while restoring prng state" + ex.message
        init_random_seed()
    finally:
        os.remove("fuzz_state.pickle")
    return msg


def save_prng_state():
    with open("fuzz_state.pickle", 'w+') as fd:
        pickle.dump(random.getstate(), fd)  # Save the state of the prng


def get_fuzzer(fuzzer_type, config):
    return FUZZERS[fuzzer_type][1].from_list(config)