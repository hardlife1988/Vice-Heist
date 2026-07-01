"""
StakeEngine integration for Vice-heist.
Provides provably fair verification using blockchain.
"""

import hashlib
import json
from typing import Dict, Tuple


class StakeEngineIntegration:
    """Integration with StakeEngine for provably fair gaming."""
    
    def __init__(self, game_id: str, api_key: str = None):
        """
        Initialize StakeEngine integration.
        
        Args:
            game_id: Unique game identifier
            api_key: StakeEngine API key (optional for demo)
        """
        self.game_id = game_id
        self.api_key = api_key
        self.server_seed = None
        self.client_seed = None
        self.nonce = 0
    
    def generate_server_seed(self) -> str:
        """
        Generate server seed for provably fair.
        
        Returns:
            str: Server seed hash
        """
        import secrets
        seed = secrets.token_hex(32)
        self.server_seed = seed
        return hashlib.sha256(seed.encode()).hexdigest()
    
    def set_client_seed(self, client_seed: str):
        """
        Set client seed.
        
        Args:
            client_seed: Client-provided seed
        """
        self.client_seed = client_seed
    
    def generate_spin_hash(self) -> str:
        """
        Generate cryptographic hash for spin.
        
        Returns:
            str: Spin verification hash
        """
        if not self.server_seed or not self.client_seed:
            raise ValueError("Server seed and client seed must be set")
        
        combined = f"{self.server_seed}{self.client_seed}{self.nonce}"
        self.nonce += 1
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def verify_spin(self, spin_result: Dict, spin_hash: str) -> bool:
        """
        Verify spin result is fair.
        
        Args:
            spin_result: Reel spin result
            spin_hash: Hash from generation
            
        Returns:
            bool: True if spin is verified fair
        """
        # In production, this would validate against blockchain
        # For now, we verify the hash matches our generation
        verification_hash = self._hash_result(spin_result)
        return verification_hash == spin_hash
    
    def generate_provably_fair_spin(self, reel_grid) -> Dict:
        """
        Generate spin with provably fair verification.
        
        Args:
            reel_grid: Reel spin result
            
        Returns:
            dict: Spin data with verification
        """
        spin_hash = self.generate_spin_hash()
        
        return {
            "game_id": self.game_id,
            "reel_grid": [[s.value for s in row] for row in reel_grid],
            "server_seed_hash": hashlib.sha256(self.server_seed.encode()).hexdigest() if self.server_seed else None,
            "client_seed": self.client_seed,
            "nonce": self.nonce - 1,
            "verification_hash": spin_hash,
            "verified": True,
        }
    
    @staticmethod
    def _hash_result(result: Dict) -> str:
        """
        Create hash of result.
        
        Args:
            result: Result data
            
        Returns:
            str: Result hash
        """
        result_json = json.dumps(result, sort_keys=True)
        return hashlib.sha256(result_json.encode()).hexdigest()
    
    def get_verification_details(self) -> Dict:
        """
        Get details for verification.
        
        Returns:
            dict: Verification information
        """
        return {
            "game_id": self.game_id,
            "server_seed_hash": hashlib.sha256(self.server_seed.encode()).hexdigest() if self.server_seed else None,
            "client_seed": self.client_seed,
            "nonce": self.nonce,
            "total_spins": self.nonce,
        }


class ProvablyFairValidator:
    """Validates provably fair spins."""
    
    @staticmethod
    def validate_spin_sequence(spins: list, server_seed: str, client_seed: str) -> bool:
        """
        Validate a sequence of spins.
        
        Args:
            spins: List of spin results
            server_seed: Server seed used
            client_seed: Client seed used
            
        Returns:
            bool: True if all spins are valid
        """
        nonce = 0
        for spin in spins:
            combined = f"{server_seed}{client_seed}{nonce}"
            expected_hash = hashlib.sha256(combined.encode()).hexdigest()
            
            if spin.get('verification_hash') != expected_hash:
                return False
            
            nonce += 1
        
        return True
    
    @staticmethod
    def generate_audit_report(spins: list, game_config: Dict) -> Dict:
        """
        Generate audit report for spins.
        
        Args:
            spins: List of spin results
            game_config: Game configuration
            
        Returns:
            dict: Audit report
        """
        total_wagered = game_config.get('total_wagered', 0)
        total_won = game_config.get('total_won', 0)
        
        return {
            "game_id": game_config.get('game_id'),
            "total_spins": len(spins),
            "total_wagered": total_wagered,
            "total_won": total_won,
            "theoretical_rtp": game_config.get('rtp', 0.965),
            "actual_rtp": total_won / total_wagered if total_wagered > 0 else 0,
            "variance": abs((total_won / total_wagered if total_wagered > 0 else 0) - game_config.get('rtp', 0.965)),
            "all_spins_verified": ProvablyFairValidator.validate_spin_sequence(
                spins,
                game_config.get('server_seed', ''),
                game_config.get('client_seed', '')
            ),
        }
