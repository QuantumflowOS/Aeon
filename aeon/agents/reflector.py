class ReflectorAgent:
    """
    Evaluates outcomes and updates rewards.
    """

    def reflect(self, protocol, success: bool):
        if protocol:
            score = 5 if success else 1
            protocol.update_reward(score)
