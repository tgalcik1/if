import sys, json

class Quest():
    def __init__(self, name, description, unlock_conditions, complete_conditions, is_unlocked=False, is_completed=False):
        self.name = name
        self.description = description

        # conditions will be dict of conditions like this {"has_items": ["item1", "item2"], "at_location": "location_name"}
        self.unlock_conditions = unlock_conditions
        self.complete_conditions = complete_conditions

        self.is_unlocked = is_unlocked
        self.is_completed = is_completed

    def check_conditions(self, quests, player, condition_type):
        # check conditions for quest to be unlocked or completed
        if condition_type == "unlock":
            conditions = self.unlock_conditions
        elif condition_type == "complete":
            conditions = self.complete_conditions

        for condition, value in conditions.items():
            # player needs to have certain items in inventory
            if condition == "has_items":
                for item in value:
                    if item not in player.inventory:
                        return False
            
            # player needs to be at a specific location
            if condition == "at_location" and value != player.location.name:
                return False
            
            # player needs to have certain other quests already completed
            if condition == "completed_quests":
                for quest_name in value:
                    if quest_name not in quests or not quests[quest_name].is_completed:
                        return False
                    
            # certain list of enemies needs to be dead

            
        
        return True

    def unlock(self):
        if not self.is_unlocked:
            self.is_unlocked = True
            print(json.dumps({"type": "header-message", "message": f"New quest unlocked: {self.name}"}))
            sys.stdout.flush()

    def complete(self):
        if not self.is_completed:
            self.is_completed = True
            print(json.dumps({"type": "header-message", "message": f"Quest completed! {self.name}"}))
            sys.stdout.flush()
