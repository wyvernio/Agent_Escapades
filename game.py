class Game:
    def __init__(self):
        self.agent_alive = True
        self.current_room = "entrance"
    
    def display_intro(self):
        print("You are a handler, watching your agent through an old terminal.")
        print("Your choices will guide your agent through trials and traps.")
        print("Can they complete their mission and make it back home?")
        print()

    def make_choice(self, choices):
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        user_choice = input("Choose an option (Enter the number): ")
        return int(user_choice) - 1

    def entrance(self):
        print("Your agent has entered the facility. They are standing at the entrance.")
        choices = ["Go left into the dark hallway", "Go right towards the glowing door"]
        choice = self.make_choice(choices)
        
        if choice == 0:
            return "dark_hallway"
        else:
            return "glowing_door"

    def dark_hallway(self):
        print("Your agent steps into the dark hallway. They hear strange noises.")
        choices = ["Investigate the noise", "Turn back to the entrance"]
        choice = self.make_choice(choices)

        if choice == 0:
            print("A trap is triggered! The ceiling collapses, and your agent is crushed.")
            self.agent_alive = False
            return None
        else:
            return "entrance"

    def glowing_door(self):
        print("Your agent approaches the glowing door. It opens automatically.")
        choices = ["Step through the door", "Run back to the entrance"]
        choice = self.make_choice(choices)

        if choice == 0:
            print("Your agent finds a treasure chest! Mission complete!")
            self.agent_alive = False
            return None
        else:
            return "entrance"

    def run_game(self):
        self.display_intro()
        while self.agent_alive:
            if self.current_room == "entrance":
                self.current_room = self.entrance()
            elif self.current_room == "dark_hallway":
                self.current_room = self.dark_hallway()
            elif self.current_room == "glowing_door":
                self.current_room = self.glowing_door()

        if not self.agent_alive:
            print("Mission Failed. Game Over.")
        else:
            print("Congratulations! Your agent completed the mission.")

if __name__ == "__main__":
    game = Game()
    game.run_game()
