# Implementing the Blockchain Technology
# I will be using Postman to interact with my blockchain
# the SHA256 hashing algorithm accepts only string values that too in hexadecimal format

# Importing the libraries
import datetime # to specify the exact date time when the coin was mined
import hashlib # hashing the blocks
import json
from flask import Flask, jsonify # Flask is used to create the web application to hold the blockchain

class Blockchain:

    #Initializing the blockchain with the genesis block and hence the previous_hash is 0
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    # creates a new block and appends to the end of blockchain once the mining is done
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1] # In python -1 points to the last the index

    # pow is a specific number that the miners has to find out by solving the complex problem, this is the proof which create block takes in as an argument
    # refer to this wikipedia link: https://en.wikipedia.org/wiki/Proof_of_work
    # this problem must be challenging to solve but easy to verify
    # the problem is that the string that we generate should start with 4 leading zeroes. If yes, then we'll say that the problem has been solved.
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # b'5', encode adds this b in front of your solution, then convert to hex which is the accepted format by SHA256
            if hash_operation[:4] == '0000': # if the first four digits of the hash is == '0000', then the condition is satisfied
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # converts our block to it's cryptographic hash equivalent
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block): # if hash of previous block of the blockchain and the current block's prev hash arent the same, then false
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000': # if pow is not valid, then also our chain is invalid
                return False
            previous_block = block
            block_index += 1
        return True

# Creating a Web App using Flask
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()
#as soon as the method is called, our chain is initialized with genesis block

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)
# host = '0.0.0.0' makes our web app publicly available so that we can later decentralize our blockchain and multiple people can access it from multiple places
