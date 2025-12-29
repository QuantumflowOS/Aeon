class Governance:
    def approve(self, action: str) -> bool:
        forbidden = ["harm", "illegal", "exploit"]
        return not any(f in action.lower() for f in forbidden)
