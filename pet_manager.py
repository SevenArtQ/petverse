from datetime import datetime, timedelta

class PetManager:
    @staticmethod
    def calculate_stats(pet):
        current_time = datetime.now().timestamp()
        hours_since_feed = (current_time - pet.last_feed) / 3600
        
        # Уменьшаем голод и счастье со временем
        hunger_loss = min(hours_since_feed * 5, 100)
        happiness_loss = min(hours_since_feed * 3, 100)
        
        pet.hunger = max(0, pet.hunger - hunger_loss)
        pet.happiness = max(0, pet.happiness - happiness_loss)
        
        return pet

    @staticmethod
    def feed_pet(pet):
        if pet.hunger >= 100:
            return False, "Питомец не голоден!"
        
        pet.hunger = min(100, pet.hunger + 30)
        pet.last_feed = datetime.now().timestamp()
        pet.experience += 5
        
        return True, "Питомец накормлен! 🍖"

    @staticmethod
    def play_with_pet(pet):
        if pet.happiness >= 100:
            return False, "Питомец не хочет играть сейчас!"
        
        pet.happiness = min(100, pet.happiness + 20)
        pet.hunger = max(0, pet.hunger - 10)
        pet.experience += 10
        
        return True, "Вы поиграли с питомцем! 🎮"

    @staticmethod
    def check_level_up(pet):
        required_exp = pet.level * 100
        if pet.experience >= required_exp:
            pet.level += 1
            return True, f"Поздравляем! Ваш питомец достиг {pet.level} уровня! 🎉"
        return False, "" 