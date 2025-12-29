# aeon/learning/rl_optimizer.py
"""
Reinforcement Learning optimizer for protocol selection.
Uses multi-armed bandit algorithms (UCB, Thompson Sampling).
"""

import numpy as np
import logging
from typing import List, Dict, Optional
from collections import defaultdict
import json


class ProtocolOptimizer:
    """
    Base class for protocol optimization strategies.
    """
    
    def __init__(self, protocols: List):
        self.protocols = protocols
        self.protocol_stats = defaultdict(lambda: {"pulls": 0, "rewards": []})
    
    def select_protocol(self, context) -> Optional[object]:
        """Select protocol based on strategy."""
        raise NotImplementedError
    
    def update(self, protocol_name: str, reward: float):
        """Update stats after protocol execution."""
        stats = self.protocol_stats[protocol_name]
        stats["pulls"] += 1
        stats["rewards"].append(reward)
    
    def get_stats(self) -> Dict:
        """Get statistics for all protocols."""
        return dict(self.protocol_stats)


class EpsilonGreedyOptimizer(ProtocolOptimizer):
    """
    Epsilon-Greedy strategy: exploit best protocol with probability (1-epsilon),
    explore random protocol with probability epsilon.
    """
    
    def __init__(self, protocols: List, epsilon: float = 0.1):
        super().__init__(protocols)
        self.epsilon = epsilon
    
    def select_protocol(self, context):
        """Select protocol using epsilon-greedy."""
        # Filter matching protocols
        matching = [p for p in self.protocols if p.matches(context)]
        if not matching:
            return None
        
        # Explore: random selection
        if np.random.random() < self.epsilon:
            protocol = np.random.choice(matching)
            logging.debug(f"Exploring: {protocol.name}")
            return protocol
        
        # Exploit: best known protocol
        best_protocol = None
        best_avg_reward = -float('inf')
        
        for protocol in matching:
            stats = self.protocol_stats[protocol.name]
            if stats["pulls"] > 0:
                avg_reward = np.mean(stats["rewards"])
            else:
                avg_reward = protocol.reward  # Use initial reward
            
            if avg_reward > best_avg_reward:
                best_avg_reward = avg_reward
                best_protocol = protocol
        
        logging.debug(f"Exploiting: {best_protocol.name if best_protocol else 'None'}")
        return best_protocol or matching[0]


class UCBOptimizer(ProtocolOptimizer):
    """
    Upper Confidence Bound (UCB1) algorithm.
    Balances exploration and exploitation using confidence bounds.
    """
    
    def __init__(self, protocols: List, c: float = 2.0):
        super().__init__(protocols)
        self.c = c  # Exploration parameter
        self.total_pulls = 0
    
    def select_protocol(self, context):
        """Select protocol using UCB1."""
        matching = [p for p in self.protocols if p.matches(context)]
        if not matching:
            return None
        
        self.total_pulls += 1
        
        # Calculate UCB scores
        best_protocol = None
        best_ucb = -float('inf')
        
        for protocol in matching:
            stats = self.protocol_stats[protocol.name]
            pulls = stats["pulls"]
            
            if pulls == 0:
                # Unvisited protocols have infinite UCB (explore first)
                return protocol
            
            avg_reward = np.mean(stats["rewards"])
            exploration_bonus = self.c * np.sqrt(np.log(self.total_pulls) / pulls)
            ucb = avg_reward + exploration_bonus
            
            if ucb > best_ucb:
                best_ucb = ucb
                best_protocol = protocol
        
        logging.debug(f"UCB selected: {best_protocol.name if best_protocol else 'None'}")
        return best_protocol


class ThompsonSamplingOptimizer(ProtocolOptimizer):
    """
    Thompson Sampling using Beta distribution.
    Bayesian approach to exploration-exploitation trade-off.
    """
    
    def __init__(self, protocols: List, alpha_prior: float = 1.0, beta_prior: float = 1.0):
        super().__init__(protocols)
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior
    
    def select_protocol(self, context):
        """Select protocol using Thompson Sampling."""
        matching = [p for p in self.protocols if p.matches(context)]
        if not matching:
            return None
        
        best_protocol = None
        best_sample = -float('inf')
        
        for protocol in matching:
            stats = self.protocol_stats[protocol.name]
            
            # Convert rewards to successes/failures
            # Assume reward is in [0, 5] range, normalize to [0, 1]
            normalized_rewards = [r / 5.0 for r in stats["rewards"]] if stats["rewards"] else []
            successes = sum(normalized_rewards)
            failures = len(normalized_rewards) - successes
            
            # Beta distribution parameters
            alpha = self.alpha_prior + successes
            beta = self.beta_prior + failures
            
            # Sample from Beta distribution
            sample = np.random.beta(alpha, beta)
            
            if sample > best_sample:
                best_sample = sample
                best_protocol = protocol
        
        logging.debug(f"Thompson Sampling selected: {best_protocol.name if best_protocol else 'None'}")
        return best_protocol


class ContextualBandit:
    """
    Contextual bandit that considers context features when selecting protocols.
    Uses linear regression to predict rewards.
    """
    
    def __init__(self, protocols: List, learning_rate: float = 0.1):
        super().__init__()
        self.protocols = protocols
        self.learning_rate = learning_rate
        
        # Weight vectors for each protocol
        self.weights = defaultdict(lambda: np.zeros(10))  # 10 context features
        self.history = []
    
    def _extract_features(self, context) -> np.ndarray:
        """Extract feature vector from context."""
        features = np.zeros(10)
        
        # Emotion features (one-hot)
        emotions = ["happy", "sad", "angry", "neutral", "excited"]
        emotion = getattr(context, 'emotion', 'neutral').lower()
        if emotion in emotions:
            features[emotions.index(emotion)] = 1.0
        
        # Intent features (one-hot)
        intents = ["work", "rest", "create", "learn", "social"]
        intent = getattr(context, 'intent', 'none').lower()
        if intent in intents:
            features[5 + intents.index(intent)] = 1.0
        
        return features
    
    def select_protocol(self, context):
        """Select protocol with highest predicted reward."""
        matching = [p for p in self.protocols if p.matches(context)]
        if not matching:
            return None
        
        features = self._extract_features(context)
        
        best_protocol = None
        best_predicted_reward = -float('inf')
        
        for protocol in matching:
            # Predict reward using linear model
            predicted_reward = np.dot(self.weights[protocol.name], features)
            
            if predicted_reward > best_predicted_reward:
                best_predicted_reward = predicted_reward
                best_protocol = protocol
        
        return best_protocol
    
    def update(self, protocol_name: str, context, actual_reward: float):
        """Update weights using gradient descent."""
        features = self._extract_features(context)
        predicted_reward = np.dot(self.weights[protocol_name], features)
        
        # Gradient descent update
        error = actual_reward - predicted_reward
        self.weights[protocol_name] += self.learning_rate * error * features
        
        self.history.append({
            "protocol": protocol_name,
            "predicted": predicted_reward,
            "actual": actual_reward,
            "error": error
        })
    
    def save_model(self, filepath: str):
        """Save model weights."""
        data = {
            "weights": {k: v.tolist() for k, v in self.weights.items()},
            "history": self.history
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_model(self, filepath: str):
        """Load model weights."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.weights = defaultdict(
            lambda: np.zeros(10),
            {k: np.array(v) for k, v in data["weights"].items()}
        )
        self.history = data.get("history", [])


class AdaptiveOptimizer:
    """
    Meta-optimizer that switches between strategies based on performance.
    """
    
    def __init__(self, protocols: List):
        self.strategies = {
            "epsilon_greedy": EpsilonGreedyOptimizer(protocols, epsilon=0.1),
            "ucb": UCBOptimizer(protocols, c=2.0),
            "thompson": ThompsonSamplingOptimizer(protocols)
        }
        self.current_strategy = "ucb"
        self.strategy_performance = defaultdict(list)
        self.evaluation_window = 50
    
    def select_protocol(self, context):
        """Select protocol using current strategy."""
        return self.strategies[self.current_strategy].select_protocol(context)
    
    def update(self, protocol_name: str, reward: float):
        """Update current strategy and evaluate performance."""
        self.strategies[self.current_strategy].update(protocol_name, reward)
        self.strategy_performance[self.current_strategy].append(reward)
        
        # Periodically evaluate and switch strategies
        if len(self.strategy_performance[self.current_strategy]) >= self.evaluation_window:
            self._evaluate_strategies()
    
    def _evaluate_strategies(self):
        """Compare strategy performance and switch if needed."""
        avg_rewards = {}
        for name, rewards in self.strategy_performance.items():
            if rewards:
                avg_rewards[name] = np.mean(rewards[-self.evaluation_window:])
        
        if avg_rewards:
            best_strategy = max(avg_rewards.items(), key=lambda x: x[1])[0]
            if best_strategy != self.current_strategy:
                logging.info(f"Switching strategy: {self.current_strategy} → {best_strategy}")
                self.current_strategy = best_strategy
