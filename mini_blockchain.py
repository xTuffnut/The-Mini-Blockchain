import hashlib
import time
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty

        print(f"\n Mining block {self.index}...")
        print(f" Target: Hash must start with {target}")

        start_time = time.time()

        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        mining_time = time.time() - start_time

        print(f" Block mined!")
        print(f" Nonce Found: {self.nonce}")
        print(f" Hash: {self.hash}")
        print(f" Mining time: {mining_time:.2f} seconds")
        print(f" Attempts: {self.nonce + 1}")
        
    def __str__(self):
            return f"""
╔═══════════════════════════════════════════════════════════════
║ BLOCK #{self.index}
╠═══════════════════════════════════════════════════════════════
║ Timestamp:     {self.timestamp}
║ Data:          {self.data}
║ Previous Hash: {self.previous_hash[:16]}...
║ Nonce:         {self.nonce}
║ Hash:          {self.hash[:16]}...
╚═══════════════════════════════════════════════════════════════
"""

class Blockchain:
     
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        print("\n Creating genesis block...")
        genesis_block = Block(
            index=0,
            timestamp=str(datetime.now()),
            data="Genesis Block - The Beginning",
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("Genesis block created successfully!")

    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, data):
        previous_block = self.get_latest_block()

        new_block = Block(
            index=previous_block.index + 1,
            timestamp=str(datetime.now()),
            data=data,
            previous_hash=previous_block.hash
        )

        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        print(f"Block #{new_block.index} added to the blockchain!")

    def is_chain_valid(self):
        print("\n Validating blockchain ...")

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                print(f" Invalid block at index {current_block.index}: Previous hash mismatch.")
                return False
            target = '0' * self.difficulty
            if current_block.hash[:self.difficulty] != target:
                print(f" Invalid block at index {current_block.index}: Hash does not meet difficulty.")
                return False
            if current_block.hash != current_block.calculate_hash():
                print(f" Invalid block at index {current_block.index}: Hash calculation mismatch.")
                return False
        print(" Blockchain is valid.")
        return True
    
    def print_chain(self):
        print("\n" + "="*70)
        print("Complete Blockchain:")
        print("="*70)

        for block in self.chain:
            print(block)

        print(f"Total blocks in chain: {len(self.chain)}")
        print(f"Difficulty level: {self.difficulty}")

    def tamper_block(self, index, new_data):
        if index <= 0 or index >= len(self.chain):
            print("Invalid block index to tamper.")
            return

        print(f"\n Tampering with block #{index}...")
        self.chain[index].data = new_data
        self.chain[index].hash = self.chain[index].calculate_hash()
        print(f" Block #{index} has been tampered with!")
    
if __name__ == "__main__":

    blockchain = Blockchain(difficulty=4)

    blockchain.add_block("Alice pays Bob 5 BTC")
    blockchain.add_block("Bob pays Charlie 2 BTC")
    blockchain.add_block("Charlie pays Dave 1 BTC")

    blockchain.print_chain()

    blockchain.is_chain_valid()

    blockchain.tamper_block(1, "Alice pays Bob 500 BTC(Tampered!)")

    blockchain.is_chain_valid()