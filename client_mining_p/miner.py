import hashlib
import requests

import json

import sys


# TODO: Implement functionality to search for a proof
def proof_of_work(last_block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    block_string = json.dumps(last_block, sort_keys=True).encode()
    proof = 0
    print("Starting finding valid proof...")
    while not valid_proof(block_string, proof):  # False
        proof += 1

    print(f"Finished! Found valid proof: {proof}")
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    # TODO
    # create encoded string
    # apply SHA 256 on encoded string (guess) & format it as hexidec
    # return T/F if string starts with 6 zeros

    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # TODO: CHANGE BACK TO SIX !!!!!!
    return guess_hash[:4] == "0000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0

    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one

        # r = requests.get(f"{node}/last_block")  # url
        r = requests.get(url=node + "/last_block")
        if r.status_code == 200:
            data = r.json()
            last_block = data['last_block']
            print("Last Block: ", last_block)
            new_proof = proof_of_work(last_block)

            # TODO: When found, POST it to the server {"proof": new_proof}
            # TODO: We're going to have to research how to do a POST in Python
            # HINT: Research `requests` and remember we're sending our data as JSON
            # TODO: If the server responds with 'New Block Forged'
            # add 1 to the number of coins mined and print it.  Otherwise,
            # print the message from the server.

            if new_proof:
                print("Found a proof: ", new_proof)
                #r = requests.post(f"{node}/mine", json={"proof": new_proof})
                post_data = {
                    "proof": new_proof
                }
                r = requests.post(url=node + "/mine", json=post_data)
                data = r.json()
                # print("JSON OBJECT: ", data)

                if data and data['message'] == 'New Block Forged':

                    coins_mined += 1
                    print(
                        f"{r.status_code} Success! {data['message']} /n Coins Mined: {coins_mined}")

                elif data and data['message'] != 'New Block Forged':
                    print(
                        f"{r.status_code} Something went wrong. /n {data['message']}")
        else:
            print("GET Error ", r.status_code)
            break
